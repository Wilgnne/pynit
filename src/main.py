#!/bin/python3.8
import subprocess
import json
import time
import threading


class Interrupt ():
    def __init__(self, code: int, response: str):
        self.code = code
        self.response = response

    def __repr__(self):
        return str(self.__dict__)


class Program ():
    def __init__(self, exec: str, interrupts=[], reopen=False):
        self.exec = exec
        self.interrupts = [Interrupt(**i) for i in interrupts]
        self.reopen = reopen
        self.command = self.exec.split(' ')
        self.process = None

        self.thread_loop = threading.Thread(target=self.thread_run)
        self.thread_loop.start()

    def thread_run(self):
        if not self.process:
            self.process = subprocess.Popen(self.command)
            main_thread = threading.main_thread()
            while main_thread.is_alive():
                code = self.process.poll()
                self.exec_interrupt(code)

                if code != None and self.reopen:
                    self.close()
                    self.process = subprocess.Popen(self.command)
            
            self.close()
            exit(0)

    def exec_interrupt(self, code: int):
        interrupt = self.interrupt_key(code)
        if interrupt == None:
            return
        elif interrupt == 'close':
            self.close()
            self.reopen = False

    def interrupt_key(self, key: int):
        f = list(filter(lambda x: x.code == key, self.interrupts))
        if len(f) > 0:
            return f[0]
        return None

    def close(self):
        self.process.terminate()

    def __repr__(self):
        return str(self.__dict__)


def main():
    file = open('startup.json')
    startup = json.load(file)

    programs = [Program(**program) for program in startup]

    [print(program, '\n') for program in programs]

    while True:
        time.sleep(0.1)


if __name__ == "__main__":
    main()
