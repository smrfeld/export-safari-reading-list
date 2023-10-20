# Safari reading list example

Install the `safarireadinglist` package in the root directory.

## Python example

```bash
python example_python.py
```

You will find the output files in the current directory including `reading_list.json` and `reading_list.csv`, in addition to the icons in a dedicated `reading_list_icons` folder.

## Command line example

In the command line, execute:

```bash
export-safari-rl export
```

To export the icons, execute:

```bash
export-safari-rl export-icons
```

## Output example

See [reading_list.json](reading_list.json).

The format is a list of dictionaries, where each dictionary conforms to the `safarireadinglist.ReadingListItem` dataclass.