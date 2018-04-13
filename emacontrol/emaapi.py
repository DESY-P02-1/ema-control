import socket
import sys
import time
from PyTango import *

class EmaApi:

    def __init__(self):
        self.ip = "192.168.58.38"
        self.port = 10004
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        try:
            self.sock.connect((self.ip, self.port))
            print '... connection established ...'
            return self.sock
        except socket.error:
            print '... socket error ...'

    def start(self):
        self.sock.send('start')

    def stop(self):
        self.sock.send('stopMotor')

    def restart(self):
        self.sock.send('restartMotor')

    def reset(self):
        self.sock.send('reset')

    def pause(self):
        print 'test'

#   def send_cmd(self, cmd, await=None):
    def send_cmd(self, cmd, await=None):
        print("Sending command: {}".format(cmd))
        self.sock.send(cmd)
        print("Sent")
        if await != None:
            self.wait_msg(await)
    
    def wait_msg(self, msg):
        while self.sock.recv(len(msg)) != msg:
            print '... waiting ...'
            #consider timeout!!
        print msg

    def set_X_axis(self, xVal):
        strng=''
        if str(xVal).isdigit()==True:
            try:
                self.sock.send("setX")
                #strng='setXaxis:waiting'
                #while self.sock.recv(len(strng)) != strng:
                while (self.sock.recv(24)).find('setXaxis:waiting')==-1:
                    #strng=self.sock.recv(24)
                    #print strng
                    print '... waiting for response ...'
                self.sock.send('%i' % xVal)
                self.wait_msg('setXaxis:done')
            except socket.error:
                print '... socket error ...'  #
        else:
            print '... xVal is not a valid number ...'

    def set_Y_axis(self, yVal):
        strng=''
        if str(yVal).isdigit()==True:
            try:
                self.sock.send("setY")
                #strng='setXaxis:waiting'
                #while self.sock.recv(len(strng)) != strng:
                while (self.sock.recv(24)).find('setYaxis:waiting')==-1:
                    #strng=self.sock.recv(24)
                    #print strng
                    print '... waiting for response ...'
                self.sock.send('%i' % yVal)
                self.wait_msg('setYaxis:done')
            except socket.error:
                print '... socket error ...'  #
        else:
            print '... yVal is not a valid number ...'

    def setAxis(self, xVal, yVal):
        strng=''
        if str(xVal).isdigit()==True:
            if str(yVal).isdigit()==True:
		self.send_cmd('setAxis#X%i#Y%i' %(xVal,yVal), await='setAxis:done')
            else:
                print '... yVal is not a valid number ...'
        else:
            print '... xVal is not a valid number ...'

   # def set_Y_axis(self, yVal):
   #     if str(yVal).isdigit()==True:
   #         try:
   #             self.sock.send("defY")
   #             while self.sock.recv(16) != 'setYaxis:waiting':
   #                 print '... waiting for response ...'
   #             self.sock.send('%i' % yVal)
   #             self.wait_msg('setYaxis:done')
   #         except socket.error:
   #             print '... socket error ...'
   #     else:
   #         print '... yVal is not a valid number ...'

    def mount_sample(self, n):
        x=((n-1)%30)+1
        y=((n-1)/30)+1
        #self.set_X_axis(x)
        #time.sleep(1)
        #self.set_Y_axis(y)
	self.setAxis(x,y)
        time.sleep(1)
        self.send_cmd('gate', await='moveGate:done')
        self.send_cmd('home', await='moveHome:done')
	self.send_cmd('next', await='moveNext:done')
        #self.send_cmd('pick', await='pickSample:done')
        self.send_cmd('gate', await='moveGate:done')
        self.send_cmd('spinner', await='moveSpinner:done')
        #self.send_cmd('release', await='releaseSample:done')
        self.send_cmd('offside', await='moveOffside:done')
        self.unmount_sample()
        return self.mount_samples([n])

    #mount_samples(range(2,250))
    #def mount_samples(self, useropts,  *mv):
    def mount_samples(self,*mv):
        for i in mv:
            self.mount_sample(i)
            print '... processing sample %i ...' % i
            #do_useropts(useropts)

    def unmount_sample(self):
        self.send_cmd('spinner', await='moveSpinner:done')
        #self.send_cmd('pickSample', await='pickSample:done')
        self.send_cmd('gate', await='moveGate:done')
	self.send_cmd('back', await='bringBack:done')
	
        #self.send_cmd('release', await='releaseSample:done')
        self.send_cmd('home', await='moveHome:done')

    def clear_sample(self):
        pass

    def make_safe(self):
        pass

