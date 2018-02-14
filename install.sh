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
printf "Blender identification: "
if [ $(which blender) == "" ]; then
	echo ${red}"NOT FOUND"${reset}
	if [ "$3" == "-y" ] || [ "$3" == "-Y" ] || [ "$3" == "yes" ]; then install_blender $url_blender "." true networkx pandas matplotlib numpy >> $log;
	else
		read -p "Do you want install it? [y/n] " confirm
		if [ "$CONFIRM" == "n" ] || [ "$CONFIRM" == "N" ]; then echo ${red}"Abort"${reset};
		else install_blender $url_blender "." true networkx pandas matplotlib numpy >> $log;
		fi
	fi
else echo ${green}"FOUND"${reset};
fi

popd > /dev/null

