import moderngl
import numpy as np
import imageio

from PIL import Image
import matplotlib.pyplot as plt

ctx = moderngl.create_standalone_context()

# vertex_shader receives vertex positions & colors, and convert it into
# the window coordinate (x [-1,1], y [-1,1])
# fragment_shader perform on each pixel and convert color
prog = ctx.program(
    vertex_shader='''
        #version 330

        in vec3 vert;
        in vec2 in_texcoord_0;

        out vec2 v_text;

        uniform float z_near;
        uniform float z_far;
        uniform float fovx;
        uniform float fovy;

        uniform vec3 center;
        uniform vec3 eye;
        uniform vec3 up;

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
            v_text = in_texcoord_0;
        }
    ''',
    fragment_shader='''
        #version 330

        uniform sampler2D Texture;

        in vec2 v_text;
        out vec4 color;

        void main() {
            color = vec4(texture(Texture, v_text).rgb, 1.0);
        }
    ''',
)

# Cylinder spec
n_sides = 100
c_h = 5 # height
c_r = 3 # radius

# screen spec
# for now assuming that the observer is centered at
# the center of the screen as well as the cylinder
# so the screen width determines the screen distance
s_h = 5
s_d = 3
gaze_direction = np.pi # in radian

# Projection spec
# this should be decided based on the screen spec


prog['z_near'].value = 0.1
prog['z_far'].value  = 100.0
# FOV is half-angle
prog['fovx'].value   = np.pi / 4.0 # fov x should be 90 deg always
prog['fovy'].value   = np.arctan(s_h/2.0/s_d)

prog['center'].value = (np.cos(gaze_direction), np.sin(gaze_direction), 0.0)
prog['eye'].value    = (0, 0, 0)
prog['up'].value     = (0, 0, 1)

#ctx.clear(1.0, 1.0, 1.0)
ctx.enable(moderngl.DEPTH_TEST | moderngl.BLEND)

# we need 6 points per side (2 triangles per side)
# 3 for x, y, z and 2 for u, v (in texture coordinate)
vertices = np.empty((6*n_sides, 5))

for i in range(n_sides):
    t_0 = 2.0 * np.pi * i / n_sides
    t_1 = 2.0 * np.pi * (i+1) / n_sides
    vertices[6*i, :]     = [c_r*np.cos(t_1), c_r*np.sin(t_1), -c_h/2, 1-(i+1)/n_sides, 1]
    vertices[6*i + 1, :] = [c_r*np.cos(t_0), c_r*np.sin(t_0), +c_h/2, 1-i/n_sides,     0]
    vertices[6*i + 2, :] = [c_r*np.cos(t_0), c_r*np.sin(t_0), -c_h/2, 1-i/n_sides,     1]
    vertices[6*i + 3, :] = [c_r*np.cos(t_1), c_r*np.sin(t_1), -c_h/2, 1-(i+1)/n_sides, 1]
    vertices[6*i + 4, :] = [c_r*np.cos(t_1), c_r*np.sin(t_1), +c_h/2, 1-(i+1)/n_sides, 0]
    vertices[6*i + 5, :] = [c_r*np.cos(t_0), c_r*np.sin(t_0), +c_h/2, 1-i/n_sides,     0]

vbo = ctx.buffer(vertices.astype('f4').tobytes())
vao = ctx.vertex_array(prog, vbo, 'vert','in_texcoord_0')

fbo = ctx.simple_framebuffer((512, 512))
fbo.use()

# load images to be used as a Texture
img = imageio.v3.imread('./map.jpeg').astype(np.uint8)
tex = ctx.texture((img.shape[1],img.shape[0]), img.shape[2], data=img)
tex.use()

print(ctx.version_code) 



for i in range(4):
    fbo.clear(0.0, 0.0, 0.0, 1.0)
    gaze_direction = i * np.pi / 2
    prog['center'].value = (np.cos(gaze_direction), np.sin(gaze_direction), 0.0)
    vao.render(moderngl.TRIANGLES)
    plt.subplot(2,2,i+1)
    plt.imshow(np.asarray(Image.frombytes('RGB', fbo.size, fbo.read(), 'raw', 'RGB', 0, -1)))
plt.show()
