#!/usr/bin/env python3
import sys
import math
from numpy import *
from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *


viewer = [0.0, 0.0, 10.0]
viewing_dir = [0.0, 0.0, -10.0] 
up = [0.0, 1.0, 0.0]
view_point = [0 for i in range(3)]
first_mouse =  True

theta = 0.0
phi = 0.0
pix2angle = 1.0

left_mouse_button_pressed = 0
right_mouse_button_pressed = 0

mouse_x_pos_old = 0
delta_x = 0

mouse_y_pos_old = 0
delta_y = 0

scale = 1.0
pos = (0.0, 0.0)
R = 10.0
space_pressed = 0

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


def example_object():
    glColor3f(1.0, 1.0, 1.0)

    quadric = gluNewQuadric()
    gluQuadricDrawStyle(quadric, GLU_LINE)
    glRotatef(90, 1.0, 0.0, 0.0)
    glRotatef(-90, 0.0, 1.0, 0.0)

    gluSphere(quadric, 1.5, 10, 10)

    glTranslatef(0.0, 0.0, 1.1)
    gluCylinder(quadric, 1.0, 1.5, 1.5, 10, 5)
    glTranslatef(0.0, 0.0, -1.1)

    glTranslatef(0.0, 0.0, -2.6)
    gluCylinder(quadric, 0.0, 1.0, 1.5, 10, 5)
    glTranslatef(0.0, 0.0, 2.6)

    glRotatef(90, 1.0, 0.0, 1.0)
    glTranslatef(0.0, 0.0, 1.5)
    gluCylinder(quadric, 0.1, 0.0, 1.0, 5, 5)
    glTranslatef(0.0, 0.0, -1.5)
    glRotatef(-90, 1.0, 0.0, 1.0)

    glRotatef(-90, 1.0, 0.0, 1.0)
    glTranslatef(0.0, 0.0, 1.5)
    gluCylinder(quadric, 0.1, 0.0, 1.0, 5, 5)
    glTranslatef(0.0, 0.0, -1.5)
    glRotatef(90, 1.0, 0.0, 1.0)

    glRotatef(90, 0.0, 1.0, 0.0)
    glRotatef(-90, 1.0, 0.0, 0.0)
    gluDeleteQuadric(quadric)


def render(time):
    global theta
    global phi
    global scale
    global pos
    global R
    global space_pressed
    global viewer
    global viewing_dir
    global up

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    #Funckja gluLookAt wykorzystywana do realizacji zadań od 3.0 do 4.5.
    #gluLookAt(viewer[0], viewer[1], viewer[2], 0.0, 0.0, 0.0, up[0], up[1], up[2])
    #Funckja gluLookAt wykorzystywana do realizacji zadania na 5.0.
    gluLookAt(viewer[0], viewer[1], viewer[2], viewer[0]+viewing_dir[0], viewer[1]+viewing_dir[1], viewer[2]+viewing_dir[2], up[0], up[1], up[2])

    #Obrót wokół osi Y
    '''if left_mouse_button_pressed:
        theta += delta_x * pix2angle

    glRotatef(theta, 0.0, 1.0, 0.0)'''
    #Obrót wokół osi X - Zadanie na 3.0
    '''if left_mouse_button_pressed:
        phi += delta_y * pix2angle
    glRotatef(phi, 1.0, 0.0, 0.0)'''
    #Obrót wokół osi X i Y.
    '''if left_mouse_button_pressed:
        theta += delta_x * pix2angle
        phi += delta_y * pix2angle

    glRotatef(theta, 0.0, 1.0, 0.0)
    glRotatef(phi, 1.0, 0.0, 0.0)'''

    #Przeskalowanie obrazu po wciśnięciu prawego przycisku myszy - Zadanie na 3.5
    '''if right_mouse_button_pressed:
        if (pos[0] > 200 and pos[1] < 200) or (pos[0] < 200 and pos[1] < 200):
            scale += 0.01
        else:
            scale -= 0.01
        
    glScalef(scale, scale, scale)'''
    #Zadanie na 4.0
    '''if left_mouse_button_pressed:
        theta += delta_x * pix2angle * 0.005
        phi += delta_y * pix2angle * 0.005
             
    viewer[0] = R * math.cos(theta) * math.cos(phi)
    viewer[1] = R * math.sin(phi)
    viewer[2] = R * math.sin(theta) * math.cos(phi)

    if right_mouse_button_pressed:
        if (pos[0] > 200 and pos[1] < 200) or (pos[0] < 200 and pos[1] < 200):
            R += 0.5
        else:
            R -= 0.5'''
     #Zadanie na 4.5 - dodanie poprawności przejść kamery wokół obiektu i wprowadzienie ograniczenia w zakresie przybliżania/oddalania kamery
    '''if left_mouse_button_pressed:
        theta += delta_x * pix2angle * 0.005
        phi += delta_y * pix2angle * 0.005
        theta = theta %(2*math.pi)
        phi = phi %(2*math.pi)
        if phi >= 0.5*math.pi and phi <= 1.5*math.pi:
            up[1] = -1.0
        else: 
            up[1] = 1.0

    viewer[0] = R * math.cos(theta) * math.cos(phi)
    viewer[1] = R * math.sin(phi)
    viewer[2] = R * math.sin(theta) * math.cos(phi)
   
    if right_mouse_button_pressed:
        
        if (pos[0] > 200 and pos[1] < 200) or (pos[0] < 200 and pos[1] < 200):
            if R >= 4.0:
                R -= 0.1
        else:
            if R <= 25.0:
                R += 0.1'''
    #Zadanie na 4.5 - wprowadzenie możliwości przełączania między trybem obracania obiektu i trybem poruszania kamerą za pomocą naciśnięcia spacji 
    '''if space_pressed == 0:
        if left_mouse_button_pressed:
            theta += delta_x * pix2angle
            phi += delta_y * pix2angle
    
        if right_mouse_button_pressed:
            if (pos[0] > 200 and pos[1] < 200) or (pos[0] < 200 and pos[1] < 200):
                scale += 0.01
            else:
                scale -= 0.01
        glRotatef(theta, 0.0, 1.0, 0.0)
        glRotatef(phi, 1.0, 0.0, 0.0)        
        glScalef(scale, scale, scale)
    else:
        if left_mouse_button_pressed:
            theta += delta_x * pix2angle * 0.005
            phi += delta_y * pix2angle * 0.005
            theta = theta %(2*math.pi)
            phi = phi %(2*math.pi)
            if phi >= 0.5*math.pi and phi <= 1.5*math.pi:
                up[1] = -1.0
            else: 
                up[1] = 1.0
        viewer[0] = R * math.cos(theta) * math.cos(phi)
        viewer[1] = R * math.sin(phi)
        viewer[2] = R * math.sin(theta) * math.cos(phi)

        if right_mouse_button_pressed:
        
            if (pos[0] > 200 and pos[1] < 200) or (pos[0] < 200 and pos[1] < 200):
                if R >= 4.0:
                    R -= 0.1
            else:
                if R <= 25.0:
                    R += 0.1'''
   
    axes()
    example_object()

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
    global space_pressed
    global viewer
    global viewing_dir
    global up

    cameraSpeed = 0.05
    if key == GLFW_KEY_ESCAPE and action == GLFW_PRESS:
        glfwSetWindowShouldClose(window, GLFW_TRUE)

    #Zadanie na 4.5 - klawisz Spacji przełącza tryb.
    if key == GLFW_KEY_SPACE and action == GLFW_PRESS:
        if space_pressed == 0:
            space_pressed = 1
        else:
            space_pressed = 0

    #Zadanie na 5.0 - W - ruch do przodu, A - ruch w lewo, S - ruch do tyłu, D - ruch w prawo 
    if key == GLFW_KEY_W and action == GLFW_REPEAT:

        viewer[0] += cameraSpeed * viewing_dir[0]
        viewer[1] += cameraSpeed * viewing_dir[1]
        viewer[2] += cameraSpeed * viewing_dir[2]
    if key == GLFW_KEY_S and action == GLFW_REPEAT:
        viewer[0] -= cameraSpeed * viewing_dir[0]
        viewer[1] -= cameraSpeed * viewing_dir[1]
        viewer[2] -= cameraSpeed * viewing_dir[2]
    
    if key == GLFW_KEY_A and action == GLFW_REPEAT:
        cross_vector = cross(viewing_dir, up)
        length_vector = linalg.norm(cross_vector)
        viewer -= cameraSpeed * (cross_vector/length_vector)
    if key == GLFW_KEY_D and action == GLFW_REPEAT:
        cross_vector = cross(viewing_dir, up)
        length_vector = linalg.norm(cross_vector)
        viewer += cameraSpeed * (cross_vector/length_vector)
        

