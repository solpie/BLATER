import bpy

bl_info = {
    "name": "Ngx Select",
    "author": "SolPie",
    "version": (1,0),
    "blender": (2, 68, 0),
    "location": "View3D > Specials > Ngx Select ",
    "description": "Select the verts on -x",
    "warning": "",
    "category": "Mesh"}

def sel_ng_x_verts(context):
    ob = context.active_object
    #sel_mode = bpy.context.tool_settings.mesh_select_mode
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.object.mode_set(mode='OBJECT')
    #
    bpy.context.tool_settings.mesh_select_mode = [True, False, False]
    #num = 0
    for v in ob.data.vertices:
        if v.co.x < 0:
            #print('select -x:',v.co.x)
            v.select = True
            #num += 1
            #print(num)
    bpy.ops.object.mode_set(mode='EDIT')
    #bpy.context.tool_settings.mesh_select_mode = sel_mode


def set_mirror(v1, v2):
    bpy.ops.object.mode_set(mode='OBJECT')
    v2.co = v1.co
    v2.co.x = -v2.co.x
    bpy.ops.object.mode_set(mode='EDIT')


class NgxSel(bpy.types.Operator):
    bl_idname = 'mesh.ngx'
    bl_label = 'Ngx Select'
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return (obj and obj.type == 'MESH')

    def execute(self, context):
        sel_ng_x_verts(context)
        return {'FINISHED'}


def menu_func(self, context):
    self.layout.operator(NgxSel.bl_idname, text="Ngx Select")


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

