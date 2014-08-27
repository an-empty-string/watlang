#!/usr/bin/env python3
import sys

class Wat:
    def __init__(self):
        self.stack = []
        self.vars = {}
        self.state = "default"
        self.buf = ""
        self.info = 0

    def _state(self, k):
        self.buf = ""
        self.state = k
        self.info = 0

    def push(self, wat):
        self.stack.append(wat)

    def pop(self):
        wat = self.stack[-1]
        self.stack = self.stack[:-1]
        return wat

    def peek(self):
        return self.stack[-1]

    def _devar(self):
        self.vars[self.pop()] = self.pop()

    def _loop(self):
        op, t = self.pop(), self.pop()
        for i in range(int(t)):
            self.pls(op)

    def dostate(self, c):
        {"default": self.do,
         "string": self.do_string,
         "number": self.do_number
        }[self.state](c)

    def ret_self(self, k):
        def ret(stack):
            stack.push(k)
        return ret

    def do(self, wat):
        k = {}
        wat = str(wat)
        for i in range(10):
            k[str(i)] = self.ret_self(i)

        k["+"] = lambda s: s.push(s.pop() + s.pop())
        k["-"] = lambda s: s.push(s.pop() - s.pop())
        k["*"] = lambda s: s.push(s.pop() * s.pop())
        k["/"] = lambda s: s.push(s.pop() / s.pop())
        k["c"] = lambda s: s.push(s.peek())
        k["e"] = lambda s: s.pls(s.pop())
        k["f"] = lambda s: s.stack.reverse()
        k["g"] = lambda s: s.push(s.vars[s.pop()])
        k["i"] = lambda s: s.push(input())
        k["l"] = Wat._loop
        k["N"] = lambda s: s.push(int(s.pop()))
        k["p"] = lambda s: print(s.pop())
        k["P"] = lambda s: sys.stdout.write(str(s.pop()))
        k["s"] = Wat._devar
        k["S"] = lambda s: s.push(str(s.pop()))
        k["{"] = lambda s: s._state("string")
        k["["] = lambda s: s._state("number")
        k["\n"] = lambda s: s
        k[" "] = lambda s: s

        k[wat](self)

    def do_string(self, c):
        if c == '{':
            self.info += 1
        elif c == '}':
            self.info -= 1
        if self.info == -1:
            self.push(self.buf)
            self._state("default")
        else:
            self.buf += c

    def do_number(self, c):
        if c != ']':
            self.buf += c
        else:
            self.push(int(self.buf))
            self._state("default")

    def pls(self, hue):
        for c in hue:
            self.dostate(c)

if __name__ == '__main__':
    mhm = open(sys.argv[1]).read(8192)
    Wat().pls(mhm)
