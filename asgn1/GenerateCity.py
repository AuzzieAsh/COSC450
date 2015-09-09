# File: GenerateCity.py
# Author: Ashley Manson
# Generates a random city layout in Blender

import bpy
import random
import math
import os
import time

DOLOGGING = True # Change if logging should be on or off
TILENUMBER_X = 4 # Number of tiles for x (rows)
TILENUMBER_Y = 3 # Number of tiles for y (cols)
DOCITY = True # Change if the City should be generated
DOGROUND = True # Change if the Ground should be created
DOOCEAN = True # Change if the Ocean should be created
DOBORDER = True # Change if the city border should be created

# Constants for Tiles Array
EMPTY = -1
BUILDING = 0
PARK = 1

# Stores what is in every tile
TILES = [[0 for rows in range(TILENUMBER_X)] for cols in range(TILENUMBER_Y)]

# Green Material
greenMaterial = bpy.data.materials.new("greenMaterial")
greenMaterial.diffuse_color = (0, 1 ,0)
greenMaterial.diffuse_shader = 'LAMBERT'
greenMaterial.diffuse_intensity = 0.1
greenMaterial.emit = 0.5

# Brown Material
brownMaterial = bpy.data.materials.new("brownMaterial")
brownMaterial.diffuse_color = (0.8, 0.2 ,0.1)
brownMaterial.diffuse_shader = 'LAMBERT'
brownMaterial.diffuse_intensity = 0.1
brownMaterial.emit = 0.5

# Dark Gray Material
darkGrayMaterial = bpy.data.materials.new("darkGrayMaterial")
darkGrayMaterial.diffuse_color = (0.1, 0.1, 0.1)
darkGrayMaterial.diffuse_shader = 'LAMBERT'
darkGrayMaterial.diffuse_intensity = 0.1
darkGrayMaterial.emit = 0.5

# Medium Gray Material
medGrayMaterial = bpy.data.materials.new("medGrayMaterial")
medGrayMaterial.diffuse_color = (0.5, 0.5, 0.5)
medGrayMaterial.diffuse_shader = 'LAMBERT'
medGrayMaterial.diffuse_intensity = 0.1
medGrayMaterial.emit = 0.5

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

# Blue Material
blueMaterial = bpy.data.materials.new("blueMaterial")
blueMaterial.diffuse_color = (0, 0.1, 1)
blueMaterial.diffuse_shader = 'LAMBERT'
blueMaterial.diffuse_intensity = 0.1
blueMaterial.emit = 0.5

# Repeated Stuff
def log(to_write):
    if DOLOGGING:
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

def do_this_thing(chance):
    chance_of_thing = random.uniform(0,1)
    if chance_of_thing <= chance:
        return True
    return False

def rand_bool():
    return bool(random.getrandbits(1))

# Blender Repeated Stuff
def select_object(the_object):
    bpy.context.selected_objects.clear()
    bpy.context.selected_objects.append(the_object)
    return

def add_colour(the_colour):
    bpy.ops.object.shade_smooth()
    bpy.context.object.data.materials.append(the_colour)
    return

def resize_object(x, y, z):
    bpy.ops.transform.resize(value = (x, y, z))
    return

def rotate_object(deg, axis):
    if axis == 'x':
        bpy.ops.transform.rotate(value = (math.radians(deg)), axis = (1, 0, 0))
    elif axis == 'y':
        bpy.ops.transform.rotate(value = (math.radians(deg)), axis = (0, 1, 0))
    elif axis == 'z':
        bpy.ops.transform.rotate(value = (math.radians(deg)), axis = (0, 0, 1))
    return

def cube_add(x, y, z):
    cube = bpy.ops.mesh.primitive_cube_add(location = (x, y, z))
    return cube

def cylinder_add(r, d, x, y, z):
    cylinder = bpy.ops.mesh.primitive_cylinder_add(radius = r, depth = d, location = (x, y, z))       
    return cylinder

def sphere_add(x, y, z):
    sphere = bpy.ops.mesh.primitive_uv_sphere_add(location = (x, y, z))
    return sphere

