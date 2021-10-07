from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy, time, pyrr, mmap, glfw, copy
import shaderLoader, udp_client
from camera import Camera
from figure import Figure
from PIL import Image

cam = Camera()
fig = Figure()

left, right, forward, backward = False, False, False, False
q, e = False, False
a, d, s, w = False, False, False, False

adfadf = [ 0, 0, 0, 0, 0, 0 ]
adfadsf = [ 0, 0, 1500, 0, 0, 1500 ]
monitor_width, monitor_height, scale, ratio = 1024, 1024, 700, 10

gui_ambient  = pyrr.Vector3([   1.0,   1.0,   1.0   ])
gui_diffuse  = pyrr.Vector3([   1.0,   1.0,   1.0   ])
gui_specular = pyrr.Vector3([   1.0,   1.0,   1.0   ])
gui_position = pyrr.Vector3([   1.0,   1.0,   1.0   ])

object_datas = []
VAO, draw_edge_len = [], 0

def mmap_read():


    start = time.time()  # 시작 시간 저장


    # 8바이트를 읽어서 byte의 갯수를 읽어온다.
    mm = mmap.mmap(-1, 8,tagname="blender_off-axis_server"); 
    
    mm.seek(0)
    
    all_byte_count = numpy.frombuffer( mm.read(8), dtype=numpy.uint64 )

    mm.close()


    # 바이트를 읽어서 정점, 엣지, 노말을 읽어온다.
    mm_data = mmap.mmap(-1, int(all_byte_count[0]), tagname="blender_off-axis_server")

    mm_data.seek(8)

    obj_num=int(numpy.frombuffer(mm_data.read(8), dtype=numpy.uint64))
    obj_index=numpy.frombuffer(mm_data.read(obj_num*24), dtype=numpy.uint64)

    obj_datas=[]


    for index in range(0,3*obj_num,3):
        
        POINT  = numpy.frombuffer( mm_data.read(obj_index[index+0]), dtype=numpy.float64 )
        INDEX  = numpy.frombuffer( mm_data.read(obj_index[index+1]), dtype=numpy.uint64  )
        NORMAL = numpy.frombuffer( mm_data.read(obj_index[index+2]), dtype=numpy.float64 )

        obj_data = [ POINT, INDEX, NORMAL]

        obj_datas.append(obj_data)

    print("time :", time.time() - start)  # 현재시각 - 시작시간 = 실행 시간

    mm_data.close()

    return [ obj_num, obj_index, obj_datas ]
def mmap_read_1():


    # 8바이트를 읽어서 byte의 갯수를 읽어온다.
    mm = mmap.mmap(-1, 8,tagname="blender_off-axis_server"); 
    
    mm.seek(0)
    
    all_byte_count = numpy.frombuffer( mm.read(8), dtype=numpy.uint64 )

    mm.close()


    # 바이트를 읽어서 정점, 엣지, 노말을 읽어온다.
    mm_data = mmap.mmap(-1, int(all_byte_count[0]), tagname="blender_off-axis_server")

    mm_data.seek(8)

    obj_num=int(numpy.frombuffer(mm_data.read(8), dtype=numpy.uint64))
    obj_index=numpy.frombuffer(mm_data.read(obj_num*24), dtype=numpy.uint64)

    obj_datas=[]

    start = time.time()  # 시작 시간 저장
    
    for index in range(0,3*obj_num,3):

        POINT  = numpy.frombuffer( mm_data.read(obj_index[index+0]), dtype=numpy.float64 )
        INDEX  = numpy.frombuffer( mm_data.read(obj_index[index+1]), dtype=numpy.uint64  )
        NORMAL = numpy.frombuffer( mm_data.read(obj_index[index+2]), dtype=numpy.float64 )

        WWWWW_POINT  = numpy.empty([len(INDEX)*3], dtype=numpy.float64)
        WWWWW_INDEX  = numpy.arange(0,len(INDEX), dtype=numpy.uint64)
        WWWWW_NORMAL = numpy.empty([len(INDEX)*3], dtype=numpy.float64)

        for OOOOO in range(0,len(INDEX)):
            DD, FF = int(OOOOO*3), int(INDEX[OOOOO]*3)
            WWWWW_POINT[DD+0] = POINT[FF+0]
            WWWWW_POINT[DD+1] = POINT[FF+1]
            WWWWW_POINT[DD+2] = POINT[FF+2]
            #print(DD,FF,OOOOO)

        for OOOOO in range(0,len(NORMAL),3):
            A,B,C, DD = OOOOO+0, OOOOO+1, OOOOO+2, int(OOOOO*3)
            WWWWW_NORMAL[DD+0] = NORMAL[A]
            WWWWW_NORMAL[DD+1] = NORMAL[B]
            WWWWW_NORMAL[DD+2] = NORMAL[C]
            WWWWW_NORMAL[DD+3] = NORMAL[A]
            WWWWW_NORMAL[DD+4] = NORMAL[B]
            WWWWW_NORMAL[DD+5] = NORMAL[C]
            WWWWW_NORMAL[DD+6] = NORMAL[A]
            WWWWW_NORMAL[DD+7] = NORMAL[B]
            WWWWW_NORMAL[DD+8] = NORMAL[C]
        
        obj_data = [ WWWWW_POINT, WWWWW_INDEX, WWWWW_NORMAL]
        #obj_data = [ POINT, INDEX, NORMAL]
        
        obj_datas.append(obj_data)

    print("time :", time.time() - start)  # 현재시각 - 시작시간 = 실행 시간

    mm_data.close()

    return [ obj_num, obj_index, obj_datas ]

