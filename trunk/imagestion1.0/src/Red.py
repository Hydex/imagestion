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
        
        self.sinapsis[0] = [random() for x in xrange(entradas)]
                
        for i in range(self.nCapas):
            inputs = entradas if i == 0 else layers[i-1]
            size   = layers[i]
            max    = size if size > max else max
            #print [i,size,max,inputs]
            
            self.sinapsis[i+1] = [random() for x in xrange(size)]
            self.capas[i] = [Perceptron(str(i)+'x'+str(x),inputs,funciones[i]) for x in xrange(size)]
            
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
        except (NameError, ValueError):
            self.addLog("ERROR en Red.simular()\nIteracion i="+str(i)+" j="+str(j)+" n="+str(n))
            self.addLog(NameError+":"+ValueError)
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
    def entrenar(self,inputs,outputs):
        self.addLog("Red.entrenar -> inputs:"+str(inputs)+"\n outputs:"+str(outputs))
        
        # paso 1: Se inicializan los pesos de todas las neuronas con valores
        #         aleatorios rango [0..1]
        self.addLog("Paso 1:")
        epochs = len(inputs[0]) # N <= {[in1,in2,...,inN] [entrada2...]}
        self.addLog("epochs:"+str(epochs))
        
        try:
            while epochs > 0:
                datos = []
                salidas = []
                
                for idx in range(len(inputs[0])):
                    # paso 2: Seleccionar el siguiente par de entrenamiento del conjunto de
                    #         entrenamiento, aplicando el vector de entrada a la entrada de la red.
                    self.addLog("Paso 2\niteracion:"+str(epochs)+"\n")
                    for i in range(entradas):
                        datos[i] = inputs[i][idx]
                    
                    # paso 3: Calcular salida de la red    
                    resultado = self.simular(entradas)
                    self.addLog("paso 3\ndatos["+(idx)+"]="+str(datos)+"\nresultados="+str(resultados))
                    
                    for i in range(len(resultado)):
                        salidas[i][idx] = resultado[i]
                    
                    # calcula el delta de error de la red buscando un minimo
                    error = zeros(len(outputs))
                    minimo = 1
                    for i in range(len(outputs)):
                        error[i] = outputs[i][idx] - salidas[i][idx]
                        if abs(error[i]) < minimo:
                            minimo = error[i]
                    
                    # paso 4: balancea los pesos en funcion a la variacion del delta de error
                    self.addLog("paso 4\ndelta error: "+str(error))
                    self.backPropagation(self.nCapas,error)
                    
                epochs = epochs - 1
            pass
        except (NameError, ValueError):
            print str(NameError)+":"+str(ValueError)
            print "ERROR Red.entrenar():\niteracion idx="+str(idx)+" de "+str(len(inputs[0]))+"\n"
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
    def backPropagation(self,capa,delta):
        self.addLog("Red.backPropagation -> capa:"+str(capa)+" delta:"+str(delta))
        
        try:
            prev = capa
            
            if capa > 0 and len(self.capas[capa]) > 0:
                sigmas = [0.0] * len(self.capas[capa -1])
                
                for i in range(len(delta)):
                    self.capas[capa][i].setSigma(delta[i])
                
                prev = capa -1
                
                # calculo de sigma en funcion de delta resultado - error
                for i in range(len(self.capas[prev])):
                    self.capas[prev][i].setSigma(0.0)
                    
                    for j in range(len(self.capas[capa])):
                        self.capas[prev][i].setCoeficiente(j,self.capas[capa][i].getSigma())
                    
                    sigmas[i] = self.capas[prev][i].getSigma()
                
                # llamada recursiva para retropropagacion en el calculo de sigma
                if prev > 0:
                    self.backPropagation(prev, sigmas)
                
                # propagacion hacia adelante en el calulo de pesos en funcion de sigma
                for i in range(len(self.capas[prev])):
                    self.capas[prev][i].balancearPesos()
                
                self.addLog("pesos: "+(self.capas))
            pass
                    
        except (NameError, ValueError):
            print NameError+":"+ValueError
            print "ERROR Red.backPropagation():\ncapa:"+str(prev)+" iteracion i="+str(i)+" de "+str(len(self.capas[prev]))+"\n"
            pass            
        
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
        
    def addLog(self,str):
        self.log.append(str)
        pass
        
    def getLog(self):
        return self.log
        pass
        
    def printLog(self):
        print dumps(self.log, sort_keys=True,indent=4, separators=(',', ': '))
        pass

