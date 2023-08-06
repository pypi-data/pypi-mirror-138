"""EUMETSAT Data Access Client"""
from __future__ import annotations

import argparse
import os
import shlex
import sys
import pathlib
import stat
import re
import fnmatch
import shutil
import itertools
from datetime import datetime
from requests.exceptions import HTTPError

import eumdac

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
    from typing import Optional, Any, Union

    if sys.version_info < (3, 9):
        from typing import Sequence, Iterable
    else:
        from collections.abc import Sequence, Iterable


def get_config_dir() -> pathlib.Path:
    return pathlib.Path(os.getenv("EUMDAC_CONFIG_DIR", (pathlib.Path.home() / ".eumdac")))


def load_credentials(parser: argparse.ArgumentParser) -> Iterable[str]:
    config_dir = get_config_dir()
    credentials_path = config_dir / "credentials"
    try:
        content = credentials_path.read_text()
    except FileNotFoundError:
        parser.error("No credentials found! Please set credentials!")
    match = re.match(r"(\w+),(\w+)$", content)
    if match is None:
        parser.error(f'Corrupted file "{credentials_path}"! Please reset credentials!')
    return match.groups()


class SetCredentials(argparse.Action):
    def __call__(
        self,
        parser: argparse.ArgumentParser,
        namespace: argparse.Namespace,
        values: Union[str, Sequence[Any], None],
        option_string: Optional[str] = None,
    ) -> None:
        token = eumdac.AccessToken(values)  # type: ignore[arg-type]
        config_dir = get_config_dir()
        config_dir.mkdir(exist_ok=True)
        credentials_path = config_dir / "credentials"
        credentials_path.touch(mode=(stat.S_IRUSR | stat.S_IWUSR))

        try:
            print(f"Credentials are correct. Token was generated: {token}")
            try:
                with credentials_path.open(mode="w") as file:
                    file.write(",".join(values))  # type: ignore[arg-type]
                namespace.credentials = values
                print(f"Credentials are written to file {credentials_path}")
            except OSError:
                print("Credentials could not written to file.")
        except HTTPError as e:
            if e.response.status_code == 401:
                print(
                    "Credentials are not correct. "
                    "Get your personal credentials at https://api.eumetsat.int/api-key"
                )
            else:
                print(f"Token API responses with a {e.response.status_code} error.")

        parser.exit()


class ListSubscriptions(argparse.Action):
    def __call__(
        self,
        parser: argparse.ArgumentParser,
        namespace: argparse.Namespace,
        values: Union[str, Sequence[Any], None],
        option_string: Optional[str] = None,
    ) -> None:
        credentials = load_credentials(parser)
        token = eumdac.AccessToken(credentials)
        datastore = eumdac.DataStore(token)
        subscriptions = datastore.subscriptions
        if not subscriptions:
            print("no subscriptions registerred")
            parser.exit()
        for subscription in datastore.subscriptions:
            lines = [
                f"Subscription ID: {subscription}",
                f"\tListener: {subscription.url}",
                f"\tCollection: {subscription.collection}",
                f"\tArea of Interesst: {subscription.area_of_interesst}",
                f"\tStatus: {subscription.status}",
            ]
            print(os.linesep.join(lines))
        parser.exit()


class DeleteSubscription(argparse.Action):
    def __call__(
        self,
        parser: argparse.ArgumentParser,
        namespace: argparse.Namespace,
        values: Union[str, Sequence[Any], None],
        option_string: Optional[str] = None,
    ) -> None:
        credentials = load_credentials(parser)
        token = eumdac.AccessToken(credentials)
        datastore = eumdac.DataStore(token)
        for subscription_id in values:  # type: ignore[union-attr]
            subscription = datastore.get_subscription(subscription_id)
            subscription.delete()
            print(f"deleted subscription {subscription_id}")
        parser.exit()


class CommandAction(argparse._SubParsersAction):  # type: ignore[type-arg]
    def __call__(
        self,
        parser: argparse.ArgumentParser,
        namespace: argparse.Namespace,
        values: Union[str, Sequence[Any], None],
        option_string: Optional[str] = None,
    ) -> None:
        super().__call__(parser, namespace, values, option_string=option_string)
        requires_credentials = [
            command
            for command, parser in self._name_parser_map.items()
            if any(action.dest == "credentials" for action in parser._actions)
        ]
        if namespace.command in requires_credentials and namespace.credentials is None:
            namespace.credentials = load_credentials(parser)


