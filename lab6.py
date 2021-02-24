#!/usr/bin/env python3
import sys
import math

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *

from PIL import Image

from random import uniform


viewer = [0.0, 0.0, 10.0]

theta = 0.0
phi = 0.0
pix2angle = 1.0

left_mouse_button_pressed = 0
mouse_x_pos_old = 0
delta_x = 0
mouse_y_pos_old = 0
delta_y = 0

mat_ambient = [1.0, 1.0, 1.0, 1.0]
mat_diffuse = [1.0, 1.0, 1.0, 1.0]
mat_specular = [1.0, 1.0, 1.0, 1.0]
mat_shininess = 20.0

light_ambient = [0.1, 0.1, 0.0, 1.0]
light_diffuse = [0.8, 0.8, 0.0, 1.0]
light_specular = [1.0, 1.0, 1.0, 1.0]
light_position = [0.0, 0.0, 10.0, 1.0]

att_constant = 1.0
att_linear = 0.05
att_quadratic = 0.001

#Domyślnie ściana jest widzialna (zadanie na 3.5)
visible_wall = True
#Domyślnie pierwsza tekstura (zadanie na 4.5)
texture1 = True

image = Image.open("tekstura.tga")
image2 = Image.open("tekstura2.tga")

#Jajko
N = 50

vertexTab = [[[0 for k in range(3)] for j in range(N)] for i in range(N)]
uTab = []
vTab = []


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

#Funkcja rysująca jajko z teksturą - zadanie na 5.0.
def draw_egg_triangle_strips():
    egg_parameters()
    
    for i in range(N):
        glBegin(GL_TRIANGLE_STRIP)
        for j in range(N):
            if(uTab[i] > 0.5 and uTab[i] < 1.0):
                glTexCoord2f(float(i + 1) / N, float(j) / N)
                glVertex3fv(vertexTab[(i + 1) % N][j])
                glTexCoord2f(float(i) / N, float(j) / N)
                glVertex3fv(vertexTab[i][j])
            else:
                glTexCoord2f(float(i) / N, float(j) / N)
                glVertex3fv(vertexTab[i][j])
                glTexCoord2f(float(i + 1) / N, float(j) / N)
                glVertex3fv(vertexTab[(i + 1) % N][j])
        glEnd()

def draw_traingle():
    glBegin(GL_TRIANGLES)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(-5.0, -5.0, 0.0)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(5.0, -5.0, 0.0)
    glTexCoord2f(0.5, 1.0)
    glVertex3f(0.0, 5.0, 0.0)
    glEnd()

#Funkcja rysująca kwadrat - zadanie na 3.0.
def draw__quadrat():
    glBegin(GL_TRIANGLES)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(5.0, 5.0, 0.0) 
    glTexCoord2f(0.0, 1.0)
    glVertex3f(-5.0, 5.0, 0.0)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(-5.0, -5.0, 0.0)
    
    glEnd()

    glBegin(GL_TRIANGLES)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(-5.0, -5.0, 0.0)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(5.0, -5.0, 0.0)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(5.0, 5.0, 0.0)
    
    glEnd()

#Funkcja rysująca ostrosłup - zadanie na 3.5.
def draw_pyramid():
    #Podstawa - kwadrat. 

    glBegin(GL_TRIANGLES)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(-3.0, -3.0, 0.0)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(-3.0, 3.0, 0.0)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(3.0, 3.0, 0.0) 
    glEnd()

    glBegin(GL_TRIANGLES)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(3.0, 3.0, 0.0)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(3.0, -3.0, 0.0)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(-3.0, -3.0, 0.0)
    
    glEnd()

    #Trójkąt -1 bok.
    if (visible_wall == True): 
        glBegin(GL_TRIANGLES)
        glTexCoord2f(0.5, 0.5)
        glVertex3f(0.0, 0.0, 5.0) 
        glTexCoord2f(0.0, 1.0)
        glVertex3f(-3.0, 3.0, 0.0)
        glTexCoord2f(0.0, 0.0)
        glVertex3f(-3.0, -3.0, 0.0)
        glEnd()

    #Trójkąt -2 bok.
    glBegin(GL_TRIANGLES)
    glTexCoord2f(0.5, 0.5)
    glVertex3f(0.0, 0.0, 5.0) 
    glTexCoord2f(0.0, 0.0)
    glVertex3f(-3.0, -3.0, 0.0)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(3.0, -3.0, 0.0)
    glEnd()

    #Trójkąt -3 bok.
    glBegin(GL_TRIANGLES)
    glTexCoord2f(0.5, 0.5)
    glVertex3f(0.0, 0.0, 5.0) 
    glTexCoord2f(1.0, 0.0)
    glVertex3f(3.0, -3.0, 0.0)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(3.0, 3.0, 0.0)
    glEnd()

    #Trójkąt -4 bok.
    glBegin(GL_TRIANGLES)
    
    glTexCoord2f(1.0, 1.0)
    glVertex3f(3.0, 3.0, 0.0)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(-3.0, 3.0, 0.0)
    glTexCoord2f(0.5, 0.5)
    glVertex3f(0.0, 0.0, 5.0)
    glEnd()