def mouse_motion_callback(window, x_pos, y_pos):
    global theta
    global phi
    global viewing_dir
    global first_mouse
    global delta_x
    global mouse_x_pos_old
    global delta_y
    global mouse_y_pos_old

     #Zadanie na 5.0 - początkowe ustawienie kursora myszy.
    if first_mouse:
        mouse_x_pos_old = 50 - x_pos
        mouse_y_pos_old = - 300 - y_pos
        first_mouse = False

    #Obliczenie różnicy położenia w poziomie dla aktualnej pozycji myszy. 
    delta_x = x_pos - mouse_x_pos_old
    mouse_x_pos_old = x_pos
    
    #Obliczenie różnicy położenia w pionie dla aktualnej pozycji myszy - zadanie na 3.0. 
    delta_y = y_pos - mouse_y_pos_old
    mouse_y_pos_old = y_pos

    #Zadanie na 5.0 - obsługa ruchu myszy
    theta += delta_x * pix2angle * 0.005
    phi += delta_y * pix2angle * 0.005

    theta = theta %(2*math.pi)
    phi = phi %(2*math.pi)
       

    view_point[0] = math.cos(theta) * math.cos(phi)
    view_point[1] = math.sin(phi)
    view_point[2] = math.sin(theta) * math.cos(phi)

    length_vector = linalg.norm(view_point)
    viewing_dir = view_point/length_vector

def mouse_button_callback(window, button, action, mods):
    global left_mouse_button_pressed
    global right_mouse_button_pressed

    if button == GLFW_MOUSE_BUTTON_LEFT and action == GLFW_PRESS:
        left_mouse_button_pressed = 1
    else:
        left_mouse_button_pressed = 0

    #Obsługa prawego przycisku myszy - zadanie na 3.5.
    if button == GLFW_MOUSE_BUTTON_RIGHT and action == GLFW_PRESS:
        right_mouse_button_pressed = 1
    else:
        right_mouse_button_pressed = 0

def main():
    global pos
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
    glfwSetCursorPos(window, 200, 200)
    glfwSetMouseButtonCallback(window, mouse_button_callback)
    glfwSwapInterval(1)

    startup()
    while not glfwWindowShouldClose(window):
        render(glfwGetTime())
        pos = glfwGetCursorPos(window)
        glfwSwapBuffers(window)
        glfwPollEvents()
    shutdown()

    glfwTerminate()


if __name__ == '__main__':
    main()
