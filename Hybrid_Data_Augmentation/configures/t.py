import json
import time
class MyClass:
    def method1(self):
        pass

    def method2(self):
        pass

    def __method3(self):
        print(111)
        pass

time.sleep(3)

obj = MyClass()
method_names = [method for method in dir(obj) if callable(getattr(obj, method)) ]
print(method_names)

obj._MyClass__method3()
