from Red import *
import json

O = 1 #0.000001
I = -1 #0.999999

#net = Net(2,1,[2,1],['TANSIG','TANSIG'])
net = Net(2,1,[2,1],['LOGSIG','LOGSIG'])

#print net.getConfiguracion()

#for i in range(len(net.capas)):
#    for j in range(len(net.capas[i])):
#        #print "capas["+str(i)+"]["+str(j)+"]entradas:"+json.dumps(net.capas[i][j].entradas, sort_keys=True,indent=4, separators=(',', ': '))
#        print "capas["+str(i)+"]["+str(j)+"]."+net.capas[i][j].name+".pesos   :"+json.dumps(net.capas[i][j].pesos, sort_keys=True,indent=4, separators=(',', ': '))
print 'PESOS  : '+str(net.getPesos())
print 'DELTAS : '+str(net.getDeltas())
print 'ERRORES: '+str(net.getErrores())

print "0 SIMULAR"
print str([O,O]) + ' => ' + str(net.simular([O,O]))
print str([O,I]) + ' => ' + str(net.simular([O,I]))
print str([I,O]) + ' => ' + str(net.simular([I,O]))
print str([I,I]) + ' => ' + str(net.simular([I,I]))

for x in range(1):
    #print str(x+1)+" ENTRENAR"
    net.setEpochs(15)
    net.entrenar([
            #[0.0001,0.0001], [0.0001,1.0], [1.0,0.0001], [1.0,1.0]
            [O,O], [O,I], [I,O], [I,I]
        ],[
             [0],   [1],   [1],   [0]
        ])

    print str(x+1)+" SIMULAR"
    print str([O,O]) + ' => ' + str(net.simular([O,O]))
    print str([O,I]) + ' => ' + str(net.simular([O,I]))
    print str([I,O]) + ' => ' + str(net.simular([I,O]))
    print str([I,I]) + ' => ' + str(net.simular([I,I]))

    print 'PESOS  : '+str(net.getPesos())
    print 'DELTAS : '+str(net.getDeltas())
    print 'ERRORES: '+str(net.getErrores())

#print "SINAPSIS:"+json.dumps(net.sinapsis, sort_keys=True,indent=4, separators=(',', ': '))
#net.panic = True

if net.panic:
    print "print LOG"
    print net.printLog()
    print "print CONFIGURACION"
    print net.getConfiguracion()
    
print net.getHistorial()


#prueba 2
