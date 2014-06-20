from Red import *
import json

O = 0 #0.01 #0.000001
I = 1 #0.99 #0.999999

# Net(entradas,salidas,[nodos,...],[funciones])
net = Net(2,1,[2,1],['TANSIG','TANSIG'])
#net = Net(2,1,[2,2,1],['LOGSIG','LOGSIG','LOGSIG'])
print 'NET   : Net(2,1,[2,1],[LOGSIG,LOGSIG])'
print 'PESOS : '+str(net.getPesos())
print 'DELTA : '+str(net.getDeltas())
print 'ERROR : '+str(net.getErrores())

print "0 SIMULAR"
print str([O,O]) + ' => ' + str(net.simular([O,O]))
print str([O,I]) + ' => ' + str(net.simular([O,I]))
print str([I,O]) + ' => ' + str(net.simular([I,O]))
print str([I,I]) + ' => ' + str(net.simular([I,I]))

for x in range(2):
    print str(x+1)+" ENTRENAR"
    net.setEpochs(100)
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

    print 'PESOS    : '+str(net.getPesos())
    print 'DELTA    : '+str(net.getDeltas())
    print 'LIST_ERR : '+str(net.getErrores())
    print 'CUAD_ERR : '+str(net.error)

#print "SINAPSIS:"+json.dumps(net.sinapsis, sort_keys=True,indent=4, separators=(',', ': '))
#net.panic = True
#print net.getHistorial()

print ""
print "print CONFIGURACION:"
print net.getConfiguracion()
 

with open("neural-network.json", "w") as text_file:
    text_file.write(dumps(net.getConfiguracion(), sort_keys=True,indent=4, separators=(',', ': ')))
    
if net.panic:
    print "print LOG"
    print net.printLog()
    


#prueba 2
