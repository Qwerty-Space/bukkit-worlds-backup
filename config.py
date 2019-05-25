import zipfile as z

## Settings
server_root = ""
backup_location = ""
archive_prefix = "Concord"
date_format = "%Y-%m-%d_T%H-%M"
delete_threshold = 5
backup_format = z.ZIP_STORED

## Backup options are:
    # ZIP_STORED
    # ZIP_DEFLATED
    # ZIP_BZIP2
    # ZIP_LZMA
