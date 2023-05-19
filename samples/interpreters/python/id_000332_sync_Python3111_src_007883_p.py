








"storeprint.py" which can be used to obtain








"to900text.py" which converts a UTF-8 character file to its






"from900text.py"









"traceprint.py" that produces am





import sys
import os.path
import argparse
import time



dynStop   =   0  
rdrStop   =   1  
ttyStop   =   2  
limitStop =   3  
otherStop = 255  

def finish (code):
    
    writeStoreToFile ()
    endTracing () 
    closeReader () 
    closePunch ()
    closeTTY ()
    sys.exit(code)

def failure (s, code):
    print ('\n\n***Halted - ', s)
    finish (code)



bit19    = 1<<18    
mask18   = 0o777777
bit18    = 1<<17
mask16   = 0o177777 
addrMask = 8191     
modMask  = 0o160000 


def normal (n):
    if n >= bit18:
        return n - bit19
    else:
        return n


traceDefault = '.trace'
tracePath    = traceDefault
traceFile    = None

def startTracing ():
    global traceFile
    try:
        traceFile = open(tracePath, 'w')
    except:
        failure('cannot open trace file ' + tracePath, otherStop)

def endTracing ():
    if not (traceFile is None):
        traceFile.close()

def trace (s):
    if not (traceFile == None):
        traceFile.write(s+'\n')


maxStore = 16*1024
store = [0 for addr in range(maxStore)]

def clearStore ():
    for word in store:
        word = 0





storePath = '.store'

def readStoreFromFile ():
    
    if not os.path.exists(storePath):
        clearStore()
    else:
        with open (storePath) as f:
            words = [int(x) for x in f.read().split()]
        store[:len(words)] = words

def writeStoreToFile ():
    with open(storePath, mode='w') as f:
        for i in range(maxStore):
         print('%7d' % store[i], file=f, end=('\n' if i % 10 == 9 else ''))


ptrDefault = '.reader'
ptrPath    = ptrDefault 
ptrBuf     = None
ptrIdx     = 0

ptpDefault = '.punch'
ptpPath    = ptpDefault 
ptpFile    = None

ttyInDefault = '.ttyin'
ttyInPath    = ttyInDefault 
ttyInBuf     = None
ttyInIdx     = 0


def closeReader ():
    if not (ptrBuf is None):
        
        try:
            with open(ptrDefault, 'wb') as f:
                f.write(ptrBuf[ptrIdx:])
        except: failure('cannot save remaining paper tape to ' + ptrDefault,
                        otherStop)


def closePunch ():
    if not (ptpFile is None):
        ptpFile.close()


def readTape ():
    global ptrBuf, ptrIdx
    if ptrBuf is None:
        try:
            with open(ptrPath, 'rb') as f: 
                ptrBuf = f.read()
        except: failure('cannot open ptr input file ' + ptrPath, otherStop)
    if ptrIdx >= len(ptrBuf):
        msg = 'run off end of input tape'
        trace(msg)
        failure(msg, rdrStop)
    code = ptrBuf[ptrIdx]
    if code < 0 | code > 128:
        failure('invalid code in paper tape input - %d' & code, otherStop)
    ptrIdx+=1
    if not (traceFile is None):
        trace('ptr read code %3d' % code)
    return code


def closeTTY ():
    if (not ttyInBuf is None):
        try:
            with open(ttyInDefault, 'wb') as f:
                f.write(ttyInBuf[ttyInIdx:])
        except: failure('cannot save remaining teletype input to ' +
                         ttyInDefault, otherStop)


def readTTYIn ():
    global ttyInBuf, ttyInIdx
    if ttyInBuf is None:
        try:
            with open(ttyInPath, 'rb') as f: 
                ttyInBuf = f.read()
        except: failure('cannot open tty input file ' + ttyInPath, otherStop)
    if ttyInIdx >= len(ttyInBuf):
        msg = 'run off end of tty input'
        trace(msg)
        failure(msg, ttyStop)
    code = ttyInBuf[ttyInIdx]
    if code < 0 | code > 128:
        failure('invalid code in tty input - %d' & code, otherStop)
    ttyInIdx+=1
    if not (traceFile is None):
        trace('tty read code %3d' % code)
    return code


def punchTape (code):
    global   ptpFile
    if ptpFile is None:
        try:
            ptpFile = open(ptpPath, 'wb') 
        except: failure('cannot open paper tape output file ' + ptpPath,
                        otherStop)
    ptpFile.write(bytes([code]))

def readTTY ():
    failure('teletype input from console not implemented', otherStop)

def writeTTY (code):
    ch = code & 127
    if ch == 10 or 32 <= ch <= 122:
        sys.stdout.write(chr(ch))




aReg = 0
qReg = 0


level = 1


sLevel1 = 0
bLevel1 = 1
sLevel4 = 6
bLevel4 = 7

scr  = sLevel1
bReg = bLevel1

def makeIns (m, f, n):
    
    return (((m << 4) + f) << 13) + n


def establishInitialInstructions ():
    store[8180] = (-3 & mask18)
    store[8181] = makeIns(0,  0, 8180)
    store[8182] = makeIns(0,  4, 8189)
    store[8183] = makeIns(0, 15, 2048)
    store[8184] = makeIns(0,  9, 8186)
    store[8185] = makeIns(0,  8, 8183)
    store[8186] = makeIns(0, 15, 2048)
    store[8187] = makeIns(1,  5, 8180)
    store[8188] = makeIns(0, 10,    1)
    store[8189] = makeIns(0,  4,    1)
    store[8190] = makeIns(0,  9, 8182)
    store[8191] = makeIns(0,  8, 8177)