def describe(args: argparse.Namespace) -> None:
    token = eumdac.AccessToken(args.credentials)
    datastore = eumdac.DataStore(token)
    if args.collection is None and args.product is None:
        for collection in datastore.collections:
            print(f"{collection} - {collection.title}")
    elif args.collection is not None and args.product is None:
        collection = datastore.get_collection(args.collection)
        date = collection.metadata["properties"].get("date", "/")
        match = re.match(r"([^/]*)/([^/]*)", date)
        start_date, end_date = match.groups()  # type: ignore[union-attr]
        start_date = start_date or "-"
        end_date = end_date or "now"
        print(f"{collection} - {collection.title}")
        print(f"Date: {start_date} - {end_date}")
        print(collection.abstract)
        print(f'Licence: {"; ".join(collection.metadata["properties"].get("rights", "-"))}')
    elif args.collection is None and args.product is not None:
        raise ValueError("Product ID requires a Collection ID!")
    else:
        product = datastore.get_product(args.collection, args.product)
        attributes = {
            "Mission": product.satellite,
            "Instrument": product.instrument,
            "Sensing Start": "none"
            if (product.sensing_start is False)
            else f"{product.sensing_start.isoformat(timespec='milliseconds')}Z",
            "Sensing End": "none"
            if (product.sensing_end is False)
            else f"{product.sensing_end.isoformat(timespec='milliseconds')}Z",
            "Size": f"{product.size} KB",
        }
        print(f"{product.collection} - {product}")
        lines = [f"{key}: {value}" for key, value in attributes.items()]
        print(os.linesep.join(lines))


def search(args: argparse.Namespace) -> None:
    token = eumdac.AccessToken(args.credentials)
    datastore = eumdac.DataStore(token)
    for collection in args.collection:
        collection = datastore.get_collection(collection)
        _query = {
            "dtstart": args.dtstart,
            "dtend": args.dtend,
            "bbox": args.bbox,
            "geo": args.geo,
            "sat": args.sat,
            "sort": args.sort,
        }
        query = {key: value for key, value in _query.items() if value is not None}
        limit = args.limit
        bbox = query.pop("bbox", None)
        if bbox is not None:
            query["bbox"] = ",".join(map(str, bbox))
        products_query = collection.search(**query)
        products = itertools.islice(products_query, limit)
        products_count = len(products_query)

        if products_count > limit and limit == 10:
            # show a warning through stderr only when more than 10 
            # products would be shown and limit keyword is not used.
            print(f"By default, only 10 of {products_count} products are displayed.", file=sys.stderr)
            print("Please use --limit to increase the number of products if necessary.", file=sys.stderr)
        print(os.linesep.join(map(str, products)))


def download(args: argparse.Namespace) -> None:
    token = eumdac.AccessToken(args.credentials)
    datastore = eumdac.DataStore(token)
    collection_id = args.collection
    if not args.product:
        if not args.time_range:
            raise ValueError("Please provide either products or a time-range!")
        start, end = args.time_range
        collection = datastore.get_collection(collection_id)
        args.product = [str(product) for product in collection.search(dtstart=start, dtend=end)]
    print(f"Output directory: {args.output_dir}")
    for product_id in args.product:
        product = datastore.get_product(collection_id, product_id)
        if args.file_pattern is None:
            enties = [None]
        else:
            matches = (fnmatch.filter(product.entries, pattern) for pattern in args.file_pattern)
            enties = sum(matches, [])
        for entry in enties:
            with product.open(entry=entry) as fsrc:
                output = args.output_dir / fsrc.name
                if output.is_file():
                    print(f"Skip {fsrc.name} it already exists")
                    continue
                print(f"Downloading {fsrc.name}")
                tmp = args.output_dir / (fsrc.name + ".tmp")
                with tmp.open(mode="wb") as fdst:
                    # note: currently, there is no content-length header
                    # in the data store http response, so it is not simple to
                    # build a progress bar. In case it is added in future,
                    # just check fsrc.getheader("Content-Length")
                    shutil.copyfileobj(fsrc, fdst)
                tmp.rename(output)


def subscribe(args: argparse.Namespace) -> None:
    token = eumdac.AccessToken(args.credentials)
    datastore = eumdac.DataStore(token)
    collection = datastore.get_collection(args.collection)
    subscription = datastore.new_subscription(
        collection, args.url, area_of_interest=args.area_of_interest
    )
    lines = [
        "Created new subscription",
        f"Subscription ID: {subscription}",
        f"\tListener: {subscription.url}",
        f"\tCollection: {subscription.collection}",
        f"\tArea of Interesst: {subscription.area_of_interesst}",
        f"\tStatus: {subscription.status}",
    ]
    print(os.linesep.join(lines))


