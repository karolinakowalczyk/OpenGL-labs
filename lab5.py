#!/usr/bin/env python3
import sys
import math

from glfw.GLFW import *
from numpy import *
from numpy import linalg as LNG

from OpenGL.GL import *
from OpenGL.GLU import *


viewer = [0.0, 0.0, 10.0]

theta = 0.0
theta2 = 0.0
phi = 0.0
phi2 = 0.0
pix2angle = 1.0

left_mouse_button_pressed = 0
right_mouse_button_pressed = 0

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

#Zmienne pomocnicze do zadania na 3.0, 3.5 i 4.0.
light_ambient_1 = [0.1, 0.1, 1.0, 1.0]
light_diffuse_1 = [0.8, 0.0, 0.8, 1.0]
light_specular_1 = [1.0, 0.0, 0.8, 1.0]
light_position_1 = [10.0, 0.0, 0.0, 1.0]

a_pressed = False 

a_1_pressed = False

a_2_pressed = False

a_3_pressed = False

d_pressed = False 

d_1_pressed = False

d_2_pressed = False

d_3_pressed = False

s_pressed = False 

s_1_pressed = False

s_2_pressed = False

s_3_pressed = False

R = 5.0
x_s1 = 0
y_s1 = 0
z_s1 = 0
x_s2 = 0
y_s2 = 0
z_s2 = 0

N = 50

vertexTab = [[[0 for k in range(3)] for j in range(N)] for i in range(N)]
uTab = []
vTab = []
componentsOfNormalVectorTab = [[[0 for k in range(6)] for j in range(N)] for i in range(N)]
normalVectorsTab = [[[0 for k in range(3)] for j in range(N)] for i in range(N)]

space_pressed = False


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

            #Xu
            componentsOfNormalVectorTab[row][col][0] = (-450 * uTab[row] ** 4 + 900 * uTab[row] ** 3 - 810 * uTab[row] ** 2 + 360 * uTab[row] - 45) * math.cos(math.pi * vTab[col])
            #Xv
            componentsOfNormalVectorTab[row][col][1] = math.pi * (90 * uTab[row] ** 5 - 225 * uTab[row] ** 4 + 270 * uTab[row] ** 3 - 180 * uTab[row] ** 2 + 45 * uTab[row]) * math.sin(math.pi * vTab[col])
            #Yu
            componentsOfNormalVectorTab[row][col][2] = 640 * uTab[row] ** 3 - 960 * uTab[row] ** 2 + 320 * uTab[row]
            #Yv
            componentsOfNormalVectorTab[row][col][3] = 0
            #Zu
            componentsOfNormalVectorTab[row][col][4] = (-450 * uTab[row] ** 4 + 900 * uTab[row] ** 3 - 810 * uTab[row] ** 2 + 360 * uTab[row] - 45) * math.sin(math.pi * vTab[col])
            #Zv
            componentsOfNormalVectorTab[row][col][5] = -math.pi * (90 * uTab[row] ** 5 - 225 * uTab[row] ** 4 + 270 * uTab[row] ** 3 - 180 * uTab[row] ** 2 + 45 * uTab[row]) * math.cos(math.pi * vTab[col])

            normalVectorsTab[row][col][0] = (componentsOfNormalVectorTab[row][col][2] * componentsOfNormalVectorTab[row][col][5]) - (componentsOfNormalVectorTab[row][col][4] * componentsOfNormalVectorTab[row][col][3])
            normalVectorsTab[row][col][1] = (componentsOfNormalVectorTab[row][col][4] * componentsOfNormalVectorTab[row][col][1]) - (componentsOfNormalVectorTab[row][col][0] * componentsOfNormalVectorTab[row][col][5])
            normalVectorsTab[row][col][2] = (componentsOfNormalVectorTab[row][col][0] * componentsOfNormalVectorTab[row][col][3]) - (componentsOfNormalVectorTab[row][col][2] * componentsOfNormalVectorTab[row][col][1])

            normalVectorsTab[row][col] = normalVectorsTab[row][col]/(LNG.norm(normalVectorsTab[row][col]))
            
            if (uTab[row] > 1/2 and uTab[row] < 1 ):
                normalVectorsTab[row][col] = (-1) * normalVectorsTab[row][col]

