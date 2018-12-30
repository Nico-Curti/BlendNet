#!/bin/bash

# $1 = -y
# $2 = installation path from root
# $3 = silent mode (true/false)

confirm=$1
if [ "$2" == "" ]; then
  path2out="toolchain"
else
  path2out=$2
fi
silent=$3

source ~/.bashrc

project="Blender Graph Viewer"
log="install_$project.log"

red=`tput setaf 1`
green=`tput setaf 2`
yellow=`tput setaf 3`
reset=`tput sgr0`

echo ${yellow}"Installing $project dependecies:"${reset}
echo " - Blender (networkx, pandas, matplotlib and numpy)"
source ./shut/bash/install_blender.sh

echo "Installation path : "${green}$path2out${reset}

pushd $HOME > /dev/null
mkdir -p $path2out
cd $path2out

echo "Looking for packages..."
# clean old log file
rm -f $log

# Blender download
if [ $silent ]; then
  install_blender $confirm true networkx pandas matplotlib numpy >> $log;
else
  install_blender $confirm true networkx pandas matplotlib numpy;
fi

popd > /dev/null

