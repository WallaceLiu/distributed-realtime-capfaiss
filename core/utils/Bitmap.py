# -*- coding: utf-8 -*-

class Bitmap(object):

    def __init__(self, max):
        self.array = bytearray([0] * max)

    def calcElemIndex(self, num, up=False):
        if up:
            return int((num + 8 - 1) / 8)  # 向上取整

        return num // 8

    def calcBitIndex(self, num):
        return num % 8

    def set(self, num):
        elemIndex = self.calcElemIndex(num)
        byteIndex = self.calcBitIndex(num)

        elem = self.array[elemIndex]
        print(elemIndex, byteIndex)
        cc = elem | (1 << byteIndex)
        # print(cc)
        self.array[elemIndex] = elem | (1 << byteIndex)

    def clean(self, i):
        elemIndex = self.calcElemIndex(i)

        byteIndex = self.calcBitIndex(i)

        elem = self.array[elemIndex]
        self.array[elemIndex] = elem & (~(1 << byteIndex))

    def output(self):
        return str(self.array)


if __name__ == "__main__":
    pin = [i for i in range(1,2000+1)]
    cc = Bitmap(2000)
    for p in pin:
        cc.set(p)
    print(cc.output())