def loadB(addr):
    global qReg
    qReg = store[addr]
    store[bReg] = qReg


def add (addr):
    global aReg
    aReg = (aReg + store[addr]) & mask18


def negAdd (addr):
    global aReg, qReg
    qReg = store[addr]
    aReg = (qReg - aReg) & mask18


def storeQ (addr):
    store[addr] = qReg >> 1


def loadA (addr):
    global aReg
    aReg = store[addr]



def storeALevel1 (addr):
    global store
    if 8180 <= addr <= 8191: 
        trace('write to initial instructions ignored')
        return
    store[addr] = aReg

def storeALevel4 (addr):
    global store
    store[addr] = aReg


def collate (addr):
    global aReg
    aReg &= store[addr]


def jumpZ (addr):
    global store
    if aReg == 0:
        store[scr] = addr


def jump (addr):
    global store
    store[scr] = addr


def jumpN (addr):
    global store
    if aReg >= bit18:
        store[scr] = addr


def count (addr):
    global store
    store[addr] = (store[addr] + 1) & mask18


def storeS (addr):
    global qReg, store
    s = store[scr]
    qReg = s & modMask
    store[addr] = s & addrMask













def multiply (addr):
    global aReg, qReg
    a = normal(aReg)
    intprod = (a * normal(store[addr]))
    qReg = (intprod <<  1) & mask18
    "undefined".
    if a<0:
        qReg = qReg | 1
    aReg = (intprod >> 17) & mask18























def divide(addr):
	global aReg, qReg
	aq = (normal(aReg) << 18) | qReg
	m  = normal(store[addr])
	intquot = ((aq // m) >> 1) & mask18
	aReg = intquot | 1
	qReg = intquot & 0o777776


















def shift (addr):
    global aReg, qReg
    places = addr & addrMask
    aq = (aReg << 18) | qReg
    if places <= 2047:
        aq = aq << places
        aReg = (aq >> 18) & mask18
        qReg = aq & mask18
    elif places >= 6144:
        places = 8192-places
        aq = ((normal(aReg) << 18) | qReg) >> places
        aReg = (aq >> 18) & mask18
        qReg = aq & mask18
    else:
        failure('unsupported i/o 14 %4d' & places, otherStop)


def inOut (addr):
    global aReg, level, scr, bReg, putStore, functionDict
    opAddr = addr & addrMask
    if opAddr == 7168:
        
        level = 4
        scr = sLevel4
        bReg = bLevel4
        functionDict[5] = storeALevel4
    elif opAddr == 2048:
        byte = readTape()
        aReg = ((aReg << 7) | byte) & mask18
    elif opAddr == 2052:
        byte = readTTYIn()
        aReg = ((aReg << 7) | byte) & mask18
    elif opAddr == 6144:
        punchTape(aReg & 255)
    elif opAddr == 6148:
        writeTTY(aReg & 255)
    else:
        failure('Unsupported i/o 15 %4d' % opAddr, otherStop)


functionDict = {  0: loadB,     1: add,           2: negAdd,   3: storeQ,
                  4: loadA,     5: storeALevel1,  6: collate,  7: jumpZ,
                  8: jump,      9: jumpN,        10: count,   11: storeS,
                 12: multiply, 13: divide,       14: shift,   15: inOut}



lastS = 0  

limit = 200000000 

def decode ():
    global lastS, limit, scr
    
    while limit > 0: 
        limit -= 1
        
        lastS = store[scr]
        store[scr] += 1
        
        instruction = store[lastS]
        f = (instruction >> 13) & 15
        a = (instruction & addrMask) | (lastS & modMask)
        m = ((a + store[bReg]) if instruction >= bit18 else a) & mask16
        trace('%d %d %d %d %d' % (lastS, instruction, aReg, qReg, store[bReg]))
        functionDict[f](m)
        if store[scr] == lastS:
            msg = 'Dynamic stop at %d' % store[scr]
            trace(msg)
            
            return dynStop
    msg = 'execution limit reached'
    trace(msg)
    failure(msg, limitStop)

jumpAddr = 8181 


def getArgs():
    global ptrPath, ptpPath, ttyInPath, jumpAddr, limit
    parser = argparse.ArgumentParser()
    parser.add_argument('-ptin',  help='paper tape input file path',
                        default='')
    parser.add_argument('-ttyin',  help='teleprinter input file path',
                        default='')
    parser.add_argument('-ptout', help='paper tape output file path',
                        default='')
    parser.add_argument('-jump', help='start address', default='')
    parser.add_argument('-trace',help='turn on tracing to .trace',
                        action="store_true")
    parser.add_argument('-limit', help='instruction execution limit',
                        type=int)
    args = parser.parse_args()
    if args.ptin != '':
        ptrPath = args.ptin
    if args.ttyin != '':
        ttyInPath = args.ttyin
    if args.ptout != '':
        ptpPath = args.ptout
    if args.jump != '':
        addr = int(args.jump)
        if 8 <= addr <= 8181:
            jumpAddr = addr
        else:
            failure('start address must be in range 8-8181', otherStop)
    if args.trace:
        startTracing()
    if args.limit:
        if args.limit < 1:
            failure('nonsensical limit - %d', args.limit, otherStop)
        else:
            limit = args.limit


getArgs()                        
readStoreFromFile()              
if jumpAddr == 8181:
    establishInitialInstructions ()  
store[scr] = jumpAddr                

res = decode()                   


finish (res)








