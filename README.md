# Mapbox Uploadscript and GUI
This is the repository for uploading new Tilesets from a local computer to your personal Mapbox Database using Mapbox API.
It is currently in alpha state, so don't expect a polished and bugfree application.

Feel free to fork and contribute.

# Introduction
These python-based applications can be used to upload new generated georeferenced images. It can be used as pure script or a GUI.
They were developed during my student research project at TU Braunschweig and become important for viewing the maptiles in a webapplication in realtime.
(check out my other repository "web_interface" for more information about the webapplication).

For a detailed desription of these scripts refer to my elaboration.
It is located in the IFF at TU Braunschweig. Feel free to ask me for a digital version.

### What it can do

- Using a config file for easy setup
- Constantly checking local repository for new Data using a simple algorithm
- Automatic upload of new recognized and predefined data of a specific dataset
- Visualization of current uploadstate and logging this data to a log.txt file

### What NOT to expect

- Recognize more than one defined dataset
- converting images to georeferenced tilesets
- bugfree and polished application

### Dependencies

Python 2.7

Mapbox Python SDK

-> https://github.com/mapbox/mapbox-sdk-py

wxPython (for GUI)

-> https://wxpython.org/

### Quick Start

**Step 1:** Create Mapbox Account:

https://www.mapbox.com/

**Step 2:** Setup configfile for scriptusage:

[AccountData]

username = *your mapbox username*

accesstoken = *your mapbox Accesstoken* 
(Create a Secret Token with permissions to upload data at your Mapboxaccount https://www.mapbox.com/account/ )

**These AccountData need to be changed in the Code of the GUI manually, because it is not using the configfile !!**

[Uploaddata]

path = *path to your local folder*

UAVname = *name of your Dataset without a running number*

datatype = *Datatype of your Tilesets i.e. ("mbtiles" or "tiff")*

startingtileset = *Starting running number of your dataset to upload first*

**These Uploaddata will be set directly in the GUI, if you are using it !!**

**Step 3:** Start script or GUI:

```sh
$ python UploadGUI.py
```
