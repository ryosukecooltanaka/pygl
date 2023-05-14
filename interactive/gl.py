import moderngl
import numpy as np
from PIL import Image

class cameraState():
    """
    The class to store camera state
    """
    def __init__(self):
        self.eye = [1, 0, 0]
        self.center = [0, 0, 0]
        self.up = [0, 1, 0]

class glWorld():
    """
    The class to manage the OpenGL context and buffers.
    """

    def __init__(self, frameHeight, frameWidth):
        # Create an opengl context
        self.ctx = moderngl.create_standalone_context()
        self.ctx.enable(moderngl.DEPTH_TEST)

        # frame buffer (need to receive)
        self.frameHeight = frameHeight
        self.frameWidth = frameWidth
        self.fbo = self.ctx.simple_framebuffer((frameWidth, frameHeight))
        self.fbo.use()

        # prepare attributes to store camera state
        self.camera = cameraState()

        # load and store GLSL shader programs, pass necessary variables
        vshader_file = open('./shaders/vshader/vshader001.glsl')
        fshader_file = open('./shaders/fshader/fshader001.glsl')
        self.shader = self.ctx.program(
                                vertex_shader=vshader_file.read(),
                                fragment_shader=fshader_file.read()
                            )
        vshader_file.close()
        fshader_file.close()
        self.initShader()

        # prepare place to store objects (as a list)
        self.objects = []

    def initShader(self):
        # insert constants to the shader
        self.shader['z_near'].value = 1
        self.shader['z_far'].value = 300
        self.shader['fovx'].value = np.pi / 4.0
        self.shader['fovy'].value = np.pi / 4.0 * self.frameHeight / self.frameWidth
        self.shader['up'].value = (self.camera.up[0], self.camera.up[1], self.camera.up[2])

    def addObject(self, vert, timage):
        """
        Given vertices and a texture, create an object and assign it to this
        world.
        """
        self.objects.append(glObject(vert, timage, self))

    def renderFrame(self):
        """
        Render the frame.
        """
        # first, clear the frame buffer.
        self.fbo.clear(0,0,0.1)

        # Next, pass the current state of the camera to the shader
        self.shader['center'].value = (self.camera.center[0], self.camera.center[1], self.camera.center[2])
        self.shader['eye'].value = (self.camera.eye[0], self.camera.eye[1], self.camera.eye[2])

        # go through all the objects, and render them
        for i in range(len(self.objects)):
            self.objects[i].tex.use()
            self.shader['rotations'].value = (self.objects[i].pitch, self.objects[i].yaw, self.objects[i].roll)
            self.shader['translations'].value = (self.objects[i].x, self.objects[i].y, self.objects[i].z)
            self.objects[i].vao.render(moderngl.TRIANGLES)

        # get the buffer content, convert to ndarray and return
        img = np.asarray(Image.frombytes("RGB", self.fbo.size, self.fbo.read(), 'raw', 'RGB', 0, -1))

        return img



class glObject():
    """
    A class that holds a 3d object.

    ...

    Attributes
    ----------
    vert: ndarray
        5 column ndarray specifying x, y, z, u, v coordinates of the object.
    timage: ndarray
        texture to be mapped onto the object.
    id: int
    x: float
    y: float
    z: float
    yaw: float
    roll: float
    pitch: float
    vbo: moderngl.Buffer
    vao: moderngl.VertexArray
    tex: moderngl.Texture
    """

    def __init__(self, vert, timage, world):
        """
        Constructer for glObject.
        """
        self.vert = vert
        self.timage = timage
        self.x = 0
        self.y = 0
        self.z = 0
        self.yaw = 0
        self.roll = 0
        self.pitch = 0

        # prepare attributes to store opengl stuff
        self.vbo = []
        self.vao = []
        self.tex = []

        # assign the object to the buffer of the opengl context
        self.assignToContext(world)

    def assignToContext(self, world):
        """
        Assign the object to the world it belongs to.
        """
        self.vbo = world.ctx.buffer(self.vert.astype('f4').tobytes())
        self.vao = world.ctx.vertex_array(world.shader, self.vbo, 'xyz', 'uv')
        self.tex = world.ctx.texture((self.timage.shape[1], self.timage.shape[0]), 3, data=self.timage)
