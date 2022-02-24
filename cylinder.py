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

# main callback function
def draw():
    # access time stamp variable t as a global variable
    # otherwise any change you apply to t will not be propagated outside the
    # function (you are operating on the local copy)
    global t

    # enable depth rendering
    glEnable(GL_DEPTH_TEST)

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
    glPushMatrix()
    glRotate(t, 0, 1, 0)
    glTranslate(0, 0, -c_height/2)
    glColor3f(0, 1, 0.5)
    draw_cylinder()
    glPopMatrix()

    glutSwapBuffers() # this is like Flip in PTB?

def draw_cylinder():
    C = gluNewQuadric()
    gluCylinder(C, c_radius, c_radius, c_height, 100, 1)

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
    glFrustum(-1, 1, -1, 1, 1, 30.0)

    # define the camera
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity() # intialize by loading identity
    gluLookAt(0,0,5,  # where your eye is
              0,0,0,  # where you are looking at
              0,1,0)  # which way is up


glutInit() # initialize opengl (create a context)
glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH) # define the display mode
glutInitWindowSize(width, height) # set the window size
glutInitWindowPosition(0, 0) # set the window position
win = glutCreateWindow(b"my window") # create a window with a title (only takes char = byte data hence b)
glutDisplayFunc(draw) # setting a callback (this happens everytime the user interacts with the window)
glutIdleFunc(draw) # draw all the time
glutMainLoop()
