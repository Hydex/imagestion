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
from Layer import *
from random import *
from json import *
from sys import *

class Net(object):

    """
    :version: 1.0
    :author:  Miguelote
    """

    #Ejemplo:
    #net = Net(2,1,[2,1],['TANSIG','TANSIG'])
    #net = Net(2,1,[2,1],['LOGSIG','LOGSIG'])
    def __init__(self,entradas,salidas,layers,funciones):
        self.nCapas   = len(layers)
        max,size      = 0,0
        self.log      = []
        #self.capas    = [None] * self.nCapas
        self.layers   = []        
        # Layers(capa,neurons,inputs,function,layers)
        self.layers   = [None] * self.nCapas
        #self.layers   = [Layer(i,layers[i],(entradas if i == 0 else layers[i]),funciones[i],self.layers) for i in xrange(len(layers))]
        self.sinapsis = [None] * (self.nCapas + 1)
        self.neuronas = 0
        self.entradas = entradas
        self.salidas  = salidas
        self.transferencias = funciones
        self.epochs   = None
        self.panic    = False
        self.expect   = []
        self.historial = []
        
        self.sinapsis[0] = [random() for x in xrange(entradas)]
                
        for i in range(self.nCapas):
            inputs = entradas if i == 0 else layers[i-1]
            size   = layers[i]
            max    = size if size > max else max
            #print [i,size,max,inputs]
            
            self.sinapsis[i+1] = [random() for x in xrange(size)]
            #self.capas[i] = [Perceptron(str(i)+'x'+str(x),inputs,funciones[i]) for x in xrange(size)]
            self.layers[i] = Layer(i,inputs,funciones[i],self.layers)
            self.neuronas += size
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
        
##        try:
        for i in xrange(self.nCapas):
            #for j in range(len(self.capas[i])):
            for j in xrange(self.layers[i].cant -1):
                #if self.capas[i][j] != None:
                for n in xrange(len(self.sinapsis[i])):
                    self.layers[i].nodos[j].entradas[n] = self.sinapsis[i][n]
                
                self.sinapsis[i+1][j] =  self.layers[i].nodos[j].calcular();
                
                if i == self.nCapas-1:
                    outputs[j] =  self.layers[i].nodos[j].salida 
                #pass
##        except:
##            err = str(exc_info())
##            self.addLog("ERROR en Red.simular('"+str(err)+"')\nIteracion i="+str(i)+" j="+str(j)+" n="+str(n))
##            print("ERROR en Net.simular('"+str(err)+"')\nIteracion i="+str(i)+" j="+str(j)+" n="+str(n))
##            self.addLog(err)
##            self.addLog (self.layers[i].nodos[j].getLog())
##            self.panic = True
##            pass
        
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
        self.addLog("Net.entrenar -> inputs:"+str(inputs)+"\n outputs:"+str(outputs))
        self.expect = outputs
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
##                    self.addLog(' =========================================================================================')
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
                    
##                    for ciclo in range(epochs):  ##
                    # paso 4: balancea los pesos en funcion a la variacion del delta de error
                    self.addLog("PASO 4: balancea los pesos en funcion a la variacion del delta de error")
                    self.addLog(">> epochs:"+str(epochs)+' pesos:'+self.getPesos())
                    #self.backPropagation(self.nCapas-1,resultado,expect)
                    
                    self.addLog("PASO 5: Calculo de error cuadratico de la red")
                    errorCuadratico = self.getErrorCuadratico()
                    self.historial.append({errorCuadratico:self.getPesos(), 'error':self.getErrores()})
                    self.addLog(">> errorCuadratico = "+str(errorCuadratico))
                    
                epochs = epochs - 1
            pass
