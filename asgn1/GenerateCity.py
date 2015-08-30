# File: Generate-City-Script.py
# Author: Ashley Manson
# Generates a random city layout in Blender

import bpy
import random
import math
import os
import time

# Change if to logging should be on or off
DO_LOGGING = True

# Number of tiles for x and y
TILENUMBER = 4 #Should be an EVEN number

# Constants for Terrain
EMPTY = -1
RIVER = 0
BUILDING = 1
PARK = 2

# Stores what is in every tile
Tiles = [[0 for x in range(TILENUMBER-1)] for y in range(TILENUMBER-1)]

# Open file for logging
if DO_LOGGING:
    LOG_FILE_PATH = bpy.path.abspath("//GenerateCity.log")
    log_file = open(LOG_FILE_PATH, 'w+')

def log(to_write):
    if DO_LOGGING:
        log_file.write(to_write)
        log_file.flush()
    return

# Clear The Screen
bpy.ops.object.select_pattern()
bpy.ops.object.delete()

log("start logging\n\n")

# Starting time of Script
SCRIPT_START_TIME = time.time()

# Park Material
parkMaterial = bpy.data.materials.new("parkMaterial")
parkMaterial.diffuse_color = (0, 1 ,0)
parkMaterial.diffuse_shader = 'LAMBERT'
parkMaterial.diffuse_intensity = 0.1
parkMaterial.emit = 0.5

# Road Material
roadMaterial = bpy.data.materials.new("roadMaterial")
roadMaterial.diffuse_color = (0.1, 0.1, 0.1)
roadMaterial.diffuse_shader = 'LAMBERT'
roadMaterial.diffuse_intensity = 0.1
roadMaterial.emit = 0.5

# White Material
whiteMaterial = bpy.data.materials.new("whiteMaterial")
whiteMaterial.diffuse_color = (0.9, 0.9, 0.9)
whiteMaterial.diffuse_shader = 'LAMBERT'
whiteMaterial.diffuse_intensity = 0.1
whiteMaterial.emit = 0.5

# Red Material
redMaterial = bpy.data.materials.new("whiteMaterial")
redMaterial.diffuse_color = (1, 0.1, 0)
redMaterial.diffuse_shader = 'LAMBERT'
redMaterial.diffuse_intensity = 0.1
redMaterial.emit = 0.9

# Water Material
waterMaterial = bpy.data.materials.new("waterMaterial")
waterMaterial.diffuse_color = (0, 0.1, 1)
waterMaterial.diffuse_shader = 'LAMBERT'
waterMaterial.diffuse_intensity = 0.1
waterMaterial.emit = 0.5

# Fills the Terrain array
def fill_tile_array():
    log("Filling Tiles array...\n")
    
    for row in range (0, TILENUMBER-1):
        for col in range (0, TILENUMBER-1):
            chance = random.uniform(0, 1)
            if chance <= 1.0:
                log(" Tiles[%d][%d] = BUILDING\n" % (row, col))
                Tiles[row][col] = BUILDING
            elif chance <= 0.0:
                log(" Tiles[%d][%d] = RIVER\n" % (row, col))
                Tiles[row][col] = RIVER
            elif chance <= 0.0:
                log(" Tiles[%d][%d] = PARK\n" % (row, col))
                Tiles[row][col] = PARK
            else: #Empty
                log(" Tiles[%d][%d] = EMPTY\n" % (row, col))
                Tiles[row][col] = EMPTY
    log("Done.\n")
    return

# Renders what is in the Terrain array
def render_tile_array():
    log("Create from Tiles array...\n")
    
    for row in range (0, TILENUMBER-1):
        for col in range (0, TILENUMBER-1):
            
            tileOffset = (TILENUMBER-2)/2
            x = (row - tileOffset) * 3
            y = (col - tileOffset) * 3
            
            if Tiles[row][col] == RIVER:
                log(" Tile [%d,%d] RIVER Created\n" % (row, col))
                create_river(x, y, row, col)
            elif Tiles[row][col] == BUILDING:
                log(" Tile [%d,%d] BUILDING Created\n" % (row, col))
                create_building(x, y)
                create_road(x, y)
            elif Tiles[row][col] == PARK:
                log(" Tile [%d,%d] PARK Created\n" % (row, col))
                create_park(x, y)
                create_road(x, y)
            else:
                create_empty()
                
    log("Done.\n")            
    return

