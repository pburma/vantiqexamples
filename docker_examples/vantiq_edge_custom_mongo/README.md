### Custom Mongo Settings.

The mongodb connection settings are provided by a mongoDbService.json file. The contents of this file can be:

```
{ 
     "host": "mongo.local",
     "databaseName: <mongodb-name>,
     "username": <username>,
     "password": <password>
}
```

1. Create a mongoDbService.json file with these details in it that will get mounted into the Vantiq container. 
2. Set the corresponding environment variables in the docker\-compose.yml file for Mongo user/pass/name. 
    - Because these are env variables note that you can set them as system env variables instead of hard coding them into the yaml file.
3. In this example I use the "links" setting to specify the connection hostname for the mongo container. The hostname can be changed to a proper hostname.

A **hosts** value can be added as an array of json objects containing a different host value. This is an example from a K8 configMap with proper char escaping. 

```
"{\n\"hosts\": [\n{ \"host\": \"mongodb-0.cluster.local\" },\n{ \"host\": \"mongodb-1.cluster.local\"},\n{\"host\": \"mongodb-2.cluster.local\"}\n}"
```

Unescaped version:

```
{
    "hosts": [
        {"host": "mongodb-0.cluster.local" },
        {"host": "mongodb-1.cluster.local"},
        {"host": "mongodb-2.cluster.local"}
    ]
}
```

Generally a single Mongo DB container is used for Edge deployments. 