from OpenGL.GL import *
import OpenGL.GL.shaders

def load_shader(shader_file):
    shader_source = ""
    with open(shader_file) as f:
        shader_source = f.read()
    f.close()
    return str.encode(shader_source)

def compile_shader(vs, gs, fs):
    vert_shader = load_shader(vs)
    geom_shader = load_shader(gs)
    frag_shader = load_shader(fs)

    vert = OpenGL.GL.shaders.compileShader(vert_shader, GL_VERTEX_SHADER  )
    freg = OpenGL.GL.shaders.compileShader(frag_shader, GL_FRAGMENT_SHADER)
    geom = OpenGL.GL.shaders.compileShader(geom_shader, GL_GEOMETRY_SHADER)

    ID = glCreateProgram()
    glAttachShader(ID, vert)
    glAttachShader(ID, freg)
    #glAttachShader(ID, geom)
    
    glLinkProgram(ID)
    
    return ID