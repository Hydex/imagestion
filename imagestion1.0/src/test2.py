from Red import *

net = Red(2,1,[2,3,1],['LOGSIG','LOGSIG','LOGSIG'])

print net.sinapsis
#print net.capas

print net.simular([0.5,0.6])

print net.sinapsis
