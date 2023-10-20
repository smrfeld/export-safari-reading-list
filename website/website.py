import json
import os
import argparse
from subprocess import Popen


def assemble_from_template(
    fname_header: str, 
    fname_template: str, 
    fname_footer: str,
    fname_json: str,
    fname_output: str,
    icon_folder: str
    ):

    with open(fname_header,'r') as f:
        header = f.read()

    with open(fname_template,'r') as f:
        template = f.read()

    with open(fname_footer,'r') as f:
        footer = f.read()

    with open(fname_json,'r') as f:
        entries = json.load(f)

    assembled = header
    for entry in entries:
        rep = {key:val for key, val in entry.items() if val != None}

        # Ensure preview text exists
        if not "PreviewText" in rep:
            rep["PreviewText"] = ""
        
        # Only keep year-month-day
        rep["DateAdded"] = rep["DateAdded"][:10]

        rep["img"] = os.path.join("img",icon_folder,rep["WebBookmarkUUID"],'thumbnail.png')

        template_sub = template.format(**rep)
        assembled += "\n" + template_sub

    assembled += "\n" + footer

    # Write
    print("Writing static site to: %s" % fname_output)
    with open(fname_output,'w') as f:
        f.write(assembled)


def main():

    parser = argparse.ArgumentParser(description='Generate static html code.')
    parser.add_argument('fname_json', type=str, help='JSON file for reading list')
    parser.add_argument('dir_icons', type=str, help='Directory with icons')
    args = parser.parse_args()

    print("Generating static site from JSON file %s" % args.fname_json)

    dir_templates = "website_template/"

    dir_out = "website_out"
    command = "rm -f %s" % dir_out
    print("Removing existing output: %s" % command)
    Popen(command, shell=True).wait()

    command = "cp -r %s %s" % (os.path.join(dir_templates,"website"),dir_out)
    print("Copying website folder: %s" % command)
    Popen(command, shell=True).wait()
    
    command = "cp -r %s %s" % (args.dir_icons,os.path.join(dir_out,'img'))
    print("Copying icons folder: %s" % command)
    Popen(command, shell=True).wait()
    
    assemble_from_template(
        fname_header=os.path.join(dir_templates,"header.html"),
        fname_template=os.path.join(dir_templates,"template.html"),
        fname_footer=os.path.join(dir_templates,"footer.html"),
        fname_json=args.fname_json,
        fname_output=os.path.join(dir_out,"index.html"),
        icon_folder=os.path.basename(args.dir_icons)
        )


if __name__ == "__main__":
    main()