##        except:
##            err = str(exc_info())
##            self.addLog("ERROR Net.entrenar():\niteracion idx="+str(idx)+" de "+str(len(inputs))+"\n")
##            print("ERROR Net.entrenar('"+str(err)+"'):\niteracion idx="+str(idx)+" de "+str(len(inputs))+"\n")
##            self.addLog(err)
##            self.panic = True
##            pass        

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
    def backPropagation2(self,capa,result,expect):
        self.addLog("Net.backPropagation -> capa:"+str(capa)+" result:"+str(result)+" expect:"+str(expect))
        i,j = 0,0
        prev = capa -1
                
        try:
            #if capa > 0 and len(self.capas[capa]) > 0:
            #    deltas = self.getDelta(capa,result,expect)
            
            pass
        except:
            err = str(exc_info())
            self.addLog("ERROR Net.backPropagation(): capa:"+str(prev)+" iteracion i="+str(i)+" de "+str(len(self.capas[prev]))+"\n")
            print("ERROR Net.backPropagation('"+str(err)+"'): capa:"+str(prev)+" iteracion i="+str(i)+" de "+str(len(self.capas[prev]))+"\n")
            self.addLog(err)
            self.addLog(self.capas[capa][j].getLog())
            self.addLog(self.capas[prev][i].getLog())
            self.panic = True 
        pass
        
##    def getError(self,capa,result,expect):
##        self.addLog("Net.getError -> capa:"+str(capa)+" result:"+str(result)+" expect:"+str(expect))
##        
##        pass
        
##    def getErrorRed(self,capa,expect):
##        self.addLog("Net.getErrorRed -> capa:"+str(capa)+" result:"+str(result)+" expect:"+str(expect))
##        error = 0.0;
##        for i in xrange(len(self.capas[capa])):
##            error += (self.capas[capa].getSalida() - expect[i])**2
##            
##        return error/self.neuronas
    
