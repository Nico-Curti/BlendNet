#!/bin/bash
source ~/.bashrc

red=`tput setaf 1`
green=`tput setaf 2`
yellow=`tput setaf 3`
reset=`tput sgr0`
cmake_version="3.10.1"
ninja_version="1.8.2"

echo ${yellow}"Installing blend_net dependecies:"${reset}
echo " - Blender (networkx, pandas, matplotlib and numpy)"
source ./shell_utils/bash/install_blender.sh

if [ "$2" == "" ]; then	path2out="toolchain"; else path2out=$2; fi
echo ${green}"Installation path : "~/$path2out${reset}

pushd $HOME > /dev/null
mkdir -p $path2out
cd $path2out

echo "Looking for packages..."

# Blender download
printf "Blender identification: "
if [ $(which blender) == "" ]; then
	echo ${red}"NOT FOUND"${reset}
	if [ "$3" == "-y" ] || [ "$3" == "-Y" ] || [ "$3" == "yes" ]; then install_blender "https://builder.blender.org/download/blender-2.79-ce3e0afe597-linux-glibc219-x86_64.tar.bz2" "." true networkx pandas matplotlib numpy;
	else
		read -p "Do you want install it? [y/n] " confirm
		if [ "$CONFIRM" == "n" ] || [ "$CONFIRM" == "N" ]; then echo ${red}"Abort"${reset};
		else install_blender "https://builder.blender.org/download/blender-2.79-ce3e0afe597-linux-glibc219-x86_64.tar.bz2" "." true networkx pandas matplotlib numpy;
		fi
	fi
else echo ${green}"FOUND"${reset};
fi

popd > /dev/null

