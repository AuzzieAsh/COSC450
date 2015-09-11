# File: GenerateCity.py
# Author: Ashley Manson
# Generates a random city layout in Blender

import bpy
import random
import math
import os
import time

DOLOGGING = True # Change if logging should be on or off
TILENUMBER_X = 5 # Number of tiles for x (rows) 
TILENUMBER_Y = 5 # Number of tiles for y (cols)
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
CAR_COLOURS = []

# Green Material
greenMaterial = bpy.data.materials.new("greenMaterial")
greenMaterial.diffuse_color = (0, 1, 0)
greenMaterial.diffuse_shader = 'LAMBERT'
greenMaterial.diffuse_intensity = 0.1
greenMaterial.emit = 0.5

# Brown Material
brownMaterial = bpy.data.materials.new("brownMaterial")
brownMaterial.diffuse_color = (0.8, 0.2, 0.1)
brownMaterial.diffuse_shader = 'LAMBERT'
brownMaterial.diffuse_intensity = 0.1
brownMaterial.emit = 0.5

# Sand Material
sandMaterial = bpy.data.materials.new("sandMaterial")
sandMaterial.diffuse_color = (0.9, 0.8, 0.3)
sandMaterial.diffuse_shader = 'LAMBERT'
sandMaterial.diffuse_intensity = 0.1
sandMaterial.emit = 0.5

# Rock Material
rockMaterial = bpy.data.materials.new("rockMaterial")
rockMaterial.diffuse_color = (0.4, 0.2, 0.1)
rockMaterial.diffuse_shader = 'LAMBERT'
rockMaterial.diffuse_intensity = 0.1
rockMaterial.emit = 0.5

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

# Yellow Material
yellowMaterial = bpy.data.materials.new("yellowMaterial")
yellowMaterial.diffuse_color = (1, 1, 0.1)
yellowMaterial.diffuse_shader = 'LAMBERT'
yellowMaterial.diffuse_intensity = 0.1
yellowMaterial.emit = 0.5

CAR_COLOURS.append(redMaterial)
CAR_COLOURS.append(blueMaterial)
CAR_COLOURS.append(greenMaterial)
CAR_COLOURS.append(brownMaterial)
CAR_COLOURS.append(yellowMaterial)

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

def cone_add(x, y, z):
    cone = bpy.ops.mesh.primitive_cone_add(location = (x, y, z))
    return cone
            
# Fills the Tile array
def fill_tile_array():
    log("fill_tile_array called...")
  
    for row in range(len(TILES)):
        for col in range(len(TILES[0])):
          
            if do_this_thing(0.9):
                log("[%d,%d] = BUILDING" % (row, col))
                TILES[row][col] = BUILDING
            else:
                log("[%d,%d] = PARK" % (row, col))
                TILES[row][col] = PARK
                    
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
                generate_cars_line(1.3, -0.3, random.randint(0, 7), x-0.2, y, 'x')
                generate_cars_line(-1.3, 0.3, random.randint(0, 7), x+0.2, y, 'x') 
            else: # move along y
                move_x = 0
                move_y = 0.7
                scale_x = 1
                scale_y = 1 - move_y
                generate_cars_line(1.3, -0.3, random.randint(0, 7), x, y+0.2, 'y')
                generate_cars_line(-1.3, 0.3, random.randint(0, 7), x, y-0.2, 'y') 
            
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
    
    create_cars(x, y, row, col)
    
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

def create_cars(x, y, row, col):
    if row == 0:
        generate_cars_line(1.3, -0.3, random.randint(0, 7), x-1.7, y, 'x')
    if col == 0:
        generate_cars_line(-1.3, 0.3, random.randint(0, 7), x, y-1.7, 'y')
    if row == len(TILES)-1:
        generate_cars_line(-1.3, 0.3, random.randint(0, 7), x+1.7, y, 'x')
    if col == len(TILES[0])-1:
        generate_cars_line(1.3, -0.3, random.randint(0, 7), x, y+1.7, 'y')
    
    generate_cars_line(-1.3, 0.3, random.randint(0, 7), x-1.3, y, 'x')
    generate_cars_line(1.3, -0.3, random.randint(0, 7), x, y-1.3, 'y')
    generate_cars_line(1.3, -0.3, random.randint(0, 7), x+1.3, y, 'x')
    generate_cars_line(-1.3, 0.3, random.randint(0, 7), x, y+1.3, 'y')
    
    return

