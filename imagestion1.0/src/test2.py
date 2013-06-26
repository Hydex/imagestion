from Red import *
import json

net = Red(2,2,[2,3,2],['LOGSIG','LOGSIG','LOGSIG'])

print "sinapsis:"+json.dumps(net.sinapsis, sort_keys=True,indent=4, separators=(',', ': '))

for i in range(len(net.capas)):
    for j in range(len(net.capas[i])):
        #print "capas["+str(i)+"]["+str(j)+"]entradas:"+json.dumps(net.capas[i][j].entradas, sort_keys=True,indent=4, separators=(',', ': '))
        print "capas["+str(i)+"]["+str(j)+"]."+net.capas[i][j].name+".pesos   :"+json.dumps(net.capas[i][j].pesos, sort_keys=True,indent=4, separators=(',', ': '))
#print net.capas

print net.simular([0.5,0.6])

print net.sinapsis

print net.getConfiguracion()

#prueba 2
