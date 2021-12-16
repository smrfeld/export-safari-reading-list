from subprocess import Popen
import argparse

import plistlib

from dataclasses import dataclass
from typing import Union
import datetime
import json
import csv

def rm_data_from_dicts_in_list(base_list):
    for i in range(0,len(base_list)):
        sub_obj = base_list[i]
        if type(sub_obj) is list:
            base_list[i] = rm_data_from_dicts_in_list(sub_obj)
        elif type(sub_obj) is dict:
            base_list[i] = rm_data_from_dict(sub_obj)
    
    return base_list

def rm_data_from_dict(base_dict):
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

def find_dicts_with_rlist_keys_in_dict(base_dict):
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

import base64

@dataclass
class ReadingListItem(json.JSONEncoder):

    title: str
    ServerID: str
    neverFetchMetadata: bool
    WebBookmarkType: str
    WebBookmarkUUID: str
    URLString: str
    DateAdded: datetime.datetime

    Data: Union[str,None] = None
    siteName: Union[str,None] = None
    PreviewText: Union[str,None] = None
    DateLastFetched: Union[datetime.datetime,None] = None
    imageURL: Union[str,None] = None
    didAttemptToFetchIconFromImageUrlKey: Union[bool,None] = None
    NumberOfFailedLoadsWithUnknownOrNonRecoverableError: Union[int,None] = None
    FetchResult: Union[int,None] = None
    AddedLocally: Union[bool,None] = None

    def to_json(self):
        df = "%Y-%m-%d %H:%M:%S"
        res = {
            "title": self.title,
            "ServerID": self.ServerID,
            "neverFetchMetadata": self.neverFetchMetadata,
            "WebBookmarkType": self.WebBookmarkType,
            "WebBookmarkUUID": self.WebBookmarkUUID,
            "URLString": self.URLString,
            "DateAdded": self.DateAdded.strftime(df)
            }

        if self.Data != None:
            res["Data"] = base64.b64encode(self.Data).decode('utf-8')
        if self.siteName != None:
            res["siteName"] = self.siteName
        if self.PreviewText != None:
            res["PreviewText"] = self.PreviewText
        if self.DateLastFetched != None:
            res["DateLastFetched"] = self.DateLastFetched.strftime(df)
        if self.imageURL != None:
            res["imageURL"] = self.imageURL
        if self.didAttemptToFetchIconFromImageUrlKey != None:
            res['didAttemptToFetchIconFromImageUrlKey'] = self.didAttemptToFetchIconFromImageUrlKey
        if self.FetchResult != None:
            res["FetchResult"] = self.FetchResult
        if self.AddedLocally != None:
            res["AddedLocally"] = self.AddedLocally
        if self.NumberOfFailedLoadsWithUnknownOrNonRecoverableError != None:
            res["NumberOfFailedLoadsWithUnknownOrNonRecoverableError"] = self.NumberOfFailedLoadsWithUnknownOrNonRecoverableError

        return res

    def to_json_full(self):
        df = "%Y-%m-%d %H:%M:%S"
        res = {
            "title": self.title,
            "ServerID": self.ServerID,
            "neverFetchMetadata": self.neverFetchMetadata,
            "WebBookmarkType": self.WebBookmarkType,
            "WebBookmarkUUID": self.WebBookmarkUUID,
            "URLString": self.URLString,
            "siteName": self.siteName,
            "PreviewText": self.PreviewText,
            "imageURL": self.imageURL,
            "didAttemptToFetchIconFromImageUrlKey": self.didAttemptToFetchIconFromImageUrlKey,
            "FetchResult": self.FetchResult,
            "AddedLocally": self.AddedLocally,
            "NumberOfFailedLoadsWithUnknownOrNonRecoverableError": self.NumberOfFailedLoadsWithUnknownOrNonRecoverableError
            }

        if self.Data != None:
            res["Data"] = base64.b64encode(self.Data).decode('utf-8')
        else:
            res["Data"] = None

        if self.DateAdded != None:
            res["DateAdded"] = self.DateAdded.strftime(df)
        else:
            res["DateAdded"] = None

        if self.DateLastFetched != None:
            res["DateLastFetched"] = self.DateLastFetched.strftime(df)
        else:
            res["DateLastFetched"] = None

        return res

    @classmethod
    def fromRDict(cls, r, include_data):
        ritem = cls(
            title=r['URIDictionary']['title'],
            ServerID=r['Sync']['ServerID'],
            neverFetchMetadata=r['ReadingListNonSync']['neverFetchMetadata'],
            WebBookmarkType=r['WebBookmarkType'],
            WebBookmarkUUID=r['WebBookmarkUUID'],
            URLString=r['URLString'],
            DateAdded=r['ReadingList']['DateAdded']
            )
        
        if include_data:
            ritem.Data = r['Sync']['Data']
        
        if 'ReadingListNonSync' in r and 'siteName' in r['ReadingListNonSync']:
            ritem.siteName = r['ReadingListNonSync']['siteName']
        if 'ReadingList' in r and 'PreviewText' in r['ReadingList']:
            ritem.PreviewText = r['ReadingList']['PreviewText']
        if 'ReadingListNonSync' in r and 'DateLastFetched' in r['ReadingListNonSync']:
            ritem.DateLastFetched = r['ReadingListNonSync']['DateLastFetched']
        if 'imageURL' in r:
            ritem.imageURL = r['imageURL']
        if 'ReadingListNonSync' in r \
            and 'didAttemptToFetchIconFromImageUrlKey' in r['ReadingListNonSync']:
            ritem.didAttemptToFetchIconFromImageUrlKey = \
                r['ReadingListNonSync']['didAttemptToFetchIconFromImageUrlKey']
        if 'ReadingListNonSync' in r \
            and 'NumberOfFailedLoadsWithUnknownOrNonRecoverableError' in r['ReadingListNonSync']:
            ritem.NumberOfFailedLoadsWithUnknownOrNonRecoverableError = \
                r['ReadingListNonSync']['NumberOfFailedLoadsWithUnknownOrNonRecoverableError']
        if 'ReadingListNonSync' in r and 'FetchResult' in r['ReadingListNonSync']:
            ritem.FetchResult = r['ReadingListNonSync']['FetchResult']
        if 'ReadingListNonSync' in r and 'AddedLocally' in r['ReadingListNonSync']:
            ritem.AddedLocally = r['ReadingListNonSync']['AddedLocally']

        return ritem

