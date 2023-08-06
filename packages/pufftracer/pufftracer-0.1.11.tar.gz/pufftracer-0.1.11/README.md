# pufftrc Package
last change 10-Feb-2022
### An alternate method to interface to tracing.
A different approach to accomplish what is in the standard library documentation as:
>Debugging and profiling -> trace -> Programmatic Interface.

### Author: Daniel L. Bates	(dan.bates)
## The pypi module pufftracer
import pufftracer.pufftrc as puff
## The singleton class Puff
A singleton class "Puff" to provide interfaces to the code tracing magic in Python.
These interfaces to filter tracing to a list of function names. And/Or to show only
calls and returns. Or a maximum call depth.
To focus on one module at a time, and omit tracing outside that module. A
Means of turning the trace On, Off, and resuming it.  

A means of communicating a predicate function to Puff to evaluate at every line, and
stopping via an assert False when this function triggers by returning True.  

A means of providing lists of locals, nonlocals and global variables to be displayed
every time they are modified.  

A trace that calls attention to any non-sequential change in line number.  

A trace object of class Puff has these interfaces:  
```
Trc = puff.Puff()
Trc.focus(module name or module filename)
Trc.On(nest=100, lines=None, funcs=None, callsonly=False)
Trc.Off()
Trc.Resume()
Trc.StopWhen(condition_function)
Trc.Watch(lcls=IsNot, globs=IsNot, nonlcls=IsNot) where IsNot is an internal None
```
This is Puff the magic Debugging Dragon.  

Of Course an example/testing frame Honalee.py is provided.  

Where else can a Magic Dragon live than in Honalee.  

This is very much through the looking glass.  
## The Trc.focus member.
```
Usage pufftrc.Puff().focus(__file__)
or
focus(module.__file__)
```
Focus the trace (allow the trace) only on one module at a time and
that module cannot be pufftrc.

## The Trc.On member.
```
Trc.On(nest=100, lines=None, funcs=None, callsonly=False)
```
nest is an int which is the maximum level of call nesting to print
the trace for. A value of -1 indidcates no limit for call nesting.  

lines can be an int representing the single line number to be traced.
lines can also be a list of two ints representing a range of line
numbers. Line numbers are the most transiant measure to control the
trace, but they are available.  

funcs is either a function reference or the function name as a string,
or a list of function references, or a list of function names as
strings.  

callsonly is a boolean. Set to True only shows calls/returns in the
trace. Set to False means trace everything.  

## The Trc.Off member.
```
Trc.Off() 
```
Stops the trace.

## The Trc.Resume member.
```
Trc.Resume()
```
continues a trace printing with no changes to
the trace parameters in effect on the preceding Trc.Off().

## The Trc.StopWhen member.
```
Trc.StopWhen(stoptestfunc) 
```
Gives a reference to a predicate function
which returns True when an event occurs where you want the state
of the program preserved. The function should be optimized for the
path that returns False.

This call must be made after the Trc.On().

The function must be valid to execute in any environment. Variables must
remain in scope.

The function may be a lambda function, but it need not be. it can take the
form:
```
def StopTheWorld():
    if not <stop the world condition>:
        return False
    <other processing>
```
Where other processing can be a smart dump of the state or a breakpoint()

## The Trc.Watch member.
```
Trc.Watch(lcls=IsNot, globs=IsNot, nonlcls=IsNot)
```
Tells puff what variables to watch for modifications to.
Ideally variables will not fall out of scope. If they do we
do not monitor them.  

Variable that are local are in the lcls list, The global variables are in the
globs list and nonlocals in the nonlcls list.  

Variables must be simple, a good list would be like "x, y, z"
This part while useful is not bullet proof.  