def cli(command_line: Optional[Sequence[str]] = None) -> None:
    # append piped args
    if not sys.stdin.isatty():
        sys.argv.extend(shlex.split(sys.stdin.read()))

    # main parser
    parser = argparse.ArgumentParser(description=__doc__, fromfile_prefix_chars="@")
    parser.add_argument("--version", action="version", version=f"%(prog)s {eumdac.__version__}")
    parser.add_argument(
        "--set-credentials",
        nargs=2,
        action=SetCredentials,
        help=(
            "permanently set consumer key and secret and exit, "
            "see https://api.eumetsat.int/api-key"
        ),
        metavar=("ConsumerKey", "ConsumerSecret"),
        dest="credentials",
    )
    parser.add_argument("--debug", help="show backtrace for errors", action="store_true")

    subparsers = parser.add_subparsers(dest="command", action=CommandAction)

    # describe parser
    parser_describe = subparsers.add_parser(
        "describe",
        help="describe a collection or product",
        epilog="example: %(prog)s -c EO:EUM:DAT:MSG:HRSEVIRI",
    )
    parser_describe.add_argument(
        "-c",
        "--collection",
        help="collection to describe",
        metavar="CollectionId",
    )
    parser_describe.add_argument("-p", "--product", help="product to describe", metavar="ProductId")
    parser_describe.add_argument(
        "--credentials",
        nargs=2,
        default=argparse.SUPPRESS,
        help="consumer key and secret, see https://api.eumetsat.int/api-key",
        metavar=("ConsumerKey", "ConsumerSecret"),
    )
    parser_describe.set_defaults(func=describe)

    # search parser
    parser_search = subparsers.add_parser(
        "search",
        help="search for products at the collection level",
        epilog="example: %(prog)s -s 2020-03-01 -e 2020-03-15T12:15 -c EO:EUM:DAT:MSG:CLM",
    )
    parser_search.add_argument(
        "-c", "--collection", nargs="+", help="collection ID(s)", required=True
    )
    parser_search.add_argument(
        "-s",
        "--start",
        type=datetime.fromisoformat,
        help="UTC start date e.g. 2002-12-21T12:30:15",
        metavar="YYYY-MM-DD[THH[:MM[:SS]]]",
        dest="dtstart",
    )
    parser_search.add_argument(
        "-e",
        "--end",
        type=datetime.fromisoformat,
        help="UTC end date e.g. 2002-12-21T12:30:15",
        metavar="YYYY-MM-DD[THH[:MM[:SS]]]",
        dest="dtend",
    )
    parser_search.add_argument(
        "--bbox",
        nargs=4,
        type=float,
        metavar=("W", "S", "E", "N"),
        help="filter by bounding box, the box is defined in EPSG:4326 decimal degrees",
    )
    parser_search.add_argument(
        "--geometry",
        help="filter by geometry, a custom geomtery in a EPSG:4326 decimal degrees.",
        dest="geo",
    )
    parser_search.add_argument("--satellite", help="filter by satellite", dest="sat")
    parser_search.add_argument("--sort", help="sort results")
    parser_search.add_argument(
        "--limit",
        type=int,
        help="Max Items to return, default = %(default)s",
        default=10,
    )
    parser_search.add_argument(
        "--credentials",
        nargs=2,
        default=argparse.SUPPRESS,
        help="consumer key and secret, see https://api.eumetsat.int/api-key",
        metavar=("ConsumerKey", "ConsumerSecret"),
    )
    parser_search.set_defaults(func=search)

    # download parser
    parser_download = subparsers.add_parser(
        "download", help="download product(s) from a collection"
    )
    parser_download.add_argument("-c", "--collection", help="collection ID", required=True)
    parser_download.add_argument("-p", "--product", nargs="*", help="product ID(s)")
    parser_download.add_argument(
        "-o",
        "--output-dir",
        type=pathlib.Path,
        help="path to output directory, default CWD",
        metavar="DIR",
        default=pathlib.Path.cwd(),
    )
    parser_download.add_argument(
        "--file-pattern",
        nargs="+",
        help="shell-style wildcard pattern(s) to filter product files",
    )
    parser_download.add_argument(
        "--time-range",
        nargs=2,
        type=datetime.fromisoformat,
        help="convenience search on UTC time range",
        metavar="YYYY-MM-DD[THH[:MM[:SS]]]",
    )
    parser_download.add_argument(
        "--credentials",
        nargs=2,
        default=argparse.SUPPRESS,
        help="consumer key and secret, see https://api.eumetsat.int/api-key",
        metavar=("ConsumerKey", "ConsumerSecret"),
    )
    parser_download.set_defaults(func=download)

    # subscribe parser
    parser_subscribe = subparsers.add_parser(
        "subscribe", help="subscribe a server for a collection"
    )
    parser_subscribe.add_argument("-c", "--collection", help="collection ID", required=True)
    parser_subscribe.add_argument(
        "-u", "--url", help="public URL of the listener server", required=True
    )
    parser_subscribe.add_argument(
        "--area-of-interest",
        help="area of interest, a custom geomtery in a EPSG:4326 decimal degrees.",
    )
    parser_subscribe.add_argument(
        "--list", help="list subscriptions and exit", action=ListSubscriptions, nargs=0
    )
    parser_subscribe.add_argument(
        "--delete",
        help="delete subscription(s) and exit",
        action=DeleteSubscription,
        nargs="+",
        metavar="SubscriptionId",
    )
    parser_subscribe.add_argument(
        "--credentials",
        nargs=2,
        default=argparse.SUPPRESS,
        help="consumer key and secret, see https://api.eumetsat.int/api-key",
        metavar=("ConsumerKey", "ConsumerSecret"),
    )
    parser_subscribe.set_defaults(func=subscribe)

    args = parser.parse_args(command_line)
    if args.command:
        try:
            args.func(args)
        except KeyboardInterrupt:
            # Ignoring KeyboardInterrupts to allow for clean CTRL+C-ing
            pass
        except Exception as error:
            if args.debug:
                raise
            parser.error(str(error))
    else:
        parser.print_help()