def plane_add(x, y, z):
    plane = bpy.ops.mesh.primitive_plane_add(location = (x, y, z))
    return plane
            
# Fills the Tile array
def fill_tile_array():
    log("fill_tile_array called...")
  
    for row in range(len(TILES)):
        for col in range(len(TILES[0])):

            chance = random.uniform(0, 1)            
            if chance <= 0.9:
                log("[%d,%d] = BUILDING" % (row, col))
                TILES[row][col] = BUILDING
            elif chance <= 1.0:
                log("[%d,%d] = PARK" % (row, col))
                TILES[row][col] = PARK
            else: # Empty
                log("[%d,%d] = EMPTY" % (row, col))
                TILES[row][col] = EMPTY
                
    log("Done.")
    
    return

# Renders what is in the Terrain array
def render_tile_array():
    log("render_tile_array called...")
    
    tile_offset_x = (len(TILES)-1)/2
    tile_offset_y = (len(TILES[0])-1)/2
    
    for row in range (len(TILES)):
        for col in range (len(TILES[0])):
            
            # Calculate x,y offset so tile object appears in the correct place        
            x = (row - tile_offset_x) * 3
            y = (col - tile_offset_y) * 3
            
            if TILES[row][col] == BUILDING:
                create_building(x, y, row, col)
                log("[%d,%d] BUILDING Created" % (row, col))
            elif TILES[row][col] == PARK:
                create_park(x, y, row, col)
                log("[%d,%d] PARK Created" % (row, col))
            else: # Empty
                log("[%d,%d] EMPTY" % (row, col))
                
    log("Done.")
    
    return
    
