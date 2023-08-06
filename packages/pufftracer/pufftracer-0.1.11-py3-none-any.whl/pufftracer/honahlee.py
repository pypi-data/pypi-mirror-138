#! Python
#HonahLee.py
'''
HonahLee: The place where Puff the magic dragon lives, as
well as other magical creatures. A place transparent and
with structures of patent frangibility with no secrets.

Changes
===============================================================================
16-Jan-2022 12:19:47 pm Initial part of 0.1.10
'''

import pufftracer.pufftrc as puff

idx = 0

def opossum ():
    global idx
    for idx in range(10):
        print("opossum on iteration", idx)

def foo ():
    x = 5
    y = 12
    z = 2*x+y
    baz()
     
def baz ():
    print ("In baz")
     
def recurse (n):
    print(n)
    if n > 0:
        recurse(n-1)
    else:
        print('Hit Bottom')

def jack ():
    recurse(3)

def jill ():
    global idx
    print("Entered jill")
    oldidx = idx
    for x in range(3):
        idx += 1
        for y in range(3):
            z = idx * 100 + x * 10 + y
    idx = oldidx
            
    
def showall ():
    global Trc
    Trc = puff.Puff()
    Trc.focus(__file__)
    # can also focus Trc.focus(module)
    Trc.On(nest=1)
    input("waiting on you\n")
    
    foo()
    Trc.On(nest=2)
    foo()
    recurse(5)
    Trc.On(funcs='foo')
    input('waiting on you A !\n')
    
    foo()
    Trc.On(funcs='baz')
    input('waiting on you B !\n')
    
    foo()
    Trc.On(funcs=('foo', baz))
    input('waiting on you C !\n')
    
    foo()
    recurse(5)
    Trc.Off()
    Trc.Resume()
    input("waiting on you D !\n")
    
    foo()
    Trc.On(lines=21)
    input("waiting on you E !\n")
    
    print("\t***** Only tracing line 21")
    foo()
    Trc.On(funcs=[jack, recurse])
    input("waiting on you F !\n")
    
    jack()
    Trc.On(callsonly=True)
    
    input("waiting on you G  !\n")
    jack()
    
    Trc.Watch(lcls="x, y, z", globs="idx")
    Trc.On()
    jill()
    Trc.Watch()
    Trc.Off()
    Trc.On(funcs=opossum)
    input("waiting on you H  !\n")
    
    Trc.StopWhen(lambda : idx > 4)
    opossum()
    print("\t\tShould not get here!!!")
    Trc.Off()
    print("Good Bye!")

if __name__ == "__main__":
    showall()
    