#Funkcja rysująca ostrosłup z inną teksturą - zadanie na 4.0.
def draw_pyramid_with_second_texture():
    #Podstawa - kwadrat. 
    glTexImage2D(
        GL_TEXTURE_2D, 0, 3, image2.size[0], image2.size[1], 0,
        GL_RGB, GL_UNSIGNED_BYTE, image2.tobytes("raw", "RGB", 0, -1)
    )

    glBegin(GL_TRIANGLES)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(-3.0, -3.0, 0.0)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(-3.0, 3.0, 0.0)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(3.0, 3.0, 0.0) 
    glEnd()

    glBegin(GL_TRIANGLES)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(3.0, 3.0, 0.0)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(3.0, -3.0, 0.0)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(-3.0, -3.0, 0.0)
    
    glEnd()

    #Trójkąt -1 bok.
    if (visible_wall == True): 
        glBegin(GL_TRIANGLES)
        glTexCoord2f(0.5, 0.5)
        glVertex3f(0.0, 0.0, 5.0) 
        glTexCoord2f(0.0, 1.0)
        glVertex3f(-3.0, 3.0, 0.0)
        glTexCoord2f(0.0, 0.0)
        glVertex3f(-3.0, -3.0, 0.0)
        glEnd()

    #Trójkąt -2 bok.
    glBegin(GL_TRIANGLES)
    glTexCoord2f(0.5, 0.5)
    glVertex3f(0.0, 0.0, 5.0) 
    glTexCoord2f(0.0, 0.0)
    glVertex3f(-3.0, -3.0, 0.0)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(3.0, -3.0, 0.0)
    glEnd()

    #Trójkąt -3 bok.
    glBegin(GL_TRIANGLES)
    glTexCoord2f(0.5, 0.5)
    glVertex3f(0.0, 0.0, 5.0) 
    glTexCoord2f(1.0, 0.0)
    glVertex3f(3.0, -3.0, 0.0)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(3.0, 3.0, 0.0)
    glEnd()

    #Trójkąt -4 bok.
    glBegin(GL_TRIANGLES)
    
    glTexCoord2f(1.0, 1.0)
    glVertex3f(3.0, 3.0, 0.0)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(-3.0, 3.0, 0.0)
    glTexCoord2f(0.5, 0.5)
    glVertex3f(0.0, 0.0, 5.0)
    glEnd()

#Funkcja rysująca ostrosłup z funkcją przełącznia się między teksturami- zadanie na 4.5.
def draw_pyramid_with_texture_change():

    if (texture1 == False):
        glTexImage2D(
            GL_TEXTURE_2D, 0, 3, image2.size[0], image2.size[1], 0,
            GL_RGB, GL_UNSIGNED_BYTE, image2.tobytes("raw", "RGB", 0, -1)
        )
    else:
        glTexImage2D(
            GL_TEXTURE_2D, 0, 3, image.size[0], image.size[1], 0,
            GL_RGB, GL_UNSIGNED_BYTE, image.tobytes("raw", "RGB", 0, -1)
        )

    glBegin(GL_TRIANGLES)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(-3.0, -3.0, 0.0)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(-3.0, 3.0, 0.0)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(3.0, 3.0, 0.0) 
    glEnd()

    glBegin(GL_TRIANGLES)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(3.0, 3.0, 0.0)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(3.0, -3.0, 0.0)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(-3.0, -3.0, 0.0)
    
    glEnd()

    #Trójkąt -1 bok.
    if (visible_wall == True): 
        glBegin(GL_TRIANGLES)
        glTexCoord2f(0.5, 0.5)
        glVertex3f(0.0, 0.0, 5.0) 
        glTexCoord2f(0.0, 1.0)
        glVertex3f(-3.0, 3.0, 0.0)
        glTexCoord2f(0.0, 0.0)
        glVertex3f(-3.0, -3.0, 0.0)
        glEnd()

    #Trójkąt -2 bok.
    glBegin(GL_TRIANGLES)
    glTexCoord2f(0.5, 0.5)
    glVertex3f(0.0, 0.0, 5.0) 
    glTexCoord2f(0.0, 0.0)
    glVertex3f(-3.0, -3.0, 0.0)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(3.0, -3.0, 0.0)
    glEnd()

    #Trójkąt -3 bok.
    glBegin(GL_TRIANGLES)
    glTexCoord2f(0.5, 0.5)
    glVertex3f(0.0, 0.0, 5.0) 
    glTexCoord2f(1.0, 0.0)
    glVertex3f(3.0, -3.0, 0.0)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(3.0, 3.0, 0.0)
    glEnd()

    #Trójkąt -4 bok.
    glBegin(GL_TRIANGLES)
    
    glTexCoord2f(1.0, 1.0)
    glVertex3f(3.0, 3.0, 0.0)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(-3.0, 3.0, 0.0)
    glTexCoord2f(0.5, 0.5)
    glVertex3f(0.0, 0.0, 5.0)
    glEnd()


