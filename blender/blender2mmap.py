import bpy, gpu, bgl
import time, timeit
import mmap, numpy


mm_data = mmap.mmap( -1, 8, tagname="blender_off-axis_server" )


class ModalOperator(bpy.types.Operator):
    bl_idname = "object.modal_operatorss"
    bl_label = "Simple Modal Operator"

    def blender_object_2_array(self, fdfdfdfd):


        ###################### data information
        
        objects_array = []

        for dffd in fdfdfdfd:#bpy.data.objects:

            if(dffd.type=="MESH"):
                
                dffd.data.calc_loop_triangles()
                
                object_array = []
                
                # vertex
                vertex = numpy.empty(3*len(dffd.data.vertices), dtype=numpy.float64)
                dffd.data.vertices.foreach_get("co",vertex)
                object_array.append(vertex)
                
                # edge
                #edge = numpy.empty(2*len(dffd.data.edges), dtype=numpy.uint64)
                #dffd.data.edges.foreach_get("vertices",edge)
                #object_array.append(edge)
                edge = numpy.empty(3*len(dffd.data.loop_triangles), dtype=numpy.uint64)
                dffd.data.loop_triangles.foreach_get("vertices",edge)
                object_array.append(edge)
                
                # polygon -> normal
                #normal = numpy.empty(3*len(dffd.data.polygons), dtype=numpy.float64)
                #dffd.data.polygons.foreach_get("normal",normal)
                #object_array.append(normal)
                normal = numpy.empty(3*len(dffd.data.vertices), dtype=numpy.float64)
                dffd.data.vertices.foreach_get("normal",normal)
                object_array.append(normal)
                
                objects_array.append(object_array)
                
                
        ###################### sturucture information

        all_bytes_length = 0
        count_bytes_length = 0
        index_bytes_length = []
        data_bytes_length = 0

        # calc data length
        for object in objects_array:
            for sasas in object:
                index_bytes_length.append(sasas.nbytes)
                data_bytes_length = sasas.nbytes + data_bytes_length

        count_bytes_length = numpy.array(
            len(objects_array), dtype=numpy.uint64
        )
        index_bytes_length = numpy.array(
            index_bytes_length, dtype=numpy.uint64
        )
        data_bytes_length = data_bytes_length
        all_bytes_length = numpy.array(
            int(
                8 + 
                count_bytes_length.nbytes + 
                index_bytes_length.nbytes + 
                data_bytes_length
            ), 
            dtype=numpy.uint64
        )
        
        
        return [
            all_bytes_length, count_bytes_length, index_bytes_length, objects_array
        ]
        
    def object_array_2_mmap(self, mm_data, byte_array):
        
        all_bytes_length = byte_array[0]
        number_of_object = byte_array[1]
        index_bytes_length = byte_array[2]
        objects_array = byte_array[3]
        
        ######################## write data ########################
        # all_bytes_length write
        mm_data.write(all_bytes_length.tobytes())

        # number write
        mm_data.write(number_of_object.tobytes())

        # index write
        for object in index_bytes_length:
            mm_data.write(object.tobytes())
            
        # data write
        for object in objects_array:
            for sasas in object:
                mm_data.write(sasas.tobytes())

    def invoke(self, context, event):
        global mm_data
        mm_data.close()
        datas = self.blender_object_2_array(bpy.data.objects)
        mm_data = mmap.mmap( -1, datas[0], tagname="blender_off-axis_server" )
        self.object_array_2_mmap(mm_data, datas)
        print(datas)
        print("ModalOperator:Start")
        print("invoke")
        return {'RUNNING_MODAL'}

class TestPanel(bpy.types.Panel):
    bl_idname = "SAMPLE_PT_LA"
    bl_label = "polygon exporter"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'off-axis'

    def draw(self, context):

        layout = self.layout
       
        row = layout.row()
        row.label(text="  Add an object")
        row = layout.row()
        row.operator(
            "object.modal_operatorss",
            text="Execute Something", 
            icon= 'CUBE'
        )
        row.operator(
            "object.modal_operatorss",
            text="Execute Something flat", 
            icon= 'CUBE'
        )
     
       
def register():
    bpy.utils.register_class(ModalOperator)
    bpy.utils.register_class(TestPanel)
  
def unregister():
    bpy.utils.unregister_class(ModalOperator)
    bpy.utils.unregister_class(TestPanel)
  
if __name__ == "__main__":
    register()

        