#!/bin/bash
source ~/.bashrc

red=`tput setaf 1`
green=`tput setaf 2`
yellow=`tput setaf 3`
reset=`tput sgr0`
cmake_version="3.10.1"
ninja_version="1.8.2"

echo ${yellow}"Installing blend_net dependecies:"
echo "- Blender (networkx and pandas)"

if [ "$2" == "" ]; then	path2out="toolchain"; else path2out=$2; fi
echo ${yellow}"Installation path : "~/$path2out

pushd $HOME
mkdir -p $path2out
cd $path2out

echo "Looking for packages..."

# Blender download
echo "Blender identification"
if [ ! -x "blender" ]; then
	echo ${red}Blender not FOUND
	if [ "$3" == "-y" ] || [ "$3" == "-Y" ] || [ "$3" == "yes" ]; then
		echo download blender from http://download.blender.org/source/blender-2.79.tar.gz
		wget http://download.blender.org/source/blender-2.79.tar.gz
		wget https://bootstrap.pypa.io/get-pip.py


	else
		read -p "Do you want install it? [y/n] " confirm
		if [ "$CONFIRM" == "n" ] || [ "$CONFIRM" == "N" ]; then echo ${red}"Abort";
		else 
			echo download blender from http://download.blender.org/source/blender-2.79.tar.gz
			wget http://download.blender.org/source/blender-2.79.tar.gz
			wget https://bootstrap.pypa.io/get-pip.py
		fi
	fi
else echo ${green}"Blender FOUND";
fi


popd

