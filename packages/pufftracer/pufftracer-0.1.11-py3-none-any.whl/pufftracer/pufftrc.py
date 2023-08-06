'''
puff_trc.py
An alternate method to interface to tracing.
A different approach to accomplish what is in the standard library documentation as:
>Debugging and profiling -> trace -> Programmatic Interface.

import pufftracer.pufftrc as puff

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

A trace object of class Puff has these interfaces.
Trc = puff.Puff()
Trc.focus(module name or module filename)
Trc.On(nest=100, lines=None, funcs=None, callsonly=False)
Trc.Off()
Trc.Resume()
Trc.StopWhen(condition_function)
Trc.Watch(lcls=IsNot, globs=IsNot, nonlcls=IsNot) where IsNot is an internal None

This is Puff the magic Debugging Dragon.

Of Course an example honalee.py is provided.

Where else can a Magic Dragon live than in Honalee.

This is very much through the looking glass.

Changes
===============================================================================
16-Jan-2022 12:21:30 pm Initial part of 0.1.10
'''
__version__ = '0.1.10'
__last_change__ = '16-Jan-2022 12:22:18 pm'

import sys
import trace
import inspect

class NonExistant (object):
    def __repr__(self):
        return "IsNot"


IsNot = NonExistant()       # None don't quite get'r done


