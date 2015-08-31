# Add some hills
def hills():
    for i in range (-4, 5):
        hill_side = bpy.ops.mesh.primitive_plane_add(location = (i*3, -(5*3)+0.8, -0.7))
        bpy.context.selected_objects.clear()
        bpy.context.selected_objects.append(hill_side)
        bpy.ops.transform.resize(value = (1.5, 1, 1))
        bpy.ops.transform.rotate(value = (math.radians(45)), axis =(1, 0, 0))
        
        hill_side = bpy.ops.mesh.primitive_plane_add(location = (i*3, (5*3)-0.8, -0.7))
        bpy.context.selected_objects.clear()
        bpy.context.selected_objects.append(hill_side)
        bpy.ops.transform.resize(value = (1.5, 1, 1))
        bpy.ops.transform.rotate(value = (math.radians(-45)), axis =(1, 0, 0))
        
        hill_side = bpy.ops.mesh.primitive_plane_add(location = ((5*3)-0.8, i*3, -0.7))
        bpy.context.selected_objects.clear()
        bpy.context.selected_objects.append(hill_side)
        bpy.ops.transform.resize(value = (1, 1.5, 1))
        bpy.ops.transform.rotate(value = (math.radians(45)), axis =(0, 1, 0))
        
        hill_side = bpy.ops.mesh.primitive_plane_add(location = (-(5*3)+0.8, i*3, -0.7))
        bpy.context.selected_objects.clear()
        bpy.context.selected_objects.append(hill_side)
        bpy.ops.transform.resize(value = (1, 1.5, 1))
        bpy.ops.transform.rotate(value = (math.radians(-45)), axis =(0, 1, 0))
    return

#cone = bpy.ops.mesh.primitive_cone_add(location = ((5*3)-1.47, (5*3)-1.47, -0.7))
#bpy.context.selected_objects.clear()
#bpy.context.selected_objects.append(cone)
#bpy.ops.transform.resize(value = (1.3, 1.3, 0.7))
#bpy.ops.transform.rotate(value = (math.radians(-45)), axis =(1, 0, 0))


# Add some buildings
def buildings_or_fields():
    for i in range(-4, 5):
        for j in range(-4, 5):
            chance = random.uniform(0, 1)
            if chance <= 0.9:
                base_n = random.randint(2, 4)
                base = bpy.ops.mesh.primitive_cube_add(location = (i*3, j*3, base_n))
                bpy.context.selected_objects.clear()
                bpy.context.selected_objects.append(base)
                bpy.ops.transform.resize(value=(1, 1, base_n))
                top_n = random.randint(base_n+1, base_n*2)
                top = bpy.ops.mesh.primitive_cube_add(location = (i*3, j*3, top_n))
                bpy.context.selected_objects.clear()
                bpy.context.selected_objects.append(top)
                bpy.ops.transform.resize(value=(0.8, 0.8, top_n))
            else:
                field = bpy.ops.mesh.primitive_plane_add(location = (i*3, j*3, 0.01))
                bpy.context.selected_objects.clear()
                bpy.context.selected_objects.append(field)
                bpy.ops.transform.resize(value = (1, 1, 1))
                bpy.ops.object.shade_smooth()
                bpy.context.object.data.materials.append(fieldMaterial)
                
            road = bpy.ops.mesh.primitive_plane_add(location = (i*3, j*3, 0))
            bpy.context.selected_objects.clear()
            bpy.context.selected_objects.append(road)
            bpy.ops.transform.resize(value = (1.5, 1.5, 1))
            bpy.ops.object.shade_smooth()
            bpy.context.object.data.materials.append(roadMaterial)
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

# http://wiki.blender.org/index.php/Dev:2.5/Py/Scripts/Cookbook/Code_snippets/Meshes
def run(origin):
    (x,y,z) = (0.707107, 0.258819, 0.965926)
    x = x + 0.7
    tz = -0.7
    verts1 = ((x,x,tz), (x,-x,tz), (-x,-x,tz), (-x,x,tz), (0,0,0.7))
    faces1 = ((1,0,4), (4,2,1), (4,3,2), (4,0,3), (0,1,2,3))
    ob1 = createMesh('Solid', origin, verts1, [], faces1)
    #verts2 = ((x,x,0), (y,-z,0), (-z,y,0))
    #“edges2 = ((1,0), (1,2), (2,0))
    #ob2 = createMesh('Edgy', origin, verts2, edges2, [])
    
    # Move second object out of the way
    ob1.select = False
    #ob2.select = True
    #bpy.ops.transform.translate(value=(0,2,0))
    return

x = (5 * 3) - 1.5
y = (5 * 3) - 1.5
z = -0.7
#run((x, y, z))
x = -(4 * 3) - 1.5
y = -(4 * 3) - 1.5
z = -0.7
#run((x, y, z))
x = -(4 * 3) - 1.5
y = (5 * 3) - 1.5
z = -0.7
#run((x, y, z))
x = (5 * 3) - 1.5
y = -(4 * 3) - 1.5
z = -0.7
#run((x, y, z))


# Random
#base_n = random.randint(2, 4)
#base = bpy.ops.mesh.primitive_cube_add(location = (24*3, 24*3, base_n))
#bpy.context.selected_objects.clear()
#bpy.context.selected_objects.append(base)
#bpy.ops.transform.resize(value=(1, 1, base_n))
#top_n = random.randint(base_n+1, base_n*2)
#top = bpy.ops.mesh.primitive_cube_add(location = (24*3, 24*3, top_n))
#bpy.context.selected_objects.clear()
#bpy.context.selected_objects.append(top)
#bpy.ops.transform.resize(value=(0.8, 0.8, top_n))


def render_terrain():
    log("Create Terrain...\n")
    
    verts = []
    faces = []
    edges = []
    
    for row in range (0, TILENUMBER-1):
        for col in range (0, TILENUMBER-1):
            
            tileOffset = (TILENUMBER-1)/2
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
