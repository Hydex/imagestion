from Red import *
import json

O = 0 #0.01 #0.000001
I = 1 #0.99 #0.999999

# Net(entradas,salidas,[nodos,...],[funciones])
net = Net(2,1,[2,1],['TANSIG','TANSIG'])
#net = Net(2,1,[2,1],['LOGSIG','LOGSIG'])
net.debug = True

print 'NET   : Net(2,1,[2,1],'+str(net.transferencias)+')'
print 'PESOS : '+str(net.getPesos())
print 'DELTA : '+str(net.getDeltas())
print 'ERROR : '+str(net.getErrores())

print "0 SIMULAR"
print str([O,O]) + ' => ' + str(net.simular([O,O]))
print str([O,I]) + ' => ' + str(net.simular([O,I]))
print str([I,O]) + ' => ' + str(net.simular([I,O]))
print str([I,I]) + ' => ' + str(net.simular([I,I]))
print ""

f = open('referencia.json', 'r')
jsNet = f.read();
f.close()
net.setConfiguracion(jsNet)
 
print "1 SIMULAR"
print str([O,O]) + ' => ' + str(net.simular([O,O]))
print str([O,I]) + ' => ' + str(net.simular([O,I]))
print str([I,O]) + ' => ' + str(net.simular([I,O]))
print str([I,I]) + ' => ' + str(net.simular([I,I]))
print ""

print "print CONFIGURACION:"
print net.getConfiguracion();
#print dumps(net.getConfiguracion(), sort_keys=True,indent=4, separators=(',', ': '))
print ""
    
if net.panic:
    print "print LOG"
    print net.printLog()
    


#prueba 2
