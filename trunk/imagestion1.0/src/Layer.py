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

class Layer(object):
    def __init__(self,capa,neurons,inputs,function,layers,padre):
        self.error = 0.0
        self.deltas = [0.0] * neurons
        self.id = capa
        self.cant = neurons
        self.layers = layers
        self.padre = padre
        self.nodos = [Perceptron(str(capa)+'x'+str(x),inputs,function,padre) for x in xrange(neurons)]
        pass
        
    def getDeltas(self,expect,result):
        self.addLog("Layer->getDeltas("+str(expect)+","+str(result)+") capa:"+str(self.id))
        post = self.id + 1
        prev = self.id -1
        capa = self.id
        self.deltas = [0.0] * self.cant
        
        if self.id == len(self.layers) -1:
            self.error = 0.0
            
            for k in xrange(self.cant):
                self.error = expect[k] - result[k]
                self.nodos[k].setError(self.error)
                derivada = self.nodos[k].fnTransf.train(result[k])
                self.deltas[k] = derivada * self.error
                self.nodos[k].setDelta(self.deltas[k])
                
                self.addLog(">> "+str(derivada)+"="+self.nodos[k].funcion+"("+str(str(result[k])+")"))
                self.addLog(">> (s) "+str(self.deltas[k])+"="+str(derivada)+"*"+str(self.error))
        else:            
            for j in xrange(self.cant):
                self.error = 0.0
                
                for k in xrange(self.layers[post].cant):
                    peso = self.layers[post].nodos[k].getPeso(j)
                    delta = self.layers[post].deltas[k]
                    self.error += delta * peso
                    
                    self.addLog(">> nodo["+str(j)+"].peso["+str(k)+"] "+str(self.error)+"+="+str(delta)+"*"+str(peso))
                
                derivada = self.nodos[j].fnTransf.train(self.nodos[j].salida)
                self.nodos[j].setError(self.error)                
                self.deltas[j] = derivada * self.error
                self.nodos[j].setDelta(self.deltas[j])   
                
                self.addLog(">> "+str(derivada)+"="+self.nodos[j].funcion+"("+str(self.nodos[j].salida)+")*"+str(self.error))
                self.addLog(">> (o) "+str(self.deltas[j])+"="+str(derivada)+"*"+str(self.error))
        
        return self.deltas
        
    def setDeltas(self,expect,result):
        self.addLog("Layer->setDeltas("+str(expect)+","+str(result)+") capa:"+str(self.id))
        post = self.id + 1
        prev = self.id -1
        capa = self.id

        if self.id == len(self.layers) -1:
            self.error = 0.0
            
            for k in xrange(self.cant):
                delta = expect[k] - result[k]
                self.nodos[k].setError(delta)
                self.error += delta
                self.deltas[k] = delta
                self.nodos[k].setDelta(delta)
                
                self.addLog(">> "+str(self.deltas[k])+"="+str(expect[k])+"-"+str(result[k]))            
        else:  
            self.error = 0.0
            for j in xrange(self.cant):
                error = 0.0
                
                for k in xrange(self.layers[post].cant):
                    peso = self.layers[post].nodos[k].getPeso(j)
                    delta = self.layers[post].deltas[k]
                    error += delta * peso
                    self.error += delta * peso
                    
                    self.addLog(">> nodo["+str(j)+"].peso["+str(k)+"] "+str(self.error)+"+="+str(delta)+"*"+str(peso))
                
                self.nodos[j].setError(error)                
                self.deltas[j] = error
                self.nodos[j].setDelta(self.deltas[j])   
                
                #self.addLog(">> "+str(derivada)+"="+self.nodos[j].funcion+"("+str(self.nodos[j].salida)+")*"+str(self.error))
                #self.addLog(">> (o) "+str(self.deltas[j])+"="+str(derivada)+"*"+str(self.error))                
              
            pass
            
    def setPesos(self,rate):
        self.addLog("Layer->setPesos("+str(rate)+") capa:"+str(self.id))
        post = self.id + 1
        prev = self.id - 1
        
        #if self.id == len(self.layers) -1:
        #for j in xrange(self.layers[prev].cant):
        for k in xrange(self.cant):
            for j in xrange(self.nodos[k].nInputs):
                derivada = self.nodos[k].fnTransf.train(self.nodos[k].getSalidaNeta())
                cambio = self.deltas[k] * derivada * self.nodos[k].entradas[j]
                peso = self.nodos[k].getPeso(j)
                self.nodos[k].setPeso(j, peso + rate*cambio)
                self.addLog(">> nodo["+str(k)+"].peso["+str(j)+"]="+str(peso)+"+"+str(rate)+"*"+str(cambio)+" = "+str(self.nodos[k].getPeso(j)))

    def getConfiguracion(self):
        capa = {
            'id'     : self.id,
            'error'  : self.error,
            'deltas' : self.deltas,
            'cant'   : self.cant,
            #'layers' : self.layers,
            'nodos'  : [
                self.nodos[x].getConfiguracion() 
                for x in xrange(self.cant)
            ]
        }
        return capa
    
    def getStrDeltas(self):
        return {'layer_'+str(self.id) : [
                self.nodos[x].getConfiguracion() 
                for x in xrange(self.cant)
            ]}
            
    def addLog(self,str):
        if self.padre.debug :
            self.padre.addLog(str)

    