# the keyboard input callback
def key_input_clb(window, key, scancode, action, mode):
    
    global left, right, forward, backward, q, e
    global a, d, s, w

    if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
        glfw.set_window_should_close(window, True)

    if key == glfw.KEY_P and action == glfw.PRESS:
        global object_datas, VAO, draw_edge_len
        object_datas = mmap_read()
        print("KEY_P")
        glDeleteVertexArrays(0,VAO)
        glDeleteVertexArrays(1,VAO)
        VAO, draw_edge_len = create_VAO(object_datas[2])


    if key == glfw.KEY_W and action == glfw.PRESS:
        forward = True
    elif key == glfw.KEY_W and action == glfw.RELEASE:
        forward = False
    if key == glfw.KEY_S and action == glfw.PRESS:
        backward = True
    elif key == glfw.KEY_S and action == glfw.RELEASE:
        backward = False
    if key == glfw.KEY_A and action == glfw.PRESS:
        left = True
    elif key == glfw.KEY_A and action == glfw.RELEASE:
        left = False
    if key == glfw.KEY_D and action == glfw.PRESS:
        right = True
    elif key == glfw.KEY_D and action == glfw.RELEASE:
        right = False
    if key == glfw.KEY_Q and action == glfw.PRESS:
        q = True
    elif key == glfw.KEY_Q and action == glfw.RELEASE:
        q = False
    if key == glfw.KEY_E and action == glfw.PRESS:
        e = True
    elif key == glfw.KEY_E and action == glfw.RELEASE:
        e = False

    if key == glfw.KEY_RIGHT  and action == glfw.PRESS:
        d = True
    elif key == glfw.KEY_RIGHT and action == glfw.RELEASE:
        d = False
    if key == glfw.KEY_LEFT and action == glfw.PRESS:
        a = True
    elif key == glfw.KEY_LEFT and action == glfw.RELEASE:
        a = False
    if key == glfw.KEY_DOWN and action == glfw.PRESS:
        s = True
    elif key == glfw.KEY_DOWN and action == glfw.RELEASE:
        s = False
    if key == glfw.KEY_UP and action == glfw.PRESS:
        w = True
    elif key == glfw.KEY_UP and action == glfw.RELEASE:
        w = False

    # if key in [glfw.KEY_W, glfw.KEY_S, glfw.KEY_D, glfw.KEY_A] and action == glfw.RELEASE:
    #     left, right, forward, backward = False, False, False, False
# do the movement, call this function in the main loop
def do_movement():
    
    global left, right, forward, backward
    global a, d, s, w
    #if left:
    #    cam.process_keyboard("LEFT")
    #if right:
    #    cam.process_keyboard("RIGHT")
    #if forward:
    #    cam.process_keyboard("FORWARD")
    #if backward:
    #    cam.process_keyboard("BACKWARD")
    if left:
        fig.process_keyboard("LEFT")
    if right:
        fig.process_keyboard("RIGHT")
    if forward:
        fig.process_keyboard("FORWARD")
    if backward:
        fig.process_keyboard("BACKWARD")
    if q:
        fig.process_keyboard("SSSSS")
    if e:
        fig.process_keyboard("ZZZZZ")


    if a:
        fig.process_keyboard("rLEFT")
    if d:
        fig.process_keyboard("rRIGHT")
    if w:
        fig.process_keyboard("rFORWARD")
    if s:
        fig.process_keyboard("rBACKWARD")
