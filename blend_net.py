# -*- coding: utf-8 -*-
"""
Created on Thu Feb  1 15:31:12 2018

@author: nico
"""

import networkx as nx # graph and layout
import pandas as pd # edges dataframe 
import sys # exit
import os # exists file
import argparse # parse command line
import ast # convert string to list
import random # nrg
# blender python
import bpy 
from math import acos#, degrees, pi
from mathutils import Vector

# Colors to turn into materials
colors = {"purple": (178, 132, 234), "gray": (11, 11, 11),
          "green": (114, 195, 0), "red": (255, 0, 75),
          "blue": (0, 131, 255), "clear": (0, 131, 255),
          "yellow": (255, 187, 0), "light_gray": (118, 118, 118)}

# Normalize to [0,1] and make blender materials
for key, value in colors.items():
    value = [x / 255.0 for x in value]
    bpy.data.materials.new(name=key)
    bpy.data.materials[key].diffuse_color = value
    bpy.data.materials[key].specular_intensity = 0.5

    # Don't specify more parameters if these colors
    if key == "gray" or key == "light_gray":
        continue

    # Transparency parameters
    bpy.data.materials[key].use_transparency = True
    bpy.data.materials[key].transparency_method = "RAYTRACE"
    bpy.data.materials[key].alpha = 0.1 if key == "clear" else 0.95
    bpy.data.materials[key].raytrace_transparency.fresnel = 0.1
    bpy.data.materials[key].raytrace_transparency.ior = 1.15

def blend_net(graph, position, node_size=3, edge_thickness=0.25):
    # Add some mesh primitives
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.mesh.primitive_uv_sphere_add()
    sphere = bpy.context.object
    bpy.ops.mesh.primitive_cylinder_add()
    cylinder = bpy.context.object
    cylinder.active_material = bpy.data.materials["light_gray"]
    
    # Keep references to all nodes and edges
    shapes = []
    # Keep separate references to shapes to be smoothed
    shapes_to_smooth = []
    
    # Draw nodes
    nx.set_node_attributes(G, [], "color")
    for node in graph.nodes():
        # Coloring rule for nodes. Edit this to suit your needs!
        col = random.choice(list(colors.keys()))
        
        # Copy mesh primitive and edit to make node
        # (You can change the shape of drawn nodes here)
        node_sphere = sphere.copy()
        node_sphere.data = sphere.data.copy()
        node_sphere.location = position[node]
        node_sphere.dimensions = [node_size] * 3
        node_sphere.active_material = bpy.data.materials[col]
        bpy.context.scene.objects.link(node_sphere)
        shapes.append(node_sphere)
        shapes_to_smooth.append(node_sphere)
        
    # Draw edges
    for source, target in graph.edges():
        # Get source and target locations by drilling down into data structure
        source_loc = position[source]#network["nodes"][edge["source"]]["location"]
        target_loc = position[target]#network["nodes"][edge["target"]]["location"]

        diff = [c2 - c1 for c2, c1 in zip(source_loc, target_loc)]
        cent = [(c2 + c1) / 2 for c2, c1 in zip(source_loc, target_loc)]
        mag = sum([(c2 - c1) ** 2 for c1, c2 in zip(source_loc, target_loc)]) ** 0.5
        
        # Euler rotation calculation
        v_axis = Vector(diff).normalized()
        v_obj = Vector((0, 0, 1))
        v_rot = v_obj.cross(v_axis)
        angle = acos(v_obj.dot(v_axis))

        # Copy mesh primitive to create edge
        edge_cylinder = cylinder.copy()
        edge_cylinder.data = cylinder.data.copy()
        edge_cylinder.dimensions = [edge_thickness] * 2 + [mag - node_size]
        edge_cylinder.location = cent
        edge_cylinder.rotation_mode = "AXIS_ANGLE"
        edge_cylinder.rotation_axis_angle = [angle] + list(v_rot)
        bpy.context.scene.objects.link(edge_cylinder)
        shapes.append(edge_cylinder)
        shapes_to_smooth.append(edge_cylinder)
        
    # Remove primitive meshes
    bpy.ops.object.select_all(action='DESELECT')
    sphere.select = True
    cylinder.select = True
    
    # If the starting cube is there, remove it
    if "Cube" in bpy.data.objects.keys():
        bpy.data.objects.get("Cube").select = True
    bpy.ops.object.delete()

    # Smooth specified shapes
    for shape in shapes_to_smooth:
        shape.select = True
    bpy.context.scene.objects.active = shapes_to_smooth[0]
    bpy.ops.object.shade_smooth()

    # Join shapes
    for shape in shapes:
        shape.select = True
    bpy.context.scene.objects.active = shapes[0]
    bpy.ops.object.join()

    # Center object origin to geometry
    bpy.ops.object.origin_set(type="ORIGIN_GEOMETRY", center="MEDIAN")

    # Refresh scene
    bpy.context.scene.update()

if __name__ == "__main__":
    argv = sys.argv
    argv = argv[argv.index("--") + 1:]  # get all args after "--"
    
    description = "BlenderNet"
    parser = argparse.ArgumentParser(description = description)
    parser.add_argument("-f", required=False, dest="filename", action="store", help="filename as json or networkx-json", default="")
    parser.add_argument("-e", required=False, dest="edges", action="store", help="string with edges", default="")
    
    if len(sys.argv) <= 1:
        parser.print_help()
        sys.exit(1)
    else:
        args = parser.parse_args(argv)
    
    filename = args.filename
    edges = args.edges
    G = nx.Graph()
    
    if filename != "" and os.path.exists(filename):
      	edges = pd.read_csv(filename, sep=",", header=None)
       	G.add_edges_from(edges.values)
            
    elif edges == "" and filename == "":
        parser.print_help()
        sys.exit(1)
    else:    
	    G.add_edges_from(ast.literal_eval(edges))

    position = nx.spring_layout(G, dim=3, scale=10)
    
    blend_net(G, position)
