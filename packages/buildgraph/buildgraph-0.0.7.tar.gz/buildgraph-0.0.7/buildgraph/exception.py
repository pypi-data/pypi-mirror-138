from functools import wraps


class EmptyGraphException(Exception):
    pass


class CircularDependencyException(Exception):
    pass


class UnusableReturnType(Exception):
    pass


class StepFailedException(Exception):
    def __init__(self, step, exc, args):
        super().__init__(str(step))

        self.step = step
        self.exc = exc
        self.args = args

    def copy(self):
        return StepFailedException(self.step, self.exc, self.args)


def pass_exceptions(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except StepFailedException as e:
            raise e.copy() from None

    return wrapper
