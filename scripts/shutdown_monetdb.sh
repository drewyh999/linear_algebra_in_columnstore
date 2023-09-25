# Make sure error got exit
set -e
echo "Shutting down monetdb"
# Get MonetDB PID in gdk lock file
MONETDB_PID=$(cat $MONETDB_INSTALL_PATH/farm/test/.gdk_lock | grep PID | awk '{split($2, a, "="); print a[2]}')
echo "MonetDB pid is $MONETDB_PID"
kill -9 $MONETDB_PID
echo "MonetDB process killed"