def render_terrain():
    log("Create Terrain...\n")
    
    verts = []
    faces = []
    edges = []
    
    for row in range (0, TILENUMBER-1):
        for col in range (0, TILENUMBER-1):
            
            tileOffset = (TILENUMBER-2)/2
            x = (row - tileOffset) * 3
            y = (col - tileOffset) * 3
            
            height = random.randint(0, 5)
            verts.append((x, y, height))
            verts.append((x+1, y, height))
            verts.append((x+1, y+1, height))
            verts.append((x, y+1, height))
            #faces.append((row, col, row+1, col+1))
            new_row = row*(TILENUMBER-1)+col
            new_col = row*(TILENUMBER-1)+col
            edges.append((new_row, new_row+1))
            edges.append((new_row+1, new_col+1))
            edges.append((new_col+1, new_col))
            edges.append((new_col, new_row))
    
    plane = createMesh('Terrain', (0, 0, 0), verts, edges, faces)
    
    log("Done.\n")            
    return


# http://wiki.blender.org/index.php/Dev:2.5/Py/Scripts/Cookbook/Code_snippets/Meshes
def createMesh(name, origin, verts, edges, faces):
    # Create mesh and object
    me = bpy.data.meshes.new(name+'Mesh')
    ob = bpy.data.objects.new(name, me)
    ob.location = origin
    ob.show_name = False
    # Link object to scene
    bpy.context.scene.objects.link(ob)
    
    # Create mesh from given verts, edges, faces. Either edges or
    # faces should be [], or you ask for problems
    me.from_pydata(verts, edges, faces)
    
    # Update mesh with new data
    me.update(calc_edges=True)
    return ob

## http://wiki.blender.org/index.php/Dev:2.5/Py/Scripts/Cookbook/Code_snippets/Meshes
#def run(origin):
#    (x,y,z) = (0.707107, 0.258819, 0.965926)
#    x = x + 0.7
#    tz = -0.7
#    verts1 = ((x,x,tz), (x,-x,tz), (-x,-x,tz), (-x,x,tz), (0,0,0.7))
#    faces1 = ((1,0,4), (4,2,1), (4,3,2), (4,0,3), (0,1,2,3))
#    ob1 = createMesh('Solid', origin, verts1, [], faces1)
#    #verts2 = ((x,x,0), (y,-z,0), (-z,y,0))
#    #“edges2 = ((1,0), (1,2), (2,0))
#    #ob2 = createMesh('Edgy', origin, verts2, edges2, [])
#    
#    # Move second object out of the way
#    ob1.select = False
#    #ob2.select = True
#    #bpy.ops.transform.translate(value=(0,2,0))
#    return

# Add a plane as the sea level
def add_water_plane(tileScale):
    log("Create Water Plane...\n")
    
    tileRange = tileScale * TILENUMBER
    
    water = bpy.ops.mesh.primitive_plane_add(location = (0, 0, -0.8))
    
    bpy.context.selected_objects.clear()
    bpy.context.selected_objects.append(water)
    
    bpy.ops.transform.resize(value=(tileRange, tileRange, 1))
    
    bpy.ops.object.shade_smooth()
    bpy.context.object.data.materials.append(waterMaterial)
    
    log("Done.\n")
    return

# Creates a river on an x,y tile
def create_river(x, y, row, col):
#    if (col + 1) >= TILENUMBER-1:
#        col = col-1
#    elif (col - 1) < 0:
#        col = col + 1
        
    if col + 1 < TILENUMBER-1:
        if Tiles[row][col+1] != RIVER:
            hill_side = bpy.ops.mesh.primitive_plane_add(location = (x, y+0.8, -0.7))
            bpy.context.selected_objects.clear()
            bpy.context.selected_objects.append(hill_side)
            bpy.ops.transform.resize(value = (1.5, 1, 1))
            bpy.ops.transform.rotate(value = (math.radians(45)), axis =(1, 0, 0))
    else:
        hill_side = bpy.ops.mesh.primitive_plane_add(location = (x, y+0.8, -0.7))
        bpy.context.selected_objects.clear()
        bpy.context.selected_objects.append(hill_side)
        bpy.ops.transform.resize(value = (1.5, 1, 1))
        bpy.ops.transform.rotate(value = (math.radians(45)), axis =(1, 0, 0))
    
    if col - 1 >= 0 and Tiles[row][col-1] != RIVER:
        hill_side = bpy.ops.mesh.primitive_plane_add(location = (x, y-0.8, -0.7))
        bpy.context.selected_objects.clear()
        bpy.context.selected_objects.append(hill_side)
        bpy.ops.transform.resize(value = (1.5, 1, 1))
        bpy.ops.transform.rotate(value = (math.radians(-45)), axis =(1, 0, 0))
    
    hill_side = bpy.ops.mesh.primitive_plane_add(location = (x-0.8, y, -0.7))
    bpy.context.selected_objects.clear()
    bpy.context.selected_objects.append(hill_side)
    bpy.ops.transform.resize(value = (1, 1.5, 1))
    bpy.ops.transform.rotate(value = (math.radians(45)), axis =(0, 1, 0))
    
    hill_side = bpy.ops.mesh.primitive_plane_add(location = (x+0.8, y, -0.7))
    bpy.context.selected_objects.clear()
    bpy.context.selected_objects.append(hill_side)
    bpy.ops.transform.resize(value = (1, 1.5, 1))
    bpy.ops.transform.rotate(value = (math.radians(-45)), axis =(0, 1, 0))
    
    return

