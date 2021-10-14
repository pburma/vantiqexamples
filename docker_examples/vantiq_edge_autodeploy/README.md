### Automate deployment at runtime with Python script

This example runs a python script once Vantiq is up and running to deploy some applications to an edge namespace which is created by the bootstrap.json file when the edge node starts up for the first time.

This approach utilizes the bootstrap.sh file as a custom entrypoint script which checks for the existence of python in the Vantiq container and will run the bootstrapping operations such as install python and run the python code to deploy applications to this edge node. If python is already installed on the container then these steps are skipped and Vantiq is launched. 

The wait-for-it.sh script runs in a wait/loop until the Vantiq port is open and reachable which is necessary in order for the python script to run which is calling the edge nodes rest endpoints to perform the automated operations.

This example is similar to the altDockerfile except it does not use a Dockerfile to create a new image and runs all the operations against the base Vantiq image. 

