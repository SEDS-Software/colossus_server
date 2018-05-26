# colossus_server

This gets the data from the DAQ to all the devices that are trying to see it.  It is meant to be used with the [Colossus_website](https://github.com/cyficowley/colossus_website/).


##### CURRENTLY THE SERVER BREAKS AND HAS TO BE RESTARTED EVERY TIME GANTNER REBOOTS

# setup

Download this repo on both the seds laptop and raspberry pi

The python main.py file will run from the seds laptop

The node server within the node folder will run from the raspberry pi

# run

Double click the colossus server icon on the desktop or run the python file `colossus_server/main.py` from the SEDS laptop. It establishes an ftp link with the DAQ and runs a flask api where the data can be requested from.  This requires a windows laptop because it has some weird dlls.

Then plug in the raspberry pi which will automatically start the websocket and start pushing the data to all connected devices on port 192.168.100:8080. (the actual ip address could possibly change but the port won't)

If it doesn't automatically start run `node ~/colossus_server/node/index.js` to start it up. All the startup configuration is done in `/etc/rc.local`.

The reason we have two different servers, the flask one just having one client and the node websocket one everyone else is because we are doing everything we can to save cpu on the seds laptop  and don't want to deal with running a legit server on windows.