def generate_cars_line(start, interval, num_of_cars, x, y, axis):
    log("Generating %d cars at [%d,%d]" % (num_of_cars, x, y))
    
    if axis == 'x':
        for i in range(num_of_cars):
            start += interval
            
            cube = cube_add(x, y+start, 0.03)
            select_object(cube)
            resize_object(0.05, 0.1, 0.03)
            add_colour(CAR_COLOURS[random.randint(0, len(CAR_COLOURS)-1)])
            
            cube = cube_add(x, y+start, 0.075)
            select_object(cube)
            resize_object(0.05, 0.05, 0.015)
            add_colour(whiteMaterial)
            
            cylinder = cylinder_add(0.02, 0.11, x, y+0.05+start, 0.02)
            select_object(cylinder)
            rotate_object(90, 'y')
            add_colour(darkGrayMaterial)
            
            cylinder = cylinder_add(0.02, 0.11, x, y-0.05+start, 0.02)
            select_object(cylinder)
            rotate_object(90, 'y')
            add_colour(darkGrayMaterial)
    
    else: # axis == 'y'
        for i in range(num_of_cars):
            start += interval
            
            cube = cube_add(x+start, y, 0.03)
            select_object(cube)
            resize_object(0.1, 0.05, 0.03)
            add_colour(CAR_COLOURS[random.randint(0, len(CAR_COLOURS)-1)])
            
            cube = cube_add(x+start, y, 0.075)
            select_object(cube)
            resize_object(0.05, 0.05, 0.015)
            add_colour(whiteMaterial)
            
            cylinder = cylinder_add(0.02, 0.11, x+0.05+start, y, 0.02)
            select_object(cylinder)
            rotate_object(90, 'x')
            add_colour(darkGrayMaterial)
            
            cylinder = cylinder_add(0.02, 0.11, x-0.05+start, y, 0.02)
            select_object(cylinder)
            rotate_object(90, 'x')
            add_colour(darkGrayMaterial)
    
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
    create_cars(x, y, row, col)
    
    return

