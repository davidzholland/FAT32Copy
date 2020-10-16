# FAT32 Copy

Copy music to a usb drive and maintain alphabetical/track order for use with car stereos.

Use at your own risk.

This script does not re-sort existing files. Rather, it assumes you have an empty drive and will maintain sorting while copying music to the drive.

A few key points:

* The primary sort is by track number meta data. Secondary sort is a natural sort by file name.
* Track numbers are removed from file names when sorting by track number for better display on small screens.
* No deletion is performed.
* Script can effectively resume where left off as it will skip existing files. I.e. If you encounter an error or files that are missing track number meta data, you can delete just the specific folder in question from the drive and re-run the script.

### Prerequisites

* Python 3

### Usage

1. Ensure the drive is empty

```sh
python copy_files.py /Full/Path/To/Source\ Directory/ /Full/Path/To/Destination/Drive/
```
