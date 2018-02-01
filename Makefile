edgelist = ""
filename = ""


ifeq ($(OS), Windows_NT)
	MKDIR_P = mkdir $(subst /,\,$(OUT)) > nul 2>&1 || (exit 0)
	INSTALL = ./install.ps1
else
	MKDIR_P = mkdir -p $(OUT) 
	INSTALL = ./install.sh
endif


install: 	install.sh \
		 	install.ps1
		$(INSTALL) -y

net:

	blender --python blend_net.py -- -e $(edgelist) -f $(filename)

example:

	$(MAKE) net edgelist="[[1,2],[2,3],[3,4]]"