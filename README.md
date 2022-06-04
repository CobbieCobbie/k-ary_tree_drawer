# _k_-ary Tree Drawer

This repository contains a small, compact drawing algorithm for [_k_-ary trees](https://handwiki.org/wiki/K-ary_tree), implemented in Python3.
The root will be drawn at first, afterwards, the drawing algorithm proceeds to draw all the children up to a specific level, placed on grid points. 
This visualization has the property to keep the edge lengths uniform, creating a straight-line drawing of uniform length straight-lines apart a rounding error.

## Prequisites

python3 preinstalled with packages _networkx_ and _matplotlib_

> pip install -r requirements.txt 

## How to run

Exemplary execution of a tertiary tree of height 4

> python ./k-ary_tree_drawer.py -k 3 -he 4 -c -i

Without arguments, the code defaults to setting k=2, h=3

## Examples

![6-ary tree of height 3](https://github.com/CobbieCobbie/k-ary_tree_drawer/blob/main/graphics/Implementation_6ary_height_3.png?raw=true "6-ary tree of height 3")  
6-ary tree of height 3

![30-ary tree of height 3](https://github.com/CobbieCobbie/k-ary_tree_drawer/blob/main/graphics/Implementation_30ary_height_3.png?raw=true "30-ary tree of height 3")  
30-ary tree of height 3
