# +-----------------------------------------------------------------------+
# | IMAGESTION                                                            |
# |                                                                       |
# | Copyright (C) 2010-Today, GNUCHILE.CL  -  Santiago de Chile           |
# | Licensed under the GNU GPL                                            |
# |                                                                       |
# | Redistribution and use in source and binary forms, with or without    |
# | modification, are permitted provided that the following conditions    |
# | are met:                                                              |
# |                                                                       |
# | o Redistributions of source code must retain the above copyright      |
# |   notice, this list of conditions and the following disclaimer.       |
# | o Redistributions in binary form must reproduce the above copyright   |
# |   notice, this list of conditions and the following disclaimer in the |
# |   documentation and/or other materials provided with the distribution.|
# | o The names of the authors may not be used to endorse or promote      |
# |   products derived from this software without specific prior written  |
# |   permission.                                                         |
# |                                                                       |
# | THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS   |
# | "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT     |
# | LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR |
# | A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT  |
# | OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, |
# | SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT      |
# | LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, |
# | DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY |
# | THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT   |
# | (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE |
# | OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.  |
# |                                                                       |
# +-----------------------------------------------------------------------+
# | Author: Miguel Vargas Welch <miguelote@gmail.com>                     |
# +-----------------------------------------------------------------------+

from Perceptron import *
from random import *
from json import *
from sys import *

class Red(object):

    """


    :version: 1.0
    :author:  Miguelote
    """

    def __init__(self,entradas,salidas,layers,funciones):
        self.nCapas   = len(layers)
        max,size      = 0,0
        self.log      = []
        self.capas    = [None] * self.nCapas
        self.sinapsis = [None] * (self.nCapas + 1)
        self.entradas = entradas
        self.salidas  = salidas
        self.transferencias = funciones
        self.epochs   = None
        self.panic    = False
        
        self.sinapsis[0] = [random() for x in xrange(entradas)]
                
        for i in range(self.nCapas):
            inputs = entradas if i == 0 else layers[i-1]
            size   = layers[i]
            max    = size if size > max else max
            #print [i,size,max,inputs]
            
            self.sinapsis[i+1] = [random() for x in xrange(size)]
            self.capas[i] = [Perceptron(str(i)+'x'+str(x),inputs,funciones[i]) for x in xrange(size)]
            
        pass

    """
    /**
    * simular
    * 
    * @param inputs
    * @return Double[]
    * 
    * Propagacion hacia adelante del la red neuronal, devolviendo una salida
    * en funcion de los argumentos de entrada.
    * 
    * Mas detalle en profundidad visitar:
    * http://galaxy.agh.edu.pl/~vlsi/AI/backp_t_en/backprop.html
    **/
    """
    def simular(self,inputs):
        self.addLog("Red.simular -> inputs:"+str(inputs))
        outputs = [None] * self.salidas
        i,j,n = 0,0,0
        
        for n in range(len(inputs)):
            self.sinapsis[0][n] = inputs[n]
        #print self.sinapsis
        
        try:
            for i in range(self.nCapas):
                for j in range(len(self.capas[i])):
                    if self.capas[i][j] != None:
                        for n in range(len(self.sinapsis[i])):
                            self.capas[i][j].entradas[n] = self.sinapsis[i][n]
                        
                        self.sinapsis[i+1][j] = self.capas[i][j].calcular();
                        
                        if i == self.nCapas-1:
                            outputs[j] = self.capas[i][j].salida 
                    pass
        except:
            err = str(exc_info())
            self.addLog("ERROR en Red.simular('"+str(err)+"')\nIteracion i="+str(i)+" j="+str(j)+" n="+str(n))
            print("ERROR en Red.simular('"+str(err)+"')\nIteracion i="+str(i)+" j="+str(j)+" n="+str(n))
            self.addLog(err)
            self.addLog(self.capas[i][j].getLog())
            self.panic = True
            pass
        
        return outputs
        
    """
    /** 
     * entrenar
     *
     * Estructura y aprendizaje:
     * - Capa de entrada con n neuronas.
     * - Capa de salida con m neuronas.
     * - Al menos una capa oculta de neuronas.
     * - Cada neurona de una capa recibe entradas de todas las
     *   neuronas de la capa anterior y envia su salida a todas
     *   las neuronas de la capa posterior. No hay conexiones
     *   hacia atras ni laterales entre neuronas de la misma capa.
     *
     * Mas detalle en profundidad visitar:
     * http://galaxy.agh.edu.pl/~vlsi/AI/backp_t_en/backprop.html
     **/    
    """
    
