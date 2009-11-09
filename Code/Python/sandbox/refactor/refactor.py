import inspect, os, re, os.path

class renameto(object):    
    def __init__(self, new_function):
        self.new_function = new_function
    
    def __call__(self, function):
        self.function = function
        return self.decorator
        
    def decorator(self, *args, **kw):
        f = inspect.currentframe().f_back
        fn = f.f_code.co_filename
        lineno = f.f_lineno
        
        in_f = file(fn)
        out_l = []
        
        for i, line in enumerate(in_f):
            if i == (lineno - 1):
                line = re.sub(r"\b%s\b" % self.function.__name__, 
                                            self.new_function.__name__, line)
            out_l.append(line)
        
        in_f.close()
        
        temp = fn + "~"
        
        if os.path.exists(temp):
            os.remove(temp)
            
        os.rename(fn, temp)
        
        out_f = file(fn, "w")
        
        for line in out_l:
            out_f.write(line)
        out_f.close()
        
        return self.new_function(*args, **kw)


def newf(arg):
    print "New trace Function: " + arg
    
@renameto(newf)
def bob(arg):
    print "Old Bob Function: " + arg

