'''
Module to set up functions to run on separate processes

Requires dill (run "pip install dill" if not already installed)
'''

from multiprocessing import Pool, cpu_count, Manager
from contextlib import closing
import dill as pickle
import types

def worker(g, e, *args, **kw):
    '''
    Generic worker function
    Unpickles given pickled function and runs function with given args
    
    Catches and re-throws exceptions. Exceptions are dealt with on the
    parent process only - avoids process hanging
    '''
    ex = None
    if not e.is_set():
        try:
            r = pickle.loads(g)(*args, **kw)
            # successful return
            return (0, r)
        except Exception as ex:
            # prematurely end all tasks
            e.set()
            # abnormal exit caused by exception
            return (1, ex)
    else:
        # null return
        return (0, ex)

def map_list(f):
    '''
    Multiprocess Map Decorator

    Maps list of args for a function and runs all function instnaces
    asynchronasly across n cpus
        - use keywords arg_list=[args, ...], cores=n
        
        - function-specific keywords can be used to set a universal
          argument, e.g.:
          
              @map_list
              def func(a, some_kw=1): return a * some_kw
          
          func(arg_list=[...], cores=x, some_kw=5)
          -> func(arg, some_kw=5) for every call of func
          
        - arg_list will accept generator functions, but for each
          iteration, the yielded value should be a tuple or list, e.g.:
          
              @map_list
              func(x): return x
              func(arg_list=((i,) for i in xrange(10)))
        
        - if arg_list not given, all non keyword args will be turned
          into a list of args to be parsed

    IMPORTANT - decorated functions cannot have functions as arguments
    
    Note - Only use for inherintly slow functions (>1 sec execution
           time) as it is not as efficient as explicitly hard coding
    '''
    def wrap(*args, **kw):
        cores = kw.pop('cores', 1)
        assert cores <= cpu_count()
        arg_list = kw.pop('arg_list', args)
        if not isinstance(arg_list, types.GeneratorType):
            arg_list = list(arg_list)
            if arg_list:
                if not isinstance(arg_list[0], (list, tuple)):
                    for i, a in enumerate(arg_list):
                        arg_list[i] = [a]
        g = pickle.dumps(f)
        error_in_func = None
        m = Manager()
        event = m.Event()
        with closing(Pool(processes=cores)) as pool:
            res = [
                pool.apply_async(
                    worker,
                    args=[g, event] + list(a),
                    kwds=kw)
                for a in arg_list]
            for r in res:
                r = r.get()
                if not r[0]:
                    yield r[1]
                else:
                    if not event.is_set():
                        event.set()
                    error_in_func = r[1]
        # raise errors on parent process
        if error_in_func:
            raise error_in_func
    return wrap

@map_list
def _test_map(out, some_kw=1):
    # kwargs are universal for all called functions if specified as a kw
    return (out, some_kw)

if __name__ == '__main__':
    # examples
    # add 'cores=x' to run on x cpus, default = 1
    print next(_test_map('b', some_kw=20))
    print next(_test_map('b', 'c', some_kw=20))
    print next(_test_map(arg_list=[1,2,3,4,5], some_kw=5))
    print next(_test_map(arg_list=[(1,1),(2,2),(3,3),(4,4),(5,5)], cores=4))
    x = (('a%d' % i,) for i in xrange(10))
    print next(_test_map(arg_list=x))
