"""
Maria Ines Vasquez Figueroa
18250
Gráficas
DR2 Lights & Shadows
Libreria de operaciones matemáticas
"""
import struct
import random
from mathLib import *
import numpy as np
from numpy import cos, sin, tan


from obj import Obj



def char(c):
    # 1 byte
    return struct.pack('=c', c.encode('ascii'))

def word(w):
    # 2 bytes
    return struct.pack('=h',w)

def dword(d):
    # 4 bytes
    return struct.pack('=l',d)

def color(r, g, b):
    return bytes([int(b * 255), int(g * 255), int(r * 255)])

def baryCoords(Ax, Bx, Cx, Ay, By, Cy, Px, Py):
    # u es para la A, v es para B, w para C
    try:
        u = ( ((By - Cy)*(Px - Cx) + (Cx - Bx)*(Py - Cy) ) /
              ((By - Cy)*(Ax - Cx) + (Cx - Bx)*(Ay - Cy)) )

        v = ( ((Cy - Ay)*(Px - Cx) + (Ax - Cx)*(Py - Cy) ) /
              ((By - Cy)*(Ax - Cx) + (Cx - Bx)*(Ay - Cy)) )

        w = 1 - u - v
    except:
        return -1, -1, -1

    return u, v, w



BLACK = color(0,0,0)
WHITE = color(1,1,1)

