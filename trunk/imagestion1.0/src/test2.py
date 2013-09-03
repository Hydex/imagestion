from Red import *
import json

O = 0 #0.000001
I = 1 #0.999999

#net = Red(2,1,[2,1],['TANSIG','TANSIG'])
net = Red(2,1,[2,1],['LOGSIG','LOGSIG'])

#print net.getConfiguracion()

#for i in range(len(net.capas)):
#    for j in range(len(net.capas[i])):
#        #print "capas["+str(i)+"]["+str(j)+"]entradas:"+json.dumps(net.capas[i][j].entradas, sort_keys=True,indent=4, separators=(',', ': '))
#        print "capas["+str(i)+"]["+str(j)+"]."+net.capas[i][j].name+".pesos   :"+json.dumps(net.capas[i][j].pesos, sort_keys=True,indent=4, separators=(',', ': '))
print 'PESOS: '+str(net.getPesos())
print 'SIGMAS: '+str(net.getSigmas())

##print "SIMULAR"
##print net.simular([0.0,1.0])
##print "sinapsis:"+json.dumps(net.sinapsis, sort_keys=True,indent=4, separators=(',', ': '))

for x in range(2):
    print str(x)+" ENTRENAR"
    net.setEpochs(100)
    net.entrenar([
            #[0.0001,0.0001], [0.0001,1.0], [1.0,0.0001], [1.0,1.0]
            [O,O], [O,I], [I,O], [I,I]
        ],[
            [0], [1], [1], [0]
        ])

    print str(x)+" SIMULAR"
    print str([0,0]) + ' => ' + str(net.simular([O,O]))
    print str([0,1]) + ' => ' + str(net.simular([O,I]))
    print str([1,0]) + ' => ' + str(net.simular([I,O]))
    print str([1,1]) + ' => ' + str(net.simular([I,I]))

    print 'PESOS: '+str(net.getPesos())
    print 'SIGMAS: '+str(net.getSigmas())

#print "SINAPSIS:"+json.dumps(net.sinapsis, sort_keys=True,indent=4, separators=(',', ': '))
#net.panic = True

if net.panic:
    print "print LOG"
    print net.printLog()
    print "print CONFIGURACION"
    print net.getConfiguracion()


#prueba 2