def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)

    glMaterialfv(GL_FRONT, GL_AMBIENT, mat_ambient)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, mat_diffuse)
    glMaterialfv(GL_FRONT, GL_SPECULAR, mat_specular)
    glMaterialf(GL_FRONT, GL_SHININESS, mat_shininess)

    glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
    glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)

    glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, att_constant)
    glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, att_linear)
    glLightf(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, att_quadratic)

    glShadeModel(GL_SMOOTH)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)

    glEnable(GL_TEXTURE_2D)
    glEnable(GL_CULL_FACE)
    glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    image = Image.open("tekstura.tga")
    image2 = Image.open("tekstura2.tga")
    glTexImage2D(
        GL_TEXTURE_2D, 0, 3, image.size[0], image.size[1], 0,
        GL_RGB, GL_UNSIGNED_BYTE, image.tobytes("raw", "RGB", 0, -1)
    )


def shutdown():
    pass


def render(time):
    global theta
    global phi
    global visible_wall

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    gluLookAt(viewer[0], viewer[1], viewer[2],
              0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

    if left_mouse_button_pressed:
        theta += delta_x * pix2angle
        phi += delta_y * pix2angle

    glRotatef(theta, 0.0, 1.0, 0.0)
    glRotatef(phi, 1.0, 0.0, 0.0)

    #Rysowanie trójkąta z teksturą.
    #draw_traingle()

    #Rysowanie kwadratu z teksturą - zadanie na 3.0.
    #draw__quadrat()

    #Ostrosłup z teksturą - zadanie na 3.5.
    #draw_pyramid()
    
    #Ostrosłup z drugą teksturą - zadanie na 4.0.
    draw_pyramid_with_second_texture()

    #Ostrosłup zmiana tekstur - zadanie na 4.5.
    #draw_pyramid_with_texture_change()

    #Jajko z teksturą - zadanie na 5.0.
    #draw_egg_triangle_strips()

    glFlush()



def update_viewport(window, width, height):
    global pix2angle
    pix2angle = 360.0 / width

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    gluPerspective(70, 1.0, 0.1, 300.0)

    if width <= height:
        glViewport(0, int((height - width) / 2), width, width)
    else:
        glViewport(int((width - height) / 2), 0, height, height)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def keyboard_key_callback(window, key, scancode, action, mods):
    global visible_wall
    global texture1

    if key == GLFW_KEY_ESCAPE and action == GLFW_PRESS:
        glfwSetWindowShouldClose(window, GLFW_TRUE)

    #Zmiana widoczności ściany po naciśnięciu spacji - zadanie na 3.5.
    if key == GLFW_KEY_SPACE and action == GLFW_PRESS:
        if visible_wall == True:
            visible_wall = False
        elif visible_wall == False:
            visible_wall = True

    #Przełącza teksturę (s jak switch :)) - Zadanie na 4.5.
    if key == GLFW_KEY_S and action == GLFW_PRESS:
        if texture1 == True:
            texture1 = False
        elif texture1 == False:
            texture1 = True         

def mouse_motion_callback(window, x_pos, y_pos):
    global delta_x
    global mouse_x_pos_old
    global delta_y
    global mouse_y_pos_old

    delta_x = x_pos - mouse_x_pos_old
    mouse_x_pos_old = x_pos

    delta_y = y_pos - mouse_y_pos_old
    mouse_y_pos_old = y_pos

def mouse_button_callback(window, button, action, mods):
    global left_mouse_button_pressed

    if button == GLFW_MOUSE_BUTTON_LEFT and action == GLFW_PRESS:
        left_mouse_button_pressed = 1
    else:
        left_mouse_button_pressed = 0


def main():
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(400, 400, __file__, None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)

    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
    glfwSetKeyCallback(window, keyboard_key_callback)
    glfwSetCursorPosCallback(window, mouse_motion_callback)
    glfwSetMouseButtonCallback(window, mouse_button_callback)
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
