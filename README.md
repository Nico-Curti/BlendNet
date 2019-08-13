| **Authors**                                     | **Project** | **Build Status**              |
|:-----------------------------------------------:|:-----------:|:-----------------------------:|
|   [**N. Curti**](https://github.com/Nico-Curti) | **BlendNet**| **Linux/OSX** : [![travis](https://travis-ci.com/Nico-Curti/BlendNet.svg?branch=master)](https://travis-ci.com/Nico-Curti/BlendNet) <br/> **Windows** : [![Windows](https://ci.appveyor.com/api/projects/status/1unn2dg52kui34la?svg=true)](https://ci.appveyor.com/project/Nico-Curti/blendnet) |

[![GitHub pull-requests](https://img.shields.io/github/issues-pr/Nico-Curti/BlendNet.svg?style=plastic)](https://github.com/Nico-Curti/BlendNet/pulls)
[![GitHub issues](https://img.shields.io/github/issues/Nico-Curti/BlendNet.svg?style=plastic)](https://github.com/Nico-Curti/BlendNet/issues)

[![GitHub stars](https://img.shields.io/github/stars/Nico-Curti/BlendNet.svg?label=Stars&style=social)](https://github.com/Nico-Curti/BlendNet/stargazers)
[![GitHub watchers](https://img.shields.io/github/watchers/Nico-Curti/BlendNet.svg?label=Watch&style=social)](https://github.com/Nico-Curti/BlendNet/watchers)

<a href="https://github.com/physycom">
<div class="image">
<img src="https://cdn.rawgit.com/physycom/templates/697b327d/logo_unibo.png" width="90" height="90">
</div>
</a>

# BlendNet
### (Blender Network viewer)

<a href="https://github.com/Nico-Curti/BlendNet/blob/master/example/star_graph.png">
<div class="image">
<img src="https://github.com/Nico-Curti/BlendNet/blob/master/example/star_graph.png" width="960" height="540">
</div>
</a>

One of the biggest problem during graph visualization is to obtain good results in 3D environment. [Blender](https://www.blender.org/) software allows to create very beautiful 3D objects and it is very easy to use by Python API.

**BlendNet** project include a simple single-file python interface to draw network in 2D and 3D using Blender support.

1. [Why BlendNet?](#why)
2. [Prerequisites](#prerequisites)
3. [Installation](#installation)
4. [Authors](#authors)
5. [License](#license)
6. [Contribution](#contribution)
7. [Acknowledgments](#acknowledgments)
8. [Citation](#citation)

## Why BlendNet?

Graph visualization is still an open problem in many applications.
Commonly the problem is related to large graph visualization in which problems arise from the rendering of a large number of nodes and a greater number of links between them.
An other open problem concern the multi-dimensional visualization of the graphs.
Despite the most common graph tools compute the node coordinates in a any space dimensions (and clearly the maximum number of possible dimension for a visualization is still three) the real visualization is often allowed only a 2D space.
The counterpart of these problems concern the pretty visualization of the graphs that it is often ignored in many tools but it can be guarantee a good result, the so called wow-effect, in a presentation.

BlendNet is a custom tool written in Python with the help of Blender API.
Blender is now a standard in the 3D rendering and it is commonly used in a wide range of graphical applications, starting from the simpler 3D dynamics to the video-games applications.
Blender is certainly more than a simple graphical viewer but the easy Python interface and the wide on-line documentation and blogs make it a useful tool for graphical representation of 3D structures.

## Prerequisites

**BlendNet** package uses Blender to render the network structure so install it before use it.
A full list of Blender instruction can be found [here](https://www.blender.org/download/).

Then you have to update the list of packages of the Python version inside Blender.
So go to the `path_to_blender/version/python/bin` directory and download `pip` as package manager and use it to install `networkx` `pandas` `matplotlib` `numpy` or use the [requirements.txt]() file inside the project as `pip install -r path_to_BlendNet/requirements.txt`.

## Installation

The scripts [install.sh](https://github.com/Nico-Curti/BlendNet/blob/master/install.sh) and [install.ps1](https://github.com/Nico-Curti/BlendNet/blob/master/install.ps1) cover a full installation example of Blender and project dependencies for Unix and Windows users, respectively. To use it please download also the submodules of the project. The full list of dependencies will be installed as no-root users so any trouble about user-privileges is ignored.

The [Makefile](https://github.com/Nico-Curti/BlendNet/blob/master/Makefile) cover a list of examples and command lines instructions about different inputs available. Just type `make help` to see the full list of available rules:

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


## Authors

* **Nico Curti** [git](https://github.com/Nico-Curti), [unibo](https://www.unibo.it/sitoweb/nico.curti2)

See also the list of [contributors](https://github.com/Nico-Curti/walkers/contributors) who participated in this project.


## License

The `BlendNet` package is licensed under the GPL License. [![License](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://github.com/Nico-Curti/BlendNet/blob/master/LICENSE.md)

## Contribution

Any contribution is more than welcome :heart:. Just fill an issue or a pull request and I will check ASAP!

## Acknowledgments

Thanks goes to all contributors of this project:

| [<img src="https://avatars0.githubusercontent.com/u/9303827?s=400&v=4" width="100px;"/><br /><sub><b>Alessandro Fabbri</b></sub>](https://github.com/allefabbri) | [<img src="https://avatars2.githubusercontent.com/u/721187?s=400&v=4" width="100px;"/><br /><sub><b>Stefano Sinigardi</b></sub>](https://github.com/cenit)
|:---:|:---:|

and to Raffaele Pepe who help me with Blender instructions.

### Citation

If you have found `BlendNet` helpful in your research, please consider citing the

```tex
@misc{BlendNet,
  author = {Nico Curti},
  title = {{B}lend{N}et},
  year = {2019},
  publisher = {GitHub},
  howpublished = {\url{https://github.com/Nico-Curti/BlendNet}},
}
```

