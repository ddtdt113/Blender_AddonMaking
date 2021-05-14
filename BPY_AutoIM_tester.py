import bpy

#-----------------------------------------------------#
#make AutoIM Panel (AutoIM = Auto Instant Mesh)

class AutoIM(bpy.types.Panel):

    bl_label = "AutoIM(beta)"
    bl_idname = "PANEL_PT_autoIM"
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
        row.operator(CreateAndExecuteButton.bl_idname, text = "Auto-Retopology", icon = "CONSOLE")
         
      
#------------------------------------------------------------------------#       
        
class CreateAndExecuteButton(bpy.types.Operator):
    bl_idname = "object.button_create" 
    bl_label = "Button Create"    
        
    def execute(self, context):
       #Announce Button Clicked fcr debug
        print("Start AutoIM(beta)")
        
       # Get info of Selected Object Name and Transform
        BaseMesh = bpy.context.active_object.name
        BaseMesh_loc = bpy.context.object.location
       
        print ("Select Object Name is :", BaseMesh)
        print ("Select Object Transform is :",BaseMesh_loc)
        
              
      # Duplicate Selected Object as "[SelectedObject]_Duplicated"
        bpy.ops.object.duplicate(linked=False, mode='TRANSLATION')
        BaseMesh_Duplicated = bpy.context.active_object
        BaseMesh_Duplicated.name = str(BaseMesh)+"_Duplicated"
        
               
        return {'FINISHED'}
    
#--------------------------------------------------------#




#-------------------------------------------------#
#register the panel with Register()

def register():
    bpy.utils.register_class(AutoIM)
    bpy.utils.register_class(CreateAndExecuteButton)
    
    


def unregister():
    bpy.utils.unregister_class(AutoIM)
    bpy.utils.unregister_class(CreateAndExecuteButton)
    


if __name__ == "__main__":
    register()

#-------------------------------------------------#