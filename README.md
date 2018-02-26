# colossus_server

This gets the data from the DAQ to all the devices that are trying to see it.  It is meant to be used with the [Colossus_website](https://github.com/cyficowley/colossus_website/).

# run

Run the python (main.py) from the SEDS laptop. It establishes an ftp link with the DAQ and runs a flask api where the data can be requested from.  This requires a windows laptop because it has some weird dlls.

Then from the server that is doing the web hosting of colossus_website run `node index.js`. This starts the websocket server which will push the data to all the actual clients.  It requests the data from the flask api on the sedstop.


The reason we have two different servers, the flask one just having one client and the node websocket one everyone else is because we are doing everything we can to save cpu on the seds laptop  and don't want to deal with running a legit server on windows.
