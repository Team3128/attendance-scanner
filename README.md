# README.md
This documentation pertains to the Team 3128 attendance scanner python libraries made to run on a Raspberry Pi 3 Model B with a connected barcode scanner. All scripts are ran from the command line.

### `recordbarcodes.py`
**Usage:** `python recordbarcodes.py`

This script records inputs from the barcode scanner(which register as key presses) and adds times when someone signs in in scan.csv. The data stored there are student IDs, local scan in times and local scan out times. If the scan out occurs on the same date as the scan in, then the hours are counted. If two adjacent scans occur on different days, then the first scan is voided, adnt eh second scan marks the beginning of a new scan.

### `proccessrecords.py`
**Usage:** `python proccessrecords.py <output filename>.csv <start date> priv=<true/false>`

This program calculates the total student in-workshop hours gained after a certain date(specified by `<start date>`) and outputs it in `<output filename>.csv`

`<output filename>`
**Note:** Include the .csv extension

`<start date>`
Enter the date in the format `YYYY-MM-DD`
