#complete your tasks in this file
def assertFinite(x : Any)->None:
    if not isinstance(x, numbers.Real): raise TypeError
    if isinstance(x,bool): raise TypeError
    if not isfinite(x): raise ValueError
