"""
Module of singleton_util. Class Singleton is represented in this module.
"""


class Singleton(type):
    """
    Class Singleton is designed for maintaining the only one instance of the other classes.
    Best practice is to use Singleton as metaclass for the other classes.
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