def create_city_border():
    log("create_city_border called...")
    
    x = ((len(TILES)-1)/2) * 3 + 2
    y = ((len(TILES[0])-1)/2) * 3 + 2
    len_x = (TILENUMBER_X*3) + 1
    len_y = (TILENUMBER_Y*3) + 1
        
    log("Creating the beach front...")
    # Create the Beach Front    
    cylinder = cylinder_add(1, len_x, x, 0, -0.1)
    select_object(cylinder)
    resize_object(0.1, 1, 1)
    rotate_object(90, 'x')
    rotate_object(90, 'y')
    add_colour(sandMaterial)

    cylinder = cylinder_add(1, len_y, 0, y, -0.1)
    select_object(cylinder)
    resize_object(0.1, 1, 1)
    rotate_object(90, 'y')
    add_colour(sandMaterial)

    sphere = sphere_add(x, y, -0.1)
    select_object(sphere)
    resize_object(1, 1, 0.1)
    add_colour(sandMaterial)
    
    sphere = sphere_add(-x, y, -0.1)
    select_object(sphere)
    resize_object(1, 1, 0.1)
    add_colour(sandMaterial)

    sphere = sphere_add(x, -y, -0.1)
    select_object(sphere)
    resize_object(1, 1, 0.1)
    add_colour(sandMaterial)
     
    sphere = sphere_add(-x-1, y+0.5, -0.1)
    select_object(sphere)
    resize_object(2, 2, 0.1)
    add_colour(sandMaterial)
    
    sphere = sphere_add(x+0.5, -y-1, -0.1)
    select_object(sphere)
    resize_object(2, 2, 0.1)
    add_colour(sandMaterial)
    
    log("Beach random variation")
    lower_case_x = min(3, len(TILES)-1)
    beach_extra_x = random.randint(lower_case_x, len(TILES)-1)
    for extra_x in range (beach_extra_x):
        sphere = sphere_add(random.uniform(1, len_x-1)-x, y, -0.11)
        select_object(sphere)
        resize_object(random.uniform(2, 3), random.uniform(2, 3), 0.1)
        add_colour(sandMaterial)
        
    lower_case_y = min(3, len(TILES[0])-1)
    beach_extra_y = random.randint(lower_case_y, len(TILES[0])-1)
    for extra_y in range (beach_extra_y):
        sphere = sphere_add(x, random.uniform(1, len_y-1)-y, -0.11)
        select_object(sphere)
        resize_object(random.uniform(2, 3), random.uniform(2, 3), 0.1)
        add_colour(sandMaterial)
    
    log("Creating the mountain outskirts...")
    # Create the Mountain Outskirts
    cylinder = cylinder_add(1, len_x+1.8, -x-1, -1, 0)
    select_object(cylinder)
    rotate_object(90, 'x')
    resize_object(1, 1, 0.1)
    add_colour(rockMaterial)
    
    cylinder = cylinder_add(1, len_y+1.8, -1, -y-1, 0)
    select_object(cylinder)
    rotate_object(90, 'y')
    resize_object(1, 1, 0.1)
    add_colour(rockMaterial)
    
    cone = cone_add(-x-3, y, 0.5)
    select_object(cone)
    resize_object(3, 1.5, 0.5)
    add_colour(rockMaterial)

    cone = cone_add(x, -y-3, 0.5)
    select_object(cone)
    resize_object(1.5, 3, 0.5)
    add_colour(rockMaterial)
    
    cone = cone_add(-x-5, -y-5, 3)
    select_object(cone)
    resize_object(5, 5, 3)
    add_colour(rockMaterial)
    
    log("Mountain random variation in X")
    mountain_x_len = ((len(TILES)-1)*3)+3
    for mountain_x in range (mountain_x_len):
        rand_height = random.uniform(1, 3)
        rand_width = random.uniform(5, 6)
        cone = cone_add(-x+mountain_x, -y-rand_width, rand_height)
        select_object(cone)
        resize_object(rand_width, rand_width, rand_height)
        add_colour(rockMaterial)
        
        numTree = random.randint(1, 3)
        for tree in range (numTree):
            randX = random.uniform(-1, 1)
            randY = random.uniform(-0.6, -0.2)
            treeThickness = random.uniform(0.05, 0.1)
            treeHeight = random.uniform(0.2, 0.4)
            treeTopZ = random.uniform(0.1, 0.3)
        
            create_tree(-x+mountain_x+randX, -y+randY, treeThickness, treeHeight, treeTopZ)
            
    
    log("Mountain random variation in Y")
    mountain_y_len = ((len(TILES[0])-1)*3)+3
    for mountain_y in range (mountain_y_len):
        rand_height = random.uniform(1, 3)
        rand_width = random.uniform(5, 6)
        cone = cone_add(-x-rand_width, -y+mountain_y, rand_height)
        select_object(cone)
        resize_object(rand_width, rand_width, rand_height)
        add_colour(rockMaterial)
        
        numTree = random.randint(1, 3)
        for tree in range (numTree):
            randX = random.uniform(-0.6, -0.2)
            randY = random.uniform(-1, 1)
            treeThickness = random.uniform(0.05, 0.1)
            treeHeight = random.uniform(0.2, 0.4)
            treeTopZ = random.uniform(0.1, 0.3)
        
            create_tree(-x+randX, -y+mountain_y+randY, treeThickness, treeHeight, treeTopZ)
        
    return

# >>> START EXECUTION <<<

# Clear The Screen
bpy.ops.object.select_pattern()
bpy.ops.object.delete()

# Open file for logging
if DOLOGGING:
    SCRIPT_START_TIME = time.time() # Starting time of Script
    log_file_path = bpy.path.abspath("//GenerateCity.log")
    log_file = open(log_file_path, 'w+')

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

# Add a plane as the sea level
if DOOCEAN:
    log("Creating the sea level...")

    tile_range = 5 * max(TILENUMBER_X, TILENUMBER_Y)

    water = plane_add(0, 0, -0.05)
    select_object(water)
    resize_object(tile_range, tile_range, 1)
    add_colour(blueMaterial)

# Generate the City Borders
if DOBORDER:
    create_city_border()

log("Tiles Rows: %d" %len(TILES))
log("Tiles Cols: %d" %len(TILES[0]))

# End
log("end logging")
if DOLOGGING:
    log_file.close()