def do_rotation():
    
    global left, right, forward, backward
    global a, d, s, w
    if a:
        cam.process_keyboard("rLEFT")
    if d:
        cam.process_keyboard("rRIGHT")
    if w:
        cam.process_keyboard("rFORWARD")
    if s:
        cam.process_keyboard("rBACKWARD")

def window_resize(window, width, height):
    global monitor_width, monitor_height
    monitor_width, monitor_height = width, height
    glViewport(0, 0, width, height)

def view_zeze():

    global adfadf,monitor_width, monitor_height, scale, ratio

    #HEAD_LX, HEAD_LY, HEAD_LZ, HEAD_RX, HEAD_RY, HEAD_RZ  = -0, 0, 1500, 0, 0, 1500
    HEAD_LX, HEAD_LY, HEAD_LZ = adfadf[0]+adfadsf[0],adfadf[1]+adfadsf[1],adfadf[2]+adfadsf[2]
    HEAD_RX, HEAD_RY, HEAD_RZ = adfadf[3]+adfadsf[3],adfadf[4]+adfadsf[4],adfadf[5]+adfadsf[5]

    HEAD_LX, HEAD_LY, HEAD_LZ = HEAD_LX/scale, HEAD_LY/scale, HEAD_LZ/scale
    HEAD_RX, HEAD_RY, HEAD_RZ = HEAD_RX/scale, HEAD_RY/scale, HEAD_RZ/scale
    left, right, bottom, top = (
        -monitor_width /scale, +monitor_width /scale, 
        -monitor_height/scale, +monitor_height/scale 
    )
    leftL, rightL, bottomL, topL = (
        (left  -HEAD_LX)/ratio, (right-HEAD_LX)/ratio, 
        (bottom+HEAD_LY)/ratio, (top  +HEAD_LY)/ratio
    )
    leftR, rightR, bottomR, topR = (
        (left  -HEAD_RX)/ratio, (right-HEAD_RX)/ratio, 
        (bottom+HEAD_RY)/ratio, (top  +HEAD_RY)/ratio
    )
    nearL, farL = HEAD_LZ/ratio, 10000
    nearR, farR = HEAD_RZ/ratio, 10000
    shifLX, siftLY, siftLZ = HEAD_LX, HEAD_LY, -HEAD_LZ
    shifRX, siftRY, siftRZ = HEAD_RX, HEAD_RY, -HEAD_RZ


    viewL  = pyrr.matrix44.create_from_translation(
        pyrr.Vector3([-shifLX,siftLY,siftLZ]))
    viewR  = pyrr.matrix44.create_from_translation(
        pyrr.Vector3([-shifRX,siftRY,siftRZ]))

    projection1 = pyrr.matrix44.create_perspective_projection_from_bounds(
        leftL, rightL, bottomL, topL, nearL, farL )
    projection2 = pyrr.matrix44.create_perspective_projection_from_bounds(
        leftR, rightR, bottomR, topR, nearR, farR )


    return ( viewL, viewR, projection1, projection2 )
def view_wwww():

    global adfadf,monitor_width, monitor_height, scale, ratio

    #HEAD_LX, HEAD_LY, HEAD_LZ, HEAD_RX, HEAD_RY, HEAD_RZ  = -0, 0, 1500, 0, 0, 1500
    HEAD_LX, HEAD_LY, HEAD_LZ = adfadf[0],adfadf[1],adfadf[2]
    HEAD_RX, HEAD_RY, HEAD_RZ = adfadf[3],adfadf[4],adfadf[5]

    HEAD_LX, HEAD_LY, HEAD_LZ = HEAD_LX/scale, HEAD_LY/scale, HEAD_LZ/scale
    HEAD_RX, HEAD_RY, HEAD_RZ = HEAD_RX/scale, HEAD_RY/scale, HEAD_RZ/scale
    left, right, bottom, top = (
        -monitor_width /scale, +monitor_width /scale, 
        -monitor_height/scale, +monitor_height/scale 
    )
    leftL, rightL, bottomL, topL = (
        (left  -HEAD_LX), (right-HEAD_LX), 
        (bottom+HEAD_LY), (top  +HEAD_LY)
    )
    leftR, rightR, bottomR, topR = (
        (left  -HEAD_RX), (right-HEAD_RX), 
        (bottom+HEAD_RY), (top  +HEAD_RY)
    )
    nearL, farL = HEAD_LZ, 10000
    nearR, farR = HEAD_RZ, 10000
    shifLX, siftLY, siftLZ = HEAD_LX, HEAD_LY, -HEAD_LZ
    shifRX, siftRY, siftRZ = HEAD_RX, HEAD_RY, -HEAD_RZ



    projectionOrtho =  pyrr.matrix44.create_orthogonal_projection_matrix(
        leftR, rightR, bottomR, topR, nearR, farR)
    viewOrtho  = pyrr.matrix44.create_from_translation(pyrr.Vector3([0,0,siftLZ]))
    rotation_mat = pyrr.Matrix44.from_x_rotation( 0 )

    return (projectionOrtho,viewOrtho,rotation_mat)

