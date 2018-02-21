edgelist = ""
edgefile = ""
nodelist = ""
nodefile = ""
dim = 3
direct = 0
node_size = 3
edge_thickness = 0.25

define HELP_WIN
**Blender viewer for graph** & @echo.\
Usage:   make draw [edgelist] [edgefile] [nodelist] [nodefile] [dim] [direct] [node_size] [edge_thickness] & @echo.\
& @echo.\
optional arguments: & @echo.\
.    edgelist       - string of edges (python-like) & @echo.\
.    edgefile       - string with the name of file as csv & @echo.\
.    nodelist       - string of nodes (python-like) & @echo.\
.    nodefile       - string with the name of file as csv & @echo.\
.    dim            - number of dimension for network plot (2 or 3) & @echo.\
.    direct         - bool for directed/undirected graph & @echo.\
.    node_size      - float for node size & @echo.\
.    edge_thickness - float for edges size & @echo.\
& @echo.\
Note : & @echo.\
- edgelist or edgefile are mutually exclusive as nodelist and nodefile & @echo.\
- edges file must be a csv with header names 'source','target' & @echo.\
- nodes file must be a csv with header names 'node',[colors],[x],[y],[z] & @echo.\
.    where node, colors and x,y,z are optional (default random colors and spring layout) & @echo.\
Example: & @echo.\
make draw edgelist='[[0,1],[1,2],[2,3]]' dim=3 & @echo.\
make draw edgefile='mynet.csv' & @echo.\
To beginner: & @echo.\
.    make test 
endef
define HELP_LINUX
**Blender viewer for graph**
Usage:  make draw [edgelist] [edgefile] [nodelist] [nodefile] [dim] [direct] [node_size] [edge_thickness]

optional arguments: 
	edgelist       - string of edges (python-like)
	edgefile       - string with the name of file as csv
	nodelist       - string of nodes (python-like)
	nodefile       - string with the name of file as csv
	dim            - number of dimension for network plot (2 or 3)
	direct         - bool for directed/undirected graph
	node_size      - float for node size
	edge_thickness - float for edges size

Note :
- edgelist or edgefile are mutually exclusive as nodelist and nodefile
- edges file must be a csv with header names 'source','target'
- nodes file must be a csv with header names 'node',[colors],[x],[y],[z] 
	where node, colors and x,y,z are optional (default random colors and spring layout)
Example: 
make draw edgefile='[[0,1],[1,2],[2,3]]' dim=3
make draw filename='mynet.csv'
To beginner:
	make test 
endef

export HELP_WIN
export HELP_LINUX

ifeq ($(OS), Windows_NT)
	MKDIR_P = mkdir $(subst /,\,$(OUT)) > nul 2>&1 || (exit 0)
	INSTALL = ./install.ps1
	message = set TAB=  & @echo %HELP_WIN%
else
	MKDIR_P = mkdir -p $(OUT) 
	INSTALL = ./install.sh
	message = echo "$$HELP_LINUX"
endif




install:    install.sh \
			install.ps1
		@$(INSTALL) -y

draw:
	@blender --python blend_net.py -- -e $(edgelist) -E $(edgefile) -n $(nodelist) -N $(nodefile) -d $(dim) -x $(direct) -s $(node_size) -l $(edge_thickness) 

test:
	@blender --python blend_net.py -- -e '[[0,1],[1,2],[2,3]]' -d 3 -x 0

star_graph:
	@python -c 'import networkx as nx; import pandas as pd; pd.DataFrame.from_records(data=list(nx.star_graph(n=8).edges)).to_csv("example/star_graph.csv", index=False, header=["Source", "Target"])'
	@blender --python blend_net.py -- -E "example/star_graph.csv" -d 3

cycle_graph:
	@python -c 'import networkx as nx; import pandas as pd; pd.DataFrame.from_records(data=list(nx.cycle_graph(n=300).edges)).to_csv("example/cycle_graph.csv", index=False, header=["Source", "Target"])'
	@blender --python blend_net.py -- -E "example/cycle_graph.csv" -d 3 -s .5 -l .1

complete_graph:
	@python -c 'import networkx as nx; import pandas as pd; pd.DataFrame.from_records(data=list(nx.complete_graph(n=10).edges)).to_csv("example/complete_graph.csv", index=False, header=["Source", "Target"])'
	@blender --python blend_net.py -- -E "example/complete_graph.csv" -d 3 -s 2.5 -l .1

test_node:
	@python -c 'import networkx as nx; import pandas as pd; edges = pd.read_csv("example/star_graph.csv"); G = nx.Graph(); edges.columns = [str(c).upper() for c in edges.columns]; edges = edges[["SOURCE", "TARGET"]].values; G.add_edges_from(edges); colors = ["blue" if G.degree[n] <= 1 else "red" for n in G.nodes]; names = [x for x in [chr(i) for i in range(ord("A"),ord("J"))]]; nodes = pd.DataFrame(data = [list(G.nodes), colors, names], index = ["node", "colors", "names"]).T; nodes.to_csv("example/star_graph_node.csv", sep=",", index=False)'
	@blender --python blend_net.py -- -E "example/star_graph.csv" -d 3 -N "example/star_graph_node.csv"

help:
	@$(message)
