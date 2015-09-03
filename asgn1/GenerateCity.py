# File: GenerateCity.py
# Author: Ashley Manson
# Generates a random city layout in Blender

import bpy
import random
import math
import os
import time

DO_LOGGING = True # Change if logging should be on or off
TILENUMBER = 10 # Number of tiles for x (rows) and y (cols)
SCRIPT_START_TIME = time.time() # Starting time of Script

# Constants for Terrain
EMPTY = -1
BUILDING = 0
PARK = 1
RIVER = 2

# Stores what is in every tile
TILES = [[0 for rows in range(TILENUMBER)] for cols in range(TILENUMBER)]
#[top, bot, left, right]
AlleyWay = [[0 for rows in range(TILENUMBER)] for cols in range(TILENUMBER)]

# Open file for logging
if DO_LOGGING:
    LOG_FILE_PATH = bpy.path.abspath("//GenerateCity.log")
    log_file = open(LOG_FILE_PATH, 'w+')

def log(to_write):
    if DO_LOGGING:
        total_time = time.time() - SCRIPT_START_TIME
        days = total_time // 86400
        hours = total_time // 3600 % 24
        minutes = total_time // 60 % 60
        seconds = total_time % 60
        log_file.write("[%.0f:%.0f:%.1f] " % (hours, minutes, seconds))
        log_file.write(to_write)
        log_file.write("\n")
        log_file.flush()
    return

# Clear The Screen
bpy.ops.object.select_pattern()
bpy.ops.object.delete()

log("start logging")

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
    log("fill_tile_array called...")
  
    for row in range(len(TILES)):
        for col in range(len(TILES[0])):
            
            chance = random.uniform(0, 1)
            
            if chance <= 1.0:
                log("[%d,%d] = BUILDING" % (row, col))
                TILES[row][col] = BUILDING
                alley_chance = []
                for i in range(4):
                    chance = random.uniform(0, 1)
                    if (chance <= 0.5):
                        alley_chance.append(1)
                    else:
                        alley_chance.append(0)
                        
                AlleyWay[row][col] = alley_chance
            elif chance <= 0.0:
                log("[%d,%d] = PARK" % (row, col))
                TILES[row][col] = PARK
            elif chance <= 0.0:
                log("[%d,%d] = RIVER" % (row, col))
                TILES[row][col] = RIVER
            else: #Empty
                log("[%d,%d] = EMPTY" % (row, col))
                TILES[row][col] = EMPTY
                
    log("Done.")
    
    return

# Renders what is in the Terrain array
def render_tile_array():
    log("render_tile_array called...")
    
    for row in range (len(TILES)):
        for col in range (len(TILES[0])):
            
            tileOffset = (TILENUMBER-1)/2
            x = (row - tileOffset) * 3
            y = (col - tileOffset) * 3
            
            if TILES[row][col] == BUILDING:
                create_building(x, y, row, col)
                log("[%d,%d] BUILDING Created" % (row, col))
            elif TILES[row][col] == PARK:
                create_park(x, y)
                log("[%d,%d] PARK Created" % (row, col))
            elif TILES[row][col] == RIVER:      
                create_river(x, y, row, col)
                log("[%d,%d] RIVER Created" % (row, col))
            else: #Empty
                create_empty()
                log("[%d,%d] EMPTY Created" % (row, col))
                
    log("Done.")
    
    return

# Add a plane as the sea level
def add_water_plane(tileScale):
    log("add_water_plane called...")
    
    tileRange = tileScale * TILENUMBER
    
    water = bpy.ops.mesh.primitive_plane_add(location = (0, 0, -0.8))
    
    bpy.context.selected_objects.clear()
    bpy.context.selected_objects.append(water)
    
    bpy.ops.transform.resize(value=(tileRange, tileRange, 1))
    
    bpy.ops.object.shade_smooth()
    bpy.context.object.data.materials.append(waterMaterial)
    
    log("Done.")
    return

