class A:
    def __init__(self, a):
        self.value = a

    def show(self):
        print(self.value)
b= A(5)
b.show()
A.show(b)