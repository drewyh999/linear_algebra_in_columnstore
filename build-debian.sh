if [ -z ${MONETDB_INSTALL_PATH} ];
  then echo "MonetDB installation path is unset";
  else echo "MonetDB installation path is set to '$MONETDB_INSTALL_PATH'";
fi
mkdir -p cmake-build-debug
mkdir -p $MONETDB_INSTALL_PATH
cmake -DCMAKE_BUILD_TYPE=Debug -DCMAKE_INSTALL_PREFIX=$MONETDB_INSTALL_PATH -DASSERT=ON -DSTRICT=0 -S . -B cmake-build-debug
cmake --build cmake-build-debug --target install