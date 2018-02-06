edgelist = ""
filename = ""
dim = 3
direct = 0

define HELP_WIN
**Blender viewer for graph** & @echo.\
Usage:   make draw [edgelist] [filename] [dim] & @echo.\
& @echo.\
optional arguments: & @echo.\
.    edgelist - string of edges (python-like) & @echo.\
.    filename - string with the name of file as csv & @echo.\
.    dim      - number of dimension for network plot (2 or 3) & @echo.\
.    direct   - bool for directed/undirected graph & @echo.\
& @echo.\
Note : & @echo.\
- edgelist or filename are mutually exclusive & @echo.\
- network file must be a csv with header names 'source','target',[colors],[x],[y],[z] & @echo.\
.    where colors and x,y,z are optional (default random colors and spring layout) & @echo.\
Example: & @echo.\
make draw edgelist='[[1,2],[2,3],[3,4]]' dim=3 & @echo.\
make draw filename='mynet.csv' & @echo.\
To beginner: & @echo.\
.    make test 
endef
define HELP_LINUX
**Blender viewer for graph**
Usage:	make draw [edgelist] [filename] [dim]

optional arguments: 
	edgelist - string of edges (python-like) 
	filename - string with the name of file as csv 
	dim      - number of dimension for network plot (2 or 3)
	direct   - bool for directed/undirected graph

Note :
- edgelist or filename are mutually exclusive
- network file must be a csv with header names 'source','target',[colors],[x],[y],[z] 
    where colors and x,y,z are optional (default random colors and spring layout)
Example: 
make draw edgelist='[[1,2],[2,3],[3,4]]' dim=3
make draw filename='mynet.csv'
To beginner:
	make test 
endef

export HELP_WIN
export HELP_LINUX

ifeq ($(OS), Windows_NT)
	MKDIR_P = mkdir $(subst /,\,$(OUT)) > nul 2>&1 || (exit 0)
	INSTALL = ./install.ps1
	message = set TAB=	& @echo %HELP_WIN%
else
	MKDIR_P = mkdir -p $(OUT) 
	INSTALL = ./install.sh
	message = echo "$$HELP_LINUX"
endif




install: 	install.sh \
		 	install.ps1
		@$(INSTALL) -y

draw:
	@blender --python blend_net.py -- -e $(edgelist) -f $(filename) -d $(dim) -x $(direct)

test:
	@blender --python blend_net.py -- -e '[[1,2],[2,3],[3,4]]' -d 3 -x 0

star_graph:
	@python -c 'import networkx as nx; import pandas as pd;pd.DataFrame.from_records(data=list(nx.star_graph(n=8).edges)).to_csv("example/star_graph.csv", index=False, header=["Source", "Target"])'
	@blender --python blend_net.py -- -f "example/star_graph.csv" -d 3

help:
	@$(message)