def refrash_VAO():
    d=1
def create_VAO(datass):

    # OBJECT DRAW

    VAO = glGenVertexArrays(len(datass)+1)
    BO0 = glGenBuffers(len(datass)+1)
    BO1 = glGenBuffers(len(datass)+1)
    BO2 = glGenBuffers(len(datass)+1)

    draw_edge_len = []
    
    for zzzz in range(0, len(datass)):

        vertex  = numpy.array(datass[zzzz][0], dtype = numpy.float32)
        indices = numpy.array(datass[zzzz][1], dtype = numpy. uint32)
        normals = numpy.array(datass[zzzz][2], dtype = numpy.float32)

        draw_edge_len.append(len(indices))

        # cube VAO
        glBindVertexArray(VAO[zzzz])

        # cube Vertex Buffer Object
        glBindBuffer(GL_ARRAY_BUFFER, BO0[zzzz])
        glBufferData(GL_ARRAY_BUFFER, vertex.itemsize * len( vertex),  vertex, GL_STATIC_DRAW)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, BO1[zzzz])
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.itemsize * len(indices), indices, GL_STATIC_DRAW)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, vertex.itemsize * 3, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)

        ## cube normals Buffer Object
        glBindBuffer(GL_ARRAY_BUFFER, BO2[zzzz])
        glBufferData(GL_ARRAY_BUFFER, normals.itemsize * len(normals), normals, GL_STATIC_DRAW)
        glVertexAttribPointer(3, 3, GL_FLOAT, GL_FALSE, normals.itemsize * 3, ctypes.c_void_p(0))
        glEnableVertexAttribArray(3)


    return VAO, draw_edge_len
def create_MARKER():
    
    # OBJECT DRAW

    VAO = glGenVertexArrays(3)

    global adfadf,monitor_width, monitor_height, scale, ratio


    # UI DRAW

    #vertices = [-50/scale, -50/scale, -0.001, 0.0, 0.0, 0.0,
    #             50/scale, -50/scale, -0.001, 0.0, 0.0, 0.0,
    #            -50/scale,  50/scale, -0.001, 0.0, 0.0, 0.0,
    #             50/scale,  50/scale, -0.001, 0.0, 0.0, 0.0]

    vertices = [(-monitor_width      )/scale, (-monitor_height      )/scale, 0.0, 0.0, 1.0, 0.0, 
                (-monitor_width +  50)/scale, (-monitor_height      )/scale, 0.0, 0.0, 1.0, 0.0, 
                (-monitor_width      )/scale, (-monitor_height +  50)/scale, 0.0, 0.0, 1.0, 0.0,
                (-monitor_width +  50)/scale, (-monitor_height +  50)/scale, 0.0, 0.0, 1.0, 0.0]
    vertices = numpy.array(vertices, dtype=numpy.float32)
    glBindVertexArray(VAO[2])
    glBindBuffer(GL_ARRAY_BUFFER, glGenBuffers(1))
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
    glEnableVertexAttribArray(0)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(0))
    glEnableVertexAttribArray(1)
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12))

    vertices = [(-monitor_width +  50)/scale, (-monitor_height      )/scale, 0.0, 1.0, 0.0, 0.0, 
                (-monitor_width + 100)/scale, (-monitor_height      )/scale, 0.0, 1.0, 0.0, 0.0,
                (-monitor_width +  50)/scale, (-monitor_height +  50)/scale, 0.0, 1.0, 0.0, 0.0,
                (-monitor_width + 100)/scale, (-monitor_height +  50)/scale, 0.0, 1.0, 0.0, 0.0 ]
    vertices = numpy.array(vertices, dtype=numpy.float32)
    glBindVertexArray(VAO[1])
    glBindBuffer(GL_ARRAY_BUFFER, glGenBuffers(1))
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
    glEnableVertexAttribArray(0)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(0))
    glEnableVertexAttribArray(1)
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12))

    # background

    vertices = [(-monitor_width      )/scale, (-monitor_height      )/scale, -0.001, 0.0, 0.0, 0.0,
                (-monitor_width + 100)/scale, (-monitor_height      )/scale, -0.001, 0.0, 0.0, 0.0,
                (-monitor_width      )/scale, (-monitor_height +  50)/scale, -0.001, 0.0, 0.0, 0.0,
                (-monitor_width + 100)/scale, (-monitor_height +  50)/scale, -0.001, 0.0, 0.0, 0.0]
    vertices = numpy.array(vertices, dtype=numpy.float32)
    glBindVertexArray(VAO[0])
    glBindBuffer(GL_ARRAY_BUFFER, glGenBuffers(1))
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
    glEnableVertexAttribArray(0)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(0))
    glEnableVertexAttribArray(1)
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12))
    return VAO