class Raytracer(object):
    def __init__(self, width, height):
        self.curr_color = WHITE
        self.clear_color = BLACK
        self.glCreateWindow(width, height)

        self.camPosition = (0,0,0)
        self.fov = 60

        self.scene = []
        self.pointLight = None
        self.ambientLight = None

    def glCreateWindow(self, width, height):
        self.width = width
        self.height = height
        self.glClear()
        self.glViewport(0, 0, width, height)

    def glViewport(self, x, y, width, height):
        self.vportx = x
        self.vporty = y
        self.vportwidth = width
        self.vportheight = height

    def glClear(self):
        self.pixels = [ [ self.clear_color for x in range(self.width)] for y in range(self.height) ]

        #Z - buffer, depthbuffer, buffer de profudidad
        self.zbuffer = [ [ float('inf') for x in range(self.width)] for y in range(self.height) ]

    def glBackground(self, texture):

        self.pixels = [ [ texture.getColor(x / self.width, y / self.height) for x in range(self.width)] for y in range(self.height) ]

    def glVertex(self, x, y, color = None):
        nx = round(( x + 1) * (self.vportwidth  / 2 ) + self.vportx)
        ny = round(( y + 1) * (self.vportheight / 2 ) + self.vporty)

        if nx >= self.width or nx < 0 or ny >= self.height or ny < 0:
            return

        try:
            self.pixels[ny][nx] = color or self.curr_color
        except:
            pass

    def glVertex_coord(self, x, y, color = None):
        if x < self.vportx or x >= self.vportx + self.vportwidth or y < self.vporty or y >= self.vporty + self.vportheight:
            return

        if x >= self.width or x < 0 or y >= self.height or y < 0:
            return

        try:
            self.pixels[y][x] = color or self.curr_color
        except:
            pass

    def glColor(self, r, g, b):

        self.curr_color = color(r,g,b)

    def glClearColor(self, r, g, b):

        self.clear_color = color(r,g,b)

    def glFinish(self, filename):
        archivo = open(filename, 'wb')

        # File header 14 bytes
        archivo.write(bytes('B'.encode('ascii')))
        archivo.write(bytes('M'.encode('ascii')))
        archivo.write(dword(14 + 40 + self.width * self.height * 3))
        archivo.write(dword(0))
        archivo.write(dword(14 + 40))

        # Image Header 40 bytes
        archivo.write(dword(40))
        archivo.write(dword(self.width))
        archivo.write(dword(self.height))
        archivo.write(word(1))
        archivo.write(word(24))
        archivo.write(dword(0))
        archivo.write(dword(self.width * self.height * 3))
        archivo.write(dword(0))
        archivo.write(dword(0))
        archivo.write(dword(0))
        archivo.write(dword(0))

        # Pixeles, 3 bytes cada uno
        for x in range(self.height):
            for y in range(self.width):
                archivo.write(self.pixels[x][y])

        archivo.close()

    def glZBuffer(self, filename):
        archivo = open(filename, 'wb')

        # File header 14 bytes
        archivo.write(bytes('B'.encode('ascii')))
        archivo.write(bytes('M'.encode('ascii')))
        archivo.write(dword(14 + 40 + self.width * self.height * 3))
        archivo.write(dword(0))
        archivo.write(dword(14 + 40))

        # Image Header 40 bytes
        archivo.write(dword(40))
        archivo.write(dword(self.width))
        archivo.write(dword(self.height))
        archivo.write(word(1))
        archivo.write(word(24))
        archivo.write(dword(0))
        archivo.write(dword(self.width * self.height * 3))
        archivo.write(dword(0))
        archivo.write(dword(0))
        archivo.write(dword(0))
        archivo.write(dword(0))

        # Minimo y el maximo
        minZ = float('inf')
        maxZ = -float('inf')
        for x in range(self.height):
            for y in range(self.width):
                if self.zbuffer[x][y] != -float('inf'):
                    if self.zbuffer[x][y] < minZ:
                        minZ = self.zbuffer[x][y]

                    if self.zbuffer[x][y] > maxZ:
                        maxZ = self.zbuffer[x][y]

        for x in range(self.height):
            for y in range(self.width):
                depth = self.zbuffer[x][y]
                if depth == -float('inf'):
                    depth = minZ
                depth = (depth - minZ) / (maxZ - minZ)
                archivo.write(color(depth,depth,depth))

        archivo.close()
    

    def rtRender(self):
        #pixel por pixel
        for y in range(self.height):
            for x in range(self.width):

                # pasar valor de pixel a coordenadas NDC (-1 a 1)
                Px = 2 * ( (x+0.5) / self.width) - 1
                Py = 2 * ( (y+0.5) / self.height) - 1

                #FOV(angulo de vision), asumiendo que el near plane esta a 1 unidad de la camara
                t = tan( (self.fov * np.pi / 180) / 2 )
                r = t * self.width / self.height
                Px *= r
                Py *= t

                
               
                directionp=(Px, Py, -1)
                directionp=division(directionp, frobenius(directionp))
                """print(direction)
                print(directionp)
                print("--------------------------------")"""
                intersectV = None
                material = None

                for obj in self.scene:
                    intersect = obj.ray_intersect(self.camPosition, directionp)
                    if intersect is not None:
                        if intersect.distance < self.zbuffer[y][x]:
                            self.zbuffer[y][x] = intersect.distance
                            material = obj.material
                            intersectV = intersect
                #cuando hay un material predeterminado
                if intersectV is not None:
                    self.glVertex_coord(x, y,self.pointColor(material, intersectV))
    
    def pointColor(self, material, intersect):

        objectColor = [material.diffuse[2] / 255,
                                material.diffuse[1] / 255,
                                material.diffuse[0] / 255]

        ambientColor = [0,0,0]
        diffuseColor = [0,0,0]
        specColor = [0,0,0]

        shadow_intensity = 0

        if self.ambientLight:
            ambientColor = [self.ambientLight.strength * self.ambientLight.color[2] / 255,
                                     self.ambientLight.strength * self.ambientLight.color[1] / 255,
                                     self.ambientLight.strength * self.ambientLight.color[0] / 255]

        if self.pointLight:
            # Sacamos la direccion de la luz para este punto
            """light_dir = np.subtract(self.pointLight.position, intersect.point)
            light_dir = light_dir / np.linalg.norm(light_dir)"""
            #print(light_dir)
            light_dirp = subtract(self.pointLight.position[0], intersect.point[0], self.pointLight.position[1], intersect.point[1], self.pointLight.position[2], intersect.point[2])
            light_dirp = division(light_dirp, frobenius(light_dirp))
            #print(light_dirp)
            #print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

            # Calculamos el valor del diffuse color
            """intensity = self.pointLight.intensity * max(0, np.dot(light_dir, intersect.normal))
            print(intensity)"""
            intensityp = self.pointLight.intensity * max(0, dot(light_dirp, intersect.normal[0],intersect.normal[1],intersect.normal[2]))
            #print(intensityp)
            diffuseColor = [intensityp * self.pointLight.color[2] / 255,
                                     intensityp * self.pointLight.color[1] / 255,
                                     intensityp * self.pointLight.color[2] / 255]

            # Iluminacion especular
            """view_dir = np.subtract(self.camPosition, intersect.point)
            view_dir = view_dir / np.linalg.norm(view_dir)
            print(view_dir)"""
            view_dirp = subtract(self.camPosition[0], intersect.point[0], self.camPosition[1], intersect.point[1], self.camPosition[2], intersect.point[2])
            view_dirp = division(view_dirp, frobenius(view_dirp))
            """print(view_dirp)
            print("------------------------------------------------------------------------------")"""

            # R = 2 * (N dot L) * N - L
            #reflect = 2 * np.dot(intersect.normal, light_dirp)
            
            reflectp=2*(dot(intersect.normal, light_dirp[0],light_dirp[1],light_dirp[2]))#funciona
            #print(reflectp)
            
            #reflect = np.multiply(reflect, intersect.normal)
            #print(reflect)
            reflectp=multiN(reflectp, intersect.normal)#funciona
            """print(reflectp)
            print("-------------------------------------------------")"""
            """reflectp
            print(reflectp)
            print("-------------------------------------------------")"""
            #reflect = np.subtract(reflect, light_dirp)
            #print(reflect)
            reflectp=subtract(reflectp[0], light_dirp[0],reflectp[1], light_dirp[1],reflectp[2], light_dirp[2])#funciona
            """print(reflectp)
            print("---------------------------------------------------------------------")"""
            # spec_intensity: lightIntensity * ( view_dir dot reflect) ** specularidad
            spec_intensity = self.pointLight.intensity * (max(0, dot(view_dirp, reflectp[0],reflectp[1],reflectp[2])) ** material.spec)

            specColor = [spec_intensity * self.pointLight.color[2] / 255,
                                  spec_intensity * self.pointLight.color[1] / 255,
                                  spec_intensity * self.pointLight.color[0] / 255]

            #print(specColor)

            for obj in self.scene:
                if obj is not intersect.sceneObject:
                    hit = obj.ray_intersect(intersect.point,  light_dirp)
                    if hit is not None and intersect.distance < frobenius(subtract(self.pointLight.position[0], intersect.point[0],self.pointLight.position[1], intersect.point[1],self.pointLight.position[2], intersect.point[2])):
                        shadow_intensity = 1

        # Formula de iluminacion
        """print(diffuseColor + specColor)
        print(sum(diffuseColor, specColor))"""
        """print((1 - shadow_intensity) * (diffuseColor + specColor))
        print(multiN((1 - shadow_intensity),sum(diffuseColor, specColor)))"""
        
        """print((ambientColor + (1 - shadow_intensity) * (diffuseColor + specColor)))
        print(sum(ambientColor, multiN((1 - shadow_intensity),sum(diffuseColor, specColor))))"""
        """print((ambientColor + (1 - shadow_intensity) * (diffuseColor + specColor)) * objectColor)
        print(multColor(sum(ambientColor, multiN((1 - shadow_intensity),sum(diffuseColor, specColor))),objectColor))
        print("------------------------------------------------")"""
        #finalColor = (ambientColor + (1 - shadow_intensity) * (diffuseColor + specColor)) * objectColor
        finalColorp=multColor(sum(ambientColor, multiN((1 - shadow_intensity),sum(diffuseColor, specColor))),objectColor)
        #Nos aseguramos que no suba el valor de color de 1

        r = min(1,finalColorp[0])
        g = min(1,finalColorp[1])
        b = min(1,finalColorp[2])

        return color(r, g, b)

                











                











