import bpy

#-----------------------------------------------------#
#make AutoIM Panel (AutoIM = Auto Instant Mesh)

class AutoIM(bpy.types.Panel):

    bl_label = "AutoIM(beta)"
    bl_idname = "panel_PT_autoIM"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    
#Panel Name
    bl_category = "AutoIM(beta)"
    bl_context = "objectmode"
    
    



    def draw(self, context):
        
        layout = self.layout
        
        layout.label(text = "AutoIM")

        row = layout.row(align = True)
        row.label(text="AutoIM is a macro for Auto-Retopology with Instant Mesh(Beta)", icon = 'ERROR')
        row = layout.row(align = True)
        row.operator(ButtonAutoIM.bl_idname, text = "Auto-Retopology", icon = "CONSOLE")
         
      
#------------------------------------------------------------------------#       
        
class ButtonAutoIM(bpy.types.Operator):
    bl_idname = "object.sample_operator" 
    bl_label = "Button AutoIM"    
    
      
    
    def execute(self, context):
        print("Hi")
        return {'FINISHED'}
        
#--------------------------------------------------------#



#-------------------------------------------------#
#register the panel with Register()

def register():
    bpy.utils.register_class(AutoIM)
    bpy.utils.register_class(ButtonAutoIM)
    
    


def unregister():
    bpy.utils.unregister_class(AutoIM)
    bpy.utils.unregister_class(ButtonAutoIM)
    


if __name__ == "__main__":
    register()

#-------------------------------------------------#