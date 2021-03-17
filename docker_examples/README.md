## Running Vantiq Edge From Docker

These examples require Docker Compose, a Vantiq license key and access to the private Vantiq repository on Docker Hub. 

[Docker Compose](https://docs.docker.com/compose/install/)

The docker compose can be broken down into docker run command but the docker-compose method provides a simple mechanism to define multiple parameters for running more than one container that interact with each other. This is helpful when setting up Vantiq which requires MongoDB for storage as the network and volume definitions can be added to the yml configuration document instead of using very long docker run commands. 

Usage:
* Make sure docker and docker\-compose are both installed. 
* Simplest way to run docker\-compose commands is from inside the directory containing the .yml file although you can reference the yml directly.
* These examples should all work on Windows, Mac and Linux. Open a shell/terminal/prompt. Simply cd into the folder containing the .yml file after cloning this git repo. 
* ```docker-compose up -d ``` will start docker in daemon mode. Leaving the \-d out is sometimes useful for troubleshooting as stdout messages will appear in your terminal.
* ```docker-compose down``` will stop the containers. If you want to delete everything, the containers, images and mongo volume add ```--rmi all -v```. Next time you run the up command the images will be redownloaded so only use if you really, really want to delete everything including the Mongo volume. 
* In these examples the license files (required for Vantiq 1.29+) are individually added using volume mount. Individual files such as those used for white labeling can be added in the same manner. 
* The image attribute contains the version name to install, this should be changed to the specific version you wish to install. The image names can be found in the Vantiq docker hub repository.
* Access to the Vantiq image on the Docker Hub website requires a login so please contact Vantiq for both a Docker login and license key. 
* TLS secrets for HTTPS deployments using a reverse ingress proxy (like Nginx or HAProxy) would need to be added by the user before running. [Docker Secrets](https://docs.docker.com/engine/swarm/secrets/)

### Kubernetes

These examples can be applied to Kubernetes pretty easily. The volume mounts for individual files and TLS secrets would go away and be converted into a configMap and much of the docker\-compose.yml file can be converted using [Kompose](https://kompose.io/) however some additional modifications to the converted .yml should be expected. Kubernetes is used for clustered deployments and one caveat here is that these are all Vantiq Edge examples which means running just 1 instance of each service as Vantiq Edge does not support clustering. 

One issue that will occur is that the network name for the Mongo connection uses underscores in the name, "vantiq_edge_mongo". This will need to get changed to a hyphen in the K8 ymls. One thing I've done in some instances is use the "links:<hostname>" attribute to set the hostname to communicate between containers but I am not sure how this converts to K8. 

