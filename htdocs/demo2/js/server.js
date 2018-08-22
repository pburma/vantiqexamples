console.log('Server-side code running');

var express = require('express');
var myParser = require("body-parser");
var Vantiq = require('vantiq-sdk');
var cors = require('cors');
var app = express();

var vantiq = new Vantiq({
    server:     'https://dev.vantiq.com',
    apiVersion: 1
});

// serve files from the public directory
app.use(express.static('public'));
app.use(myParser.urlencoded({extended : true}));
app.use(myParser.json());

//Cors settings
app.use(cors({origin: 'null'}));

// start the express web server listening on 8080
app.listen(8080, () => {
  console.log('listening on 8080');
});

vantiq.accessToken = "8D79h2jxhQOjwfpc8bEYT3cXCnX2lyaDFEjwTg_VhbM=";
//vantiq.accessToken = "<YOUR VANTIQ ACCESS TOKEN>";

console.log("Access Token: " + vantiq.accessToken);

////START SELECT////
function select(resource, prop, where, sort, callback){
  vantiq.select(resource, prop, where, sort)
  .then((result) => {
    if(callback){
      callback(result);
    }
  })
  .catch((error) => {
    console.log("Error " + error);
  })
}

app.post('/select', (req, res) => {
  var resource = req.body.resource;
  var prop = req.body.prop;
  var where = req.body.where;
  var sort = req.body.sort;
  console.log("REQUEST " + resource);
  if(resource){
    select(resource, prop, where, sort, function(response) {
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
////END SELECT////

////START SELECTONE////
function selectone(resource, id, callback){
  vantiq.selectone(resource, id)
  .then((result) => {
    if(callback){
      callback(result);
    }
  })
  .catch((error) => {
    console.log("Error " + error);
  })
}

app.post('/selectone', (req, res) => {
  var resource = req.body.resource;
  var id = req.body.id;
  console.log("REQUEST " + resource);
  if(resource){
    selectone(resource, id, function(response) {
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
////END SELECTONE////

////START COUNT////
function count(resource, where, callback){
  vantiq.count(resource, where)
  .then((result) => {
    if(callback){
      callback(result);
    }
  })
  .catch((error) => {
    console.log("Error " + error);
  })
}

app.post('/count', (req, res) => {
  var resource = req.body.resource;
  var where = req.body.where;
  console.log("REQUEST " + resource);
  if(resource){
    count(resource, where, function(response) {
      if(response){
        console.log(response);
        res.send(JSON.stringify(response));
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
////END COUNT////

////START INSERT////
function insert(resource, object, callback){
  vantiq.insert(resource, object)
  .then((result) => {
    if(callback){
      callback(result);
    }
  })
  .catch((error) => {
    console.log("Error " + error);
  })
}

app.post('/insert', (req, res) => {
  var resource = req.body.resource;
  var object = req.body.object;
  console.log("REQUEST " + resource);
  if(resource){
    insert(resource, object, function(response) {
      if(response){
        console.log(response);
        res.send(JSON.stringify(response));
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
////END INSERT////

////START UPDATE////
function update(resource, id, props, callback){
  vantiq.update(resource, id, props)
  .then((result) => {
    if(callback){
      callback(result);
    }
  })
  .catch((error) => {
    console.log("Error " + error);
  })
}

app.post('/update', (req, res) => {
  var resource = req.body.resource;
  var id = req.body.id;
  var props = req.body.props;
  console.log("REQUEST " + resource);
  if(resource){
    update(resource, id, props, function(response) {
      if(response){
        console.log(response);
        res.send(JSON.stringify(response));
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
////END UPDATE////

////START UPSERT////
function upsert(resource, object, callback){
  vantiq.upsert(resource, object)
  .then((result) => {
    if(callback){
      callback(result);
    }
  })
  .catch((error) => {
    console.log("Error " + error);
  })
}

app.post('/upsert', (req, res) => {
  var resource = req.body.resource;
  var id = req.body.id;
  var props = req.body.props;
  console.log("REQUEST " + resource);
  if(resource){
    upsert(resource, object, function(response) {
      if(response){
        console.log(response);
        res.send(JSON.stringify(response));
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
////END UPSERT////

////START DELETE////
function del(resource, where, callback){
  vantiq.delete(resource, where)
  .then((result) => {
    if(callback){
      callback(result);
    }
  })
  .catch((error) => {
    console.log("Error " + error);
  })
}

app.post('/delete', (req, res) => {
  var resource = req.body.resource;
  var where = req.body.where;
  console.log("REQUEST " + resource);
  if(resource){
    del(resource, where, function(response) {
      if(response == false){
        res.sendStatus(200);
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
////END DELETE////

////START EXECUTE////
function execute(procedure, params, callback){
  vantiq.execute(procedure, params)
  .then((result) => {
    if(callback){
      callback(result);
    }
  })
  .catch((error) => {
    console.log("Error " + error);
  })
}

app.post('/execute', (req, res) => {
  var procedure = req.body.procedure;
  var params = {};
  if(req.body.params) {
    params = req.body.params;
  }
  console.log("REQUEST " + procedure);
  if(procedure){
    execute(procedure, params, function(response) {
      if(response){
        res.send(response);
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
////END EXECUTE////

////START PUBLISH////
function publish(resource, id, payload, callback){
  vantiq.publish(resource, id, payload)
    .then((result) => {
      console.log("Published message successfully.");
      if(callback) {
        callback(result);
      }
    })
    .catch((error) => {
      console.log("Error " + error);
    })
}

app.post('/publish', (req, res) => {
  var resource = 'topics';
  var id = req.body.id;
  var payload = req.body.payload;
  if(req.body.resource){
    resource = req.body.resource;
  }
   if(id){
     publish(resource, id, payload, function(response){
         if(response == false) {
           res.sendStatus(200);
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
////END PUBLISH////

////START UPLOAD////
function upload(name, fileType, content, callback){
  vantiq.upload(name, fileType, content)
    .then((result) => {
      console.log("Published message successfully.");
      if(callback) {
        callback(result);
      }
    })
    .catch((error) => {
      console.log("Error " + error);
    })
}

app.post('/upload', (req, res) => {
  var name = req.body.name;
  var fileType = req.body.fileType;
  var content = req.body.content;
   if(name){
     upload(name, fileType, content, function(response){
         if(response) {
           res.send(response);
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
////END UPLOAD////

////START DOWNLOAD////
function download(path, callback){
  vantiq.download(path)
    .then((result) => {
      if(callback) {
        callback(result);
      }
    })
    .catch((error) => {
      console.log("Error " + error);
    })
}

app.post('/download', (req, res) => {
  var path = req.body.path;
   if(path){
     download(path, function(response){
         if(response) {
           res.send(response);
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
////END DOWNLOAD////
