import functools


def get_args_dict(fn, args, kwargs, to_exclude=[]):
    args_names = fn.__code__.co_varnames[:fn.__code__.co_argcount]
    return {
        k: v for k, v in {**dict(zip(args_names, args)), **kwargs}.items()
        if not k in to_exclude
    }

def error_handler(logger, action):
    def decorator(func):
        @functools.wraps(func)
        def inner(self, *args, **kwargs):
            try:
                return func(self, *args, **kwargs)
            except Exception as exc:
                args_dict = get_args_dict(func, args, kwargs, ["self"])
                logger.error(
                    "[%s] Failed %s %s (%s)",
                    self, action, args_dict or "", exc
                )
                return None

        return inner
    return decorator
