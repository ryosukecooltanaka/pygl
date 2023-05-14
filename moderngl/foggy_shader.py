# Designing custom shaders to simulate fog effect (i.e. color depends on
# the distance)

import numpy as np
from matplotlib import pyplot as plt
import moderngl
from PIL import Image

# First, creat a stand alone OpenGL context
ctx = moderngl.create_standalone_context()

# Next, define shader
# vertex shader
v_shader = '''
    #version 410

    in vec3 vert;

    uniform float z_near;
    uniform float z_far;
    uniform float fovx;
    uniform float fovy;

    uniform vec3 center;
    uniform vec3 eye;
    uniform vec3 up;

    out float hoge;

    mat4 perspective() {
        float zmul = (-2.0 * z_near * z_far) / (z_far - z_near);
        float xmul = 1.0 / tan(fovx);
        float ymul = 1.0 / tan(fovy);
        return mat4(
            xmul, 0.0, 0.0, 0.0,
            0.0, ymul, 0.0, 0.0,
            0.0, 0.0, -1.0, -1.0,
            0.0, 0.0, zmul, 0.0
        );
    }
    mat4 lookat() {
        vec3 forward = normalize(center - eye);
        vec3 side = normalize(cross(forward, up));
        vec3 upward = cross(side, forward);
        return mat4(
            side.x, upward.x, -forward.x, 0,
            side.y, upward.y, -forward.y, 0,
            side.z, upward.z, -forward.z, 0,
            -dot(eye, side), -dot(eye, upward), dot(eye, forward), 1
        );
    }



    void main() {
        gl_Position = perspective() * lookat() * vec4(vert, 1.0);
        hoge = vert.z;
    }
'''
# fragement shader
f_shader = '''
    #version 410

    in float hoge;
    out vec4 color;

    void main() {
        color = vec4(0.3, 0.0, 1.0, 1 - hoge/10.0);
    }
'''

# Create shader program object
prog = ctx.program(vertex_shader=v_shader, fragment_shader=f_shader)

# assign projection parameters
# Note: cropping??
prog['z_near'].value = 5.0
prog['z_far'].value  = 100.0

# FOV is half-angle
prog['fovx'].value   = np.pi / 4.0 # 45 deg x 2
prog['fovy'].value   = np.pi / 4.0 # 45 deg x 2

prog['center'].value = (0.0, 0.0, 1.0)
prog['eye'].value    = (0.0, 0.0, 0.0)
prog['up'].value     = (0.0, 1.0, 0.0)

# allow depth and alpha blending
ctx.enable(moderngl.DEPTH_TEST | moderngl.BLEND)

# Prepare frame buffer with size 512 x 512
fbo = ctx.simple_framebuffer((512, 512))
fbo.use()

# model preparation

vbo = []  # array for buffers containing vertices
vao = []  # array for VertexArray objects, which is going to be rendered

# I will make a lot of triangles
triangle = np.empty((3,3))
triangle[0,:] = [-1.0, -1.0, 0.0]
triangle[1,:] = [+1.0, -1.0, 0.0]
triangle[2,:] = [0.0, 0.0, 0.0]

# copy with z offset
for i in range(30):
    temp = triangle + np.tile([0, -3, i],(3,1))
    vbo.append(ctx.buffer(temp.astype('f4').tobytes()))
    vao.append(ctx.vertex_array(prog, vbo[i], 'vert'))

# render
fbo.clear(1.0, 1.0, 1.0, 1.0)

for this_vao in vao:
    this_vao.render(moderngl.TRIANGLES)


# visualize
plt.figure()
plt.imshow(np.asarray(Image.frombytes('RGB', fbo.size, fbo.read(), 'raw', 'RGB', 0, -1)))
plt.show()
