import os
import zipfile
import config as c
from datetime import datetime
import logging

logging.basicConfig(level=logging.DEBUG)

d = datetime.now()
archive_name = f"concordia_backup-{d.strftime(c.date_format)}.zip"

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

def main():
    zipf = zipfile.ZipFile(os.path.join(c.backup_location, archive_name), "w", zipfile.ZIP_DEFLATED)
    zipdirs((world, world_nether, world_end), zipf)
    print(zipf)
    zipf.close()



if __name__ == "__main__":
    main()
