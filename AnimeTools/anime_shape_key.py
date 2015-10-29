# -*- coding: utf-8 -*-
__author__ = 'SolPie'
import bpy
## shape key  #########################################################################


class PollShapeKey():
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = 'Anime'

    @classmethod
    def poll(cls, context):
        return context.scene.anime_shape_key

class PanelShapeKey(PollShapeKey, bpy.types.Panel):
    bl_idname = "Anime Shape Key"
    bl_label = "Shape Key"

    def draw(self, context):
        active_obj = context.active_object
        layout = self.layout

        col = layout.column()
        col.operator("anime.shapekey_mirror", text="Mirror")

class ShapeAddMirrorKey(bpy.types.Operator):
    bl_idname = 'anime.shapekey_mirror'
    bl_label = 'Mirror'
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        #bpy.ops.object.mode_set(mode='OBJECT')
        src_obj = bpy.context.active_object
        bpy.ops.object.duplicate()

        bpy.ops.object.shape_key_mirror(use_topology=False)
        dup_obj = bpy.context.active_object

        src_obj.select = True
        bpy.context.scene.objects.active = src_obj

        bpy.ops.object.shape_key_transfer()
        bpy.context.object.show_only_shape_key = False

        bpy.ops.object.select_all(action='DESELECT')
        bpy.context.scene.objects.active = dup_obj
        dup_obj.select = True
        bpy.ops.object.delete(use_global=False)

        src_obj.select = True
        bpy.context.scene.objects.active = src_obj
        return {'FINISHED'}
