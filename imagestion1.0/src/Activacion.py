# +-----------------------------------------------------------------------+
# | IMAGESTION                                                            |
# |                                                                       |
# | Copyright (C) 2010-Today, GNUCHILE.CL	- Santiago de Chile           |
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

class Activacion(object):

    """
    funciones de activacion para la simulacion y entrenamiento
    de un perceptron

    :version: 1.0
    :author:  Miguelote
    """

    def __init__(self,type):
        self.tipo = type
        self.funciones = {
            "HARDLIM":"hardlim(expr)",
            "HARDLIMS":"hardlim(expr)",
            "POSLIN":"poslin(expr)",
            "PURELIN":"purelin(expr)",
            "SATLIN":"satlin(expr)",
            "SATLINS":"satlins(expr)",
            "LOGSIG":"logsis(expr)",
            "TANSIG":"tansig(expr)",
            "RADBAS":"radbas(expr)",
            "UNDEFINED":"undefined(expr)"
        }
        self.derivadas = {
            "LOGSIG":"logsis_derivada(expr)",
            "TANSIG":"tansig_derivada(expr)",
            "PURELIN":"purelin_derivada(expr)",
            "POSLIN":"poslin_derivada(expr)",
            "RADBAS":"undefined(expr)",
            "UNDEFINED":"undefined(expr)"
        }
        pass
    
    def exe(self,val):
        valor   = null
        funcion = self.funciones[self.tipo].replace('expr',val)
        exec "valor = "+funcion
        return valor
        pass
        
    def train(self,val):
        valor   = null
        funcion = self.derivadas[self.tipo].replace('expr',val)
        exec "valor = "+funcion
        return valor
        pass
        
    def hardlim(self,val):
        return 0.0 if val < 0.0 else 1.0
        pass
        
    def hardlims(self,val):
        return -1.0 if val < 0.0 else 1.0
        pass
        
    def poslin(self,val):
        return 0.0 if val < 0.0 else val
        pass
        
    def purelin(self,val):
        return val
        pass
        
    def satlin(self,val):
        return 0.0 if val < 0.0 else 1.0 if val > 1.0 else val
        pass
        
    def satlins(self,val):
        return -1.0 if val < -1.0 else 1.0 if val > 1.0 else val
        pass
        
    def logsis(self,val):
        return 1.0 / (1.0 + math.exp(-val))
        pass
        
    def tansig(self,val):
        return (math.exp(val) - math.exp(-val)) / (math.exp(val) + math.exp(-val))
        pass
        
    def radbas(self,val):
        pass
        
    def logsis_derivada(self,val):
        return val * (1.0 - val)
        pass
        
    def tansig_derivada(self,valor):
        val = self.tansig(valor)
        return 1 - val*val
        pass
        
    def poslin_derivada(self,val):
        return 1.0
        pass
        
    def purelin_derivada(self,val):
        return 1.0
        pass
        
    def undefinded(self,val):
        return null
        pass
        
    
    

