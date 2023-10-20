# Safari reading list example

Install the `safarireadinglist` package in the root directory.

## Python example

```bash
python example_python.py
```

You will find the output files in the current directory including `reading_list.json` and `reading_list.csv`, in addition to the icons in a dedicated `reading_list_icons` folder.

## Example of output format

See [reading_list.json](reading_list.json). The format is a list of dictionaries, where each dictionary conforms to the `safarireadinglist.ReadingListItem` dataclass.

## Command line example

In the command line, execute:

```bash
export-safari-rl export
```

The reading list will be in `reading_list.json`. You may also provide other options: `export-safari-rl --help`.

To export the icons, execute:

```bash
export-safari-rl export-icons
```

The icons will be in the `reading_list_icons` folder.

For more options, see `export-safari-rl --help`. Here are some examples: 

* Export to CSV:
    ```
    export-safari-rl export --fname-out reading_list.csv
    ```
    will write the reading list to `reading_list.csv`.

* Specify the source directory for the icons:
    ```
    export-safari-rl export-icons --dir-icons ~/Library/Safari/ReadingListArchives
    ```
    The default is `~/Library/Safari/ReadingListArchives`.

* Specify the source directory for the reading list `.plist` file:
    ```
    export-safari-rl export --fname-bookmarks ~/Library/Safari/Bookmarks.plist
    ```
    The default is `~/Library/Safari/Bookmarks.plist`.

* Include cached data for the websites:
    ```
    export-safari-rl export --include-data
    ```
    The data is written to the `Data` field. The default is to exclude this data.