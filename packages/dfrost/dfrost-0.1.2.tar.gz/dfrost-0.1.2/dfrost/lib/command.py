from functools import cache


@cache
def get_command_registry():
    return dict()


def register(name, setup_fn=lambda par: par):
    def wrapper(command_fn):
        get_command_registry()[name] = (setup_fn, command_fn)
        return command_fn

    return wrapper
