import logging
logger = logging.getLogger(__name__)

# Set up logging to stdout before other imports
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


import safarireadinglist as srl
import argparse
import os


def cli():

    parser = argparse.ArgumentParser(description='Export reading list.')
    parser.add_argument(
        'command',
        type=str,
        help='Command - either export the reading list or copy the icons',
        choices=['export','export-icons']
        )
    parser.add_argument(
        '--fname-out',
        type=str,
        help='Name of output JSON or CSV file',
        required=False,
        default="reading_list.json"
        )
    parser.add_argument(
        '--fname-bookmarks', 
        type=str, 
        help='Bookmarks.plist file', 
        default="~/Library/Safari/Bookmarks.plist",
        required=False
        )
    parser.add_argument(
        '--dir-icons-out',
        type=str,
        help='Name of output directory for icons',
        required=False,
        default="reading_list_icons"
        )
    parser.add_argument(
        '--dir-icons', 
        type=str, 
        help='Reading list icons directory', 
        default="~/Library/Safari/ReadingListArchives",
        required=False
        )
    parser.add_argument(
        '--include-data', 
        action='store_true',
        help='Include the cached data for the site',
        required=False
        )
    parser.add_argument(
        '--tmp-plist-fname',
        type=str,
        help='Name of temporary plist file. Will be deleted after use.',
        default="tmp.plist",
        required=False
        )

    args = parser.parse_args()

    if args.command == 'export':
        rlist = srl.export_reading_list(
            fname_bookmarks=args.fname_bookmarks,
            include_data=args.include_data,
            tmp_plist_fname=args.tmp_plist_fname
            )
        logger.info(f"You have: {len(rlist)} items in your reading list")

        # Write
        ext = os.path.splitext(args.fname_out)[1]
        if ext == ".json":
            srl.write_reading_list_to_json(rlist, args.fname_out)
        elif ext == ".csv":
            srl.write_reading_list_to_csv(rlist, args.fname_out)
        else:
            raise NotImplementedError(f"Unknown extension: {args.fname_out} - must be .json or .csv")
        logger.info(f"Wrote reading list to file: {args.fname_out}")
    
    elif args.command == 'export-icons':
        srl.copy_icons(args.dir_icons, args.dir_icons_out)
        logger.info(f"Exported icons to directory: {args.dir_icons_out}")

    else:
        raise NotImplementedError(f"Unknown command: {args.command}")