##    Ejemplo
##    net.entrenar([
##            [0.0,0.0], [0.0,1.0], [1.0,0.0], [1.0,1.0]
##        ],[
##            [0.0], [1.0], [1.0], [0.0]
##        ])

    def entrenar(self,inputs,outputs):
        self.addLog("Red.entrenar -> inputs:"+str(inputs)+"\n outputs:"+str(outputs))
        idx = 0
        minimo = 1
        
        # paso 1: Se inicializan los pesos de todas las neuronas con valores
        #         aleatorios rango [0..1]
        epochs = self.epochs if self.epochs != None else len(inputs) # N <= {[in1,in2,...,inN] [entrada2...]}
        self.addLog("PASO 1: Se inicializan los pesos de todas las neuronas con valores aleatorios rango [0..1]")
        self.addLog(">> epochs:"+str(epochs)+' idx=len(inputs[0]):'+str(len(inputs[0])))
        
        try:
            for ciclo in range(epochs):
            #for idx in range(len(inputs)):
                #datos = [None] * self.entradas
                self.addLog(">> idx:"+str(idx)+" -----------------------------------------------------------------------------------------")
                salidas = [[None] * len(outputs[0])] * len(outputs)
                
                ## [[0.0,0.0], [0.0,1.0], [1.0,0.0], [1.0,1.0]]
                for idx in range(len(inputs)):
                #for ciclo in range(epochs):
                    self.addLog('>> salidas:'+str(salidas))
                    self.addLog('>> ciclo:'+str(ciclo)+' =========================================================================================')
                    # paso 2: Seleccionar el siguiente par de entrenamiento del conjunto de
                    #         entrenamiento, aplicando el vector de entrada a la entrada de la red.
                    self.addLog("PASO 2: Seleccionar el siguiente par de entrenamiento del conjunto de entrenamiento, aplicando el vector de entrada a la entrada de la red.")
                    datos = [None] * len(inputs[idx])
                    
                    for i in range(len(inputs[idx])):
                        datos[i] = inputs[idx][i]
                    
                    # paso 3: Calcular salida de la red    
                    resultado = self.simular(datos)
                    self.addLog("PASO 3: Calcular salida de la red")
                    self.addLog(">> datos:"+str(datos)+" resultado:"+str(resultado)+' salidas:'+str(salidas))
                    
                    for i in range(len(salidas[idx])):
                        self.addLog('>> salidas['+str(idx)+']['+str(i)+']='+str(resultado[i]))
                        salidas[idx][i] = resultado[i]
                    
                    # calcula el delta de error de la red buscando un minimo
                    error = [None] * len(resultado)
                    self.addLog("calcula el delta de error de la red buscando un minimo")
                    self.addLog(">> nro de resultados: "+str(len(resultado)))
                    expect = outputs[idx]
                    
