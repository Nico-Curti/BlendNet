| **Authors**  | **Project** |
|:------------:|:-----------:|
|   N. Curti   |   BlendNet  |

<a href="https://github.com/physycom">
<div class="image">
<img src="https://cdn.rawgit.com/physycom/templates/697b327d/logo_unibo.png" width="90" height="90">
</div>
</a>

# Blender Network viewer

<a href="https://github.com/Nico-Curti/blend_net/blob/master/example/star_graph.png">
<div class="image">
<img src="https://github.com/Nico-Curti/blend_net/blob/master/example/star_graph.png" width="960" height="540">
</div>
</a>

One of the biggest problem during graph visualization is to obtain good results in 3D environment. [Blender](https://www.blender.org/) software allow to create very beautifull 3D objects and it is very easy to use throw the python support.

**BlendNet** project include a simple python interface to Blender environment to draw network in 2D and 3D as required in the input file.

## Installation

The scripts [install.sh](https://github.com/Nico-Curti/blend_net/blob/master/install.sh) and [install.ps1](https://github.com/Nico-Curti/blend_net/blob/master/install.ps1) cover a full installation example of Blender and project dependencies for Unix and Windows users, respectivelly.

## How to use

The [Makefile](https://github.com/Nico-Curti/blend_net/blob/master/Makefile) cover a list of examples and command lines instructions about different inputs available. Just type `make help` to see the full list of available rules:

```bash
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
```

A list of examples could be found in [example](https://github.com/Nico-Curti/blend_net/tree/master/example) directory.

## Contributions

Any contribution is more than welcome. Just fill an issue or a pull request and I will check ASAP!

## Authors

* **Nico Curti** [git](https://github.com/Nico-Curti), [unibo](https://www.unibo.it/sitoweb/nico.curti2)

## License

This project is released under GPL license. [![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://github.com/Nico-Curti/blend_net/blob/master/LICENSE)