def main():

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
        dest='fname_bookmarks',
        type=str, 
        help='Bookmarks.plist file', 
        default="~/Library/Safari/Bookmarks.plist"
        )
    parser.add_argument(
        '--dir-icons-out',
        dest='dir_icons_out',
        type=str,
        help='Name of output directory for icons'
        )
    parser.add_argument(
        '--dir-icons', 
        dest='dir_icons',
        type=str, 
        help='Reading list icons directory', 
        default="~/Library/Safari/ReadingListArchives"
        )
    parser.add_argument(
        '--include-data', 
        dest='include_data', 
        action='store_true',
        help='Include the cached data for the site'
        )
    parser.add_argument(
        '--exclude-data', 
        dest='include_data', 
        action='store_false',
        help='Exclude the cached data for the site'
        )
    parser.set_defaults(include_data=False)

    args = parser.parse_args()

    fname_plist = "tmp.plist"
    command = "cp %s %s" % (args.fname_bookmarks, fname_plist)
    print("Making temporary copy of reading list: %s" % command)
    Popen(command, shell=True).wait()

    with open("tmp.plist",'rb') as f:
        res = plistlib.load(f)
    
    # res = rm_data_from_dict(res)
    print(args.include_data)
    rlist = find_dicts_with_rlist_keys_in_dict(res)
    print("You have: %d items in your reading list" % len(rlist))

    # Iterate over reading list items
    ritems = [ ReadingListItem.fromRDict(r,args.include_data) for r in rlist ]
    
    # Dump
    if args.output_mode == 'json':
        
        # Write JSON
        with open(args.fname_out,'w') as f:
            rjson = [ r.to_json() for r in ritems ]
            json.dump(rjson,f,indent=3)
        print("Wrote reading list to JSON file: %s" % args.fname_out)

    elif args.output_mode == 'csv':
        
        # Dump to CSV
        with open(args.fname_out,'w') as f:
            csv_writer = csv.writer(f)

            rjson = [ r.to_json_full() for r in ritems ]

            # Write header
            csv_writer.writerow(rjson[0].keys())
 
            # Write contents
            for row in rjson:
                csv_writer.writerow(row.values())

    # Clean up
    command = "rm -f %s" % fname_plist
    print("Removing tmp file: %s" % command)
    Popen(command, shell=True).wait()
    
    # Copy icons
    if args.dir_icons_out:
        command = "cp -r %s %s" % (args.dir_icons, args.dir_icons_out)
        print("Copying icons directory: %s" % command)
        Popen(command, shell=True).wait()

    print("Done.")

if __name__ == "__main__":
    main()
