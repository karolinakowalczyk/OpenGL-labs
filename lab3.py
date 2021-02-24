#!/usr/bin/env python3
import sys
import math
from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *

from random import uniform
N = 50

vertexTab = [[[0 for k in range(3)] for j in range(N)] for i in range(N)]
uTab = []
vTab = []
colorTab = [[[0 for k in range(3)] for j in range(N)] for i in range(N)]

for i in range (0, N):
    for j in range (0, N):
        colorTab [i][j][0] = uniform(0.0, 1.0)
        colorTab [i][j][1] = uniform(0.0, 1.0)
        colorTab [i][j][2] = uniform(0.0, 1.0)
for j in range(N):
    colorTab[N-1][j][0] = colorTab[0][N-1-j][0]
    colorTab[N-1][j][1] = colorTab[0][N-1-j][1]
    colorTab[N-1][j][2] = colorTab[0][N-1-j][2]

for i in range(N):
    colorTab[i][N-1][0] = colorTab[N-1-i][0][0]
    colorTab[i][N-1][1] = colorTab[N-1-i][0][1]
    colorTab[i][N-1][2] = colorTab[N-1-i][0][2]
R = 1.0
r = 0.2

def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)

def shutdown():
    pass


def axes():
    glBegin(GL_LINES)

    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(-5.0, 0.0, 0.0)
    glVertex3f(5.0, 0.0, 0.0)

    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(0.0, -5.0, 0.0)
    glVertex3f(0.0, 5.0, 0.0)

    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(0.0, 0.0, -5.0)
    glVertex3f(0.0, 0.0, 5.0)

    glEnd()


def render(time):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    spin(time * 180 / 3.1415)
    axes()
    #draw_egg_points()
    #draw_egg_lines()
    draw_egg_triangles()
    #draw_egg_triangle_strips()
    #torus()
    
    glFlush()

def spin(angle):
    glRotatef(angle, 1.0, 0.0, 0.0)
    glRotatef(angle, 0.0, 1.0, 0.0)
    glRotatef(angle, 0.0, 0.0, 1.0)

# Funckja pomocnicza wyznaczająca parametry: u, v, x, y, z dla jajka.

def egg_parameters(): 
    for i in range (0, N):
        uTab.append(i/(N-1))
        vTab.append(i/(N-1))
    uTab.append(1.0)
    vTab.append(1.0)
    
    for row in range (0, N):
        for col in range(0, N):
            vertexTab[row][col][0] = (-90 * uTab[row] ** 5 + 225 * uTab[row] ** 4 - 270 * uTab[row] ** 3 + 180 * uTab[row] ** 2 - 45 * uTab[row]) * math.cos(math.pi * vTab[col])
            vertexTab[row][col][1] = (160 * uTab[row] ** 4 - 320 * uTab[row] ** 3 + 160 * uTab[row] ** 2) - 4
            vertexTab[row][col][2] = (-90 * uTab[row] ** 5 + 225 * uTab[row] ** 4 - 270 * uTab[row] ** 3 + 180 * uTab[row] ** 2 - 45 * uTab[row]) * math.sin(math.pi * vTab[col])

# Funckja pomocnicza wyznaczająca parametry: u, v, x, y, z dla torusa.

def torus_parameters():
    for i in range (0, N):
        uTab.append(i/(N-1))
        vTab.append(i/(N-1))
    uTab.append(1.0)
    vTab.append(1.0)
    
    for row in range (0, N):
        for col in range(0, N):
            vertexTab[row][col][0] = (R + r * math.cos(2 * math.pi * vTab[col])) * math.cos(2 * math.pi * uTab[row]) - 4
            vertexTab[row][col][1] = (R + r * math.cos(2 * math.pi * vTab[col])) * math.sin(2 * math.pi * uTab[row])
            vertexTab[row][col][2] = r * math.sin(2 * math.pi * vTab[col])

# Zadanie na 3.0.

def draw_egg_points():
    egg_parameters()

    glBegin(GL_POINTS)
    glColor3f(0.0, 1.0, 0.0)
    for i in range(N):
        for j in range(N):
            glVertex3fv(vertexTab[i][j])
    glEnd()

# Zadanie na 3.5.
    
