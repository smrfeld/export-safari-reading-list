# Export Safari reading list to CSV or JSON

<img src="readme_imgs/reading_list.jpg" alt="drawing" width="400"/>

## Sample results

<img src="readme_imgs/json.png" alt="drawing" width="700"/>

<img src="readme_imgs/csv.png" alt="drawing" width="700"/>

## Requirements

The [plistlib](https://docs.python.org/3/library/plistlib.html) module:
```
pip install plistlib
```

Tested on mac `11.4` Big Sur, Safari `14.1.1`.

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
    python export_reading_list.py csv reading_list.csv --dir-icons-out reading_list_icons
    ```
    copies the icons to the folder `reading_list_icons`. They match up to the entries through the `WebBookmarkUUID` key.
* Specify the source directory for the icons:
    ```
    python export_reading_list.py csv reading_list.csv --dir-icons ~/Library/Safari/ReadingListArchives
    ```
    The default is `~/Library/Safari/ReadingListArchives`.
* Specify the source directory for the reading list `.plist` file:
    ```
    python export_reading_list.py csv reading_list.csv --fname-bookmarks ~/Library/Safari/Bookmarks.plist
    ```
    The default is `~/Library/Safari/Bookmarks.plist`.
* Include cached data for the websites:
    ```
    python export_reading_list.py csv reading_list.csv --include-data
    ```
    The data is written to the `Data` field. The default is the `--exclude-data` option, which excludes the data.

## Website

To generate the website from the `website_template` folder, run:
```
python website.py reading_list.json reading_list_icons
```
The output is in the `website_out` folder.

<img src="readme_imgs/website.png" alt="drawing" width="800"/>