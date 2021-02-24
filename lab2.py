#!/usr/bin/env python3
import sys
import random 
from math import *
from random import randint
from random import uniform


from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *

clr1 = uniform(0.0, 1.0)
clr2 = uniform(0.0, 1.0)
clr3 = uniform(0.0, 1.0)
clr4 = uniform(0.0, 1.0)
clr5 = uniform(0.0, 1.0)
clr6 = uniform(0.0, 1.0)
clr7 = uniform(0.0, 1.0)
clr8 = uniform(0.0, 1.0)
clr9 = uniform(0.0, 1.0)
clr10 = uniform(0.0, 1.0)
clr11 = uniform(0.0, 1.0)
clr12 = uniform(0.0, 1.0)

def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.5, 0.5, 0.5, 1.0)


def shutdown():
    pass

   
def render(time):
    #draw_tringle_v1()
    #draw_tringle_v2()
    #draw_rectangle(1, 5, 80, 50)
    #draw_rectangle_rand(0, 0, 50, 30, 0.2)
    #draw_rectangle_rand_dynamic(0, 0, 150, 150, 0.8)
    draw_sierpinski_carpet(0,  0, 200, 200, 3)
    #draw_sierpinski_tringle(-70, -70, 70, 5)

# Funkcja rysująca trójkąt równoboczny - wykorzystywana przy rysowaniu trójkąta sierpińskiego.

def draw_equilateral_tringle(x, y, a):
    glBegin(GL_TRIANGLES)
    glColor3f(1.0, 0.0, 0.0)
    glVertex2f(x, y)
    glColor3f(1.0, 0.0, 0.0)
    glVertex2f(x+a, y)
    glColor3f(1.0, 0.0, 0.0)
    glVertex2f(x+0.5*a, y+a)
    glEnd()

    glFlush()

# Zadanie na 5.0 - trójkąt sierpińskiego. 

def draw_sierpinski_tringle(x0, y0, a, n):

   x1 = x0 + a
   y1 = y0

   x2 = x0 + 0.5*a 
   y2 = y0 + a 
   
   if n>0:
        newX1 = (x0 + x2)/2
        newX2 = (x1 + x2)/2

        newA = newX2 - newX1
        draw_sierpinski_tringle(x0, y0, newA, n-1)
        draw_sierpinski_tringle(x2, y2, newA, n-1)
        draw_sierpinski_tringle(x1, y1, newA, n-1)
   else:
        draw_equilateral_tringle(x0, y0, a)    

# Zadanie na 4.5

def draw_sierpinski_carpet(x, y, a, b, n):

    newA = a/3
    newB = b/3
    
    draw_rectangle(x, y, newA, newB)

    newX = 0
    newY = 0

    if n>1:
        carpet = 0 
        for i in range (-3, 3):
            for j in range (-3,3):
                newX = i * (a/3) + x
                newY = j * (b/3) + y 
                carpet += draw_sierpinski_carpet(newX, newY, newA, newB, n-1)
        return 1 + carpet
    else:
        return 1
    
# Zadanie na 4.0 - tutaj ponownie nie byłam pewna, czy chodziło Panu o to, żeby wraz ze zmianą wielkości prostokąta zmieniał się też kolor (draw_rectangle_rand_dynamic)
# czy też, żeby kolor został wylosowany tylko raz (draw_rectangle_rand). 

def draw_rectangle_rand_dynamic(x, y, a, b, d):

    clr1 = uniform(0.0, 1.0)
    clr2 = uniform(0.0, 1.0)
    clr3 = uniform(0.0, 1.0)
    clr4 = uniform(0.0, 1.0)
    clr5 = uniform(0.0, 1.0)
    clr6 = uniform(0.0, 1.0)
    clr7 = uniform(0.0, 1.0)
    clr8 = uniform(0.0, 1.0)
    clr9 = uniform(0.0, 1.0)
    clr10 = uniform(0.0, 1.0)
    clr11 = uniform(0.0, 1.0)
    clr12 = uniform(0.0, 1.0)
  
    glClear(GL_COLOR_BUFFER_BIT)
    defor = uniform(1.0 - d, 1.0 + d)
    glBegin(GL_TRIANGLES)
    glColor3f(clr1, clr2, clr3)
    glVertex2f(x-0.5*(a*defor), y+0.5*(b*defor))
    glColor3f(clr4, clr5, clr6)
    glVertex2f(x+0.5*(a*defor), y+0.5*(b*defor))
    glColor3f(clr7, clr8, clr9)
    glVertex2f(x+0.5*(a*defor), y-0.5*(b*defor))
    glEnd()

    glBegin(GL_TRIANGLES)
    glColor3f(clr1, clr2, clr3)
    glVertex2f(x-0.5*(a*defor), y+0.5*(b*defor))
    glColor3f(clr10, clr11, clr12)
    glVertex2f(x-0.5*(a*defor), y-0.5*(b*defor))
    glColor3f(clr7, clr8, clr9)
    glVertex2f(x+0.5*(a*defor), y-0.5*(b*defor))
    glEnd()

    glFlush()