## Sample Output
```
  "c:\0\honahlee.py"
*** Puff trace focused on module file :
	 C:\0\honahlee.py
***Tracing On, nest = 1 lines =None funcs = None callsonly = False
waiting on you
			*** "foo" called ***
honahlee.py(23):     x = 5
honahlee.py(24):     y = 12
honahlee.py(25):     z = 2*x+y
honahlee.py(26):     baz()
In baz
			*** return from "baz" ***
			*** return from "foo" ***
***Tracing On, nest = 2 lines =None funcs = None callsonly = False
			*** "foo" called ***
honahlee.py(23):     x = 5
honahlee.py(24):     y = 12
honahlee.py(25):     z = 2*x+y
honahlee.py(26):     baz()
			*** "baz" called ***
honahlee.py(29):     print ("In baz")
In baz
			*** return from "baz" ***
			*** return from "foo" ***
			*** "recurse" called ***
honahlee.py(32):     print(n)
5
honahlee.py(33):     if n > 0:
honahlee.py(34):         recurse(n-1)
			*** "recurse" called ***
honahlee.py(32):     print(n)
4
honahlee.py(33):     if n > 0:
honahlee.py(34):         recurse(n-1)
3
2
1
0
Hit Bottom
			*** return from "recurse" ***
			*** return from "recurse" ***
***Tracing On, nest = 100 lines =None funcs = ['foo'] callsonly = False
waiting on you A !
			*** "foo" called ***
honahlee.py(23):     x = 5
honahlee.py(24):     y = 12
honahlee.py(25):     z = 2*x+y
honahlee.py(26):     baz()
In baz
***Tracing On, nest = 100 lines =None funcs = ['baz'] callsonly = False
waiting on you B !
			*** "baz" called ***
honahlee.py(29):     print ("In baz")
In baz
			*** return from "baz" ***
***Tracing On, nest = 100 lines =None funcs = ['foo', 'baz'] callsonly = False
waiting on you C !
			*** "foo" called ***
honahlee.py(23):     x = 5
honahlee.py(24):     y = 12
honahlee.py(25):     z = 2*x+y
honahlee.py(26):     baz()
			*** "baz" called ***
honahlee.py(29):     print ("In baz")
In baz
			*** return from "baz" ***
			*** return from "foo" ***
5
4
3
2
1
0
Hit Bottom
***Tracing Off
***Tracing Resumed
waiting on you D !
			*** "foo" called ***
honahlee.py(23):     x = 5
honahlee.py(24):     y = 12
honahlee.py(25):     z = 2*x+y
honahlee.py(26):     baz()
			*** "baz" called ***
honahlee.py(29):     print ("In baz")
In baz
			*** return from "baz" ***
			*** return from "foo" ***
***Tracing On, nest = 100 lines =None funcs = None callsonly = False
waiting on you E !
	***** Only tracing line 21
			*** "foo" called ***
honahlee.py(23):     x = 5
honahlee.py(24):     y = 12
honahlee.py(25):     z = 2*x+y
honahlee.py(26):     baz()
			*** "baz" called ***
honahlee.py(29):     print ("In baz")
In baz
			*** return from "baz" ***
			*** return from "foo" ***
***Tracing On, nest = 100 lines =None funcs = ['jack', 'recurse'] callsonly = False
waiting on you F !
			*** "jack" called ***
honahlee.py(39):     recurse(3)
			*** "recurse" called ***
honahlee.py(32):     print(n)
3
honahlee.py(33):     if n > 0:
honahlee.py(34):         recurse(n-1)
			*** "recurse" called ***
honahlee.py(32):     print(n)
2
honahlee.py(33):     if n > 0:
honahlee.py(34):         recurse(n-1)
			*** "recurse" called ***
honahlee.py(32):     print(n)
1
honahlee.py(33):     if n > 0:
honahlee.py(34):         recurse(n-1)
			*** "recurse" called ***
honahlee.py(32):     print(n)
0
honahlee.py(33):     if n > 0:
Line number sequence break	...
honahlee.py(36):         print('Hit Bottom')
Hit Bottom
			*** return from "recurse" ***
			*** return from "recurse" ***
			*** return from "recurse" ***
			*** return from "recurse" ***
			*** return from "jack" ***
***Tracing On, nest = 100 lines =None funcs = None callsonly = True
waiting on you G  !
			*** "jack" called ***
			*** "recurse" called ***
3
			*** "recurse" called ***
2
			*** "recurse" called ***
1
			*** "recurse" called ***
0
Hit Bottom
			*** return from "recurse" ***
			*** return from "recurse" ***
			*** return from "recurse" ***
			*** return from "recurse" ***
			*** return from "jack" ***
*** Watch Puff.lcls={'x': IsNot, 'y': IsNot, 'z': IsNot}
*** Watch Puff.globs={'idx': IsNot}
***Tracing On, nest = 100 lines =None funcs = None callsonly = False
			*** "jill" called ***
	>>>>>>> global idx initially set to 0
honahlee.py(43):     print("Entered jill")
Entered jill
honahlee.py(44):     oldidx = idx
honahlee.py(45):     for x in range(3):
	>>>>>>> local x initially set to 0
honahlee.py(46):         idx += 1
	>>>>>>> global idx was 0 is now set to 1
honahlee.py(47):         for y in range(3):
	>>>>>>> local y initially set to 0
honahlee.py(48):             z = idx * 100 + x * 10 + y
	>>>>>>> local z initially set to 100
Line number sequence break	...
honahlee.py(47):         for y in range(3):
	>>>>>>> local y was 0 is now set to 1
honahlee.py(48):             z = idx * 100 + x * 10 + y
	>>>>>>> local z was 100 is now set to 101
Line number sequence break	...
honahlee.py(47):         for y in range(3):
	>>>>>>> local y was 1 is now set to 2
honahlee.py(48):             z = idx * 100 + x * 10 + y
	>>>>>>> local z was 101 is now set to 102
Line number sequence break	...
honahlee.py(47):         for y in range(3):
Line number sequence break	...
honahlee.py(45):     for x in range(3):
	>>>>>>> local x was 0 is now set to 1
honahlee.py(46):         idx += 1
	>>>>>>> global idx was 1 is now set to 2
honahlee.py(47):         for y in range(3):
	>>>>>>> local y was 2 is now set to 0
honahlee.py(48):             z = idx * 100 + x * 10 + y
	>>>>>>> local z was 102 is now set to 210
Line number sequence break	...
honahlee.py(47):         for y in range(3):
	>>>>>>> local y was 0 is now set to 1
honahlee.py(48):             z = idx * 100 + x * 10 + y
	>>>>>>> local z was 210 is now set to 211
Line number sequence break	...
honahlee.py(47):         for y in range(3):
	>>>>>>> local y was 1 is now set to 2
honahlee.py(48):             z = idx * 100 + x * 10 + y
	>>>>>>> local z was 211 is now set to 212
Line number sequence break	...
honahlee.py(47):         for y in range(3):
Line number sequence break	...
honahlee.py(45):     for x in range(3):
	>>>>>>> local x was 1 is now set to 2
honahlee.py(46):         idx += 1
	>>>>>>> global idx was 2 is now set to 3
honahlee.py(47):         for y in range(3):
	>>>>>>> local y was 2 is now set to 0
honahlee.py(48):             z = idx * 100 + x * 10 + y
	>>>>>>> local z was 212 is now set to 320
Line number sequence break	...
honahlee.py(47):         for y in range(3):
	>>>>>>> local y was 0 is now set to 1
honahlee.py(48):             z = idx * 100 + x * 10 + y
	>>>>>>> local z was 320 is now set to 321
Line number sequence break	...
honahlee.py(47):         for y in range(3):
	>>>>>>> local y was 1 is now set to 2
honahlee.py(48):             z = idx * 100 + x * 10 + y
	>>>>>>> local z was 321 is now set to 322
Line number sequence break	...
honahlee.py(47):         for y in range(3):
Line number sequence break	...
honahlee.py(45):     for x in range(3):
Line number sequence break	...
honahlee.py(49):     idx = oldidx
			*** return from "jill" ***
	>>>>>>> global idx was 3 is now set to 0
*** Puff not watching variables
***Tracing Off
***Tracing On, nest = 100 lines =None funcs = ['opossum'] callsonly = False
waiting on you H  !
***Trace and target execution stop when condition is True
			*** "opossum" called ***
honahlee.py(19):     for idx in range(10):
honahlee.py(20):         print("opossum on iteration", idx)
opossum on iteration 0
Line number sequence break	...
honahlee.py(19):     for idx in range(10):
honahlee.py(20):         print("opossum on iteration", idx)
opossum on iteration 1
Line number sequence break	...
honahlee.py(19):     for idx in range(10):
honahlee.py(20):         print("opossum on iteration", idx)
opossum on iteration 2
Line number sequence break	...
honahlee.py(19):     for idx in range(10):
honahlee.py(20):         print("opossum on iteration", idx)
opossum on iteration 3
Line number sequence break	...
honahlee.py(19):     for idx in range(10):
honahlee.py(20):         print("opossum on iteration", idx)
opossum on iteration 4
Line number sequence break	...
honahlee.py(19):     for idx in range(10):
honahlee.py(20):         print("opossum on iteration", idx)
***Trace and execution ends because of StopWhen
Traceback (most recent call last):
  File "C:\0\honahlee.py", line 111, in <module>
    showall()
  File "C:\0\honahlee.py", line 105, in showall
    opossum()
  File "C:\0\honahlee.py", line 20, in opossum
    print("opossum on iteration", idx)
  File "C:\0\honahlee.py", line 20, in opossum
    print("opossum on iteration", idx)
  File "C:\Users\Dan Bates\AppData\Local\Programs\Python\Python310\lib\site-packages\pufftracer\pufftrc.py", line 195, in smalltrace
    assert False, "***Puff had a StopWhen return True"
AssertionError: ***Puff had a StopWhen return True
```
## Watch For:
This topic is doscussed on more detail in the chapter on Debugging in a book I have written.
I will update this with information when the book is published.
