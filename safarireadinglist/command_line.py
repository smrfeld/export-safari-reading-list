import safarireadinglist as srl
import argparse
import logging


logger = logging.getLogger(__name__)


def cli():

    # Parse args
    parser = argparse.ArgumentParser(description='Export reading list.')
    parser.add_argument(
        'output_mode',
        type=str,
        help='JSON or CSV mode',
        choices=['csv','json']
        )
    parser.add_argument(
        'fname_out',
        type=str,
        help='Name of output JSON or CSV file'
        )
    parser.add_argument(
        '--fname-bookmarks', 
        type=str, 
        help='Bookmarks.plist file', 
        default="~/Library/Safari/Bookmarks.plist"
        )
    parser.add_argument(
        '--dir-icons-out',
        type=str,
        help='Name of output directory for icons'
        )
    parser.add_argument(
        '--dir-icons', 
        type=str, 
        help='Reading list icons directory', 
        default="~/Library/Safari/ReadingListArchives"
        )
    parser.add_argument(
        '--include-data', 
        action='store_true',
        help='Include the cached data for the site'
        )
    parser.add_argument(
        '--tmp-plist-fname',
    )

    args = parser.parse_args()

    rlist = srl.export_reading_list(
        fname_bookmarks=args.fname_bookmarks,
        include_data=args.include_data
        )
    logger.info(f"You have: {len(rlist)} items in your reading list")

    # Write
    if args.output_mode == "json":
        srl.write_reading_list_to_json(rlist, args.fname_out)
    elif args.output_mode == "csv":
        srl.write_reading_list_to_csv(rlist, args.fname_out)
    else:
        raise NotImplementedError(f"Unknown output mode: {args.output_mode}")


