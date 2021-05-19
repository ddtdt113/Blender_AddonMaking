import bpy
import bmesh

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
         
 #----------------------------------------------------------------------------------------------------------#     
 
#------------------------Main Execute Part-------------------------------------#       
        
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
       
      # Debug BaseMEsh_Duplicated.Name
        print("BaseMesh_Duplicated is :"+ BaseMesh_Duplicated.name)
      
      
   #----------------------BaseMesh_Duplicated Instant Mesh Setting ---------------------#
   # --------------------you can add more setting after the beta test is over---------- #
   #------------------------------------------------------------------------------------#
          
      # Set the number of crease level in Instant Mesh Setting (Test Default = 4)
        bpy.ops.object.instant_meshes_remesh(crease=4)
        
      # Set the number of Vertex Count in Instant Mesh Setting (Test Default = 4)
        bpy.ops.object.instant_meshes_remesh(verts=30000)
        
    #-------------------Add Setting about Instant Mesh in here-------------------------#
    
    
    
    #----------------------------------------------------------------------------------#
               # bpy.ops.object.select_all(action='DESELECT')
        print("------------------------------Start Retopolozied by Instant Mesh---------------------------------")
        bpy.ops.object.shade_flat()        
        bpy.ops.mesh.customdata_custom_splitnormals_clear()
        
        bpy.ops.object.data_transfer(use_reverse_transfer=False,use_freeze=False,data_type='UV',use_create=True
        ,vert_mapping='NEAREST',use_auto_transform=False, use_object_transform= True,use_max_distance=False
        ,max_distance=1,ray_radius=0, islands_precision=0.1,layers_select_src='ACTIVE',layers_select_dst='ACTIVE'
        ,mix_mode='REPLACE',mix_factor=1)        
        
        bpy.ops.object.instant_meshes_remesh(remeshIt=True)
        bpy.ops.object.instant_meshes_remesh(remeshIt=False)
        
        print("------------------------------End Retopolozied by Instant Mesh---------------------------------")
                            
    #---------------------------Unwrap it with Smart UV-----------------------------------------#
        bpy.data.objects[str(BaseMesh_Duplicated.name)+"_remesh"].select_set(True)
        
        context.view_layer.objects.active = context.scene.objects.get(str(BaseMesh_Duplicated.name)+'_remesh')
        
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.uv.smart_project(angle_limit=1.15192, island_margin=0.0, correct_aspect=True, scale_to_bounds=False)
        bpy.data.objects[str(BaseMesh_Duplicated.name)+'_remesh'].select_set(True)
        bpy.ops.object.mode_set(mode='OBJECT')
    
    #---------------------------Set Texture_bake to the Material----------------------------------------#
       
       
        
      
      
      
        
        
               
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