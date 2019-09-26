import bpy
#メタデータ
bl_info = {
    "name" : "Driver for Shapekey ",             # プラグイン名
    "author" : "Pom",                  
    "version" : (0,1),                  
    "blender" : (2, 80, 0),              
    "location" : "3dView > object",   # Blender内部でのプラグインの位置づけ
    "description" : "add driver for shapekey",   
    "warning" : "",
    "wiki_url" : "",                    
    "tracker_url" : "",                 
    "category" : "Properties"                   
}

class add_driver(bpy.types.Operator):

    bl_idname = "driver.shapekey"               # ID名
    bl_label = "add driver for shapekeys"              # メニューに表示される文字列
    bl_description = "add driver for shapekeys"        # メニューに表示される説明文
    bl_options = {'REGISTER', 'UNDO'}

    # 実際にAddonが処理を実施する処理
    def execute(self, context):
        
        context = bpy.context
        selected_obj = context.active_object
        selected_objName = context.active_object.name
        selected_obj_data = selected_obj.data
        obj_shapekeys = selected_obj_data.shape_keys

        #Armaruteの重複を確認
        for armature in bpy.data.armatures:
            if armature.name == selected_objName + '_Shapekeys':
                bpy.data.armatures.remove(armature)
                        
        for armature in bpy.context.scene.objects:
            if armature.name ==  selected_objName + '_Shapekeys':
                bpy.data.objects.remove(item)
            
        #Armatureを作成
        bpy.ops.object.armature_add(location=(0.0,0.0,5.0))
        armature_obj = context.active_object
        armature_obj.name = selected_objName + '_Shapekeys'
        armature_obj.data.name = selected_objName + '_Shapekeys'    

        for NumberOfShapekeys in range(len(obj_shapekeys.key_blocks)):
            bpy.ops.object.mode_set(mode='EDIT')
            #boneを作成
            cur_bone = armature_obj.data.edit_bones.new('bone')
            cur_bone.name = (obj_shapekeys.key_blocks[NumberOfShapekeys].name)
            cur_bone.head = (0.0,0.0,0.0)
            cur_bone.tail = (0.0,0.0,1.0)
            #デフォルトで入っているドライバーの変数を削除
            cur_key = obj_shapekeys.key_blocks[NumberOfShapekeys] 
            cur_key.driver_remove('value')
            #ドライバーの変数を追加
            influence = cur_key.driver_add('value', -1)
            influence.driver.type = 'SUM'
            var = influence.driver.variables.new()
            var.name = 'influence_value'
            var.type = 'TRANSFORMS'
            TargetPath = bpy.data.objects.get(selected_objName + '_Shapekeys')
            var.targets[0].id = TargetPath
            var.targets[0].bone_target = cur_key.name
            var.targets[0].transform_type = 'LOC_Z'
            var.targets[0].transform_space = 'LOCAL_SPACE'

        bpy.ops.object.mode_set(mode='OBJECT')
        return {'FINISHED'}             # 成功した場合はFINISHEDを返す


#メニューに追加
def menu_func(self, context):
    self.layout.operator("driver.shapekey")

#インストール時の処理
def register():
    bpy.utils.register_class(add_driver)
    bpy.types.VIEW3D_MT_object.append(menu_func)

#アンインストール時の処理
def unregister():
    bpy.utils.unregister_class(add_driver)
    bpy.types.VIEW3D_MT_object.remove(menu_func)

if __name__ == "__main__":
    register()