def draw_normal_vectors():
    egg_parameters()

    for i in range(N):
        for j in range(N):
            glBegin(GL_LINES)
            glVertex3fv(vertexTab[i][j])
            glVertex3fv(vertexTab[i][j] + normalVectorsTab[i][j])
            glEnd()
            
    for i in range(N):
        glBegin(GL_TRIANGLE_STRIP)
        for j in range(N):
            glNormal3fv(normalVectorsTab[i][j])
            glVertex3fv(vertexTab[i][j])

            glNormal3fv(normalVectorsTab[(i+1) % N][j])
            glVertex3fv(vertexTab[(i + 1) % N][j])
        glEnd()

def draw_egg_triangle_strips():
    egg_parameters()
    
    for i in range(N):
        glBegin(GL_TRIANGLE_STRIP)
        for j in range(N):
            glNormal3fv(normalVectorsTab[i][j])
            glVertex3fv(vertexTab[i][j])
            glNormal3fv(normalVectorsTab[(i+1) % N][j])
            glVertex3fv(vertexTab[(i + 1) % N][j])
        glEnd()


def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)

    #Zadanie na 3.0 - dwa źródła światła, wykorzystywane też w zadaniu na 3.5 i w zadaniu na 4.0.
    '''glMaterialfv(GL_FRONT, GL_AMBIENT, mat_ambient)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, mat_diffuse)
    glMaterialfv(GL_FRONT, GL_SPECULAR, mat_specular)
    glMaterialf(GL_FRONT, GL_SHININESS, mat_shininess)

    glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
    glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)

    glLightfv(GL_LIGHT1, GL_AMBIENT, light_ambient_1)
    glLightfv(GL_LIGHT1, GL_DIFFUSE, light_diffuse_1)
    glLightfv(GL_LIGHT1, GL_SPECULAR, light_specular_1)
    glLightfv(GL_LIGHT1, GL_POSITION, light_position_1)


    glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, att_constant)
    glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, att_linear)
    glLightf(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, att_quadratic)

    glLightf(GL_LIGHT1, GL_CONSTANT_ATTENUATION, att_constant)
    glLightf(GL_LIGHT1, GL_LINEAR_ATTENUATION, att_linear)
    glLightf(GL_LIGHT1, GL_QUADRATIC_ATTENUATION, att_quadratic)

    glShadeModel(GL_SMOOTH)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHT1)'''

    #Jedno źródło światła - wykorzytywane w zadaniu na 4.5 i 5.0.
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
    

def shutdown():
    pass


