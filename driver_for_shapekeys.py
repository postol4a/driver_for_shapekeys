import bpy

bl_info = {
    "name" : "Driver for Shapekey ",             # プラグイン名
    "author" : "Pom",                  # 作者
    "version" : (0,1),                  # プラグインのバージョン
    "blender" : (2, 80, 0),              # プラグインが動作するBlenderのバージョン
    "location" : "3dView > object",   # Blender内部でのプラグインの位置づけ
    "description" : "add driver for shapekey",   # プラグインの説明
    "warning" : "",
    "wiki_url" : "",                    # プラグインの説明が存在するWikiページのURL
    "tracker_url" : "",                 # Blender Developer OrgのスレッドURL
    "category" : "Properties"                   # プラグインのカテゴリ名
}

class add_driver(bpy.types.Operator):

    bl_idname = "driver.shapekey"               # ID名
    bl_label = "add driver for shapekeys"              # メニューに表示される文字列
    bl_description = "add driver for shapekeys"        # メニューに表示される説明文
    bl_options = {'REGISTER', 'UNDO'}

    # 実際にプラグインが処理を実施する処理
    def execute(self, context):
        
        #Ref Target Obj
        context = bpy.context
        selected_obj = context.active_object
        selected_objName = context.active_object.name
        selected_obj_data = selected_obj.data
        obj_shapekeys = selected_obj_data.shape_keys

        #check if duplicate armature
        for armature in bpy.data.armatures:
            if armature.name == selected_objName + '_Shapekeys':
                bpy.data.armatures.remove(armature)
                        
        for item in bpy.context.scene.objects:
            if item.name ==  selected_objName + '_Shapekeys':
                bpy.data.objects.remove(item)
            
        #create armature
        bpy.ops.object.armature_add(location=(0.0,0.0,5.0))
        armature_obj = context.active_object
        armature_obj.name = selected_objName + '_Shapekeys'
        armature_obj.data.name = selected_objName + '_Shapekeys'    

        for NumberOfShapekeys in range(len(obj_shapekeys.key_blocks)):
            bpy.ops.object.mode_set(mode='EDIT')
            #create bone
            cur_bone = armature_obj.data.edit_bones.new('bone')
            cur_bone.name = (obj_shapekeys.key_blocks[NumberOfShapekeys].name)
            cur_bone.head = (0.0,0.0,0.0)
            cur_bone.tail = (0.0,0.0,1.0)
            #remove default var
            cur_key = obj_shapekeys.key_blocks[NumberOfShapekeys] 
            cur_key.driver_remove('value')
            #add driver var
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

