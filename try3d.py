# tutorial
# https://noobtuts.com/python/opengl-introduction
# the whole thing is very sensitive to variable type

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np

window = 0
width, height = 500, 500
t = 0.0 # just a timestamp to change things

# define the parameter of cubes
nCube = 10
cube_angles   = np.random.rand(nCube,1) * 360
cube_axes     = np.random.rand(nCube,3)
cube_position = 10*(np.random.rand(nCube,3) - 0.5)


def draw():
    global t
    glEnable(GL_DEPTH_TEST)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) # clear buffer (black screen now)
    glLoadIdentity() # reset position

    # define camera
    refresh(width,height)
    t += 0.01

    # draw cube
    glMatrixMode(GL_MODELVIEW)
    for i in range(nCube):
        glPushMatrix()

        glTranslated(cube_position[i,0], cube_position[i,1], cube_position[i,2]) # move
        glRotatef(cube_angles[i] + t*50, cube_axes[i,0], cube_axes[i,1], cube_axes[i,2]) # rotate
        draw_cube()
        glPopMatrix()


    glutSwapBuffers() # this is like Flip in PTB?


def draw_rect(x, y, z, rw, rh):
    glBegin(GL_QUADS) # tell OpenGL we want a rectangle
    glVertex3f(x, y, z) # define vertices in a counterclockwise order
    glVertex3f(x+rw, y, z)
    glVertex3f(x+rw, y+rh, z)
    glVertex3f(x, y+rh, z)
    glEnd()

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




# Updates the camera
def refresh(w, h):
    glViewport(0, 0, w, h) # map projected image ranging from -1 to 1 to the actual screen
    glMatrixMode(GL_PROJECTION) # tell open GL we are definying projction matrix
    glLoadIdentity()
    # Define a frustum for a perspective projection
    # Position of four edges of the near plane + Z-position of near and far
    # planes (camera is supposed to be at the origin)
    glFrustum(-1, 1, -1, 1, 2, 30.0)

    glMatrixMode(GL_MODELVIEW) # tell open GL we are definying modelview matrix
    glLoadIdentity()
    gluLookAt(20*np.cos(t), 0, 20*np.sin(t),  # where your eye is
              0,0,0,  # where you are looking at
              0.0, 1.0, 0.0)  # which way is up



glutInit()
glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)
glutInitWindowSize(width, height)
glutInitWindowPosition(0, 0)
win = glutCreateWindow(b"my window") # only takes char = byte data
glutDisplayFunc(draw) # setting a callback (this happens everytime the user interacts with the window)
glutIdleFunc(draw) # draw all the time
glutMainLoop()