class Puff ():
    # a singleton
    instance = None
    last_nesting = nesting = 100

    lines = None
    funcs = None
    # The selected file which is the only file
    # therefore the only module we trace within.
    filename  = ""  # An empty string for filename traces nothing
    id_compare = False
    globs = lcls = nonlcls = None
    lastfunc  = ("<none>", nesting)
    callsonly = False
    line_no   = -1
    StopWhenFunc = lambda : False  # noqa: E731

    def __init__ (self):
        cls = Puff
        # if no focus we debug in the file which created a Trc object
        cls.filename = inspect.stack()[-2].filename
        if cls.instance is None: # a singleton behaviour
            cls.instance = self
            sys.settrace(Puff.tracefunc)
        return None
        assert False, "Puff instantiated voked more than a singleton class should be!"

    def __del__ (self):
        # put trace back to the way it was.
        Puff.instance = None
        sys.settrace(None)

    @staticmethod
    def NoWatch (frame):    # this do nothing function is called when there are
        """
        When WatchProcess point here and is called we promptly return
        """
        return              # no variables to watch
    

    WatchProcess = NoWatch  # WatchProcess is either NoWatch of DoWatch
        
    @staticmethod
    def tracefunc (frame, event, arg):
        cls = Puff
        if frame.f_code.co_filename != cls.filename:
            return cls.smalltrace
        if event == "call":
            cls.last_nesting, cls.nesting = cls.nesting, cls.nesting - 1
            cls.line_no = -1
            # cls.nesting -= 1
        return cls.smalltrace
        

    def focus (self, file):
        '''
Usage puff_trc.Puff().focus(__file__)
or
focus(module.__file__)

Focus the trace (allow the trace) only on one module at a time and
that module cannot be puff_trc
        '''
        id_compare = False
        filename = ""
        if file == None:
            id_compare = True
            filename = inspect.stack()[-2].f_code.filename
        elif type(file) == type(inspect):
            filename = filename.__filename__
            id_compare = True
        else:
            filename = file
            id_compare = False
        if file == __file__:
            Puff.filename = ""
            Puff.id_compare = False
            print("*** Puff cannot focus on", filename, "***")
            return
        Puff.id_compare = id_compare
        Puff.filename = filename
        print("*** Puff trace focused on module file :\n\t", Puff.filename)


        
    @staticmethod
    def smalltrace (frame, why, arg):
        cls = Puff
        code_filename = frame.f_code.co_filename
        if cls.id_compare:
            if code_filename is not cls.filename:
                return cls.smalltrace
        elif code_filename == cls.filename:
            cls.filename = code_filename
            cls.id_compare = True
        else:
            return cls.smalltrace

        assert code_filename is not __file__,f"smalltrace cannot trace Puff"
            
        if cls.lines is not None:
            lineno = frame.f_lineno
            if not (cls.lines[0] <= lineno <= cls.lines[1]):
                return cls.smalltrace
        func = frame.f_code.co_name
        if cls.funcs is not None:
            if func not in cls.funcs:
                return cls.smalltrace

        if why == "return":
            cls.last_nesting, cls.nesting = cls.nesting, cls.nesting + 1
            cls.line_no = -1

        if cls.nesting < 0:
            return cls.smalltrace
        if cls.lastfunc != (func, cls.nesting):
            cls.line_no = -1
            if cls.nesting > cls.last_nesting:
                print(f'\t\t\t*** return from "{func}" ***')
            elif cls.nesting < cls.last_nesting:
                print(f'\t\t\t*** "{func}" called ***')
            cls.lastfunc = (func, cls.nesting)
        Puff.WatchProcess(frame)

        # the act of printing a trace. Someday we might just print
        # this ourselves
        
        lineno=frame.f_lineno
        if not cls.callsonly:
            if cls.line_no > 0:
                if lineno != (cls.line_no + 1):
                    print("Line number sequence break\t...")
            trace.Trace().localtrace_trace(frame, why, arg)
        cls.line_no = lineno
        if cls.StopWhenFunc():
            print("***Trace and execution ends because of StopWhen")
            # replace with breakpoint()?
            # replace with raise or sys.SystemExit()
            assert False, "***Puff had a StopWhen return True"
        return cls.smalltrace

    @staticmethod
    def makelist (something):
        # something coerced to be None or a list of something
        if something is None:
            return None
        if type(something) == type(""):
            return something.split(", ")
        if isinstance(something, tuple):
            return list(something)
        if type(something) != type([]):  # noqa: E721
            something = [something]
        return something

    @staticmethod
    def makedict (something):
        RetDict = dict()
        somethinglist = Puff.makelist(something)
        for thing in somethinglist:
            RetDict[thing] = IsNot
        return RetDict
        
    @staticmethod
    def MakeItGo ():
        '''A call is necessary to start the trace'''
        # a call forces a tracefunc which then kicks off
        # small traces

    def On (self, nest=100, lines=None, funcs=None, callsonly=False):
        """
Trc.On(nest=100, lines=None, funcs=None, callsonly=False)
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
""" 
        cls = Puff
        if isinstance(lines, list):
            cls.lines    = sorted(lines)
        elif type(cls.lines) == type(0):
            cls.lines = [cls.lines, cls.lines]
        else:
            cls.lines    = None
        cls.funcs        = cls.makelist(funcs)
        cls.last_nesting = cls.nesting = nest
        cls.lastfunc     = ('<none>', nest)
        cls.callsonly    = callsonly
        if cls.funcs is not None:
            for i, element in enumerate(cls.funcs):
                if type(element) == type(cls.MakeItGo):  # noqa: E721
                    cls.funcs[i] = element.__name__
        print("***Tracing On, nest =", cls.nesting, "lines =", end="")
        print(cls.lines, "funcs =", cls.funcs, "callsonly =", callsonly)
        cls.StopWhenFunc = lambda : False
        sys.settrace(cls.tracefunc)
        cls.MakeItGo()     # Takes a call to make it go
        

    def Off (self):
        """
Trc.Off() Stops the trace.
"""
        sys.settrace(None)
        Puff.MakeItGo()  # hoping tracefunc makes it stop
        print("***Tracing Off")
        

    def Resume (self):
        """
Trc.Resume() continues a trace printing with no changes to
the trace parameters in effect on the preceding Trc.Off().
"""
        # resumes on a call
        sys.settrace(Puff.tracefunc)
        Puff.lastfunc = None
        print("***Tracing Resumed")
        sys.settrace(Puff.tracefunc)  # tracefunc on next call
        Puff.MakeItGo()     # Takes a call to make it go
        

    def StopWhen (self, condition_func):
        """
Trc.StopWhen(stoptestfunc) Gives a reference to a predicate function
which returns True when an event occurs where you want the state
of the program preserved. The function should be optimized for the
path that returns False.

This call mustbe made after the Trc.On().

The function must be valid to execute in any environment. Variables must
remain in scope.

The function may be a lambda function, but it need not be. it can take the
form
def StopTheWorld():
    if not <stop the world condition>:
        return False
    <other processing>
Where other processing can be a smart dump of the state or a breakpoint()
"""
        # condition is a predicate which must evalutate to False to continue
        # and when True causes a end to execution via breakpoint or assert
        Puff.StopWhenFunc = condition_func
        print("***Trace and target execution stop when condition is True")
        

    def Watch (self, lcls=IsNot, globs=IsNot, nonlcls=IsNot):
        """
Trc.Watch(lcls=IsNot, globs=IsNot, nonlcls=IsNot)
tells puff what variables to watch for modifications to.
Ideally variables will not fall out of scope. If they do we
do not monitor them.

Variable that are local are in the lcls list, The global variables are in the
globs list and nonlocals in the nonlcls list.
Variables must be simple, a good list would be like "x, y, z"
This part while useful is not bullet proof.
"""
        flg = False
        if lcls is IsNot:
            Puff.lcls = dict()
        else:
            Puff.lcls = Puff.makedict(lcls)
            print(f"*** Watch {Puff.lcls=}")
            flg = True
        if globs is IsNot:
            Puff.globs = dict()
        else:
            Puff.globs = Puff.makedict(globs)
            print(f"*** Watch {Puff.globs=}")
            flg = True
        if nonlcls is IsNot:
            Puff.nonlcls = dict()
        else:
            Puff.nonlcls = Puff.makedict(nonlcls)
            print(f"*** Watch {Puff.nonlcls=}")
            flg = True
        if flg:
            Puff.WatchProcess = Puff.DoWatch
        else:
            Puff.WatchProcess = Puff.NoWatch
            print("*** Puff not watching variables")
    

    @staticmethod
    def DoWatchHelper (thiskind, thisdict, thatdict):
        """
        Called for each kind of variable being watched:
        locals, globals and nonlocals.
        traverse the dictionary looking for variables
        which have changed.
        This slows things down a great deal.
        """
        for var in thisdict:
            oldval = thisdict[var]
            if var not in thatdict:
                continue
            newval = thatdict[var]
            if newval != oldval:
                if oldval is IsNot:
                    oldvalstr = f"\t>>>>>>> {thiskind} {var} initially"
                else:
                    oldvalstr = f"\t>>>>>>> {thiskind} {var} was {oldval} is now"
                thisdict[var] = newval
                print(oldvalstr, f"set to {newval}")
        return
        

    @staticmethod
    def DoWatch (frame):
        """
        The real Watch used when we are watching variables. Use the helper
        for each kind of variables and frame we are using.
        """
        Puff.DoWatchHelper("local", Puff.lcls, frame.f_locals)
        Puff.DoWatchHelper("global", Puff.globs, frame.f_globals)
        if Puff.nonlcls == {}:
            return
        for frm in inspect.stack():
            if Puff.DoWatchHelper("nonlocal", Puff.nonlcls, frm.f_locals):
                return
                

'''
No Main for testing here.
In the current form should this module trace itself
results will be unpredictable. Keep safe guards in place
'''
