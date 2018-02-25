var Client = require('ftp');

var c = new Client();
c.on('ready', function() {
  c.list(function(err, list) {
    if (err) throw err;
    console.dir(list);
    c.end();
  });
});
// connect to localhost:21 as anonymous
c.connect({"host":"192.168.1.28", "user":"6","password":"6"});
c.get("hd0/DATA",() => {
	
});