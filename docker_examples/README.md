## Running Vantiq Edge From Docker

These examples require Docker Compose, a Vantiq license key and access to the private Vantiq repository on Docker Hub. 

[Docker Compose](https://docs.docker.com/compose/install/)

The docker compose can be broken down into docker run command but the docker-compose method provides a simple mechansim to define multiple parameters for running more than one container that interact with each other. This is helpful when setting up Vantiq which requires MongoDB for storage as the network and volume definitions can be added to the yml configuration document instead of using very long docker run commands. 

Usage:
* Make sure docker and docker\-compose are both installed. 
* Simplest way to run docker\-compose commands is from inside the directory containing the .yml file although you can reference the yml directly.
* ```docker-compose up -d ``` will start docker in daemon mode. Leaving the \-d out is sometimes useful for troubleshooting as stdout messages will appear in your terminal.
* ```docker-compose down``` will stop the containers. If you want to delete everything, the containers, images and mongo volume add ```--rmi all -v```. Next time you run the up command the images will be redownloaded so only use if you really, really want to delete everything include the Mongo volume. 
* In these examples the license files (required for Vantiq 1.29+) are individually added using volume mount. Individual files such as those used for white labeling can be added in the same manner. 
* Access to the Vantiq image on the Docker Hub website requires a login so please contact Vantiq for both a Docker login and license key. 
* TLS secrets for HTTPS deployments using a reverse ingress proxy (like Nginx or HAProxy) would need to be added by the user before running. [Docker Secrets] (https://docs.docker.com/engine/swarm/secrets/)

These examples can be applied to Kubernetes pretty easily. The volume mounts for individual files and TLS secrets would go away and be converted into a configMap and much of the docker\-compose.yml file can be converted using [Kompose] (https://kompose.io/) however some additional modifications to the converted .yml should be expected. Kubernetes is used for clustered deployments and one caveat here is that these are all Vantiq Edge examples which means running 1 replica instance of each service. 