def draw_egg_lines():
    egg_parameters()

    for i in range(N):
        for j in range(N):
            glBegin(GL_LINES)
            glColor3f(1.0, 1.0, 1.0)
            glVertex3fv(vertexTab[i][j])
            glVertex3fv(vertexTab[(i + 1) % N][j])
            glEnd()

            glBegin(GL_LINES)
            glColor3f(1.0, 1.0, 1.0)
            glVertex3fv(vertexTab[i][j])
            glVertex3fv(vertexTab[i][(j+1) % N])
            glEnd()

# Zadanie na 4.0.  
          
def draw_egg_triangles():
    egg_parameters()

    for i in range(0, N):
        for j in range(0, N):
            glBegin(GL_TRIANGLES)
    
            glColor3fv(colorTab[i][j])
            glVertex3fv(vertexTab[i][j])
            glColor3fv(colorTab[(i+1)%N][j])
            glVertex3fv(vertexTab[(i+1)%N][j])
            glColor3fv(colorTab[i][(j+1)%N])
            glVertex3fv(vertexTab[i][(j+1)%N])

            glEnd()
            glBegin(GL_TRIANGLES)

            glColor3fv(colorTab[(i+1)%N][(j+1)%N])
            glVertex3fv(vertexTab[(i+1)%N][(j+1)%N])
            glColor3fv(colorTab[(i+1)%N][j])
            glVertex3fv(vertexTab[(i+1)%N][j])
            glColor3fv(colorTab[i][(j+1)%N])
            glVertex3fv(vertexTab[i][(j+1)%N])
            glEnd()
    
# Zadanie na 4.5.

def draw_egg_triangle_strips():
    egg_parameters()
    
    for i in range(N):
        glBegin(GL_TRIANGLE_STRIP)
        for j in range(N):
            glColor3fv(colorTab[i][j])
            glVertex3fv(vertexTab[i][j])
            glColor3fv(colorTab[(i + 1) % N][j])
            glVertex3fv(vertexTab[(i + 1) % N][j])
        glEnd()

# Zadanie na 5.0.

def torus():
    displ = 0.0
    torus_parameters()
    for k in range (0, 8):

        for i in range(0, N):
            for j in range(0, N):
                glBegin(GL_TRIANGLES)
        
                glColor3fv(colorTab[i][j])
                glVertex3f(vertexTab[i][j][0]+displ, vertexTab[i][j][1],vertexTab[i][j][2])
                glColor3fv(colorTab[(i+1)%N][j])
                glVertex3f(vertexTab[(i+1)%N][j][0]+displ, vertexTab[(i+1)%N][j][1], vertexTab[(i+1)%N][j][2])
                glColor3fv(colorTab[i][(j+1)%N])
                glVertex3f(vertexTab[i][(j+1)%N][0]+displ, vertexTab[i][(j+1)%N][1], vertexTab[i][(j+1)%N][2])

                glEnd()
                glBegin(GL_TRIANGLES)

                glColor3fv(colorTab[(i+1)%N][(j+1)%N])
                glVertex3f(vertexTab[(i+1)%N][(j+1)%N][0]+displ, vertexTab[(i+1)%N][(j+1)%N][1], vertexTab[(i+1)%N][(j+1)%N][2])
                glColor3fv(colorTab[(i+1)%N][j])
                glVertex3f(vertexTab[(i+1)%N][j][0]+displ, vertexTab[(i+1)%N][j][1], vertexTab[(i+1)%N][j][2])
                glColor3fv(colorTab[i][(j+1)%N])
                glVertex3f(vertexTab[i][(j+1)%N][0]+displ, vertexTab[i][(j+1)%N][1], vertexTab[i][(j+1)%N][2])
                glEnd()
        displ +=1.0
  

def update_viewport(window, width, height):
    if width == 0:
        width = 1
    if height == 0:
        height = 1
    aspect_ratio = width / height

    glMatrixMode(GL_PROJECTION)
    glViewport(0, 0, width, height)
    glLoadIdentity()

    if width <= height:
        glOrtho(-7.5, 7.5, -7.5 / aspect_ratio, 7.5 / aspect_ratio, 7.5, -7.5)
    else:
        glOrtho(-7.5 * aspect_ratio, 7.5 * aspect_ratio, -7.5, 7.5, 7.5, -7.5)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def main():
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(400, 400, __file__, None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)

    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
    glfwSwapInterval(1)

    startup()
    while not glfwWindowShouldClose(window):
        render(glfwGetTime())
        glfwSwapBuffers(window)
        glfwPollEvents()
    shutdown()

    glfwTerminate()


if __name__ == '__main__':
    main()
