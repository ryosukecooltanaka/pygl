# tutorial
# https://noobtuts.com/python/opengl-introduction

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

window = 0
w, h = 500, 500

def draw():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) # clear buffer (black screen now)
    glLoadIdentity() # reset position
    # 2d mode
    refresh2d(w,h)
    # draw rectangle
    glColor3f(0.0, 0.0, 0.7)
    draw_rect(30,30,50,50)

    glColor3f(0.7, 0.0, 0.7)
    draw_rect(100,30,50,50)

    glColor3f(0.0, 0.7, 0.7)
    draw_rect(170,30,50,50)

    glutSwapBuffers() # this is like Flip in PTB?

def draw_rect(x, y, w, h):
    glBegin(GL_QUADS) # tell OpenGL we want a rectangle
    glVertex2f(x, y) # define vertices in a counterclockwise order
    glVertex2f(x+w, y)
    glVertex2f(x+w, y+h)
    glVertex2f(x, y+h)
    glEnd()

def refresh2d(w, h): # setting a camera to look at things as if 2d
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, w, 0.0, h, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()



glutInit()
glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)
glutInitWindowSize(w, h)
glutInitWindowPosition(0, 0)
win = glutCreateWindow(b"my window") # only takes char = byte data
glutDisplayFunc(draw) # setting a callback (this happens everytime the user interacts with the window)
glutIdleFunc(draw) # draw all the time
glutMainLoop()
