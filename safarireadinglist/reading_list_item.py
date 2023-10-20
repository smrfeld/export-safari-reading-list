from dataclasses import dataclass
from typing import Union, Dict
import json
import datetime
import base64


@dataclass
class ReadingListItem(json.JSONEncoder):

    # Title
    title: str

    # Server ID
    ServerID: str

    # neverFetchMetadata
    neverFetchMetadata: bool

    # WebBookmarkType
    WebBookmarkType: str

    # WebBookmarkUUID
    WebBookmarkUUID: str
    
    # URLString
    URLString: str

    # Date added
    DateAdded: datetime.datetime

    # Data
    Data: Union[str,None] = None

    # siteName
    siteName: Union[str,None] = None

    # PreviewText
    PreviewText: Union[str,None] = None

    # DateLastFetched
    DateLastFetched: Union[datetime.datetime,None] = None

    # imageURL
    imageURL: Union[str,None] = None

    # didAttemptToFetchIconFromImageUrlKey
    didAttemptToFetchIconFromImageUrlKey: Union[bool,None] = None

    # NumberOfFailedLoadsWithUnknownOrNonRecoverableError
    NumberOfFailedLoadsWithUnknownOrNonRecoverableError: Union[int,None] = None

    # FetchResult
    FetchResult: Union[int,None] = None

    # AddedLocally
    AddedLocally: Union[bool,None] = None


    def to_json(self) -> Dict:
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
            res["Data"] = self.Data
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


    def to_json_full(self) -> Dict:
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

        res["Data"] = self.Data
        res["DateAdded"] = self.DateAdded.strftime(df) if self.DateAdded != None else None
        res["DateLastFetched"] = self.DateLastFetched.strftime(df) if self.DateLastFetched != None else None

        return res


    @classmethod
    def from_dict(cls, r: Dict, include_data: bool):
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
            ritem.Data = base64.b64encode(r['Sync']['Data']).decode('utf-8')
        
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
