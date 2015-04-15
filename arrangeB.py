bl_info = {
    "name": "arrange tools",
    "category": "Object",
}

import bpy


def ObjectArrangeB(self, X, Y, Z):
    sels = bpy.context.selected_objects
    if len(sels[:]) > 1:
        # VARIABLES
        dif = sels[-1].location - sels[0].location
        chunkglobal = dif / (len(sels[:]) - 1)
        chunkx = 0
        chunky = 0
        chunkz = 0
        deltafst = sels[0].location

        # ORDENA
        for OBJECT in sels[:]:
            if X:  OBJECT.location.x = deltafst[0] + chunkx
            if Y:  OBJECT.location[1] = deltafst[1] + chunky
            if Z:  OBJECT.location.z = deltafst[2] + chunkz
            chunkx += chunkglobal[0]
            chunky += chunkglobal[1]
            chunkz += chunkglobal[2]
    else:
        self.report({'ERROR'}, "Selection is only 1!")


class DialogArrangeB(bpy.types.Operator):
    bl_idname = "object.arrange_objs"
    bl_label = "Arrange object"
    Boolx = bpy.props.BoolProperty(name="X")
    Booly = bpy.props.BoolProperty(name="Y")
    Boolz = bpy.props.BoolProperty(name="Z")

    def execute(self, context):
        ObjectArrangeB(self, self.Boolx, self.Booly, self.Boolz)
        return {'FINISHED'}

    def invoke(self, context, event):
        self.Boolx = True
        self.Booly = True
        self.Boolz = True
        return context.window_manager.invoke_props_dialog(self)


def arrage():
    act_obj = bpy.context.active_object
    sels = bpy.context.selected_objects
    sortZ = []
    for idx in range(0, len(sels)):
        sortZ.append(sels[idx])
        pass

    sortZ = sorted(sortZ, key=lambda obj: obj.location[2])

    act_z = 0
    invert = .20
    print('sortZ')
    for idx in range(0, len(sortZ)):
        print(sortZ[idx].location[2])
        if sortZ[idx] is act_obj:
            act_z = sortZ[idx].location[2]
            pass
        else:
            if invert == 0:
                invert = sortZ[idx].location[2] - act_z
            sortZ[idx].location[2] = act_z + (invert * idx)
        pass
    pass


def register():
    bpy.utils.register_class(DialogArrangeB)


def unregister():
    bpy.utils.unregister_class(DialogArrangeB)
    # arrage()