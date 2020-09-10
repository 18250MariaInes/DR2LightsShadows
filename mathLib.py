"""
Maria Ines Vasquez Figueroa
18250
Gráficas
DR1 Spheres & Textures
Libreria de operaciones matemáticas
"""

def subtract( x0, x1, y0, y1, z0, z1):
    res=[]
    res.append(x0-x1)
    res.append(y0-y1)
    res.append(z0-z1)
    return res
#Realiza la resta entre 2 listas de 2 entradas
def subtractTwo(x0, x1, y0, y1):
    res=[]
    res.append(x0-x1)
    res.append(y0-y1)
    return res
#realiza producto cruz entre dos listas
def cross( v0, v1):
    res=[]
    res.append(v0[1]*v1[2]-v1[1]*v0[2])
    res.append(-(v0[0]*v1[2]-v1[0]*v0[2]))
    res.append(v0[0]*v1[1]-v1[0]*v0[1])
    return res

#Calcula normal de Frobenius
def frobenius( norm):
    return((norm[0]**2+norm[1]**2+norm[2]**2)**(1/2))

#calcula la division entre elementos de una lista y la normal de frobenius
def division(norm, frobenius):
    #si la division es entre cero regresa un not a number
    if (frobenius==0):
        res=[]
        res.append(float('NaN'))
        res.append(float('NaN'))
        res.append(float('NaN'))
        return res
        #return float('NaN')
    else:
        res=[]
        res.append(norm[0]/ frobenius)
        res.append(norm[1]/ frobenius)
        res.append(norm[2]/ frobenius)
        return res

#realiza producto punto entre la matriz y la luz
def dot(normal, lightx, lighty, lightz):
    return (normal[0]*lightx+normal[1]*lighty+normal[2]*lightz)

def multiN(c, normal):
    return (normal[0]*c,normal[1]*c,normal[2]*c)

def dot4(matrix1, matrix2):
    return (matrix1[0]*matrix2[0]+matrix1[1]*matrix2[1]+matrix1[2]*matrix2[2]+matrix1[3]*matrix2[3])

def multiplicacion(matriz1, matriz2, c1, f1, c2, f2): #función para multiplicar matrices
    matriz3 = []
    for i in range(f1):
        matriz3.append( [0] * c2 )

    for i in range(f1):
        for j in range(c2):
            for k in range(f2):
                    numf=matriz1[i][k] * matriz2[k][j]
                    matriz3[i][j] += numf
                
                
    return matriz3

def multiplicacionV(G, v, f1, c2): #función para multiplicar matrices, esta fue un fracaso pero la dejo porque tengo fe que algun día funcionará
    result = []
    for i in range(0,f1): #this loops through columns of the matrix
        total = 0
        for j in range(0,c2): #this loops through vector coordinates & rows of matrix
            total +=  v[i] *G[j][i]
        result.append(total)
    return result
    
def multMaster( v, M): #función para multiplicar desde matrices hasta vectores
    c = []
    for i in range(0,len(v)):
        temp=[]
        for j in range(0,len(M[0])):
            s = 0
            for k in range(0,len(v[0])):
                s += v[i][k]*M[k][j]
            temp.append(s)
        c.append(temp)
    return c