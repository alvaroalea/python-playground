from __future__ import print_function
import sys
import os
import getopt

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def tarjeta_tipo(nombre):
    """
    return the long description of the card, and if is supported by this program
    """
    if (nombre=="ADV151-P"):
        return 1,1,"32 DI - Entradas Digitales"
    if (nombre=="ADV151-E"):
        return 1,1,"32 DI - Entradas Digitales tipo SOE"
    if (nombre=="ADV551-P"):
        return 1,1,"32 DO - Salidas Digitales"
    if (nombre=="AAI143-H"):
        return 1,2,"16 AI - Entradas Analogicas"
    if (nombre=="AAI543-H"):
        return 1,2,"16 A0 - Salidas Analogicas"
    if (nombre=="ALE111"):
        return 0,0,"Modulo Comunicaciones Ethernet"
    if (nombre=="ALE111Dup"):
        return 0,0,"Modulo Comunicaciones Ethernet (Redundante)"
    if (nombre=="ALP121"):
        return 0,0,"Modulo Comunicaciones Profibus"
    return 0,"bad card name"


def decodifica(filename,ntipo,controlador,nodo,slot):
   """
   rutina principal del programa, vuelca en std out la I/O list de esa tarjeta.
   """
   eprint ("explorando archivo:",filename)
   if ntipo==1:
        npins=32
   if ntipo==2:
        npins=16
   with open(filename,'rb') as fi:
    fi.seek(0x200,0)
    pinA = []
    otagA = []
    descA = []
    ftagA = []
    for a in range(npins):
        bpint=fi.read(32)
        btag=fi.read(16)
        bdesc=fi.read(32)
        bdummy=fi.read(16)
        tag=btag.decode('utf-8')

        pinA.append(bpint.decode('utf-8'))
        descA.append(bdesc.decode('utf-8'))
        if ntipo==1:
            otagA.append("")
            ftagA.append(tag)
        if ntipo==2:
            otagA.append(tag)
            ftagA.append(tag[3:])
    if ntipo==1:
        fi.seek(0xE00,0)
        for b in range(npins):
            btag=fi.read(16)
            bdesc=fi.read(32)
            bdummy=fi.read(80)
            descA[b]=bdesc.decode('utf-8')
    for c in range(npins):
        print(pinA[c], ";", otagA[c], ";", sep='', end='')
        print(controlador+":"+nodo+":"+slot+"-"+str(c+1), ";", sep='', end='')
        print(ftagA[c], ";", descA[c], sep='')




def main(argv):
 BKDIR = "C:\\CENTUMVP\\eng\\BKProject\\"
 PRJNAME = "YANBUMST"
 DOMAIN = "01"
 CONTROLER = "08"
 try:
      opts, args = getopt.getopt(argv,"hc:d:p:",["help","controler=","domain=","project="])
 except getopt.GetoptError:
      eprint ('error, tir get_io.py --help')
      sys.exit(2)
 for opt, arg in opts:
      if opt in('-h',"--help"):
         eprint ('usage:')
         eprint ('get_io.py --controler=NN, --domain=NN --project=tttttt')
         eprint ('get_io.py -c NN, -d NN -p tttttt')
         sys.exit()
      elif opt in ("-c", "--controler"):
         CONTROLER = arg
      elif opt in ("-d", "--domain"):
         DOMAIN = arg
      elif opt in ("-p", "--project"):
         PRJNAME = arg


 CTRNAME = "FCS"+DOMAIN+CONTROLER

 mypath = BKDIR + PRJNAME + "\\FCS" + DOMAIN + CONTROLER + "\\IOM"

 eprint ()
 eprint ("Centum VP I/O List exporter, V0.0.1 by A. Alea (C) 2020")
 eprint ("exploring proyect:", PRJNAME, " controler: FCS"+DOMAIN+CONTROLER  )

 nododir = os.listdir(mypath)

 eprint ("found",len(nododir)," nodes")

 for nodo in nododir:
    eprint (nodo)
    tmpdir = mypath+"\\"+nodo
    tmpfiles = os.listdir(tmpdir)
    for x in tmpfiles:
            if x.endswith(".edf"):
                tipo = x[1:-4]
                soportada,ntipo,texto = tarjeta_tipo(tipo)
                eprint ("Slot:",x[0], "tipo:",tipo, " - ", texto)
                if soportada==1:
                     decodifica(mypath+"\\"+nodo+"\\"+x,ntipo,CTRNAME,(nodo[4:]),(x[0]))
    eprint ()


if __name__ == "__main__":
    main(sys.argv[1:])
