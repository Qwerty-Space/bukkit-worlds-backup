import os
import time
import logging
import zipfile
import config as c
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
    for path in paths:
        add_files(path)

def remove_old():
    files = os.listdir(c.backup_location)
    for f in files:
        if os.stat(os.path.join(c.backup_location, f)).st_mtime < now - c.delete_threshold * 86400:
            print(f)


def main():
    zipf = zipfile.ZipFile(os.path.join(c.backup_location, archive_name), "w", zipfile.ZIP_DEFLATED)
    zipdirs((world, world_nether, world_end), zipf)
    print(zipf)
    zipf.close()


if __name__ == "__main__":
    main()
    remove_old()