##    def getDelta(self,capa,result,expect):
##        deltas = []
##        post = capa + 1
##        
##        if capa == self.nCapas -1:
##            deltas = [0] * len(result)
##            error = 0.0
##            
##            for k in xrange(self.nCapas -1):
##                error = expect[k] - result[k]
##                deltas[k] = self.capas[capa][k].fnTransf.train(result[k]) * error
##                self.capas[capa][k].setDelta(deltas[k])
##                pass
##        else:
##            deltas = [0] * len(self.capas[capa])
##            
##            for j in xrange(len(self.capas[capa])):
##                error = 0.0
##                
##                for k in xrange(len(self.capas[post]) -1):
##                    error += deltas[k] * self.capas[post][k].getPeso(k)
##                
##                deltas[j] = self.capas[capa][j] * error
##                pass
##        
##        return deltas
        
    def backPropagation(self,capa,result,expect):
        self.addLog("Net.backPropagation -> capa:"+str(capa)+" result:"+str(result)+" expect:"+str(expect))
        i,j = 0,0
        delta = [0] * len(result)
        prev = capa
        
        try:
            for i in xrange(len(delta)):
                # calculo de delta en funcion de delta (esperado - resultado)
                delta[i] = expect[i] - result[i]
                self.layers[capa].nodos[i].setDelta(delta[i])
                if capa == self.nCapas -1:
                    self.capas[capa][i].setError(delta[i]*self.layers[capa].nodos[i].fnTransf.train(result[i]))
                self.addLog('>> delta['+str(i)+']:'+str(delta[i])+' = '+str(expect[i])+' - '+str(result[i]))
                                        
            self.addLog('>> neuronas:'+str(len(self.capas[capa])))
            
            if capa > 0 and len(self.capas[capa]) > 0:
                prev = capa -1
                self.addLog('propagacion hacia atras en el calulo para ajuste de delta [capa:'+str(capa)+'][prev:'+str(prev)+']')
                
                # calculo del error para la capa
                deltas = [0] * self.layers[prev].cant
                expect = [0] * self.layers[prev].cant
                
                for i in xrange(len(self.capas[prev])):
                    # calcula la sumatoria de los pesos con el coeficiente de error delta
                    self.addLog('<< capa[prev:'+str(prev)+'][i:'+str(i)+'] errores:'+str(self.getErrores()))
                    
                    for j in xrange(self.layers[capa].cant):
                        dlta  = self.layers[prev].nodos[i].getDelta()
                        error = self.layers[prev].nodos[i].getError()

                        self.layers[prev].nodos[i].setDelta(dlta + self.layers[capa].nodos[j].getCoeficiente(i))                        
                        self.layers[prev].nodos[i].setError(error + self.layers[capa].nodos[j].getErrorCapa())
                        deltas[j] = self.layers[prev].nodos[i].getError()
                        expect[j] = self.layers[prev].nodos[i].getSalida()

                    self.addLog('>> capa[prev:'+str(prev)+'][i:'+str(i)+'] errores:'+str(self.getErrores()))
                
                self.addLog('>> Net.deltas[]:'+str(self.getDeltas()))
                
                self.addLog('llamada recursiva para retropropagacion en el calculo de delta')
                # llamada recursiva para retropropagacion en el calculo de delta
                self.backPropagation(prev, deltas, expect)
                
                self.addLog('propagacion hacia adelante en el calulo de pesos en funcion de delta')
                # propagacion hacia adelante en el calulo de pesos en funcion de delta

                for i in xrange(self.layers[prev].cant):
                    self.addLog('<< capa[prev:'+str(prev)+'][i:'+str(i)+'].pesos:'+str([self.capas[prev][i].pesos]))
                    self.layers[prev].nodos[i].balancearPesos()
                    self.addLog(self.layers[prev].nodos[i].getLog())
                    self.addLog('>> capa[prev:'+str(prev)+'][i:'+str(i)+'].pesos:'+str([self.capas[prev][i].pesos]))
            pass
                    
        except:
            err = str(exc_info())
            self.addLog("ERROR Net.backPropagation(): capa:"+str(prev)+" iteracion i="+str(i)+" de "+str(len(self.capas[prev]))+"\n")
            print("ERROR Net.backPropagation('"+str(err)+"'): capa:"+str(prev)+" iteracion i="+str(i)+" de "+str(len(self.capas[prev]))+"\n")
            self.addLog(err)
            self.addLog(self.layers[capa].nodos[j].getLog())
            self.addLog(self.layers[prev].nodos[i].getLog())
            self.panic = True           
       
    """
    # Obtiene el error cuadratico de la red
    """ 
    def getErrorCuadratico(self):
        error = 0
        
        for j in range(self.nCapas):
            for k in range(len(self.capas[j])):
                if self.capas[j][k] != None:
                    error += self.layers[j].nodos[k].getErrorCuadratico()
                pass
                
        return error/2

        
    """
    # Obtiene una estructura de la instancia de la red neuronal
    # y la exporta en formato JSON 
    """
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
                self.layers[y].nodos[x].getConfiguracion() 
                for x in xrange(self.layers[y].cant)
            ] 
            for y in xrange(len(self.layers))
        ]
        return dumps(data, sort_keys=True,indent=4, separators=(',', ': '))

    def getEpochs(self):
        return self.epochs
        
    def setEpochs(self,valor):
        self.epochs = valor
        
    def getPeso(self,i,w,capa):
        return self.layers[capa].nodos[w].getPeso[i]
        
    def setPeso(self,i,w,capa,valor):
        self.layers[capa].nodos[w].setPeso(i,valor)
        
    def getSalida(self,w,capa):
        #return self.capas[capa][w].getSalida()
        return self.layers[capa].nodos[w].getSalida()
        
    def addLog(self,str):
        self.log.append(str)
        #print str
        
    def getLog(self):
        return self.log
        
    def getPesos(self):
        lst = []
        for i in range(self.nCapas):
            for j in range(self.layers[i].cant):
                #lst.append("capas["+str(i)+"]["+str(j)+"].pesos:"+str(self.capas[i][j].pesos))
                lst.append({ self.layers[i].nodos[j].name : self.layers[i].nodos[j].pesos})
                
        #return dumps(lst, sort_keys=True,indent=4, separators=(',', ': '))
        return str(lst)

    def getDeltas(self):
        lst = []
        for i in range(self.nCapas):
            for j in range(self.layers[i].cant):
                lst.append({self.layers[i].nodos[j].name : self.layers[i].nodos[j].delta})
                
        return str(lst)
            
    def getErrores(self):
        lst = []
        for i in range(self.nCapas):
            for j in range(self.layers[i].cant):
                lst.append({self.layers[i].nodos[j].name : self.layers[i].nodos[j].error})
                
        return str(lst)
            
    def getEntradas(self):
        lst = []
        for i in range(self.nCapas):
            for j in range(self.layers[i].cant):
                lst.append({self.layers[i].nodos[j].name : self.layers[i].nodos[j].entradas})
                
        return dumps(lst, sort_keys=True,indent=4, separators=(',', ': '))
    
    def getHistorial(self):
        return dumps(self.historial, sort_keys=True,indent=4, separators=(',', ': '))
            
    def printLog(self):
        print dumps(self.log, sort_keys=True,indent=4, separators=(',', ': '))

