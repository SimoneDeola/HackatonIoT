var express = require('express');
var fs = require("fs");
const sqlite3 = require('sqlite3').verbose();
var app = express();



let db = new sqlite3.Database(__dirname + '/database.db', (err) => {
  if (err) {
    return console.error(err.message);
  }
  console.log("connected to database: " + __dirname + '/database.db');
});




app.get('/', function (req, res) {
   res.send('Hello World');
})


var server = app.listen(8081, function () {
   var host = server.address().address
   var port = server.address().port
   
   console.log("Example app listening at http://%s:%s", host, port)
})