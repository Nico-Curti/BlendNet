edgelist = ""
filename = ""
dim = 3


ifeq ($(OS), Windows_NT)
	MKDIR_P = mkdir $(subst /,\,$(OUT)) > nul 2>&1 || (exit 0)
	INSTALL = ./install.ps1
	HELP = Write-Host "Blender viewer for graph:\nUsage:\tmake net edgelist='' filename='' dim=3\n"
else
	MKDIR_P = mkdir -p $(OUT) 
	INSTALL = ./install.sh
	HELP = echo "Blender viewer for graph:\nUsage:\tmake net edgelist='' filename='' dim=3\n"
endif


install: 	install.sh \
		 	install.ps1
		$(INSTALL) -y

net:

	blender --python blend_net.py -- -e $(edgelist) -f $(filename) -d $(dim)

example:

	$(MAKE) net filename="test.csv" dim=3



#edgelist="[[1,2],[2,3],[3,4]]" dim=3

help:
	$(HELP)
