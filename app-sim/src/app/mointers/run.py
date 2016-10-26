#!/bin/env python
#coding:utf-8

import subprocess
import Queue
import threading
import time
import copy

from lib.core.data import logger
from lib.core.datatype import AttribDict

import curses


class iostat():
    def __init__(self,args):
        self.exitFlag = False
        self.cpuStatQueue = Queue.Queue(-1)
        self.DeviceQueue = Queue.Queue(-1)
        self.args = args.split()

        al = len(self.args)
        if al == 3:
            self.count = int(self.args[2])
        else:
            self.count = True
            
    def __del__(self):
        curses.nocbreak(); curses.echo()
        curses.endwin()

    def get_data(self):
        cpu =0 
        sda = 0

        try:
            sp = subprocess.Popen(self.args,stdout=subprocess.PIPE,stderr=subprocess.PIPE)

            for line in iter(sp.stdout.readline,""):
                if self.exitFlag:
                    break
                if line == "\n":
                    continue

                data = line[:-1].lstrip().rstrip()
                if data.startswith("avg-cpu") and cpu == 0:
                    cpu = 1
                    continue
                if data.startswith("Device") and sda == 0:
                    sda = 1
                    continue

                if cpu:
                    self.cpuStatQueue.put(data.split())
                    cpu = 0
                if sda:
                    self.DeviceQueue.put(data.split())
                    sda = 0

            sp.kill()
        except Exception as e:
            logger.error(str(e))
            


    def show(self):
        t = threading.Thread(target=self.get_data,args=())
        t.setDaemon(True)
        t.start()
        try:
            mainwindow = curses.initscr()
            curses.cbreak(); mainwindow.keypad(1); curses.noecho()
            mainwindow.border(0)
            mainwindow.refresh()
            curses.start_color() 
            curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_GREEN)
            (h,w)= mainwindow.getmaxyx()

            l1= mainwindow.subwin(8,w/2,0,0)
            l1.border(0)

            t1 = threading.Thread(target=self._showdata,args=(l1,))
            t1.setDaemon(True)
            t1.start()

            t1.join()
            t.join()

            mainwindow.addstr(h/2,w/2-15,"RUN OVER,PLEASE ENTER!",curses.color_pair(1))
            mainwindow.getch()
            
        finally:
            curses.nocbreak(); mainwindow.keypad(0); curses.echo()
            curses.endwin()

    def _showdata(self,l1):
        count = self.count
        (y,x) = l1.getbegyx()
        (h,w) = l1.getmaxyx()
        l1.addstr(0,w/2-8," ".join(self.args))
        
        while(count):
            title = ""
            data = self.cpuStatQueue.get()
            l1.addstr(y+2,x+1,"%10s:%10s%10s%10s%10s%10s%10s" % ("avg-cpu","%user","%nice","%system","%iowai","%steal","%idle"))

            info = "%11s%10s%10s%10s%10s%10s%10s" % (title,data[0],data[1],data[2],data[3],data[4],data[5])
            l1.addstr(y+3,x+1,info)
            title = "avg-cpu:"
            #logger.info(info)


            data = self.DeviceQueue.get()
            l1.addstr(y+5,x+1,"%10s:%12s%12s%12s%12s%12s" % ("Device","tps","kB_read/s","kB_wrtn/s","kB_read","kB_wrtn"))

            info = "%11s%12s%12s%12s%12s%12s" % (data[0],data[1],data[2],data[3],data[4],data[5])
            l1.addstr(y+6,x+1,info)
            #logger.info(info)

            l1.refresh()
            if type(count) == int:
                count -= 1
        self.exitFlag = True

           
def main():
    #error
    #t = iostat("pdsh -R exce -w root@clent02 ssh iostat 2 6 -oConnectTimeout=15")
    t = iostat("iostat 2 5")
    t.show()


