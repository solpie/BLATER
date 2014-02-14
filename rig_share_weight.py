import bpy

bl_info = {
    "name": "Share weight",
    "author": "SolPie",
    "version": (1, 1),
    "blender": (2, 69, 0),
    "location": "View3D > Specials > Share weight",
    "description": "Share weight",
    "warning": "",
    "category": "Rig"}


def auto_weight():
    scn = bpy.context.scene
    ob_edit = bpy.context.active_object
    ob_mesh = None

    #find ob_mesh
    obs = bpy.context.selected_objects
    for ob in obs:
        if ob == ob_edit:
            pass
        else:
            ob_mesh = ob
    ob_mesh.select = False
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.duplicate()
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.armature.select_all(action='INVERT')
    bpy.ops.armature.delete()
    bpy.ops.object.mode_set(mode='OBJECT')

    tmp_bones = bpy.context.active_object
    print(ob_edit, ob_mesh, tmp_bones)

    #Auto weight
    ob_edit.select = False
    ob_mesh.select = True
    tmp_bones.select = True
    scn.objects.active = tmp_bones
    bpy.ops.object.parent_set(type='ARMATURE_AUTO')
    ob_mesh.modifiers[-1].object = bpy.data.objects[ob_edit.name]

    ob_edit.select = True
    ob_mesh.select = True
    tmp_bones.select = False
    scn.objects.active = ob_edit
    bpy.ops.object.parent_set(type='ARMATURE', keep_transform=False)

    #delete tmp bones
    ob_edit.select = False
    ob_mesh.select = False
    tmp_bones.select = True
    scn.objects.active = tmp_bones
    bpy.ops.object.delete(use_global=False)

    #pose mode
    scn.objects.active = ob_edit
    bpy.ops.object.posemode_toggle()


class ShareWeight(bpy.types.Operator):
    bl_idname = 'armature.sharewight'
    bl_label = 'share weight from one armature'
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return (obj and obj.type == 'ARMATURE')

    def execute(self, context):
        auto_weight()
        return {'FINISHED'}


def menu_func(self, context):
    self.layout.operator(ShareWeight.bl_idname, text="Share weight")


def register():
    bpy.utils.register_module(__name__)
    bpy.types.VIEW3D_MT_armature_specials.append(menu_func)


def unregister():
    bpy.utils.unregister_module(__name__)
    bpy.types.VIEW3D_MT_armature_specials.remove(menu_func)
