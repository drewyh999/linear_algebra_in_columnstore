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
in this configuration file, we assume that you choose to install the MonetDB in the same folder as the code and you initailize a database called test.


Also, you should make sure that the cmake settings of clion have the following Cmake options:
`-DCMAKE_INSTALL_PREFIX=[PATH TO YOUR FAVORATE MONETDB INSTALLATION] -DASSERT=ON -DSTRICT=0`

## Clion remote development
You can use jetbrains client to directly develop and debug code that are on the server from your own computer.
In clion, go to `file -> remote development -> ssh connection` then use the same credentials you use to log in the vm then 
a jetbrains client will be installed on the vm and you can start to develop and debug exactly the same as the local clion

## Build on debian server
If you don't want to use jetbrain's remote development features, you can also use the script `build-debian.sh` in the 
root directory of the project to easily build the MonetDB, note that you should also set the `MONETDB_INSTALL_PATH` before you
run that script