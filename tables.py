# Sine wave table generator
#
# Copyright (c)2016 Paul Forgey
#
# run as: python tables.py > synth.osc.tables.spin
#
#                            TERMS OF USE: MIT License
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import math
import sys

def round(n):
    m = math.modf(n)
    n = int(m[1])
    if m[0] >= 0.5:
        n += 1

    return int(n)

def sin(n):
    n = round(math.sin(n / 4096.0 * math.pi) * 16384.0)
    if n > 0x3fff:
        n = 0x3fff
    return n

def log(n):
    if n > 0:
        n = math.log(n / 16384.0) / math.log(2.0)
        n = -round(n * 2048.0)
        n = n & 0x7fff
    else:
        n = 0x7fff
    return n

def alog(n):
    n = math.pow(2.0, (n / 2048.0)) - 1.0
    n = round(n * 16384.0)
    if n > 0x3fff:
        n = 0x3fff
    return n

def sines():
    print ("Sines")

    for x in range(0, 0x0800, 0x20):
        sys.stdout.write("WORD ")

        for y in range(0, 0x20):
            n = log(sin(x+y)) << 1

            sys.stdout.write(str(n))

            if y < 0x1f:
                sys.stdout.write(",")
            else:
                sys.stdout.write(" \'" + hex(x) + "\n")

    print


def exps():
    print ("Exps")

    for x in range(0, 0x800, 0x20):
        sys.stdout.write("WORD ")

        for y in range(0, 0x20):
            n = alog((x+y) ^ 0x7ff) | 0x4000
            sys.stdout.write(str(n))

            if y < 0x1f:
                sys.stdout.write(",")
            else:
                sys.stdout.write(" \'" + hex(x) + "\n")

    print


def tables():
    print "'This code is automatically generated"
    print "'Do not edit"
    print
    print "PUB SinesPtr"
    print "    return @Sines"
    print
    print "PUB ExpsPtr"
    print "    return @Exps"
    print
    print "DAT"
    sines()
    exps()


def sinewave(e):
    for x in range(0, 0x2000):
        n = x & 0x7ff
        if (x & 0x800):
            n = n ^ 0x7ff
        n = log(sin(n)) + e
        y = alog((n & 0x7ff) ^ 0x7ff) | 0x4000
        n >>= 11
        y >>= n
        if (x & 0x1000):
            y = -y
        print y


def sinewave2():
    for x in range(0, 0x2000):
        y = round(math.sin(x / 4096.0 * math.pi) * 32767.0)
        print y


tables()

