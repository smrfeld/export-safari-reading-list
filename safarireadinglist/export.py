from safarireadinglist.reading_list_item import ReadingListItem

from subprocess import Popen

import plistlib

from typing import List, Dict
import json
import csv
import logging


logger = logging.getLogger(__name__)


def export_reading_list(fname_bookmarks: str, include_data: bool, tmp_plist_fname: str = "tmp.plist") -> List[ReadingListItem]:

    try:

        command = "cp %s %s" % (fname_bookmarks, tmp_plist_fname)
        logger.debug("Making temporary copy of reading list: %s" % command)
        run_command(command)

        # Load the plist file
        with open(tmp_plist_fname, 'rb') as f:
            res = plistlib.load(f)
        
        # Find the reading list items
        rlist = find_dicts_with_rlist_keys_in_dict(res)
        logger.debug("You have: %d items in your reading list" % len(rlist))

        # Iterate over reading list items
        ritems = [ ReadingListItem.from_dict(r, include_data) for r in rlist ]
        
    finally:

        # Clean up
        command = "rm -f %s" % tmp_plist_fname
        print("Removing tmp file: %s" % command)
        run_command(command)

    logger.debug("Done.")

    return ritems
    

def copy_icons(dir_icons_in: str, dir_icons_out: str):
    command = "cp -r %s %s" % (dir_icons_in, dir_icons_out)
    print("Copying icons directory: %s" % command)
    run_command(command)


def write_reading_list_to_json(ritems: List[ReadingListItem], fname_out: str):
    with open(fname_out,'w') as f:
        rjson = [ r.to_json() for r in ritems ]
        json.dump(rjson,f,indent=3)
    print("Wrote reading list to JSON file: %s" % fname_out)


def write_reading_list_to_csv(ritems: List[ReadingListItem], fname_out: str):
    with open(fname_out,'w') as f:
        csv_writer = csv.writer(f)

        rjson = [ r.to_json_full() for r in ritems ]

        # Write header
        csv_writer.writerow(rjson[0].keys())

        # Write contents
        for row in rjson:
            csv_writer.writerow(row.values())


def run_command(s: str):
    Popen(s, shell=True).wait()


def rm_data_from_dicts_in_list(base_list: List) -> List:
    for i in range(0,len(base_list)):
        sub_obj = base_list[i]
        if type(sub_obj) is list:
            base_list[i] = rm_data_from_dicts_in_list(sub_obj)
        elif type(sub_obj) is dict:
            base_list[i] = rm_data_from_dict(sub_obj)
    
    return base_list


def rm_data_from_dict(base_dict: Dict) -> Dict:
    # Remove data
    if "Data" in base_dict:
        del base_dict["Data"]

    # Go through remaining keys/values
    keys = list(base_dict.keys())
    for key in keys:
        if type(base_dict[key]) is list:
            base_dict[key] = rm_data_from_dicts_in_list(base_dict[key])
        elif type(base_dict[key]) is dict:
            base_dict[key] = rm_data_from_dict(base_dict[key])

    return base_dict

def find_dicts_with_rlist_keys_in_dict(base_dict: Dict) -> List:
    ret = []

    for key,val in base_dict.items():
        if key == "Children":
            # Recurse down
            for child_dict in val:
                ret += find_dicts_with_rlist_keys_in_dict(child_dict)
        elif key == "ReadingList":
            ret.append(base_dict)
            break
        
    return ret