def draw_rectangle_rand(x, y, a, b, d):
  
    glClear(GL_COLOR_BUFFER_BIT)
    defor = uniform(1.0 - d, 1.0 + d)
    glBegin(GL_TRIANGLES)
    glColor3f(clr1, clr2, clr3)
    glVertex2f(x-0.5*(a*defor), y+0.5*(b*defor))
    glColor3f(clr4, clr5, clr6)
    glVertex2f(x+0.5*(a*defor), y+0.5*(b*defor))
    glColor3f(clr7, clr8, clr9)
    glVertex2f(x+0.5*(a*defor), y-0.5*(b*defor))
    glEnd()

    glBegin(GL_TRIANGLES)
    glColor3f(clr1, clr2, clr3)
    glVertex2f(x-0.5*(a*defor), y+0.5*(b*defor))
    glColor3f(clr10, clr11, clr12)
    glVertex2f(x-0.5*(a*defor), y-0.5*(b*defor))
    glColor3f(clr7, clr8, clr9)
    glVertex2f(x+0.5*(a*defor), y-0.5*(b*defor))
    glEnd()

    glFlush()

# Zadanie na 3.5
# x, y - współrzędne środka prostokąta 
def draw_rectangle(x, y, a, b):

    glBegin(GL_TRIANGLES)
    glColor3f(0.0, 1.0, 0.0)
    glVertex2f(x-0.5*a, y+0.5*b)
    glColor3f(0.0, 1.0, 0.0)
    glVertex2f(x+0.5*a, y+0.5*b)
    glColor3f(0.0, 1.0, 0.0)
    glVertex2f(x+0.5*a, y-0.5*b)
    glEnd()

    glBegin(GL_TRIANGLES)
    glColor3f(0.0, 1.0, 0.0)
    glVertex2f(x-0.5*a, y+0.5*b)
    glColor3f(0.0, 1.0, 0.0)
    glVertex2f(x-0.5*a, y-0.5*b)
    glColor3f(0.0, 1.0, 0.0)
    glVertex2f(x+0.5*a, y-0.5*b)
    glEnd()

    glFlush()

# Zadanie na 3.0 
# Zrobiłam dwa warianty, ponieważ nie byłam pewna, który z nich miał Pan na myśli :)
def draw_tringle_v1():
    glClear(GL_COLOR_BUFFER_BIT)

    glBegin(GL_TRIANGLES)
    glColor3f(1.0, 0.0, 0.0)
    glVertex2f(-50.0, 0.0)
    glColor3f(0.0, 1.0, 0.0)
    glVertex2f(0.0, 50.0)
    glColor3f(0.0, 0.0, 1.0)
    glVertex2f(50.0, 0.0)
    glEnd()

    glFlush()

def draw_tringle_v2():
    glClear(GL_COLOR_BUFFER_BIT)

    glBegin(GL_TRIANGLES)
    glColor3f(0.0, 0.0, 0.0)
    glVertex2f(-50.0, 0.0)
    glColor3f(0.0, 0.0, 0.0)
    glVertex2f(0.0, 50.0)
    glColor3f(0.0, 0.0, 0.0)
    glVertex2f(50.0, 0.0)
    glEnd()

    glBegin(GL_POINTS)
    glColor3f(1.0, 0.0, 0.0)
    glVertex2f(-50.0, 0.0)
    glColor3f(0.0, 1.0, 0.0)
    glVertex2f(0.0, 50.0)
    glColor3f(0.0, 0.0, 1.0)
    glVertex2f(50.0, 0.0)
    
    glEnd()

    glFlush()

def update_viewport(window, width, height):
    if height == 0:
        height = 1
    if width == 0:
        width = 1
    aspectRatio = width / height

    glMatrixMode(GL_PROJECTION)
    glViewport(0, 0, width, height)
    glLoadIdentity()

    if width <= height:
        glOrtho(-100.0, 100.0, -100.0 / aspectRatio, 100.0 / aspectRatio,
                1.0, -1.0)
    else:
        glOrtho(-100.0 * aspectRatio, 100.0 * aspectRatio, -100.0, 100.0,
                1.0, -1.0)

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
