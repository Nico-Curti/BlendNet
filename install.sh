#!/bin/bash

# $1 = -y
# $2 = installation path from root

source ~/.bashrc

project="Blender Graph Viewer"

red=`tput setaf 1`
green=`tput setaf 2`
yellow=`tput setaf 3`
reset=`tput sgr0`

if [[ "$OSTYPE" == "darwin"* ]]; then
    url_blender="https://ftp.halifax.rwth-aachen.de/blender/release/Blender2.79/blender-2.79-macOS-10.6.tar.gz"
else
    url_blender="https://ftp.halifax.rwth-aachen.de/blender/release/Blender2.79/blender-2.79-linux-glibc219-x86_64.tar.bz2"
fi

printf ${yellow}"Installing $project dependecies:\n"${reset}
printf " - Blender (networkx, pandas, matplotlib and numpy)\n"
source ./shell_utils/bash/install_blender.sh

if [ "$2" == "" ]; then path2out="toolchain"; else path2out=$2; fi
printf ${green}"Installation path : "~/$path2out"\n"${reset}

pushd $HOME > /dev/null
mkdir -p $path2out
cd $path2out

log="install_$project.log"

echo "Looking for packages..."

# Blender download
install_blender $1 true networkx pandas matplotlib numpy >> $log;

popd > /dev/null

