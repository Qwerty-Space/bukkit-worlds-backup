import os
import logging
import zipfile
import config as c
import time
from datetime import datetime, date

logging.basicConfig(level=logging.DEBUG)

now = time.time()# + 7 * 86400
formated_date = time.strftime(c.date_format)
archive_name = f"{c.archive_prefix}_{formated_date}.zip"

world = os.path.join(c.server_root, "world")
world_nether = os.path.join(c.server_root, "world_nether")
world_end = os.path.join(c.server_root, "world_the_end")


def zipdirs(paths, ziph):
    # ziph is zipfile handle
    def add_files(path):
        for root, dirs, files in os.walk(path):
            for f in files:
                f_dir = os.path.join(root, f)
                ziph.write(f_dir, arcname=os.path.relpath(os.path.join(root, f), c.server_root))
                print(f"Written file {f}")
    for path in paths:
        if not os.path.isdir(path):
            print(f"{path} does not exist")
            continue
        print(f"Adding {path}")
        add_files(path)

def backup():
    try:
        zipf = zipfile.ZipFile(os.path.join(c.backup_location, archive_name), "w", c.backup_format)
    except FileNotFoundError:
        print(f"{c.backup_location} does not exist")
    print("Zipping files")
    zipdirs((world, world_nether, world_end), zipf)
    zipf.close()

def remove_old():
    print("Checking for old files:")

    with os.scandir(c.check_location) as fs:
        sorted_files = sorted(fs, key=lambda f: (f.stat().st_mtime, f.path))
        rmamnt = max(0, len(sorted_files) - c.delete_threshold)

    for f in sorted_files[0:rmamnt]:
        print(f.name)
        os.remove(f.path)

    print(f"{rmamnt} file(s) removed.")


if __name__ == "__main__":
    backup()
    remove_old()
