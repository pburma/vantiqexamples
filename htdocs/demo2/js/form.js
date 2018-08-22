var express = require('express');
var bodyParser = require('body-parser');
var Vantiq = require('vantiq-sdk');
var app     = express();

var vantiq = new Vantiq({
    server:     'https://dev.vantiq.com',
    apiVersion: 1
});

vantiq.accessToken = "8D79h2jxhQOjwfpc8bEYT3cXCnX2lyaDFEjwTg_VhbM=";

//Note that in version 4 of express, express.bodyParser() was
//deprecated in favor of a separate 'body-parser' module.
app.use(bodyParser.urlencoded({ extended: true }));


app.listen(8080, function() {
  console.log('Server running at http://127.0.0.1:8080/');
});

console.log("Access Token: " + vantiq.accessToken);

function select(resource, callback){
  vantiq.select(resource)
  .then((result) => {
    if(callback){
      callback(result);
    }
  })
  .catch((error) => {
    console.log("Error " + error);
  })
}

//app.use(express.bodyParser());
app.post('/select', (req, res) => {
  var resource = req.body.resource;
  console.log("REQUEST " + req);
  if(resource){
    select(resource, function(response) {
      if(response){
        console.log(response);
        res.send(response);
        //res.sendStatus(200);
      }
      else {
        res.sendStatus(400);
      }
    })
  }
  else {
    res.sendStatus(400);
  }
});
