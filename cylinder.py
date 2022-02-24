# replicate a cylinder with texture mapped similar to psycho5

# import stuff
# Note: GLUT/GLU are really outdated and depreciated
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np
from PIL import Image as Image

# parameters
width, height = 500, 500
c_radius = 1
c_height = 3
t = 0 # just a time stamp

# load Image
img = Image.open('./map.png')
img_data = np.array(list(img.getdata()), np.uint8)

outimg_list = []

# main callback function
def draw():
    # access time stamp variable t as a global variable
    # otherwise any change you apply to t will not be propagated outside the
    # function (you are operating on the local copy)
    global t, outimg_list

    # enable depth rendering + 2d texture mapping
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_TEXTURE_2D)

    # clear buffer (black screen now)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # load identity matrix
    glLoadIdentity()

    # define camera
    refresh()

    # update the timestamp to move things
    t += 1

    # draw the cylinder
    # make sure we are opearting on the modelview matrix
    # this already has the camera matrix defined in refresh()
    glMatrixMode(GL_MODELVIEW)
    # implement rotation of the world
    glPushMatrix()
    glRotate(90, 1, 0, 0)
    glRotate(-t, 0, 0, 1)

    # draw_cylinder()
    draw_sphere()

    glPopMatrix()

    glutSwapBuffers() # this is like Flip in PTB?
    if t%10==0 & t<360:
        temp = np.flipud(glReadPixels(0, 0, width, height, GL_RGB, GL_FLOAT))
        outimg_list.append(Image.fromarray((temp * 255).astype(np.uint8)))
        if t==350:
            outimg_list[0].save('out.gif', save_all=True, append_images=outimg_list[1:],duration=100,loop=0)


# function to draw a cylinder
def draw_cylinder():
    # move so that the cylinder is centered
    glMatrixMode(GL_MODELVIEW)
    glTranslate(0, 0, -c_height/2)

    C = gluNewQuadric()
    gluQuadricTexture(C, GLU_TRUE) # generate texture coordinate for C
    gluCylinder(C, c_radius, c_radius, c_height, 100, 1)



# or sphere
def draw_sphere():
    C = gluNewQuadric()
    # mapping to sphere happens inside? so need to flip the texture?
    gluQuadricOrientation(C, GLU_OUTSIDE)
    gluQuadricTexture(C, GLU_TRUE) # generate texture coordinate for C
    gluSphere(C, c_radius, 20, 20)


# This function defines the camera and projection
def refresh():
    # define the viewport transform
    # this maps NDC cube ranging from [-1,1] to actual screen coordinate
    # nothing interesting happens here
    glViewport(0, 0, width, height)

    # define the projection (use the perspective projection)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity() # intialize by loading identity
    # Define a frustum for a perspective projection
    # Position of four edges of the near plane + Z-position of near and far
    # planes (camera is supposed to be at the origin)
    # numbers are in the model coordinate (but after all rotations etc)
    glFrustum(-0.5, 0.5, -0.5, 0.5, 2, 30.0)

    # define the camera
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity() # intialize by loading identity
    gluLookAt(0,3,5,  # where your eye is
              0,0,0,  # where you are looking at
              0,1,0)  # which way is up


glutInit() # initialize opengl (create a context)
glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH) # define the display mode
glutInitWindowSize(width, height) # set the window size
glutInitWindowPosition(0, 0) # set the window position
win = glutCreateWindow(b"my window") # create a window with a title (only takes char = byte data hence b)

# prepare a texture
tid = glGenTextures(1)

# flip the texture coordinate otherwise it is inverted
glMatrixMode(GL_TEXTURE)
glTranslatef(0.5, 0.5, 0)
glRotate(180,0,1,0)
glTranslatef(-0.5, -0.5, 0)
glMatrixMode(GL_MODELVIEW)

# tell opengl to map the texture to verticies
glBindTexture(GL_TEXTURE_2D, tid)

# wrapping parameters
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
# Set texture filtering parameters
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR) # use nearlest when texture is smaller than object
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR) # use nearlest when texture is bigger than object

# associate texture Id to the image
glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, img.size[0], img.size[1], 0,
             GL_RGBA, GL_UNSIGNED_BYTE, img_data)



glutDisplayFunc(draw) # setting a callback (this happens everytime the user interacts with the window)
glutIdleFunc(draw) # draw all the time
glutMainLoop()
