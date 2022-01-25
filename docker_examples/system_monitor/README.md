## Use Vantiq to monitor docker system and container disk, cpu and memory utilization.

This example will use the Docker API to pull system utilization data such as disk utilization, memory use and cpu use per container. I used Docker's v1.41 API in this example. 

[Docker API v1.41](https://docs.docker.com/engine/api/v1.41/)

The Docker API has to be made available before the sample project can be used. This means enabling the API for the Windows/Mac/Linux host you are using and also making the API available from inside the container. The instructions seem to vary by OS and there isn't a good guide on the docker website so a Google search is needed here to find the best instructions. 

The second part of this is making the API endpoint accessible from inside the container. There may be different ways to do this but I choose to enable the host.docker.internal URL available from inside the container. To do this modify the Vantiq service entry in the docker-compose.yml to include the following:

    extra_hosts:
    - "host.docker.internal:host-gateway"

Usage:
* Enable the Docker API based on the directions you find from a Google search. (Docker desktop on Windows has a setting you can tick off to enable the tcp daemon)
* Stop your docker containers if they are running and modify your yml file to include the extra_hosts entry. 
* Restart docker and restart your containers (docker-compose down, docker-compose up -d)
* Log into Vantiq and navigate to a new or existing namespace (anything other than System)
* Use the Project --> Import button to bring up the import dialog. Drag and drop the Zip file located in this repo into that dialog. 
* Run the DockerMonitor client. 

You should see the system performance stats for each running container as this time. 

### How it works
* A Source called DockerAPI was setup to connect to http://host.docker.internal:2375. 
* A procedure called listContainers is run by the Client when the page loads. 
* The listContainers procedure will run getStats and getDiskUsage procedures. 
* getStats reads the results of /containers/{id}/stats?stream=false to produce the CPU and memory utilization. 
* getDiskUage uses the API exec feature to run a "df -h" on the containers command line to get disk data and then uses a regex to pull out the disk size/used/available/use% details for the overlay row which is the "/" root filesystem path. 

The client uses a simple data table to display the results. 

### How to use
The intended purpose of this code is to be able to run periodic checks on the system details and look for problems like low disk space. To implement such an application a Scheduled Event can be created that runs the listContainer code periodically. The easiest way to build a monitor is to create an App that uses basic conditionals to trigger alerts. The scheduled event should run the procedures that need to be modified to output the results to a topic. Your app will then consume the details on that topic and a filter can be added to look for issues like low disk space eg; "event.use < 90%". The downstream event can then send an alert or trigger a collaboration. 