# Creates a building on an x,y tile
def create_building(x, y, row, col):
    
    do_ground = True

    # How many Building to occupy a single tile
    num_of_buildings = random.randint(1, 4)

    if num_of_buildings == 1:
        base_z = random.uniform(0.5, 0.8)
        
        if do_this_thing(0.9):
            base = cube_add(x, y, base_z)
            select_object(base)
            resize_object(1, 1, base_z)
            
            top_z = random.uniform(base_z+0.1, base_z+0.5)
            top = cube_add(x, y, top_z)
            select_object(top)
            resize_object(0.9, 0.5, top_z)
            
            top_z = random.uniform(base_z+0.1, base_z+0.5)
            top = cube_add(x, y, top_z)
            select_object(top)
            resize_object(0.5, 0.9, top_z)
            
        else:
            base = cylinder_add(1, base_z*2, x, y, base_z)
            
            top_z = random.uniform(base_z+0.1, base_z+0.5)
            top = cylinder_add(0.9, top_z*2, x, y, top_z)

    elif num_of_buildings == 2:
        
        if rand_bool(): # side by side buildings
            
            if rand_bool(): # move along x
                move_x = 0.7
                move_y = 0
                scale_x = 1 - move_x
                scale_y = 1
            else: # move along y
                move_x = 0
                move_y = 0.7
                scale_x = 1
                scale_y = 1 - move_y
            
            # Building 1
            base_z = random.uniform(1,2)
            
            if do_this_thing(0.9):
                base = cube_add(x+move_x, y+move_y, base_z)
                select_object(base)
                resize_object(scale_x, scale_y, base_z)
            else:
                base = cylinder_add(1, base_z*2, x+move_x, y+move_y, base_z)
                select_object(base)
                resize_object(scale_x, scale_y, 1)
            
            ground = plane_add(x+move_x, y+move_y, 0)
            select_object(ground)
            resize_object(scale_x+0.1, scale_y+0.1, 1)
            
            # Building 2
            base_z = random.uniform(1,2)
            
            if do_this_thing(0.9):
                base = cube_add(x-move_x, y-move_y, base_z)
                select_object(base)
                resize_object(scale_x, scale_y, base_z)
            else:
                base = cylinder_add(1, base_z*2, x-move_x, y-move_y, base_z)
                select_object(base)
                resize_object(scale_x, scale_y, 1)
            
            ground = plane_add(x-move_x, y-move_y, 0)
            select_object(ground)
            resize_object(scale_x+0.1, scale_y+0.1, 1)
            
            do_ground = False
            
        else: # do a corner building
            
            if rand_bool(): # move in positive x
                move_x = 0.6
                move_sec_x = move_x + 0.1
                scale_x = 1 - move_x
            else: # move in negative x
                move_x = -0.6
                move_sec_x = move_x - 0.1
                scale_x = 1 + move_x
            
            if rand_bool(): # move in positive y
                move_y = 0.6
                move_sec_y = move_y + 0.1
                scale_y = 1 - move_y
            else: # move in negative y
                move_y = -0.6
                move_sec_y = move_y - 0.1
                scale_y = 1 + move_y
            
            # Building 1, made up of two blocks
            base_z = random.uniform(1,2)
            
            base = cube_add(x+move_x, y, base_z)
            select_object(base)
            resize_object(scale_x, 1, base_z)
            
            base = cube_add(x, y+move_y, base_z)
            select_object(base)
            resize_object(1, scale_y, base_z)
            
            # Building 2, chance of it being created
            if rand_bool(): # create a second building 
                base_z = random.uniform(base_z, base_z+1)
                create_skyscraper(x-move_sec_x, y-move_sec_y, scale_x-0.1, base_z)
            
            else: # create a courtyard thingy
                create_tree(x-(move_sec_x/2), y-(move_sec_y/2), 0.07, 0.2, 0.07*2)

    # Create 3 buildings on a tile
    elif num_of_buildings == 3:
        
        if rand_bool(): # create a long building
            
            moveInX = rand_bool()
            
            if moveInX: # move in x axis
                move_y = 0
                scale_y = 1
                
                if rand_bool(): # positive x
                    move_x = 0.6
                    scale_x = 1 - move_x
                else: # negative x
                    move_x = -0.6
                    scale_x = 1 + move_x

            else: # move in y axis
                move_x = 0
                scale_x = 1
                
                if rand_bool(): # positive y
                    move_y = 0.6
                    scale_y = 1 - move_y
                else: # negative y
                    move_y = -0.6
                    scale_y = 1 + move_y
            
            base_z = random.uniform(1,2)
            base = cube_add(x+move_x, y+move_y, base_z)
            select_object(base)
            resize_object(scale_x, scale_y, base_z)
            
            if moveInX: # move in x
                base_z = random.uniform(base_z, base_z+2)
                base = cube_add(x-move_x, y-move_x, base_z)
                select_object(base)
                resize_object(scale_x, scale_x, base_z)
                
                base_z = random.uniform(base_z, base_z+2)
                base = cube_add(x-move_x, y+move_x, base_z)
                select_object(base)
                resize_object(scale_x, scale_x, base_z)
            
            else: # move in y
                base_z = random.uniform(base_z, base_z+2)
                base = cube_add(x-move_y, y-move_y, base_z)
                select_object(base)
                resize_object(scale_y, scale_y, base_z)
                
                base_z = random.uniform(base_z, base_z+2)
                base = cube_add(x+move_y, y-move_y, base_z)
                select_object(base)
                resize_object(scale_y, scale_y, base_z)
                
        else: # create three skinny buildings
            emptySpot = random.randint(0,3) # [TL=0, TR=1, BL=2, BR=3]
            move_xy = 0.6
            scale_xy = 1 - move_xy
            
            if emptySpot != 0:
                base_z = random.uniform(2,3)
                create_skyscraper(x+move_xy, y-move_xy, scale_xy, base_z)

            if emptySpot != 1:
                base_z = random.uniform(2,3)
                create_skyscraper(x+move_xy, y+move_xy, scale_xy, base_z)

            if emptySpot != 2:
                base_z = random.uniform(2,3)
                create_skyscraper(x-move_xy, y-move_xy, scale_xy, base_z)
                
            if emptySpot != 3:
                base_z = random.uniform(2,3)
                create_skyscraper(x-move_xy, y+move_xy, scale_xy, base_z)
            
    else: # num_of_buildings == 4
        move_xy = 0.6
        scale_xy = 1 - move_xy
    
        base_z = random.uniform(2,3)
        create_skyscraper(x+move_xy, y-move_xy, scale_xy, base_z)

        base_z = random.uniform(2,3)
        create_skyscraper(x+move_xy, y+move_xy, scale_xy, base_z)

        base_z = random.uniform(2,3)
        create_skyscraper(x-move_xy, y-move_xy, scale_xy, base_z)

        base_z = random.uniform(2,3)
        create_skyscraper(x-move_xy, y+move_xy, scale_xy, base_z)
        
    if do_ground:
        create_footpath(x, y)
    
    return