def render(time):
    global theta
    global phi
    global theta2
    global phi2
    global R
    global light_position
    global light_position_1
    global x_s1
    global y_s1
    global z_s1
    global x_s2
    global y_s2
    global z_s2

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    gluLookAt(viewer[0], viewer[1], viewer[2],
              0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

    #Rysowanie sfery i jej obracanie - potrzebne do zadania na 3.0 i 3.5.
    '''if left_mouse_button_pressed:
        theta += delta_x * pix2angle

    glRotatef(theta, 0.0, 1.0, 0.0)

    quadric = gluNewQuadric()
    gluQuadricDrawStyle(quadric, GLU_FILL)
    gluSphere(quadric, 3.0, 10, 10)
    gluDeleteQuadric(quadric)'''
    

    #Zadanie na 4.0 - poruszanie źródłami światła i wizualizacja.

    '''quadric = gluNewQuadric()
    gluQuadricDrawStyle(quadric, GLU_FILL)
    gluSphere(quadric, 3.0, 10, 10)
    gluDeleteQuadric(quadric)

    if left_mouse_button_pressed:
        theta += delta_x * pix2angle * 0.005
        phi -= delta_y * pix2angle * 0.005
        x_s1 = R * math.cos(theta) * math.cos(phi)
        y_s1 = R * math.sin(phi)
        z_s1 = R * math.sin(theta) * math.cos(phi)

    
    if right_mouse_button_pressed:
        theta2 += delta_x * pix2angle * 0.005
        phi2 -= delta_y * pix2angle * 0.005
        x_s2 = R * math.cos(theta2) * math.cos(phi2)
        y_s2 = R * math.sin(phi2)
        z_s2 = R * math.sin(theta2) * math.cos(phi2)
    
    light_position = [x_s1, y_s1, z_s1]
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)

    glTranslatef(x_s1, y_s1, z_s1)

    #Wizualizacja 1 źródła światła.
    quadric = gluNewQuadric()
    gluQuadricDrawStyle(quadric, GLU_LINE)
    gluSphere(quadric, 0.5, 6, 5)
    gluDeleteQuadric(quadric)

    x_s2 = R * math.cos(theta2) * math.cos(phi2)
    y_s2 = R * math.sin(phi2)
    z_s2 = R * math.sin(theta2) * math.cos(phi2)

    light_position_1 = [x_s2, y_s2, z_s2]
    
    glLightfv(GL_LIGHT1, GL_POSITION, light_position_1)

    glTranslatef(-x_s1, -y_s1, -z_s1)
    glTranslatef(x_s2, y_s2, z_s2)

    #Wizualizacja 2 źródła światła.
    quadric = gluNewQuadric()
    gluQuadricDrawStyle(quadric, GLU_LINE)
    gluSphere(quadric, 0.5, 6, 5)
    gluDeleteQuadric(quadric)'''

    #Zadanie na 4.5 - obracanie rysowanie jajka - pokolorowane w połowie, wyświetlanie wektorów normalnych w połowie.
    #UWAGA! Żeby zobaczyć zadanie na 4.5 należy zakomentować linijki: 125 i 126, linijka 125 zaczyna się od: if (uTab[row] > 1/2 and uTab[row] < 1 ).
    '''if left_mouse_button_pressed:
        theta += delta_x * pix2angle * 2

    glRotatef(theta, 0.0, 1.0, 0.0)
    draw_egg_triangle_strips()
    draw_normal_vectors()'''

    # Zadanie na 5.0
    if left_mouse_button_pressed:
        theta += delta_x * pix2angle * 2

    glRotatef(theta, 0.0, 1.0, 0.0)
    if (space_pressed == False):
        draw_egg_triangle_strips()
    else:
        draw_normal_vectors()


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

#Zadanie na 3.5:
#Key A: light_ambient -> key 1: pierwszy parametr tablicy light_ambient, key 2: drugi parametr tablicy light_ambient, key 3: trzeci parametr tablicy light_ambient
#Key D: light_diffuse -> key 1, key 2, key 3 - analogicznie do light_ambient
#Key S: light_specular -> key 1, key 2, key 3 - analogicznie do light_ambient
def keyboard_key_callback(window, key, scancode, action, mods):
    global light_ambient
    global light_diffuse
    global light_specular
    global a_pressed 
    global a_1_pressed
    global a_2_pressed
    global a_3_pressed
    global d_pressed 
    global d_1_pressed
    global d_2_pressed
    global d_3_pressed
    global s_pressed 
    global s_1_pressed
    global s_2_pressed
    global s_3_pressed
    global space_pressed

    if key == GLFW_KEY_ESCAPE and action == GLFW_PRESS:
        glfwSetWindowShouldClose(window, GLFW_TRUE)
    if key == GLFW_KEY_A and action == GLFW_PRESS:
        print("a pressed!")
        a_pressed = True
        d_pressed = False
        s_pressed = False
        d_1_pressed = False
        d_2_pressed = False
        d_3_pressed = False
        s_1_pressed = False
        s_2_pressed = False
        s_3_pressed = False

    if (a_pressed):
        if key == GLFW_KEY_1 and action == GLFW_PRESS:
            print("1 pressed!")
            a_1_pressed = True
    if(a_1_pressed):
        a_2_pressed = False
        a_3_pressed = False
        if key == GLFW_KEY_UP and action == GLFW_PRESS:
            print("UP pressed!")
            if(light_ambient[0] <= 0.9):
                light_ambient[0] += 0.1
                light_ambient[0] = round(light_ambient[0], 1)
                print (light_ambient[0])
        if key == GLFW_KEY_DOWN and action == GLFW_PRESS:
            print("DOWN pressed!")
            if(light_ambient[0] >= 0.1):
                light_ambient[0] -= 0.1 
                light_ambient[0] = round(light_ambient[0], 1)
                print (light_ambient[0])
    if (a_pressed):
        if key == GLFW_KEY_2 and action == GLFW_PRESS:
            print("2 pressed!")
            a_2_pressed = True
    if(a_2_pressed):
        a_1_pressed = False
        a_3_pressed = False
        if key == GLFW_KEY_UP and action == GLFW_PRESS:
            print("UP pressed!")
            if(light_ambient[1] <= 0.9):
                light_ambient[1] += 0.1
                light_ambient[1] = round(light_ambient[1], 1)
                print (light_ambient[1])
        if key == GLFW_KEY_DOWN and action == GLFW_PRESS:
            print("DOWN pressed!")
            if(light_ambient[1] >= 0.1):
                light_ambient[1] -= 0.1 
                light_ambient[1] = round(light_ambient[1], 1)
                print (light_ambient[1])
    if (a_pressed):
        if key == GLFW_KEY_3 and action == GLFW_PRESS:
            print("3 pressed!")
            a_3_pressed = True
    if(a_3_pressed):
        a_1_pressed = False
        a_2_pressed = False
        if key == GLFW_KEY_UP and action == GLFW_PRESS:
            print("UP pressed!")
            if(light_ambient[2] <= 0.9):
                light_ambient[2] += 0.1
                light_ambient[2] = round(light_ambient[2], 1)
                print (light_ambient[2])
        if key == GLFW_KEY_DOWN and action == GLFW_PRESS:
            print("DOWN pressed!")
            if(light_ambient[2] >= 0.1):
                light_ambient[2] -= 0.1 
                light_ambient[2] = round(light_ambient[2], 1)
                print (light_ambient[2])

    if key == GLFW_KEY_D and action == GLFW_PRESS:
        print("d pressed!")
        a_pressed = False
        d_pressed = True
        s_pressed = False

        a_1_pressed = False
        a_2_pressed = False
        a_3_pressed = False
        s_1_pressed = False
        s_2_pressed = False
        s_3_pressed = False

    if (d_pressed):
        if key == GLFW_KEY_1 and action == GLFW_PRESS:
            print("1 pressed!")
            d_1_pressed = True
    if(d_1_pressed):
        d_2_pressed = False
        d_3_pressed = False
        if key == GLFW_KEY_UP and action == GLFW_PRESS:
            print("UP pressed!")
            if(light_diffuse[0] <= 0.9):
                light_diffuse[0] += 0.1
                light_diffuse[0] = round(light_diffuse[0], 1)
                print (light_diffuse[0])
        if key == GLFW_KEY_DOWN and action == GLFW_PRESS:
            print("DOWN pressed!")
            if(light_diffuse[0] >= 0.1):
                light_diffuse[0] -= 0.1 
                light_diffuse[0] = round(light_diffuse[0], 1)
                print (light_diffuse[0])

    if (d_pressed):
        if key == GLFW_KEY_2 and action == GLFW_PRESS:
            print("2 pressed!")
            d_2_pressed = True    
    if(d_2_pressed):
        d_1_pressed = False
        d_3_pressed = False
        if key == GLFW_KEY_UP and action == GLFW_PRESS:
            print("UP pressed!")
            if(light_diffuse[1] <= 0.9):
                light_diffuse[1] += 0.1
                light_diffuse[1] = round(light_diffuse[1], 1)
                print (light_diffuse[1])
        if key == GLFW_KEY_DOWN and action == GLFW_PRESS:
            print("DOWN pressed!")
            if(light_diffuse[1] >= 0.1):
                light_diffuse[1] -= 0.1 
                light_diffuse[1] = round(light_diffuse[1], 1)
                print (light_diffuse[1])
    if (d_pressed):
        if key == GLFW_KEY_3 and action == GLFW_PRESS:
            print("3 pressed!")
            d_3_pressed = True
    if(d_3_pressed):
        d_1_pressed = False
        d_2_pressed = False
        if key == GLFW_KEY_UP and action == GLFW_PRESS:
            print("UP pressed!")
            if(light_diffuse[2] <= 0.9):
                light_diffuse[2] += 0.1
                light_diffuse[2] = round(light_diffuse[2], 1)
                print (light_diffuse[2])
        if key == GLFW_KEY_DOWN and action == GLFW_PRESS:
            print("DOWN pressed!")
            if(light_diffuse[2] >= 0.1):
                light_diffuse[2] -= 0.1 
                light_diffuse[2] = round(light_diffuse[2], 1)
                print (light_diffuse[2])

    if key == GLFW_KEY_S and action == GLFW_PRESS:
        print("s pressed!")
        a_pressed = False
        d_pressed = False
        s_pressed = True

        a_1_pressed = False
        a_2_pressed = False
        a_3_pressed = False
        d_1_pressed = False
        d_2_pressed = False
        d_3_pressed = False

    if (s_pressed):
        if key == GLFW_KEY_1 and action == GLFW_PRESS:
            print("1 pressed!")
            s_1_pressed = True
    if(s_1_pressed):
        s_2_pressed = False
        s_3_pressed = False
        if key == GLFW_KEY_UP and action == GLFW_PRESS:
            print("UP pressed!")
            if(light_specular[0] <= 0.9):
                light_specular[0] += 0.1
                light_specular[0] = round(light_specular[0], 1)
                print (light_specular[0])
        if key == GLFW_KEY_DOWN and action == GLFW_PRESS:
            print("DOWN pressed!")
            if(light_specular[0] >= 0.1):
                light_specular[0] -= 0.1 
                light_specular[0] = round(light_specular[0], 1)
                print (light_specular[0])

    if (s_pressed):
        if key == GLFW_KEY_2 and action == GLFW_PRESS:
            print("2 pressed!")
            s_2_pressed = True
    if(s_2_pressed):
        s_1_pressed = False
        s_3_pressed = False
        if key == GLFW_KEY_UP and action == GLFW_PRESS:
            print("UP pressed!")
            if(light_specular[1] <= 0.9):
                light_specular[1] += 0.1
                light_specular[1] = round(light_specular[1], 1)
                print (light_specular[1])
        if key == GLFW_KEY_DOWN and action == GLFW_PRESS:
            print("DOWN pressed!")
            if(light_specular[1] >= 0.1):
                light_specular[1] -= 0.1 
                light_specular[1] = round(light_specular[1], 1)
                print (light_specular[1])

    if (s_pressed):
        if key == GLFW_KEY_3 and action == GLFW_PRESS:
            print("3 pressed!")
            s_3_pressed = True
    if(s_3_pressed):
        s_1_pressed = False
        s_2_pressed = False
        if key == GLFW_KEY_UP and action == GLFW_PRESS:
            print("UP pressed!")
            if(light_specular[2] <= 0.9):
                light_specular[2] += 0.1
                light_specular[2] = round(light_specular[2], 1)
                print (light_specular[2])
        if key == GLFW_KEY_DOWN and action == GLFW_PRESS:
            print("DOWN pressed!")
            if(light_specular[2] >= 0.1):
                light_specular[2] -= 0.1 
                light_specular[2] = round(light_specular[2], 1)
                print (light_specular[2])

    if key == GLFW_KEY_SPACE and action == GLFW_PRESS:  
            print("Space pressed")
            space_pressed = not space_pressed
    update_light()

    #Funkcja wykorzystywana w zadaniu na 3.5 - aktualizuje światło w widoku.
def update_light():
    glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
    glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)

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
    global right_mouse_button_pressed

    if button == GLFW_MOUSE_BUTTON_LEFT and action == GLFW_PRESS:
        left_mouse_button_pressed = 1
    else:
        left_mouse_button_pressed = 0

    
    if button == GLFW_MOUSE_BUTTON_RIGHT and action == GLFW_PRESS:
        right_mouse_button_pressed = 1
    else:
        right_mouse_button_pressed = 0


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
