# -*- coding: utf-8 -*-
__author__ = 'SolPie'
import bpy
bl_info = {
    "name": "Anime Tools",
    "author": "SolPie",
    "version": (1, 0),
    "blender": (2, 76, 0),
    "location": "View3D > Tools > Anime",
    "description": "misc tool",
    "warning": "",
    "category": "Animation"}
## CREA PANELES EN TOOLS
bpy.types.Scene.anime_cloth_group = bpy.props.BoolProperty(default=False)
bpy.types.Scene.anime_cloth_group_name = bpy.props.StringProperty(name="group name",default="Cloth")

class AnimePanel(bpy.types.Panel):
    bl_label = 'Objects'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = 'Anime'
    bl_context = ""

    def draw(self, context):
        active_obj = context.active_object
        layout = self.layout

        col = layout.column(align=True)

        row = col.row()
        row.prop(bpy.context.scene, "anime_cloth_group", text="Cloth Group", icon="OBJECT_DATAMODE")
        row.prop(bpy.context.scene, "anime_cloth_group_name", text="Name")
        # col.operator("anime.cloth.init", text="init cloth group UI")
        #col.prop(bpy.context.scene, "anime_object_tools", text="Object", icon="OBJECT_DATAMODE")


# POLLS
class PollCloth():
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = 'Anime'

    @classmethod
    def poll(cls, context):
        return context.scene.anime_cloth_group

## PANELES
class PanelCloth(PollCloth, bpy.types.Panel):
    bl_idname = "Anime Cloth group"
    bl_label = "Cloth Group"

    def draw(self, context):
        active_obj = context.active_object
        layout = self.layout
        col = layout.column(align=1)
        row = col.row()

        groupName = context.scene.anime_cloth_group_name
        if bpy.data.groups.get(groupName):
            for obj in bpy.data.groups[groupName].objects:
                colrow = col.row(align=1)
                colrow.label(text=obj.name)
                colrow.operator("anime.cloth_bake", text="Bake").objName = obj.name
                
                pass

class ClothBake(bpy.types.Operator):
    bl_idname = 'anime.cloth_bake'
    bl_label = 'Bake'
    bl_options = {'REGISTER', 'UNDO'}
    objName = bpy.props.StringProperty()

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        bakeObj =  bpy.data.objects[self.objName]
        #deselect
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.select_all(action='DESELECT')

        bpy.context.scene.objects.active = bakeObj
        bakeObj.select = True
        #
        if not bakeObj.modifiers.get("Cloth"):
            bpy.ops.object.modifier_add(type='CLOTH')
        for modifier in bakeObj.modifiers:
            if modifier.type == 'CLOTH':
                override = {'scene': bpy.context.active_base.id_data, 'active_object': object, 'point_cache': modifier.point_cache}
                bpy.ops.ptcache.free_bake(override)
                bpy.ops.ptcache.bake(override,bake=True)
        print(self.objName)
        return {'FINISHED'}



def register():
    bpy.utils.register_module(__name__)

def unregister():
    bpy.utils.unregister_module(__name__)


if __name__ == "__main__":
    register()
