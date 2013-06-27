from Red import *
import json

net = Red(2,1,[2,3,1],['LOGSIG','LOGSIG','LOGSIG'])

#print net.getConfiguracion()

for i in range(len(net.capas)):
    for j in range(len(net.capas[i])):
        #print "capas["+str(i)+"]["+str(j)+"]entradas:"+json.dumps(net.capas[i][j].entradas, sort_keys=True,indent=4, separators=(',', ': '))
        print "capas["+str(i)+"]["+str(j)+"]."+net.capas[i][j].name+".pesos   :"+json.dumps(net.capas[i][j].pesos, sort_keys=True,indent=4, separators=(',', ': '))
#print net.capas

print "SIMULAR"
print net.simular([0.5,0.6])

print "sinapsis:"+json.dumps(net.sinapsis, sort_keys=True,indent=4, separators=(',', ': '))

print "ENTRENAR"
net.entrenar([
        [0.0,0.0], [0.0,1.0], [1.0,0.0], [1.0,1.0]
    ],[
        [0.0], [1.0], [1.0], [0.0]
    ])

print "sinapsis:"+json.dumps(net.sinapsis, sort_keys=True,indent=4, separators=(',', ': '))

print "print LOG"
print net.printLog()


#prueba 2