def create_TEXTURE():
    textureID = glGenTextures(1)
    glBindTexture(GL_TEXTURE_CUBE_MAP, textureID)
    # load image
    #sfdaf= [ "right.jpg", "left.jpg", "top.jpg", "bottom.jpg", "front.jpg", "back.jpg" ]
    sfdaf= [ "0.bmp","1.bmp","2.bmp","3.bmp","4.bmp","5.bmp" ]
    for i in range(0,6):
        image = Image.open("texture/skybox/"+str(sfdaf[i]))
        img_data = numpy.array(list(image.getdata()), numpy.uint8)
        print(img_data.shape)
        glTexImage2D(
            GL_TEXTURE_CUBE_MAP_POSITIVE_X + i,
            0, GL_RGB, image.width, image.width,
            0, GL_RGB, GL_UNSIGNED_BYTE, img_data
        )
    glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
    glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
    glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_R, GL_CLAMP_TO_EDGE)
    return textureID
def create_SKYBOX():
    vertices = numpy.array([        
        -1.0,  1.0, -1.0,
        -1.0, -1.0, -1.0,
         1.0, -1.0, -1.0,
         1.0, -1.0, -1.0,
         1.0,  1.0, -1.0,
        -1.0,  1.0, -1.0,

        -1.0, -1.0,  1.0,
        -1.0, -1.0, -1.0,
        -1.0,  1.0, -1.0,
        -1.0,  1.0, -1.0,
        -1.0,  1.0,  1.0,
        -1.0, -1.0,  1.0,

         1.0, -1.0, -1.0,
         1.0, -1.0,  1.0,
         1.0,  1.0,  1.0,
         1.0,  1.0,  1.0,
         1.0,  1.0, -1.0,
         1.0, -1.0, -1.0,

        -1.0, -1.0,  1.0,
        -1.0,  1.0,  1.0,
         1.0,  1.0,  1.0,
         1.0,  1.0,  1.0,
         1.0, -1.0,  1.0,
        -1.0, -1.0,  1.0,

        -1.0,  1.0, -1.0,
         1.0,  1.0, -1.0,
         1.0,  1.0,  1.0,
         1.0,  1.0,  1.0,
        -1.0,  1.0,  1.0,
        -1.0,  1.0, -1.0,

        -1.0, -1.0, -1.0,
        -1.0, -1.0,  1.0,
         1.0, -1.0, -1.0,
         1.0, -1.0, -1.0,
        -1.0, -1.0,  1.0,
         1.0, -1.0,  1.0
    ], dtype= numpy.float32)*1000
    # skybox VAO
    skyboxVAO = glGenVertexArrays(1)
    skyboxVBO = glGenBuffers(1)
    glBindVertexArray(skyboxVAO)
    glBindBuffer(GL_ARRAY_BUFFER, skyboxVBO)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
    glEnableVertexAttribArray(10)
    glVertexAttribPointer(10, 3, GL_FLOAT, GL_FALSE, vertices.itemsize * 3, ctypes.c_void_p(0))
    return skyboxVAO
        
