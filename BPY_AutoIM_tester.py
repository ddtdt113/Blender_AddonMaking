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
        BaseMesh = bpy.context.active_object
        BaseMesh_loc = bpy.context.object.location
       
        print ("Select Object Name is :", BaseMesh.name)
        print ("Select Object Transform is :",BaseMesh_loc)
        
              
      # Duplicate Selected Object as "[SelectedObject]_Duplicated"
        bpy.ops.object.duplicate(linked=False, mode='TRANSLATION')
        BaseMesh_Duplicated = bpy.context.active_object
        BaseMesh_Duplicated.name = str(BaseMesh.name)+"_Duplicated"
       
      # Debug BaseMEsh_Duplicated.Name
        print("BaseMesh_Duplicated is :"+ BaseMesh_Duplicated.name)
      
      
   #----------------------BaseMesh_Duplicated Instant Mesh Setting ---------------------#
   # --------------------you can add more setting after the beta test is over---------- #
   #------------------------------------------------------------------------------------#
          
      # Set the number of crease level in Instant Mesh Setting (Test Default = 4)
        bpy.ops.object.instant_meshes_remesh(crease=4)
        
      # Set the number of Vertex Count in Instant Mesh Setting (Test Default = 4)
        vertex = bpy.context.active_object.data.vertices
        vertex_count = len(vertex)
        
        print(BaseMesh.name + "'s Vertex Count is : " + str(vertex_count))

    #----------------------------------------------------------------------------------#
        # bpy.ops.object.select_all(action='DESELECT')
        print("------------------------------Start Retopolozied by Instant Mesh---------------------------------")
        
        bpy.ops.object.shade_flat()        
        bpy.ops.mesh.customdata_custom_splitnormals_clear()
        
        bpy.ops.object.data_transfer(use_reverse_transfer=False,use_freeze=False,data_type='UV',use_create=True
        ,vert_mapping='NEAREST',use_auto_transform=False, use_object_transform= True,use_max_distance=False
        ,max_distance=1,ray_radius=0, islands_precision=0.1,layers_select_src='ACTIVE',layers_select_dst='ACTIVE'
        ,mix_mode='REPLACE',mix_factor=1)        
        
        bpy.ops.object.instant_meshes_remesh(crease = 2, verts = vertex_count, openUI=False, remeshIt=True)
        
        bpy.ops.object.instant_meshes_remesh(remeshIt=False)
        
        print("------------------------------End Retopolozied by Instant Mesh---------------------------------")
                            
    #---------------------------Unwrap it with Smart UV-----------------------------------------#
        bpy.data.objects[BaseMesh_Duplicated.name+"_remesh"].select_set(True)
        
        BaseMesh_remesh = context.scene.objects.get(BaseMesh_Duplicated.name+'_remesh')
        context.view_layer.objects.active = BaseMesh_remesh
        
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.uv.smart_project(angle_limit=1.15192, island_margin=0.0, correct_aspect=True, scale_to_bounds=False)
        bpy.data.objects[BaseMesh_Duplicated.name + '_remesh'].select_set(True)
        bpy.ops.object.mode_set(mode='OBJECT')
    
    #---------------------------Make and Set Texture to the Material----------------------------------------#
        
        mat = bpy.data.materials.get('Material')
        tex = BaseMesh.name + '_Tx_remesh'
       
    #---------------------------Check Default Material-----------------------------------------------------#
        
        #bpy.ops.view3d.material_remove_object()
        
       
        if mat is None :
            bpy.data.materials.new(name = 'Material')
        else :
            BaseMesh_remesh.data.materials.clear() # delete all Material
        
        BaseMesh_remesh.data.materials.append(mat)
        print ('Material Generated')
       
            
        BaseMesh_remesh.active_material.use_nodes = True
        Shader = mat.node_tree.nodes['Principled BSDF']
        
        
        texNode = mat.node_tree.nodes.new('ShaderNodeTexImage') 
        bpy.ops.image.new(name=tex, width=1024, height=1024, color=(0.0, 0.0, 0.0, 1.0), alpha=True, generated_type='BLANK', float=False, use_stereo_3d=False)
        print(tex+': texture generated')
        
        texImage = bpy.data.images[tex]        
        texNode.image = texImage
        
        mat.node_tree.links.new(Shader.inputs['Base Color'], texNode.outputs['Color'])
        print('Shader and Texture Connected')
        
    #---------------------------Bake Texture----------------------------------------#        
        renderer =  bpy.context.scene
        
        
        bpy.data.objects[BaseMesh_remesh.name].select_set(True)
        
        bpy.context.scene.render.engine= 'CYCLES'
        renderer.cycles.bake_type = 'DIFFUSE'
        renderer.cycles.device = 'GPU'
        renderer.render.bake.use_pass_direct = False
        renderer.render.bake.use_pass_indirect = False
        renderer.render.bake.use_selected_to_active = True
        bpy.context.scene.render.bake.max_ray_distance = 0.1
               
       
       
        
        
        # print(type(BaseMesh_remesh)) =bpy_types.Object
        

        
    #-----------------------Renderer Set for Bake Texture---------------------------#
        
        bpy.ops.object.select_all(action='DESELECT')
        bpy.data.objects[BaseMesh.name].select_set(True)
        bpy.data.objects[BaseMesh_remesh.name].select_set(True)
        
        
        
        
    #------------------------Let's Bake--------------------------------------------#    
        bpy.ops.object.bake(type='DIFFUSE', pass_filter={'COLOR'}, filepath=''
                            , width=4096, height=4096, margin=16, use_selected_to_active=True
                            , max_ray_distance=0.1, cage_extrusion=0.0, cage_object=''
                            , normal_space='TANGENT', normal_r='POS_X', normal_g='POS_Y'
                            , normal_b='POS_Z'
                            , target='IMAGE_TEXTURES'
                            , save_mode='INTERNAL'
                            , use_clear=False, use_cage=False
                            , use_split_materials=False
                            , use_automatic_name=False, uv_layer='')
        
        print("Bake Completed :)")
        
        
        
      
      
      
        
        
               
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