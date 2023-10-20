import safarireadinglist as srl

# Export reading list
rlist = srl.export_reading_list()
print(f"You have {len(rlist)} items in your reading list")

# Log first item
print(rlist[0].to_json())

# Write to JSON
srl.write_reading_list_to_json(rlist, "reading_list.json")

# Write to CSV
srl.write_reading_list_to_csv(rlist, "reading_list.csv")

# Write icons to directory
srl.export_icons("reading_list_icons")

# Read from JSON
import json
with open("reading_list.json") as f:
    rlist_json = json.load(f)

    # The JSON is a list of dictionaries
    rlist = [ srl.ReadingListItem.from_dict(r) for r in rlist_json ]