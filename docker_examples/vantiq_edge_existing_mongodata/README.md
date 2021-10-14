## Running Vantiq Edge with pre-existing data from Mongo

This is experimental solution to pre-load Vantiq with mongo.

There are a couple approaches that could be considered here. One is to setup Vantiq and load it with the content first and then save the Mongo image and commit it as a separate image to docker. The second approach which is used here is to export the Mongo database and mount the export file into the container at run time and load it, which means you have to check for the existence of the Vantiq collections at startup to make sure you don't re-run the import.

Currently this setup does not check for existing import data and resets the Vantiq server back to this original configuration each time there is a restart. A custom shell script would need to be added to replace the default entry-point file that would do a check to see if the import has already occurred, either by looking for existing data on the drive or logging into mongo and running the show collections command.



