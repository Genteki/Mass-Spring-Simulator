if __name__ == '__main__':
    from ursina import *

    app = Ursina()

    verts = ((0,0,0), (1,0,0), (.5, 1, 0), (-.5,1,0))
    tris = (0,1,2,3,2,1,0)#(1, 2, 0, 2, 3, 0)
    uvs = None #((1.0, 0.0), (0.0, 1.0), (0.0, 0.0), (1.0, 1.0))
    norms = ((0,0,1),) * len(verts)
    colors = (color.red, color.blue, color.lime, color.black)


    e = Entity(model=Mesh(vertices=verts, triangles=tris, uvs=uvs, normals=norms, colors=colors, mode='ngon'), scale=2)
    # line mesh test
    verts = (Vec3(0,0,0), Vec3(0,1,0), Vec3(1,1,0), Vec3(2,2,0), Vec3(0,3,0), Vec3(-2,3,0))
    #tris = ((0,1), (3,4,5))

    #lines = Entity(model=Mesh(vertices=verts, triangles=tris, mode='line', thickness=4), color=color.cyan, z=-1)
    #points = Entity(model=Mesh(vertices=verts, mode='point', thickness=.05), color=color.red, z=-1.01)
    plane = Entity(model="plane", scale=(20,1,20),y=-0,texture="white_cube", texture_scale=(20,20))


    EditorCamera()
    app.run()