def create_skyscraper(x, y, scale_xy, height):
    
    if do_this_thing(0.9): # create square skyscraper
        base = cube_add(x, y, height)
        select_object(base)
        resize_object(scale_xy, scale_xy, height) 
    else: # create circle skyscraper
        base = cylinder_add(scale_xy, height*2, x, y, height)
        
    return

def create_tree(x, y, radius, height, scale_z):
    tree_trunk = cylinder_add(radius, height*2, x, y, height)
    select_object(tree_trunk)
    add_colour(brownMaterial)
    
    tree_bush = sphere_add(x, y, height*2)
    select_object(tree_bush)
    resize_object(radius*2, radius*2, scale_z)
    add_colour(greenMaterial)
    
    grass = sphere_add(x, y, 0)
    select_object(grass)
    resize_object(0.2, 0.2, 0.01)
    add_colour(greenMaterial)
        
    return

def create_footpath(x, y):
    ground = plane_add(x, y, 0)
    select_object(ground)
    resize_object(1.1, 1.1, 1)
    add_colour(whiteMaterial)
    
    return
def create_park(x, y, row, col):
    
    # Create Park
    park = plane_add(x, y, 0.001)
    select_object(park)
    resize_object(1, 1, 1)
    add_colour(greenMaterial)
    
    # Add Some Trees To The Park
    numTree = random.randint(2, 4)
    for tree in range (numTree):
        randX = random.uniform(-0.5, 0.5)
        randY = random.uniform(-0.5, 0.5)
        treeThickness = random.uniform(0.05, 0.1)
        treeHeight = random.uniform(0.2, 0.4)
        treeTopZ = random.uniform(0.1, 0.3)
        
        create_tree(x+randX, y+randY, treeThickness, treeHeight, treeTopZ)
        
    create_footpath(x, y)
    
    return

def create_road_and_path(x, y, row, col):
    
    path_length_x = 1.2
    move_x_1 = 0
    move_x_2 = 0
    slide_x = 0
    
    path_length_y = 1.2
    move_y_1 = 0
    move_y_2 = 0
    slide_y = 0
    
    # If one of the edge tile
    if row == 0 or row == len(TILES)-1:
        path_length_x = 1
    if row == 0:
        move_x_1 = 0.4
        slide_x = 0.2
    elif row == len(TILES)-1:
        move_x_2 = -0.4
        slide_x = -0.2
        
    if col == 0 or col == len(TILES[0])-1:
        path_length_y = 1
    if col == 0:
        move_y_1 = 0.4
        slide_y = 0.2
    elif col == len(TILES)-1:
        move_y_2 = -0.4
        slide_y = -0.2
    
    # If not an edge tile  
    if row != 0 and col != 0 and row != len(TILES)-1 and col != len(TILES[0])-1:
        if AlleyWay[row][col][0] != AlleyWay[row][col][1]:
            if AlleyWay[row][col][0] == 1:
                path_length_y += 0.1
                move_y_2 += 0.2
                slide_y += 0.1
            elif AlleyWay[row][col][1] == 1:
                path_length_y += 0.1
                move_y_1 -= 0.2
                slide_y -= 0.1
        elif AlleyWay[row][col][0] == 1:
            path_length_y += 0.2
            move_y_1 -= 0.2
            move_y_2 += 0.2
        
        if AlleyWay[row][col][2] != AlleyWay[row][col][3]:
            if AlleyWay[row][col][2] == 1:
                path_length_x += 0.1
                move_x_1 -= 0.2
                slide_x -= 0.1
            elif AlleyWay[row][col][3] == 1:
                path_length_x += 0.1
                move_x_2 += 0.2
                slide_x += 0.1
        elif AlleyWay[row][col][2] == 1:
            path_length_x += 0.2
            move_x_1 -= 0.2
            move_x_2 += 0.2
           
   # Roads/Ground 
    ground = bpy.ops.mesh.primitive_plane_add(location = (x, y, 0))
    select_object(ground)
    bpy.ops.transform.resize(value = (1.5, 1.5, 1))
    add_colour(darkGrayMaterial)
    
    # First Path
    path = bpy.ops.mesh.primitive_plane_add(location = (x+1.1+move_x_2, y+slide_y, 0.01))
    select_object(path)
    bpy.ops.transform.resize(value = (0.1, path_length_y, 1))
    add_colour(whiteMaterial)
    
    # Second Path
    path = bpy.ops.mesh.primitive_plane_add(location = (x-1.1+move_x_1, y+slide_y, 0.01))
    select_object(path)
    bpy.ops.transform.resize(value = (0.1, path_length_y, 1))
    add_colour(whiteMaterial)

    # Third Path
    path = bpy.ops.mesh.primitive_plane_add(location = (x+slide_x, y+1.1+move_y_2, 0.01))
    select_object(path)
    bpy.ops.transform.resize(value = (path_length_x, 0.1, 1))
    add_colour(whiteMaterial)
    
    # Forth Path
    path = bpy.ops.mesh.primitive_plane_add(location = (x+slide_x, y-1.1+move_y_1, 0.01))
    select_object(path)
    bpy.ops.transform.resize(value = (path_length_x, 0.1, 1))
    add_colour(whiteMaterial)
    
    return

