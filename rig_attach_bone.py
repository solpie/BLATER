import bpy

bl_info = {
    "name": "Attach bone",
    "author": "SolPie",
    "version": (1, 1),
    "blender": (2, 69, 0),
    "location": "View3D > Specials > Attach bone",
    "description": "attach one bone to another",
    "warning": "",
    "category": "Rig"}


def auto_weight():
    scn = bpy.context.scene
    edit_ob = bpy.context.active_object
    ob_mesh = None

    #find ob_mesh
    obs = bpy.context.selected_objects
    for ob in obs:
        if ob == edit_ob:
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
    print(edit_ob, ob_mesh, tmp_bones)

    #Auto weight
    edit_ob.select = False
    ob_mesh.select = True
    tmp_bones.select = True
    scn.objects.active = tmp_bones
    bpy.ops.object.parent_set(type='ARMATURE_AUTO')
    ob_mesh.modifiers[-1].object = bpy.data.objects[edit_ob_name]

    edit_ob.select = True
    ob_mesh.select = True
    tmp_bones.select = False
    scn.objects.active = edit_ob
    bpy.ops.object.parent_set(type='ARMATURE', keep_transform=False)

    #delete tmp bones
    edit_ob.select = False
    ob_mesh.select = False
    tmp_bones.select = True
    scn.objects.active = tmp_bones
    bpy.ops.object.delete(use_global=False)

    #pose mode
    scn.objects.active = edit_ob
    bpy.ops.object.posemode_toggle()


def attach(context):
    scn = bpy.context.scene
    ops = bpy.ops
    edit_ob = context.active_object
    obs = context.selected_objects
    for obj in obs:
        scn.objects.active = obj
        if obj == edit_ob:
            edit_bone = context.active_bone
        else:
            target_ob = obj
    print(edit_ob, target_ob)
    # print(edit_bone, target_bone)
    def snap_head(select_head=True):
        bpy.ops.object.editmode_toggle()
        scn.objects.active = target_ob
        target_ob.select = True
        edit_ob.select = False
        bpy.ops.object.editmode_toggle()
        target_bone = context.active_bone
        bpy.ops.armature.select_all(action='DESELECT')
        target_bone.select_head = select_head
        target_bone.select_tail = not select_head
        # print(target_bone, target_bone.select, target_bone.select_head, target_bone.select_tail)
        bpy.ops.view3d.snap_cursor_to_selected()
        #snap head to cursor
        bpy.ops.object.editmode_toggle()
        scn.objects.active = edit_ob
        target_ob.select = False
        edit_ob.select = True
        bpy.ops.object.editmode_toggle()
        edit_bone = context.active_bone
        bpy.ops.armature.select_all(action='DESELECT')
        edit_bone.select_head = select_head
        edit_bone.select_tail = not select_head
        bpy.ops.view3d.snap_selected_to_cursor(use_offset=False)
        #set roll
        edit_bone.roll = target_bone.roll

        #snap cursor to head
    snap_head(True)
    snap_head(False)


class AttachBone(bpy.types.Operator):
    bl_idname = 'armature.attachbone'
    bl_label = 'attach one bone to another'
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return (obj and obj.type == 'ARMATURE')

    def execute(self, context):
        # attach(context)
        auto_weight()
        return {'FINISHED'}


def menu_func(self, context):
    self.layout.operator(AttachBone.bl_idname, text="Attach bone")


def register():
    bpy.utils.register_module(__name__)
    bpy.types.VIEW3D_MT_armature_specials.append(menu_func)


def unregister():
    bpy.utils.unregister_module(__name__)
    bpy.types.VIEW3D_MT_armature_specials.remove(menu_func)
