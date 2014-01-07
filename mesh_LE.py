import bpy, bmesh

bl_info = {
    "name": "len edge",
    "author": "SolPie",
    "version": (1, 0),
    "blender": (2, 69, 0),
    "location": "View3D > Specials > LE",
    "description": "move edge to the right position",
    "warning": "",
    "category": "Mesh"}

def vertex_active(me):
    bm = bmesh.from_edit_mesh(me)

    for elem in reversed(bm.select_history):
        if isinstance(elem, bmesh.types.BMVert):
            return elem
    else:
        return None

def edge_active(me):
    bm = bmesh.from_edit_mesh(me)

    for elem in reversed(bm.select_history):
        if isinstance(elem, bmesh.types.BMEdge):
            return elem
    else:
        return None

def edge_active_verts(me):
    bm = bmesh.from_edit_mesh(me)
    for elem in reversed(bm.select_history):
        if isinstance(elem, bmesh.types.BMEdge):
            return (elem.calc_length(),elem.verts[0].co,elem.verts[1].co)
    else:
        return None
    pass

def calc_length(axis):
    ob = bpy.context.active_object
    ob.update_from_editmode()
    verts_sel = [v for v in ob.data.vertices if v.select]
    xyz = axis
    x1 = None
    cursor = bpy.context.scene.cursor_location[xyz]
    length = None
    length_max = 0.0
    for v in verts_sel:
        x2 = v.co[xyz]
        length = abs(x2 - cursor)
        if length > length_max:
            length_max = length
    return length_max

def vert_match(v,verts,verts_match):
    if (v.co.x == verts[0].x 
        and v.co.y ==verts[0].y
        and v.co.z ==verts[0].z)\
        or (v.co.x == verts[1].x 
        and v.co.y ==verts[1].y
        and v.co.z ==verts[1].z):
        if not verts_match[0]:
            verts_match[0] = v
        else:
            verts_match[1] = v
            pass
        return True 
    return False

def edge_match(e,verts):
    check_count = 0
    for idx in e.vertices:
        #v = 
        print(idx)
        #if vert_match(v,verts):
         #   check_count +=1
        pass
    if check_count==2:
        return True
    return False

def calc_scale_point(axis,verts_of_edge,v):
    dis1 = abs((verts_of_edge[0].co - v.co)[axis])
    dis2 = abs((verts_of_edge[1].co - v.co)[axis])
    print('==dis==',dis1,dis2)
    if dis1>dis2:
        return verts_of_edge[0]
    else:
        return verts_of_edge[1]

def len_edge_in_edge_mode(target_length, on_axis):
    on_axis = int(on_axis)

    a = [False, False, False]
    a[on_axis] = True
    axis = a

    ob = bpy.context.active_object
    cur_length,v1,v2 = edge_active_verts(ob.data)
    print(cur_length,v1, v2)
    s = target_length / cur_length
    size = (s, s, s)
    print('size',size)

    bpy.ops.view3d.cursor3d()
    verts_active = [None,None]

    ob.update_from_editmode()
    #edge_sel = [e for e in ob.data.edges if e.select and not edge_match(e,[v1,v2])]
    verts_sel = [v for v in ob.data.vertices if v.select and not vert_match(v,[v1,v2],verts_active)]
    sp = calc_scale_point(on_axis, verts_active, verts_sel[0])
    #push
    tmp_cursor = bpy.context.space_data.cursor_location
    
    bpy.context.space_data.cursor_location = sp.co
    bpy.context.space_data.pivot_point = 'CURSOR'
    bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='VERT')  
    bpy.ops.transform.resize(value=size, constraint_axis=axis,
                             constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED',
                             proportional_edit_falloff='SMOOTH', proportional_size=1)
    #pop
    bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='EDGE')
    bpy.context.space_data.cursor_location = tmp_cursor
    print(sp)


    print('--',verts_sel,verts_active)
    pass

def is_asix_edge(co1, co2):
    sub_co = co1 - co2
    zero_count = 0
    for v in sub_co:
        if v==0:
            zero_count += 1
            pass
    if zero_count==2:
        return True
    return False




def len_edge_in_vert_mode(target_length,on_axis):
    print("Dialog Runs", target_length)
    print(on_axis)
    bpy.context.space_data.pivot_point = 'ACTIVE_ELEMENT'
    bpy.ops.view3d.snap_cursor_to_selected()
    
    axis_idx = int(on_axis) 
    a = [False, False, False]
    a[axis_idx] = True
    axis = a

    cur_length = calc_length(axis=axis_idx)
    s = target_length / cur_length *.5
    size = (s, s, s)

    bpy.ops.transform.resize(value=size, constraint_axis=axis,
                             constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED',
                             proportional_edit_falloff='SMOOTH', proportional_size=1)
    pass

class LEDialogOperator(bpy.types.Operator):
    bl_idname = "object.dialog_operator"
    bl_label = "Len the Edge"
    print
    target_length = bpy.props.FloatProperty(name="length")
    on_axis = bpy.props.EnumProperty(items = [("0",'x axis','xd'),("1",'y axis','yd'),("2",'z axis','zd')],name = "axis", description="desc", default = ("0"))
        
     
    def execute(self, context):
        # len_edge_in_vert_mode(self.target_length, self.on_axis)
        len_edge_in_edge_mode(self.target_length, self.on_axis)
        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)


def len_edge(context):
    bpy.ops.object.dialog_operator('INVOKE_DEFAULT')
    pass


class LE(bpy.types.Operator):
    bl_idname = 'mesh.le'
    bl_label = 'Len the edge'
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return (obj and obj.type == 'MESH')

    def execute(self, context):
        len_edge(context)
        return {'FINISHED'}


def menu_func(self, context):
    self.layout.operator(LE.bl_idname, text=LE.bl_label)


def register():
    bpy.utils.register_module(__name__)
    bpy.types.VIEW3D_MT_edit_mesh_specials.append(menu_func)
    bpy.types.VIEW3D_MT_edit_mesh_vertices.append(menu_func)


def unregister():
    bpy.utils.unregister_module(__name__)
    bpy.types.VIEW3D_MT_edit_mesh_specials.remove(menu_func)
    bpy.types.VIEW3D_MT_edit_mesh_vertices.remove(menu_func)


if __name__ == "__main__":
    register()