##                    for i in range(len(resultado)):
##                        error[i] = outputs[idx][i] - salidas[idx][i]
##                        self.addLog('>> error['+str(i)+']:'+str(error[i])+' = '+str(outputs[idx][i])+' - '+str(salidas[idx][i]))
##                        if abs(error[i]) < minimo:
##                            minimo = error[i]
##                    
##                    self.addLog(">> error minimo encontrado: "+str(minimo))
                    
                    # paso 4: balancea los pesos en funcion a la variacion del delta de error
                    self.addLog("PASO 4: balancea los pesos en funcion a la variacion del delta de error")
                    #self.backPropagation(self.nCapas-1,error)
                    self.backPropagation(self.nCapas-1,resultado,expect)
                    
                epochs = epochs - 1
            pass
        except:
            err = str(exc_info())
            self.addLog("ERROR Red.entrenar():\niteracion idx="+str(idx)+" de "+str(len(inputs))+"\n")
            print("ERROR Red.entrenar('"+str(err)+"'):\niteracion idx="+str(idx)+" de "+str(len(inputs))+"\n")
            self.addLog(err)
            self.panic = True
            pass        

    """   
    #  backPropagation
    # 
    # Algoritmo de retropropagacion
    # 
    # El procedimiento de retropropagacion es una forma relativamente eficiente
    # de calcular que tanto se mejora el desempeno con los cambios individuales
    # en los pesos. Se conoce como procedimiento de retropropagacion porque,
    # primero calcula cambios en la capa final, reutiliza gran parte de los
    # mismos calculos para calcular los cambios de los pesos de la penultima
    # capa y, finalmente, regresa a la capa inicial.
    #
    #
    """         
    #def backPropagation(self,capa,delta):
    def backPropagation(self,capa,result,expect):
        self.addLog("Red.backPropagation -> capa:"+str(capa)+" result:"+str(result)+" expect:"+str(expect))
        i,j = 0,0
        delta = [0] * len(result)
        prev = capa
        
        try:
            for i in xrange(len(result)-1):
                delta[i] = expect[i] - result[i]
                self.addLog('>> delta['+str(i)+']:'+str(delta[i])+' = '+str(expect[i])+' - '+str(result[i]))
                                        
            self.addLog('>> neuronas:'+str(len(self.capas[capa])))
            if capa > 0 and len(self.capas[capa]) > 0:
                prev = capa -1
                self.addLog('propagacion hacia atras en el calulo para ajuste de sigma [capa:'+str(capa)+'][prev:'+str(prev)+']')
                
                # calculo del error para la capa
                for j in xrange(len(delta)):
                    self.capas[capa][j].setError(delta[j]*self.capas[capa][j].fnTransf.train(result[j]))
                    self.capas[capa][j].setSigma(delta[j])
                    self.capas[capa][j].setDelta(delta[j])
                
                # calculo de sigma en funcion de delta (resultado - error)
                self.addLog('>> neuronas capa inferior:'+str(len(self.capas[prev]))+' red.sigmas[]:'+str(self.getSigmas()))
                sigmas = [0] * len(self.capas[prev])

                for i in xrange(len(self.capas[prev])):
                    # calcula la sumatoria de los pesos con el coeficiente de error sigma
                    self.capas[prev][i].setSigma(0.0)
                    
                    for j in xrange(len(self.capas[capa])):
                        sigma = self.capas[prev][i].getSigma()
                        
                        self.addLog('<< capa[prev:'+str(prev)+'][i:'+str(i)+'].sigma:'+str(sigma)+' += '+str(self.capas[capa][j].pesos[i])+' * '+str(self.capas[capa][j].getSigma()))
                        
                        self.capas[prev][i].setSigma(sigma + self.capas[capa][j].getCoeficiente(i))
                        sigmas[j] = self.capas[prev][i].getSigma()
                        
                        self.addLog('>> capa[prev:'+str(prev)+'][i:'+str(i)+'].sigma:'+str(sigmas[j])+' += '+str(self.capas[capa][j].pesos[i])+' * '+str(self.capas[capa][j].getSigma()))

                self.addLog('>> red.sigmas[]:'+str(self.getSigmas()))
                
                self.addLog('llamada recursiva para retropropagacion en el calculo de sigma')
                # llamada recursiva para retropropagacion en el calculo de sigma
                #self.backPropagation(prev, sigmas)
                self.backPropagation(prev, sigmas, expect)
                
                self.addLog('propagacion hacia adelante en el calulo de pesos en funcion de sigma')
                # propagacion hacia adelante en el calulo de pesos en funcion de sigma

                for i in xrange(len(self.capas[prev])):
                    self.addLog('<< capa[prev:'+str(prev)+'][i:'+str(i)+'].pesos:'+str([self.capas[prev][i].pesos]))
                    self.capas[prev][i].balancearPesos()
                    self.addLog(self.capas[prev][i].getLog())
                    self.addLog('>> capa[prev:'+str(prev)+'][i:'+str(i)+'].pesos:'+str([self.capas[prev][i].pesos]))
            pass
                    
        except:
            err = str(exc_info())
            self.addLog("ERROR Red.backPropagation(): capa:"+str(prev)+" iteracion i="+str(i)+" de "+str(len(self.capas[prev]))+"\n")
            print("ERROR Red.backPropagation('"+str(err)+"'): capa:"+str(prev)+" iteracion i="+str(i)+" de "+str(len(self.capas[prev]))+"\n")
            self.addLog(err)
            self.addLog(self.capas[capa][j].getLog())
            self.addLog(self.capas[prev][i].getLog())
            self.panic = True           
        
    def getConfiguracion(self):
        data = {
            'nCapas':self.nCapas,
            'sinapsis':self.sinapsis,
            'entradas':self.entradas,
            'salidas':self.salidas,
            'funciones':self.transferencias   
        }
        data['capas'] = [
            [
                self.capas[y][x].getConfiguracion() 
                for x in xrange(len(self.capas[y]))
            ] 
            for y in xrange(len(self.capas))
        ]
        return dumps(data, sort_keys=True,indent=4, separators=(',', ': '))
        pass

    def getEpochs(self):
        return self.epochs
        pass
        
    def setEpochs(self,valor):
        self.epochs = valor
        pass
        
    def getPeso(self,i,w,capa):
        return self.capas[capa][w].getPeso[i]
        pass
        
    def setPeso(self,i,w,capa,valor):
        self.capas[capa][w].setPeso(i,valor)
        pass
        
    def getSalida(self,w,capa):
        return self.capas[capa][w].getSalida()
        pass
        
    def addLog(self,str):
        self.log.append(str)
        #print str
        pass
        
    def getLog(self):
        return self.log
        pass
        
    def getPesos(self):
        lst = []
        for i in range(len(self.capas)):
            for j in range(len(self.capas[i])):
                #lst.append("capas["+str(i)+"]["+str(j)+"].pesos:"+str(self.capas[i][j].pesos))
                lst.append({self.capas[i][j].name:self.capas[i][j].pesos})
                
        #return dumps(lst, sort_keys=True,indent=4, separators=(',', ': '))
        return str(lst)

    def getSigmas(self):
        lst = []
        for i in range(len(self.capas)):
            for j in range(len(self.capas[i])):
                lst.append({self.capas[i][j].name:self.capas[i][j].sigma})
                
        return str(lst)
            
    def getEntradas(self):
        lst = []
        for i in range(len(self.capas)):
            for j in range(len(self.capas[i])):
                lst.append({self.capas[i][j].name : self.capas[i][j].entradas})
                
        return dumps(lst, sort_keys=True,indent=4, separators=(',', ': '))
    
    def printLog(self):
        print dumps(self.log, sort_keys=True,indent=4, separators=(',', ': '))
        pass

