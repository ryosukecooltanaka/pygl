# tutorial
# https://noobtuts.com/python/opengl-introduction
# the whole thing is very sensitive to variable type

# import stuff
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np

# parameters
width, height = 500, 500 # window size
t = 0.0 # just a timestamp to change things

# define the parameter of cubes
nCube = 10
cube_angles   = np.random.rand(nCube,1) * 360
cube_axes     = np.random.rand(nCube,3)
cube_position = 10*(np.random.rand(nCube,3) - 0.5)

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
    refresh(width,height)

    # update the timestamp to move things
    t += 0.01

    # draw cube
    # make sure we are opearting on the modelview matrix
    # this already has the camera matrix defined in refresh()
    glMatrixMode(GL_MODELVIEW)
    for i in range(nCube):
        # save the current matrix
        glPushMatrix()
        # move and rotate the coordinate for each cube
        # translation comes first so the thing rotates on the spot
        glTranslated(cube_position[i,0], cube_position[i,1], cube_position[i,2]) # move
        glRotatef(cube_angles[i] + t*50, cube_axes[i,0], cube_axes[i,1], cube_axes[i,2]) # rotate
        draw_cube()
        # bring back the original coordinate before the translation and rotation
        glPopMatrix()
    glutSwapBuffers() # this is like Flip in PTB?

# Draw a cube with different side colors and the edge length = 2
# centered at the origin
def draw_cube():
    glBegin(GL_QUADS) # I am drawing a bunch of rectangles

    glColor3f(1,0,1)
    glVertex3f(1,-1,1)
    glVertex3f(1,-1,-1)
    glVertex3f(1,1,-1)
    glVertex3f(1,1,1)

    glColor3f(0,1,1)
    glVertex3f(-1,1,1)
    glVertex3f(1,1,1)
    glVertex3f(1,1,-1)
    glVertex3f(-1,1,-1)

    glColor3f(1,1,0)
    glVertex3f(1,-1,-1)
    glVertex3f(-1,-1,-1)
    glVertex3f(-1,1,-1)
    glVertex3f(1,1,-1)

    glColor3f(1,0,0)
    glVertex3f(-1,-1,-1)
    glVertex3f(-1,-1,1)
    glVertex3f(-1,1,1)
    glVertex3f(-1,1,-1)

    glColor3f(0,1,0)
    glVertex3f(-1,-1,-1)
    glVertex3f(1,-1,-1)
    glVertex3f(1,-1,1)
    glVertex3f(-1,-1,1)

    glColor3f(0,0,1)
    glVertex3f(-1,-1,1)
    glVertex3f(-1,1,1)
    glVertex3f(1,1,1)
    glVertex3f(1,-1,1)

    glEnd()

# This function defines the camera and projection
def refresh(w, h):
    # define the viewport transform
    # this maps NDC cube ranging from [-1,1] to actual screen coordinate
    # nothing interesting happens here
    glViewport(0, 0, w, h)


    # define the projection (use the perspective projection)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity() # intialize by loading identity
    # Define a frustum for a perspective projection
    # Position of four edges of the near plane + Z-position of near and far
    # planes (camera is supposed to be at the origin)
    # numbers are in the model coordinate (but after all rotations etc)
    glFrustum(-1, 1, -1, 1, 2, 30.0)

    # define the camera
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity() # intialize by loading identity
    gluLookAt(20*np.cos(t), 0, 20*np.sin(t),  # where your eye is
              0,0,0,                          # where you are looking at
              0.0, 1.0, 0.0)                  # which way is up



glutInit() # initialize opengl
glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH) # define the display mode
glutInitWindowSize(width, height) # set the window size
glutInitWindowPosition(0, 0) # set the window position
win = glutCreateWindow(b"my window") # create a window with a title (only takes char = byte data hence b)
glutDisplayFunc(draw) # setting a callback (this happens everytime the user interacts with the window)
glutIdleFunc(draw) # draw all the time
glutMainLoop()
