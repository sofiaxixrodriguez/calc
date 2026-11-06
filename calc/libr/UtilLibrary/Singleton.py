class SingletonMeta(type):

    __instances: dict = {}

    def __call__(self, *args, **kwargs):
        if self not in self.__instances:
            instance = super().__call__(*args, **kwargs)
            self.__instances[self] = instance
        return self.__instances[self]



# class Example(metaclass=SingletonMeta):
#     def __init__(self):
#         pass
#
#
# if __name__ == '__main__':
#     s1 = Example()
#     s2 = Example()
#
#     if id(s1) == id(s2):
#         print('Singleton Works, both variables have the same instance')
#     else:
#         print('Fail')