def main():


    global object_datas, VAO, draw_edge_len


    udp_client.init()


    ###################################################################
    # 데이터 불러들이기
    ###################################################################
    object_datas = mmap_read()
    #import index
    #object_datas = index.mmap_read_1()


    ###################################################################
    # glfw 설정
    ###################################################################
    # initialize glfw
    if not glfw.init():
        return

    window = glfw.create_window(
        monitor_width, monitor_height, "My OpenGL window", None, None)

    if not window:
        glfw.terminate()
        return

    glfw.set_window_size_callback(window, window_resize)
    # set the mouse position callback
    #glfw.set_cursor_pos_callback(window, mouse_look_clb)
    # set the keyboard input callback
    glfw.set_key_callback(window, key_input_clb)
    # capture the mouse cursor
    #glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_DISABLED)
    # make the context current
    glfw.make_context_current(window)
    # v-sync
    glfw.swap_interval(1)
    #monitor_size = glfw.get_video_modes(glfw.get_primary_monitor())
    #monitor_size = glfw.get_video_modes(glfw.get_primary_monitor())
    #
    #print(glfw.get_monitor_physical_size(glfw.get_primary_monitor()))
    #for akfad in monitor_size:
    print(glfw.get_window_size(window))



    ###################################################################
    # 셰이더 컴파일
    ###################################################################
    shader = shaderLoader.compile_shader(
        "shader_code/video_18_vert.vs", 
        "shader_code/test.gs", 
        "shader_code/video_18_frag.fs"
    )


    ###################################################################
    # 오브젝트 GPU에 전달
    ###################################################################
    VAO, draw_edge_len = create_VAO(object_datas[2])
    VAO_marker         = create_MARKER()
    skyboxVAO          = create_SKYBOX()
    cubemapTexture     = create_TEXTURE()
        

    ###################################################################
    # 쉐이더 사용
    ###################################################################
    glUseProgram(shader)


    ###################################################################
    # OPENGL 설정
    ###################################################################
    glClearColor(1,0,1,1)
    ###############################
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LEQUAL)
    ###############################
    #glEnable(GL_TEXTURE_CUBE_MAP)
    #glEnable(GL_MULTISAMPLE);  
    #glEnable(GL_BLEND)
    ###############################
    glEnable(GL_FRAMEBUFFER_SRGB); 
    ###############################
    #glEnable(GL_CULL_FACE) 
    #glCullFace(GL_FRONT)
    #glFrontFace(GL_CW)
    ###############################
    #glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    #glShadeModel(GL_FLAT)


    ###################################################################
    # OPENGL 설정
    ###################################################################
    selector = glGetUniformLocation(shader, "selector")

    (viewL, viewR, projection1, projection2) = view_zeze()
    (projectionOrtho,viewOrtho,rotation_mat) = view_wwww()

    view_loc           = glGetUniformLocation(shader, "view")
    light_loc          = glGetUniformLocation(shader, "light")
    proj_loc           = glGetUniformLocation(shader, "projection")
    model_loc          = glGetUniformLocation(shader, "model")
    transformLoc       = glGetUniformLocation(shader, "transform")
    ortho              = glGetUniformLocation(shader, "ortho")
    orthoView          = glGetUniformLocation(shader, "orthoView")
    
    light_ambient      = glGetUniformLocation(shader, "light.ambient")
    light_diffuse      = glGetUniformLocation(shader, "light.diffuse")
    light_specular     = glGetUniformLocation(shader, "light.specular")
    light_position     = glGetUniformLocation(shader, "light.position")
    material_ambient   = glGetUniformLocation(shader, "material.ambient")
    material_diffuse   = glGetUniformLocation(shader, "material.diffuse")
    material_specular  = glGetUniformLocation(shader, "material.specular")
    material_shininess = glGetUniformLocation(shader, "material.shininess")

    glUniform3fv(light_ambient     , 1, pyrr.Vector3([   1.0,   1.0,   1.0]))
    glUniform3fv(light_diffuse     , 1, pyrr.Vector3([   1.0,   1.0,   1.0]))
    glUniform3fv(light_specular    , 1, pyrr.Vector3([   1.0,   1.0,   1.0]))
    glUniform3fv(light_position    , 1, pyrr.Vector3([ 200.0, 200.0, 200.0]))
    glUniform3fv(material_ambient  , 1, pyrr.Vector3([   0.0,   0.5,   0.5]))
    glUniform3fv(material_diffuse  , 1, pyrr.Vector3([   1.0,   1.0,   1.0]))
    glUniform3fv(material_specular , 1, pyrr.Vector3([   1.0,   1.0,   0.0]))
    glUniform1i (material_shininess, 64 )

    glUniformMatrix4fv(ortho, 1, GL_FALSE, projectionOrtho)
    glUniformMatrix4fv(orthoView, 1, GL_FALSE, viewOrtho)
    
    currentFrame = glfw.get_time()
    lastFrame = currentFrame; 

    # 스카이큐브
    projection = pyrr.matrix44.create_perspective_projection_matrix(160, 800/800, 0.1, 10000000000000)
    view = pyrr.matrix44.create_from_translation(pyrr.Vector3([0, 0, 0]))
    
    skybox   = glGetUniformLocation(shader, "skybox") 
    view_loc = glGetUniformLocation(shader, "view")
    proj_loc = glGetUniformLocation(shader, "projection")
    
    glUniformMatrix4fv(view_loc, 1, GL_FALSE, view)
    glUniformMatrix4fv(proj_loc, 1, GL_FALSE, projection)
    glUniform1i(skybox, 0); 

    def sky():
        glUniform1i(selector,2)
        glBindVertexArray(skyboxVAO)
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_CUBE_MAP, cubemapTexture)
        glDrawArrays(GL_TRIANGLES, 0, 36)
        glBindVertexArray(0)
    
    while not glfw.window_should_close(window):

        glfw.poll_events()

        asasasasa = udp_client.read()
        #print(asasasasa)

        adfadsf[0] = (asasasasa[3]*100)
        adfadsf[3] = (asasasasa[3]*100)
        adfadsf[1] =-(asasasasa[4]*100)
        adfadsf[4] =-(asasasasa[4]*100)
        adfadsf[2] = (asasasasa[5]*100)
        adfadsf[5] = (asasasasa[5]*100)

        global gui_ambient , gui_diffuse , gui_specular, gui_position
        glUniform3fv(light_ambient , 1, gui_ambient  )
        glUniform3fv(light_diffuse , 1, gui_diffuse  )
        glUniform3fv(light_specular, 1, gui_specular )
        glUniform3fv(light_position, 1, gui_position )

        currentFrame = glfw.get_time()
        deltaTime = currentFrame - lastFrame

        do_movement()
        do_rotation()

        ( viewL, viewR, projection1, projection2 ) = view_zeze()

        #model = cam.get_view_matrix()
        model = fig.get_figure_matrix()

        glUniformMatrix4fv(transformLoc, 1, GL_FALSE, rotation_mat)
        glUniformMatrix4fv(   light_loc, 1, GL_FALSE, model)
        glUniformMatrix4fv(   model_loc, 1, GL_FALSE, model)

        ###################################################################
        # 출력
        ###################################################################

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glUniform1i(selector,1)
        for asdfad in range(0,len(draw_edge_len)):
            glBindVertexArray(VAO[asdfad])
            glUniformMatrix4fv(view_loc, 1, GL_FALSE, viewL)
            glUniformMatrix4fv(proj_loc, 1, GL_FALSE, projection1)
            glDrawElements(GL_TRIANGLES, draw_edge_len[asdfad], GL_UNSIGNED_INT, None)
        glUniform1i(selector,0)
        glBindVertexArray(VAO_marker[2])
        glDrawArrays(GL_TRIANGLE_STRIP, 0, 4)
        glBindVertexArray(VAO_marker[0])
        glDrawArrays(GL_TRIANGLE_STRIP, 0, 4)
        sky()
        glfw.swap_buffers(window)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glUniform1i(selector,1)
        for asdfad in range(0,len(draw_edge_len)):
            glBindVertexArray(VAO[asdfad])
            glUniformMatrix4fv(view_loc, 1, GL_FALSE, viewR)
            glUniformMatrix4fv(proj_loc, 1, GL_FALSE, projection2)
            glDrawElements(GL_TRIANGLES, draw_edge_len[asdfad], GL_UNSIGNED_INT, None)
        glUniform1i(selector,0)
        glBindVertexArray(VAO_marker[1])
        glDrawArrays(GL_TRIANGLE_STRIP, 0, 4)
        glBindVertexArray(VAO_marker[0])
        glDrawArrays(GL_TRIANGLE_STRIP, 0, 4)
        sky()
        glfw.swap_buffers(window)

    glfw.terminate()

#main()