#!/usr/bin/env python3
import sys
import os
import zipfile
from bs4 import BeautifulSoup

def bundle_downloads(index_html_files):
    """
    For each index.html in the list, parse out the data-downloads-uid and
    data-downloads-files attributes. Then create a zip in public/zips/<uid>.zip.
    """
    for html_file in index_html_files:
        with open(html_file, "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")

        # find all the blocks
        blocks = soup.find_all("div", class_="download-example-block")
        if not blocks:
            continue

        for block in blocks:
            uid = block.get("data-downloads-uid")        # e.g., "example1-tcl"
            files_str = block.get("data-downloads-files") # e.g., "file1.tcl|file2.tcl"

            if not uid or not files_str:
                continue

            files_list = files_str.split("|")
            # directory containing index.html
            dirpath = os.path.dirname(html_file)

            # create the "public/zips" folder if needed
            zip_dir = os.path.join("public", "zips")
            os.makedirs(zip_dir, exist_ok=True)

            zip_path = os.path.join(zip_dir, f"{uid}.zip")
            print(f"Creating zip: {zip_path}")
            print(f" - Found files: {files_list}")

            with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
                for rel_file in files_list:
                    full_path = os.path.join(dirpath, rel_file)
                    if os.path.isfile(full_path):
                        # add the file to the zip archive
                        zf.write(full_path, arcname=rel_file)
                    else:
                        print(f"WARNING: file not found: {full_path}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python bundle-downloads.py public/examples/*/index.html [etc...]")
        sys.exit(1)

    bundle_downloads(sys.argv[1:])

if __name__ == "__main__":
    main()

