# attendance-scanner
These python scripts are for recording, processing, and generating summaries of attendance data. The Team 3128 Attendance Scanner python libraries run on a Raspberry Pi 3 Model B with a connected barcode scanner to record student IDs. All scripts run from the command line.

### `recordbarcodes.py`
**Usage:** `python recordbarcodes.py`

This script records inputs from the barcode scanner (which register as keyboard input, where the end of a barcode is signified by a whitespace character) and records the times in `scans.csv`. The hours between a scan in and scan out are counted only if the two scans occur on the same date. If the most recent out occurs on a different day than the penultimate scan, the second-to-last scan is ignored and the most recent scan is considered a scan in. Aditionally, a notification is displayed on the LCD panel as to wether the student signed in or signed out, in which the amount of time from that "session" is displayed.

### `proccessrecords.py`
**Usage:** `python proccessrecords.py <output filename>.csv <start date> priv=<true/false>`

This program calculates the total in-workshop hours gained by each student after a certain date (specified by `<start date>` in the form `MM/DD/YYYY`) and outputs it in `<output filename>.csv`

`<output filename>`  
**Note:** Include the .csv extension

`<start date>`  
Enter the date in the format `YYYY-MM-DD`

`prive=<true/false>`  
Wether or not the summary file should be encrypted only to be read by the aristocracy.
