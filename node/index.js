const WebSocket = require('ws');
const http = require('http');
 
// const websocket = new WebSocket();
const ws = new WebSocket.Server({ port: 8080 });
 

ws.on('error', () => console.log('errored'));

ws.on('uncaughtException', () => console.log("errored uncought"));

ws.on('connection', function connection(ws) {
  ws.isAlive = true;
  ws.on('pong', heartbeat);
});


function noop() {}
 
function heartbeat() {
  this.isAlive = true;
}
 
const interval = setInterval(function ping() {
  ws.clients.forEach(function each(ws) {
    if (ws.isAlive === false) return ws.terminate();
    ws.isAlive = false;
    ws.ping(noop);
  });
}, 30000);


ws.on('close', function () {
  console.log('disconnected client');
});


ws.broadcast = function broadcast(data) {
	let newData = JSON.stringify(data); 
  ws.clients.forEach(function each(client) {
    if (client.readyState === WebSocket.OPEN) {
    	try{
      	client.send(newData,function () { /* ignore errors */ });
    	}
    	catch(e){
  			console.log('caught e');
    	}
    }
    else{
    	console.log(client.readyState);
    }
  });

};


setInterval(() => {http.get('http://192.168.1.21:5000/', (res) => {
	  const { statusCode } = res;

	  let error;
	  if (statusCode !== 200) {
	    error = new Error('Request Failed.\n' +
	        'Status Code: ${statusCode}\nIts possible the server hasnt started yet');
	  }
	  if (error) {
	    console.error(error.message);
	    // consume response data to free up memory
	    res.resume();
	    return;
	  }

	  res.setEncoding('utf8');
	  let rawData = '';
	  res.on('data', (chunk) => { rawData += chunk; });
	  res.on('end', () => {
	    try {
	      ws.broadcast(JSON.parse(rawData));
	    } catch (e) {
	      console.error(e.message);
	    }
	  });
	}).on('error', (e) => {
	  console.error(`Got error: ${e.message}`);
	})} ,1000);
	







