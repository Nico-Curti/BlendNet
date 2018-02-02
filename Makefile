edgelist = ""
filename = ""
dim = 3

define HELP
**Blender viewer for graph**
Usage:\tmake net [edgelist] [filename] [dim]"

optional arguments:
	edgelist -> string of edges (python-like)
	filename -> string with the name of file as csv
	dim      -> number of dimension for network plot (2 or 3)

Note :
- edgelist or filename are mutually exclusive
- network file must be a csv with header names 'source','target',[colors],[x],[y],[z]
    where colors and x,y,z are optional (default random colors and spring layout)
Example:
make net edgelist='[[1,2],[2,3],[3,4]]' dim=3
make net filanem='mynet.csv'
To beginner:
	make example
endef

export HELP

ifeq ($(OS), Windows_NT)
	MKDIR_P = mkdir $(subst /,\,$(OUT)) > nul 2>&1 || (exit 0)
	INSTALL = ./install.ps1
	message = "npt work"
else
	MKDIR_P = mkdir -p $(OUT) 
	INSTALL = ./install.sh
	message = echo "$$HELP"
endif




install: 	install.sh \
		 	install.ps1
		$(INSTALL) -y

net:

	blender --python blend_net.py -- -e $(edgelist) -f $(filename) -d $(dim)

example:

	$(MAKE) net filename="test.csv" dim=3

help:
	$(message)
