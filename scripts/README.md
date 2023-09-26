# Useful scripts for starting and stopping MonetDB

## Starting MonetDB
If you don't want to use IDE to run the Mserver, you can use the script `start_monetdb.sh` to start, 
however, you need to set the environment variable `MONETDB_INSTALL_PATH` where you have installed your monetdb install, for instance, mine is `/Users/zhuyuanhao/Downloads/uzh/MasterThesis/MonetDB-11.43.25/install`
Then also specify your db path `MONETDB_DB_PATH` , this is the path you give in the `mserver5` command
Then using `bash start_monetdb.sh` you can start the MonetDB in command line

## Force shutting down MonetDB 
There are a lot of times when you cannot just press control+D to stop the MonetDB instance, to save your time, the `shutdown_monetdb.sh` will got to the database path
and get the PID of the MonetDB in the `.gdk_lock` file then kill it with flag -9 to force quit the MonetDB

## Configuration file for Clion
Here I also attached a configuration file for clion which you can use then run MonetDB compiling all files in one click