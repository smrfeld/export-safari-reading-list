# Export Safari reading list to CSV or JSON

<img src="readme_imgs/json.png" alt="drawing" width="400"/>

<img src="readme_imgs/csv.png" alt="drawing" width="400"/>

## Requirements

The [plistlib](https://docs.python.org/3/library/plistlib.html) module:
```
pip install plistlib
```

## Usage

Basic usage:
* Export to CSV:
    ```
    python export_reading_list.py csv reading_list.csv
    ```
    will write the reading list to `reading_list.csv`.
* Export to JSON:
    ```
    python export_reading_list.py json reading_list.json
    ```
    will write the reading list to `reading_list.json`.

Options:
* Also copy the reading list icons:
    ```
    python export_reading_list.py csv reading_list.csv --dir_icons_out reading_list_icons
    ```
    copies the icons to the folder `reading_list_icons`. They match up to the entries through the `WebBookmarkUUID` key.
* Specify the source directory for the icons:
    ```
    python export_reading_list.py csv reading_list.csv --dir_icons ~/Library/Safari/ReadingListArchives
    ```
    The default is `~/Library/Safari/ReadingListArchives`.
* Specify the source directory for the reading list `.plist` file:
    ```
    python export_reading_list.py csv reading_list.csv --fname_bookmarks ~/Library/Safari/Bookmarks.plist
    ```
    The default is `~/Library/Safari/Bookmarks.plist`.