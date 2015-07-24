# File: Generate-City-Script.py
# Author: Ashley Manson
# Generates a random city layout in Blender

import bpy
import random
import math
import os
import time

# Change Based on Where to store GenerateCity.log
#LOG_FILE_PATH = '/Users/localash/Desktop/COSC450/COSC450-Assignment1'
LOG_FILE_PATH = 'E:/Users/Ashley/Desktop/COSC450/COSC450-Assignment1'

def log(to_write):
    log_file.write(to_write)
    return

# Create/Open file for writing
log_file = open(LOG_FILE_PATH + '/GenerateCity.log', 'w+')
log(":: start\n\n")

# Starting time of Script
SCRIPT_START_TIME = time.time()

# Clear The Screen
bpy.ops.object.select_pattern()
bpy.ops.object.delete()

# Number of tiles for x and y
TILENUMBER = 50 #Should be an EVEN number

# Constants for Terrain
EMPTY = -1
RIVER = 0
BUILDING = 1
PARK = 2

# Stores what is in every tile
Terrain = [[0 for x in range(TILENUMBER-1)] for x in range(TILENUMBER-1)]

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

# Water Material
waterMaterial = bpy.data.materials.new("waterMaterial")
waterMaterial.diffuse_color = (0, 0.1, 1)
waterMaterial.diffuse_shader = 'LAMBERT'
waterMaterial.diffuse_intensity = 0.1
waterMaterial.emit = 0.5

# Fills the Terrain array
def generate_terrain():
    for row in range (0, TILENUMBER-1):
        for col in range (0, TILENUMBER-1):
            chance = random.uniform(0, 1)
            if chance <= 0.2:
                log(" Terrain[%d][%d] = RIVER\n" % (row, col))
                Terrain[row][col] = RIVER
            elif chance <= 0.8:
                log(" Terrain[%d][%d] = BUILDING\n" % (row, col))
                Terrain[row][col] = BUILDING
            elif chance <= 1.0:
                log(" Terrain[%d][%d] = PARK\n" % (row, col))
                Terrain[row][col] = PARK
            else: #Empty
                log(" Terrain[%d][%d] = EMPTY\n" % (row, col))
                Terrain[row][col] = EMPTY
    return

# Add a plane as the sea level
def add_water_plane(tileScale):
    tileRange = tileScale * TILENUMBER
    
    water = bpy.ops.mesh.primitive_plane_add(location = (0, 0, -0.8))
    
    bpy.context.selected_objects.clear()
    bpy.context.selected_objects.append(water)
    
    bpy.ops.transform.resize(value=(tileRange, tileRange, 1))
    
    bpy.ops.object.shade_smooth()
    bpy.context.object.data.materials.append(waterMaterial)
    
    return

# Renders what is in the Terrain array
def render_terrain():
    for row in range (0, TILENUMBER-1):
        for col in range (0, TILENUMBER-1):
            
            tileOffset = (TILENUMBER-2)/2
            x = (row - tileOffset) * 3
            y = (col - tileOffset) * 3
            
            if Terrain[row][col] == RIVER:
                log(" Tile [%d,%d] = RIVER Created\n" % (row, col))
                create_river(x, y)
            elif Terrain[row][col] == BUILDING:
                log(" Tile [%d,%d] = BUILDING Created\n" % (row, col))
                create_building(x, y)
                create_road(x, y)
            elif Terrain[row][col] == PARK:
                log(" Tile [%d,%d] = PARK Created\n" % (row, col))
                create_park(x, y)
                create_road(x, y)
            else:
                create_empty()
                
    return

# Creates a river on an x,y tile
def create_river(x, y):
    hill_side = bpy.ops.mesh.primitive_plane_add(location = (x, y+0.8, -0.7))
    bpy.context.selected_objects.clear()
    bpy.context.selected_objects.append(hill_side)
    bpy.ops.transform.resize(value = (1.5, 1, 1))
    bpy.ops.transform.rotate(value = (math.radians(45)), axis =(1, 0, 0))
    
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
    
    top_z = random.randint(base_z+1, base_z*2)
    top = bpy.ops.mesh.primitive_cube_add(location = (x, y, top_z))
    
    bpy.context.selected_objects.clear()
    bpy.context.selected_objects.append(top)
    
    bpy.ops.transform.resize(value=(0.8, 0.8, top_z))
    
    return

# Creates a road at an x,y tile
def create_road(x, y):
    road = bpy.ops.mesh.primitive_plane_add(location = (x, y, 0))
    
    bpy.context.selected_objects.clear()
    bpy.context.selected_objects.append(road)
    
    bpy.ops.transform.resize(value = (1.5, 1.5, 1))
    
    bpy.ops.object.shade_smooth()
    bpy.context.object.data.materials.append(roadMaterial)
    
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

log("Filling Terrain array...\n")
generate_terrain()
log("Done.\n")

log("Create from Terrain array...\n")
render_terrain()
log("Done.\n")

log("Create Water Plane...\n")
add_water_plane(1.5)
log("Done.\n")

# End Script Time
SCRIPT_END_TIME = time.time()
total = SCRIPT_END_TIME - SCRIPT_START_TIME
days = total // 86400
hours = total // 3600 % 24
minutes = total // 60 % 60
seconds = total % 60

log("Total Time (H:M:S): %.0f:%.0f:%.1f\n" % (hours, minutes, seconds))

log("\n:: end\n")
log_file.close()
