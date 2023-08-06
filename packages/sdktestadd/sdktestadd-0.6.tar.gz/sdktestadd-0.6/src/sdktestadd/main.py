import pandas


class SdkTest(object):
    def __init__(self, num):
        self.num = num

    def add_test(self):
        return self.num + 1

    def sub_test(self):
        return self.num - 1
