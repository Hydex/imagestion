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
    def __init__(self,capa,neurons,inputs,function):
        self.error = 0.0
        self.deltas = [0.0] * neurons
        self.id = capa
        self.cant = neurons
        self.nodos = [Perceptron(str(capa)+'x'+str(x),inputs,function) for x in xrange(neurons)]
        pass
        
    def getDeltas(self):
        deltas = []
        post = capa + 1
        
        if capa == self.nCapas -1:
            deltas = [0] * len(result)
            error = 0.0
            
            for k in xrange(self.nCapas -1):
                error = expect[k] - result[k]
                deltas[k] = self.capas[capa][k].fnTransf.train(result[k]) * error
                self.capas[capa][k].setDelta(deltas[k])
                pass
        else:
            deltas = [0] * len(self.capas[capa])
            
            for j in xrange(len(self.capas[capa])):
                error = 0.0
                
                for k in xrange(len(self.capas[post]) -1):
                    error += deltas[k] * self.capas[post][k].getPeso(k)
                
                deltas[j] = self.capas[capa][j] * error
                pass
        
        return deltas
        