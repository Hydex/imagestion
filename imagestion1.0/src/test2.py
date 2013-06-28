from Red import *
import json

net = Red(2,1,[2,3,1],['LOGSIG','LOGSIG','LOGSIG'])

#print net.getConfiguracion()

print "PESOS"
print net.getPesos()
#print "ENTRADAS"
#print net.getEntradas()
#print "SIMULAR"
#print net.simular([0.5,0.6])

#print "sinapsis:"+json.dumps(net.sinapsis, sort_keys=True,indent=4, separators=(',', ': '))

print "ENTRENAR"
net.entrenar([
        [0.1,0.1], [0.1,0.9], [0.9,0.1], [0.9,0.9]
    ],[
        [0.0], [1.0], [1.0], [0.0]
    ])

print "sinapsis:"+json.dumps(net.sinapsis, sort_keys=True,indent=4, separators=(',', ': '))

print "print LOG"
print net.printLog()


#prueba 2
