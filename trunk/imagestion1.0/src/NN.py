import math
import random
import string

def matriz(x,y) :
    m = []
    for i in range(x):
        m.append([0.0]*y)
    return m

def sigmoide(x):
    return math.tanh(x)

def dsigmoide(x):
    return 1.0 - x**2

def iniciar_perceptron():
    global nodos_ent, nodos_ocu, nodos_sal, pesos_ent, pesos_sal
    global act_ent, act_ocu, act_sal
    random.seed(0)
    
    nodos_ent = nodos_ent +1
    act_ent = [1.0]*nodos_ent
    act_ocu = [1.0]*nodos_ocu
    act_sal = [1.0]*nodos_sal
    
    pesos_ent = matriz(nodos_ent, nodos_ocu)
    pesos_sal = matriz(nodos_ocu, nodos_sal)
    
    for i in range(nodos_ent):
        for j in range(nodos_ocu):
            pesos_ent[i][j] = random.uniform(-0.5, 0.5)
    
    for j in range(nodos_ocu):
        for k in range(nodos_sal):
            pesos_sal[j][k] = random.uniform(-0.5, 0.5)
            
def actualiza_nodos(entradas):    
    global nodos_ent, nodos_ocu, nodos_sal, pesos_ent, pesos_sal
    global act_ent, act_ocu, act_sal
    
    if len(entradas) != nodos_ent -1:
        raise ValueError('Numero de nodos de entrada incorrecto')
    
    for i in range(nodos_ent -1):
        act_ent[i] = float(entradas[i])
        
    for j in range(nodos_ocu):
        sum = 0.0
        for i in range(nodos_ent):
            sum = sum + pesos_ent[i][j] * act_ent[i]
        act_ocu[j] = sigmoide(sum)
        
    for k in range(nodos_sal):
        sum = 0.0
        for j in range(nodos_ocu):
            sum = sum + pesos_sal[j][k] * act_ocu[j]
        act_sal[k] = sigmoide(sum)
        
    return act_sal[:]

def retropropagacion(objetivo,l):
    global nodos_ent, nodos_ocu, nodos_sal, pesos_ent, pesos_sal
    global act_ent, act_ocu, act_sal
    if len(objetivo) != nodos_sal:
        raise ValueError('numero de objetivos incorrecto')
    
    delta_salida = [0.0] * nodos_sal
    for k in range(nodos_sal):
        error = objetivo[k] - act_sal[k]
        delta_salida[k] = dsigmoide(act_sal[k]) * error
        
    delta_oculto = [0.0] * nodos_ocu
    for j in range(nodos_ocu):
        error = 0.0
        for k in range(nodos_sal):
            error = error + delta_salida[k]*pesos_sal[j][k]
        delta_oculto[j] = dsigmoide(act_ocu[j]) * error
        
    for j in range(nodos_ocu):
        for k in range(nodos_sal):
            cambio = delta_salida[k]*act_ocu[j]
            pesos_sal[j][k] = pesos_sal[j][k] + l*cambio
            
    for i in range(nodos_ent):
        for j in range(nodos_ocu):
            cambio = delta_oculto[j]*act_ent[i]
            pesos_ent[i][j] = pesos_ent[i][j] + l*cambio
            
    error = 0.0
    for k in range(len(objetivo)):
        error = error + 0.5*(objetivo[k] - act_sal[k])**2
    return error

def clasificar(patron):
    for p in patron:
        print p[0], '->', actualiza_nodos(p[0])
        
def entrenar_perceptron(patron, l, max_iter=1000):
    for i in range(max_iter):
        error = 0.0
        for p in patron:
            entradas = p[0]
            objetivo = p[1]
            actualiza_nodos(entradas)
            error = error + retropropagacion(objetivo, l)
        
        if error < 0.001:
            break
        
if __name__ == '__main__':
    datos_ent = [
        [[0,0], [0]],
        [[0,1], [1]],
        [[1,0], [1]],
        [[1,1], [0]],
    ]
        
    nodos_ent = 2
    nodos_ocu = 2
    nodos_sal = 1
    l = 0.5
    
    iniciar_perceptron()
    print 'ANTES'
    clasificar(datos_ent)
    entrenar_perceptron(datos_ent, l)
    print 'DESPUES'
    clasificar(datos_ent)
    
    print 'PESOS ENT: '+str(pesos_ent)
    print 'PESOS SAL: '+str(pesos_sal)
    