# Creates a building on an x,y tile
def create_building(x, y):
    base_z = random.randint(2, 4)
    base = bpy.ops.mesh.primitive_cube_add(location = (x, y, base_z))
    
    bpy.context.selected_objects.clear()
    bpy.context.selected_objects.append(base)
    
    bpy.ops.transform.resize(value=(1, 1, base_z))
    
    bpy.ops.object.shade_smooth()
    bpy.context.object.data.materials.append(redMaterial)
    
    top_z = random.randint(base_z+1, base_z*2)
    top = bpy.ops.mesh.primitive_cube_add(location = (x, y, top_z))
    
    bpy.context.selected_objects.clear()
    bpy.context.selected_objects.append(top)
    
    bpy.ops.transform.resize(value=(0.8, 0.8, top_z))
    
    bpy.ops.object.shade_smooth()
    bpy.context.object.data.materials.append(redMaterial)
    
    return

# Creates a road at an x,y tile
def create_road(x, y):
    path_length = 1.1
    ground = bpy.ops.mesh.primitive_plane_add(location = (x, y, 0))
    
    bpy.context.selected_objects.clear()
    bpy.context.selected_objects.append(ground)
    
    bpy.ops.transform.resize(value = (1.5, 1.5, 1))
    
    bpy.ops.object.shade_smooth()
    bpy.context.object.data.materials.append(roadMaterial)
    
    path = bpy.ops.mesh.primitive_plane_add(location = (x+1.1, y, 0.01))

    bpy.context.selected_objects.clear()
    bpy.context.selected_objects.append(path)
    
    bpy.ops.transform.resize(value = (0.1, path_length, 1))
    
    bpy.ops.object.shade_smooth()
    bpy.context.object.data.materials.append(whiteMaterial)
    
    path = bpy.ops.mesh.primitive_plane_add(location = (x-1.1, y, 0.01))

    bpy.context.selected_objects.clear()
    bpy.context.selected_objects.append(path)
    
    bpy.ops.transform.resize(value = (0.1, path_length, 1))
    
    bpy.ops.object.shade_smooth()
    bpy.context.object.data.materials.append(whiteMaterial)

    path = bpy.ops.mesh.primitive_plane_add(location = (x, y+1.1, 0.01))

    bpy.context.selected_objects.clear()
    bpy.context.selected_objects.append(path)
    
    bpy.ops.transform.resize(value = (path_length, 0.1, 1))
    
    bpy.ops.object.shade_smooth()
    bpy.context.object.data.materials.append(whiteMaterial)
    
    path = bpy.ops.mesh.primitive_plane_add(location = (x, y-1.1, 0.01))

    bpy.context.selected_objects.clear()
    bpy.context.selected_objects.append(path)
    
    bpy.ops.transform.resize(value = (path_length, 0.1, 1))
    
    bpy.ops.object.shade_smooth()
    bpy.context.object.data.materials.append(whiteMaterial)
    return
    
# Creates a park on an x,y tile
def create_park(x, y):
    park = bpy.ops.mesh.primitive_plane_add(location = (x, y, 0.01))
    
    bpy.context.selected_objects.clear()
    bpy.context.selected_objects.append(park)
    
    bpy.ops.transform.resize(value = (1, 1, 1))
    
    bpy.ops.object.shade_smooth()
    bpy.context.object.data.materials.append(parkMaterial)
    
    return

# Empty Tile
def create_empty():
    print("Empty Tile")
    return

fill_tile_array()
render_tile_array()
add_water_plane(1.5)
#render_terrain()

# End Script Time
SCRIPT_END_TIME = time.time()
total = SCRIPT_END_TIME - SCRIPT_START_TIME
days = total // 86400
hours = total // 3600 % 24
minutes = total // 60 % 60
seconds = total % 60

log("Total Time (H:M:S): %.0f:%.0f:%.1f\n" % (hours, minutes, seconds))

log("\nend logging\n")

if DO_LOGGING:
    log_file.close()
