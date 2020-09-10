"""
Maria Ines Vasquez Figueroa
18250
Gráficas
DR1 Spheres & Textures
Main
"""

from gl import Raytracer, color, V2, V3
from obj import Obj, Texture
from sphere import Sphere, Material,PointLight, AmbientLight


brick = Material(diffuse = color(0.8, 0.25, 0.25 ), spec = 16)
stone = Material(diffuse = color(0.4, 0.4, 0.4 ), spec = 32)
grass = Material(diffuse = color(0.5, 1, 0), spec = 32)
glass = Material(diffuse = color(0.25, 1, 1), spec = 64)
coal = Material(diffuse = color(0, 0, 0), spec = 32)
snow = Material(diffuse = color(1, 1, 1), spec = 64)
carrot=Material(diffuse = color(1, 0.54, 0), spec = 64)
eyes=Material(diffuse = color(0.90, 0.90, 0.90))
pink_center=Material(diffuse = color(0.976, 0.38, 1))
pink_bow=Material(diffuse = color(0.984, 0.6, 1), spec = 64)



width = 500
height = 800
r = Raytracer(width,height)
r.pointLight = PointLight(position = V3(-2,2,0), intensity = 1)
r.ambientLight = AmbientLight(strength = 0.1)
#dibujo de muñeco de nieve
#cuerpo
r.scene.append( Sphere((0, 0.7,  -5), 0.5, snow) )
r.scene.append( Sphere((0, 0, -5), 0.6, snow) )
r.scene.append( Sphere((0, -1, -5), 0.9, snow) )

#botones
r.scene.append( Sphere((0, 0,  -4), 0.1, coal) )
r.scene.append( Sphere((0, -0.4, -4), 0.1, coal) )
r.scene.append( Sphere((0, -0.8, -4), 0.1, coal) )

#nariz
r.scene.append( Sphere((0, 0.6,  -4), 0.1, carrot) )

#sonrisa
r.scene.append( Sphere((-0.08, 0.4,  -4), 0.05, coal) )
r.scene.append( Sphere((0.08, 0.4,  -4), 0.05, coal) )
r.scene.append( Sphere((-0.20, 0.47,  -4), 0.05, coal) )
r.scene.append( Sphere((0.20, 0.47,  -4), 0.05, coal) )

#ojos
r.scene.append( Sphere((-0.09, 0.8,  -4), 0.08, eyes) )
r.scene.append( Sphere((0.09, 0.8,  -4), 0.08, eyes) )
r.scene.append( Sphere((-0.09, 0.7,  -3.5), 0.03, coal) )
r.scene.append( Sphere((0.09, 0.7,  -3.5), 0.03, coal) )

#bow
"""r.scene.append( Sphere((-0.06, 1.005,  -4.1), 0.08, pink_bow) )
r.scene.append( Sphere((0, 1,  -4), 0.05, pink_center) )
r.scene.append( Sphere((0.06, 1.005,  -4.1), 0.08, pink_bow) )"""



"""r.scene.append( Sphere(V3(    0,   0, -5),    1, brick) )
r.scene.append( Sphere(V3( -0.5, 0.5, -3), 0.25, stone) )"""


r.rtRender()

r.glFinish('output.bmp')





