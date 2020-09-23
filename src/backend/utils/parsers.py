import sys, inspect

def kwarg_parser(fields, kwargs):

    # Getting the name of the object from which this was called
    obj_name = inspect.getmodule(sys._getframe(1)).__name__
    obj_name = obj_name.split('.')[-1].capitalize()

    if kwargs == {}:
        return fields.copy()

    for key, value in kwargs.items():

        key = key.lower()

        if key not in fields.keys():
            msg = (f'\n\nAttempt to set invalid parameter \'{key}\'')
            raise SyntaxError(msg)

        elif not isinstance(value, type(fields[key])):
            msg = (f'\n\nParameter \'{key}\'> expects a(n) {type(fields[key])}'
                   f', but was given a(n) \'{type(value)}\' instead.')
            raise ValueError(msg)

    for key, value in fields.items():
        if key not in kwargs.keys():
            kwargs[key] = value

    return kwargs

def format_bytes(b:int) -> str:
    '''
        Given a value in bytes, will convert it to whatever order of magnitude
        needed for compactness (e.g. b=1024 should return `1 KB`)

        Inspired by https://stackoverflow.com/a/52379087
    '''
    step = 1024
    for prefix in ('B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'):
        if b < step:
            return f'{b:.2g}{prefix}'
        b /= step
    return f'{b}B'