# Creates a river on an x,y tile
def create_river(x, y, row, col):
#    if (col + 1) >= TILENUMBER-1:
#        col = col-1
#    elif (col - 1) < 0:
#        col = col + 1
        
    if col + 1 < TILENUMBER-1:
        if TILES[row][col+1] != RIVER:
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
def create_building(x, y, row, col):
    
    scale_b_x = 1
    scale_t_x = 0.8
    move_x = 0
    
    scale_b_y = 1
    scale_t_y = 0.8
    move_y = 0
    
    if row == 0 or row == len(TILES)-1:
        scale_b_x = 0.8
        scale_t_x = 0.6
        
    if row == 0:
        move_x = 0.2
    elif row == len(TILES)-1:
        move_x = -0.2
        
    if col == 0 or col == len(TILES)-1:
        scale_b_y = 0.8
        scale_t_y = 0.6
        
    if col == 0:
        move_y = 0.2
    elif col == len(TILES)-1:
        move_y = -0.2
        
    if row != 0 and col != 0 and row != len(TILES)-1 and col != len(TILES)-1:
        if AlleyWay[row][col][0] != AlleyWay[row][col][1]:
            if AlleyWay[row][col][0] == 1:
                move_y = 0.1
                scale_b_y += 0.1
                scale_t_y += 0.1
            elif AlleyWay[row][col][1] == 1:
                move_y = -0.1
                scale_b_y += 0.1
                scale_t_y += 0.1
        elif AlleyWay[row][col][0] == 1:
            scale_b_y += 0.2
            scale_t_y += 0.2
        
        if AlleyWay[row][col][2] != AlleyWay[row][col][3]:
            if AlleyWay[row][col][2] == 1:
                move_x = -0.1
                scale_b_x += 0.1
                scale_t_x += 0.1
            elif AlleyWay[row][col][3] == 1:
                move_x = 0.1
                scale_b_x += 0.1
                scale_t_x += 0.1
        elif AlleyWay[row][col][2] == 1:
            scale_b_x += 0.2
            scale_t_x += 0.2
            
    # Create Building
    base_z = random.randint(2, 4)
    base = bpy.ops.mesh.primitive_cube_add(location = (x+move_x, y+move_y, base_z))
    
    bpy.context.selected_objects.clear()
    bpy.context.selected_objects.append(base)
    
    bpy.ops.transform.resize(value=(scale_b_x, scale_b_y, base_z))
    
    bpy.ops.object.shade_smooth()
    bpy.context.object.data.materials.append(redMaterial)
    
    top_z = random.randint(base_z+1, base_z*2)
    top = bpy.ops.mesh.primitive_cube_add(location = (x+move_x, y+move_y, top_z))
    
    bpy.context.selected_objects.clear()
    bpy.context.selected_objects.append(top)
    
    bpy.ops.transform.resize(value=(scale_t_x, scale_t_y, top_z))
    
    bpy.ops.object.shade_smooth()
    bpy.context.object.data.materials.append(redMaterial)
    
    # Create surrounding path and road
    path_length_x = 1.2
    move_x_1 = 0
    move_x_2 = 0
    slide_x = 0
    
    path_length_y = 1.2
    move_y_1 = 0
    move_y_2 = 0
    slide_y = 0
    
    if row == 0 or row == len(TILES)-1:
        path_length_x = 1
    if row == 0:
        move_x_1 = 0.4
        slide_x = 0.2
    elif row == len(TILES)-1:
        move_x_2 = -0.4
        slide_x = -0.2
        
    if col == 0 or col == len(TILES)-1:
        path_length_y = 1
    if col == 0:
        move_y_1 = 0.4
        slide_y = 0.2
    elif col == len(TILES)-1:
        move_y_2 = -0.4
        slide_y = -0.2
        
    if row != 0 and col != 0 and row != len(TILES)-1 and col != len(TILES)-1:
        if AlleyWay[row][col][0] != AlleyWay[row][col][1]:
            if AlleyWay[row][col][0] == 1:
                path_length_y += 0.1
                #move_y_1 += 0.1
                move_y_2 += 0.2
                slide_y += 0.1
            elif AlleyWay[row][col][1] == 1:
                path_length_y += 0.1
                move_y_1 -= 0.2
                #move_y_2 -= 0.1
                slide_y -= 0.1
        elif AlleyWay[row][col][0] == 1:
            path_length_y += 0.2
            move_y_1 -= 0.2
            move_y_2 += 0.2
        
        if AlleyWay[row][col][2] != AlleyWay[row][col][3]:
            if AlleyWay[row][col][2] == 1:
                path_length_x += 0.1
                move_x_1 -= 0.2
                #move_x_2 -= 0.1
                slide_x -= 0.1
            elif AlleyWay[row][col][3] == 1:
                path_length_x += 0.1
                #move_x_1 += 0.1
                move_x_2 += 0.2
                slide_x += 0.1
        elif AlleyWay[row][col][2] == 1:
            path_length_x += 0.2
            move_x_1 -= 0.2
            move_x_2 += 0.2
            
    ground = bpy.ops.mesh.primitive_plane_add(location = (x, y, 0))
    
    bpy.context.selected_objects.clear()
    bpy.context.selected_objects.append(ground)
    
    bpy.ops.transform.resize(value = (1.5, 1.5, 1))
    
    bpy.ops.object.shade_smooth()
    bpy.context.object.data.materials.append(roadMaterial)
    
    path = bpy.ops.mesh.primitive_plane_add(location = (x+1.1+move_x_2, y+slide_y, 0.01))

    bpy.context.selected_objects.clear()
    bpy.context.selected_objects.append(path)
    
    bpy.ops.transform.resize(value = (0.1, path_length_y, 1))
    
    bpy.ops.object.shade_smooth()
    bpy.context.object.data.materials.append(whiteMaterial)
    
    path = bpy.ops.mesh.primitive_plane_add(location = (x-1.1+move_x_1, y+slide_y, 0.01))

    bpy.context.selected_objects.clear()
    bpy.context.selected_objects.append(path)
    
    bpy.ops.transform.resize(value = (0.1, path_length_y, 1))
    
    bpy.ops.object.shade_smooth()
    bpy.context.object.data.materials.append(whiteMaterial)

    path = bpy.ops.mesh.primitive_plane_add(location = (x+slide_x, y+1.1+move_y_2, 0.01))

    bpy.context.selected_objects.clear()
    bpy.context.selected_objects.append(path)
    
    bpy.ops.transform.resize(value = (path_length_x, 0.1, 1))
    
    bpy.ops.object.shade_smooth()
    bpy.context.object.data.materials.append(whiteMaterial)
    
    path = bpy.ops.mesh.primitive_plane_add(location = (x+slide_x, y-1.1+move_y_1, 0.01))

    bpy.context.selected_objects.clear()
    bpy.context.selected_objects.append(path)
    
    bpy.ops.transform.resize(value = (path_length_x, 0.1, 1))
    
    bpy.ops.object.shade_smooth()
    bpy.context.object.data.materials.append(whiteMaterial)
    
    return

# Creates a road at an x,y tile
def create_road(x, y):

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
add_water_plane(2)

bpy.context.selected_objects.clear()

log("Tiles Rows: %d" %len(TILES))
log("Tiles Cols: %d" %len(TILES[0]))

log("end logging")

if DO_LOGGING:
    log_file.close()
