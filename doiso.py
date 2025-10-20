import os
import math

def doiso(n, m):
    steps = 0
    while m > n:
        if m % 2 == 0:
            m //= 2
        else:
            m += 1
        steps += 1

    steps += (n - m)
    return steps

n = int(input().strip())
m = int(input().strip())

print(doiso(n, m))
