# +-----------------------------------------------------------------------+
# | IMAGESTION                                                            |
# |                                                                       |
# | Copyright (C) 2010-Today, GNUCHILE.CL - Santiago de Chile             |
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

from Activacion import *
from random import *
from json import *

class Perceptron(object):

    """
    :version: 1.0
    :author:  Miguelote
    """

    def __init__(self,name,inputs,funcion):
        self.entradas = [0 for x in xrange(inputs)] 
        self.pesos    = [random() for x in xrange(inputs)]
        self.log      = []
        self.name     = name
        self.rate     = 0.5
        self.bias     = 0.0
        self.wBias    = 0.0
        self.salida   = 0.0
        self.sigma    = 0.0 #random() #0.0
        self.funcion  = funcion
        self.fnTransf = Activacion(funcion)
        pass
        
    def getSumPesosEntradas(self):
        i    = 0
        suma = 0.0
        
        try:
            for i in range(len(self.entradas)):
                suma += self.entradas[i] * self.pesos[i]
                #self.addLog(str(suma)+" = "+str(self.entradas[i])+" * "+str(self.pesos[i]))
            pass
            
        except:
            err = exc_info()[0]
            self.addLog ("ERROR en Perceptron.getSumPesosEntradas() - Iteracion i="+str(i))
            self.addLog (err)
            
        return suma + self.bias*self.wBias
        
    def calcular(self):
        #self.addLog("Perceptron.calcular(name:"+self.name+", entradas:"+str(self.entradas)+')')
        suma = self.getSumPesosEntradas()
        self.setSalida(suma)
        res = self.fnTransf.exe(self.salida)
        return res
            
    def setCoeficiente(self,i,sigma):
        #if i<=len(self.pesos):
        self.sigma += self.pesos[i] * sigma
        pass
     
    def getCoeficiente(self,i):
        #if i<=len(self.pesos):
        return self.pesos[i] * self.sigma
     
    def balancearPesos(self):
        e = self.getSumPesosEntradas()
##        output = self.salida
##        e = self.calcular() 
##        self.salida = output           
         
        for i in range(len(self.pesos)):
            peso = self.pesos[i]
            fn = self.fnTransf.train(e)
            prod = self.rate*self.sigma*self.salida*fn
            self.addLog(str(peso + prod)+' = '+self.name+'.'+self.funcion+'('+str(e)+'):'+str(fn)+' * '+str(self.rate)+' * '+str(self.sigma)+' * '+str(self.entradas[i])+' + '+str(peso))
            self.pesos[i] = peso + prod
            pass
         
    """
    # setSigma
    # 
    #  Al comparar la senal de salida con una respuesta deseada o salida objetivo,
    #  d(t), se produce una senal de error, e(t), energia de error. Senal de error
    #  en la neurona de salida j en la iteracion t
    #          e(t)=d(t) - y(t)
    #  donde t denota el tiempo discreto, y(t) representa la salida de la capa previa.
    # 
    #  Regla Delta Generalizada Es una extension de la regla delta propuesta por Widrow (1960).
    #  Se usa en redes con capas intermedias con conexiones hacia delante y cuyas celulas
    #  tienen funciones de activacion continuas. Estas funciones continuas son no decrecientes
    #  y derivables (la funcion sigmoidal pertenece a este tipo de funciones).
    #
    """ 
    
    def setSigma(self,sigma):
        self.sigma = sigma
        pass
        
    def getSigma(self):
        return self.sigma
        pass
        
    def setBias(self,bias):
        self.bias = bias
        pass
    
    def getBias(self):
        return self.bias
    
    def setSalida(self,salida):
        self.salida = salida
        pass
        
    def getSalida(self):
        return self.salida
    
    def getwBias(self):
        return self.wBias
    
    def setwBias(self,bias):
        self.wBias = bias
        pass
        
    def setPeso(self,idx,peso):
        self.pesos[idx] = peso
        pass
        
    def getPeso(self,idx):
        return self.pesos[idx]
    
    def getPesos(self):
        return self.pesos
    
    def setId(self,id):
        self.id = id
        pass
        
    def getId(seld):
        return self.id
    
    def inicializarPesos(self):
        pass
        
    def getConfiguracion(self):
        data = {
            'entradas':self.entradas,
            'pesos':self.pesos,
            'name':self.name,
            'rate':self.rate,
            'bias':self.bias,
            'wBias':self.wBias,
            'salida':self.salida,
            'sigma':self.sigma,
            'funcion':self.funcion             
        }

        return data
        pass
        
    def getEntradas(self):
        return self.entradas
        pass
        
    def setConfiguracion(self):
        pass
        
    def addLog(self,str):
        self.log.append(str)
        #print str
        pass
        
    def getLog(self):
        log = self.log
        self.log = []
        return log
        pass
        
    def printLog(self):
        #print dumps(self.log, sort_keys=True,indent=4, separators=(',', ': '))
        pass
