from Red import *
import json

O = 0.01 #0.000001
I = 0.99 #0.999999

#net = Net(2,1,[3,2,1],['TANSIG','TANSIG','TANSIG'])
net = Net(2,1,[3,2,1],['LOGSIG','LOGSIG','LOGSIG'])

print 'PESOS : '+str(net.getPesos())
print 'DELTA : '+str(net.getDeltas())
print 'ERROR : '+str(net.getErrores())

print "0 SIMULAR"
print str([O,O]) + ' => ' + str(net.simular([O,O]))
print str([O,I]) + ' => ' + str(net.simular([O,I]))
print str([I,O]) + ' => ' + str(net.simular([I,O]))
print str([I,I]) + ' => ' + str(net.simular([I,I]))

for x in range(1):
    print str(x+1)+" ENTRENAR"
    net.setEpochs(1000)
    net.entrenar([
            [O,O], [O,I], [I,O], [I,I]
        ],[
             [O],   [I],   [I],   [O]
        ])

    print str(x+1)+" SIMULAR"
    print str([O,O]) + ' => ' + str(net.simular([O,O]))
    print str([O,I]) + ' => ' + str(net.simular([O,I]))
    print str([I,O]) + ' => ' + str(net.simular([I,O]))
    print str([I,I]) + ' => ' + str(net.simular([I,I]))

    print 'PESOS : '+str(net.getPesos())
    print 'DELTA : '+str(net.getDeltas())
    print 'ERROR : '+str(net.getErrores())

#print "SINAPSIS:"+json.dumps(net.sinapsis, sort_keys=True,indent=4, separators=(',', ': '))
#net.panic = True
#print net.getHistorial()

if net.panic:
    print "print LOG"
    print net.printLog()
    print "print CONFIGURACION"
    print str(net)
    


#prueba 2