# >>> START EXECUTION <<<

# Clear The Screen
bpy.ops.object.select_pattern()
bpy.ops.object.delete()

# Open file for logging
if DOLOGGING:
    SCRIPT_START_TIME = time.time() # Starting time of Script
    LOG_FILE_PATH = bpy.path.abspath("//GenerateCity.log")
    log_file = open(LOG_FILE_PATH, 'w+')

# Start
log("start logging")

# Generate the City
if DOCITY:
    fill_tile_array()
    render_tile_array()

# Add a plane as the ground
if DOGROUND:
    log("Creating the ground...")

    tile_range_x = 1.5*TILENUMBER_Y + 0.5
    tile_range_y = 1.5*TILENUMBER_X + 0.5

    ground = plane_add(0, 0, -0.001)
    select_object(ground)
    resize_object(tile_range_x, tile_range_y, 1)
    add_colour(darkGrayMaterial)

    log("Done.")

# Add a plane as the sea level
if DOOCEAN:
    log("Creating the sea level...")

    tile_range = 3 * max(TILENUMBER_X, TILENUMBER_Y)

    water = plane_add(0, 0, -0.1)
    select_object(water)
    resize_object(tile_range, tile_range, 1)
    add_colour(blueMaterial)

    log("Done.")

# Generate the City Borders
if DOBORDER:
    log("Create City Border...")
    x = ((len(TILES)-1)/2) * 3 + 2
    y = ((len(TILES[0])-1)/2) * 3 + 2
    len_x = (TILENUMBER_X*3) + 1
    len_y = (TILENUMBER_Y*3) + 1
            
    cylinder = cylinder_add(1, len_x, x, 0, -0.1)
    select_object(cylinder)
    resize_object(0.1, 1, 1)
    rotate_object(90, 'x')
    rotate_object(90, 'y')

    cylinder = cylinder_add(1, len_y, 0, y, -0.1)
    select_object(cylinder)
    resize_object(0.1, 1, 1)
    rotate_object(90, 'y')

    sphere = sphere_add(x, y, -0.1)
    select_object(sphere)
    resize_object(1, 1, 0.1)
    
    sphere = sphere_add(-x, y, -0.1)
    select_object(sphere)
    resize_object(1, 1, 0.1)

    sphere = sphere_add(x, -y, -0.1)
    select_object(sphere)
    resize_object(1, 1, 0.1)
    
    log("Done")
log("Tiles Rows: %d" %len(TILES))
log("Tiles Cols: %d" %len(TILES[0]))

# End
log("end logging")
if DOLOGGING:
    log_file.close()
