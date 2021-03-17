## Advanced Edge Deployment

Provides examples of heavy customizations including:

* Overriding the docker entry script to perform some custom automation eg; onboarding processes
* Incorporating other services as adjacent containers.
* Utilizing new env variables to help automate deployments

Will not show customizations to the mongo setup or white labeling as those have their own example pages. 

## Vantiq Docker Image

The Vatiq docker image is built with an entrypoint script that runs when the container starts up. This example will customize the entrypoint script to run a series of bash command before the Vantiq service is started. 

**NOTE** this is probably not the best solution for production deployments, for example I use this method to run a python script which requires first installing python using apt commands. It would be better to build a custom Vantiq docker image using a Dockerfile to customize the image and then using the docker build and export commands to create a shareable custom image in a tar.gz that can be loaded with docker import. However...this approach is helpful when sharing large files is not possible as only the text yaml/sh/py files need to be shared as opposed to a very large docker image file.

### Entrypoint

The Vantiq docker image can be examined using the docker inspect command which will show all the images details. One detail in particular is the entrypoint setting which specifies the commands to run when the container boots up. For Vantiq this file is:

/opt/vantiq/bin/vantiq.sh

It is possible to create a custom version of this script but I prefer to leave it as is and run it after I have done all my bootstrapping steps, which means overriding the entrypoint setting with a new file in the docker\-compose.yml file. 

The following additional files are needed to run this example:

* ```bootstrap.sh```  - this becomes our new entrypoint file
* ```vantiqedge_bootstrap.py``` - python script that performs more complex onboarding actions
* ```wait-for-it.sh``` - lets me know when Vantiq is up and running so I can run the python script. You can find this file here [Wait For It](https://github.com/vishnubob/wait-for-it)

The license files are also needed. 

### bootstrap.sh and vantiqedge_bootstrap.py

These files are used to perform automation activities to run before Vantiq starts up. The bootstrap.sh file is authored in a way to only perform the python installation once, and then run the vantiq.sh entrypoint script on subsequent reboots. 

Example ```bootstrap.sh```

This file will check to see if python is installed. If not we know we are in a first run situation and can install python, initiate the wait-for-it loop and then run the vantiqedge_bootstrap.py python script once the Vantiq server is up and running. 

If python is already installed we simply then execute the vantiq.sh entrypoint script. 

Example ```vantiqedge_bootstrap.py```

This file will perform some onboarding functions through Vantiq's API interface to automatically onboard an edge node by adding a cloud node definition to a namespace. The ```wait-for-it.sh``` shell script is important to ensure Vantiq's API is accessible prior to running the python script. 

The result is that an onboarding process can be fully automated for Vantiq which includes adding a local cloud node and a remote edge node definition so that an application deployment could also automatically occur that might run specific customer applications or just include a series of management tools so that it will be possible to automate the onboarding of customers for multi-tenet installations. 

### Env variables

In order to make the deployment more dynamic and less static a number of environment variables have been defined so that users can set their own node properties, cloud tokens, ect. These variables, especially the CLOUDTOKEN, need to be filled out prior to running the example script. Users can customize their own env variables which can be either pulled into a shell script or a python script as shown in this project using the os.getenv() method.  

## Other Customizations

* A MQTT broker was added as a separate service which is included in the deployment. 
* The MQTT container is given as hostname definition. 
* An additional Links definition was added so that a Vantiq source can connect to the MQTT broker, the URL used in this example is "mqtt.local". Now a local data source like an AI inference engine, an IoT device, ect can stream data into Vantiq via the MQTT broker using the docker host IP and port 1883 or by adding the service to the docker configuration as well and using the mqtt.local hostname. 

