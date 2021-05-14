import bpy


#make AutoIM Panel (AutoIM = Auto Instant Mesh)

class AutoIM(bpy.types.Panel):

    bl_label = "AutoIM(beta)"
    bl_idname = "panel_PT_AutoIM"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    
#Panel Name
    bl_category = "AutoIM(beta)"
    
    
    def move_cube(self, context) :
        #make cube
       bpy.ops.mesh.primitive_cube_add(location = (0.0,0.0,1.0))
       bpy.ops.transfomr.resize(value=(4,4,4))
       
       #Get the Cube object and rename
       cube = bpy.context.object
       cube.name = 'Test1'
       


    def draw(self, context):
        
        layout = self.layout

        row = layout.row()
        row.label(text="AutoIM is the macro for Auto-Retopology with Instant Mesh(Beta)", icon = 'ERROR')
        row = layout.row()
        row.operator('button.autoIM', text = "Auto-Retopology")
        
        
class button_AutoIM(bpy.types.Operator):
    bl_idnmae = "button.autoIM" #translate to C-name BUTTON_OT_explode
    bl_label = "Button AutoIM"    
    bl_options = 'PRESET'    
    
    def execute(self, context):
        #self.report({'INFO'}, "HELLO WORLD")
        print("AutoIM Started")
        return {'FINISHED'}
        





#register the panel with Register()

def register():
    bpy.utils.register_class(button_AutoIM)
    bpy.utils.register_class(AutoIM)
    


def unregister():
    bpy.utils.unregister_class(button_AutoIM)
    bpy.utils.unregister_class(AutoIM)
    


if __name__ == "__main__":
    register()
