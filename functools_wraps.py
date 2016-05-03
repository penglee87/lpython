from functools import wraps
'''
https://docs.python.org/3.4/library/functools.html?highlight=functools#functools.partial
@functools.wraps
'''

def my_decorator(f):
    @wraps(f)
    def wrapper(*args, **kwds):
        print('Calling decorated function')
        return f(*args, **kwds)
    return wrapper
    
    
    
@my_decorator
def example():
    """Docstring"""
    print('Called example function')

example()

example.__name__

example.__doc__
