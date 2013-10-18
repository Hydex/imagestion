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
    def __init__(self,capa,inputs,function,layers):
        self.error = 0.0
        self.deltas = [0.0] * inputs
        self.id = capa
        self.cant = inputs
        self.layers = layers
        self.nodos = [Perceptron(str(capa)+'x'+str(x),inputs,function) for x in xrange(inputs)]
        pass
        
    def getDeltas(self,expect,result):
        post = self.id + 1
        self.deltas = [0.0] * self.cant
        
        if self.id == len(self.layers) -1:
            self.error = 0.0
            
            for k in xrange(self.cant -1):
                self.error = expect[k] - result[k]
                self.deltas[k] = self.nodos[k].fnTransf.train(result[k]) * self.error
                self.nodos[k].setDelta(self.deltas[k])
        else:            
            for j in xrange(self.cant -1):
                self.error = 0.0
                
                for k in xrange(self.layers[post].cant -1):
                    self.error += self.layers[post].deltas[k] * self.layers[post].nodos[k].getPeso(k)
                
                self.deltas[j] = self.nodos[j] * self.error
        
        return self.deltas
        
    def setPesos(self,rate):
        post = self.id + 1
        prev = self.id - 1
        
        #if self.id == len(self.layers) -1:
        for j in xrange(self.layers[prev].cant) -1:
            for k in xrange(self.cant) -1:
                cambio = self.deltas[k] * self.layers[prev].nodos[j].salida
                peso = self.nodos[k].getPeso(j)
                self.nodos[k].setPeso(j, peso + rate*cambio)

        