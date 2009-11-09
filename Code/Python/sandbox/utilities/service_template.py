import os, sys
import threading

import win32serviceutil
import win32service
import win32event

class ServiceThread (threading.Thread):

  def __init__ (self, *args, **kwds):
    threading.Thread.__init__ (self, *args, **kwds)
    self.setDaemon (1)
    self.start ()

  def run (self):
    #
    # do something useful
    #
    pass

class Service (win32serviceutil.ServiceFramework):
  _svc_name_ = "ServiceTemplate"
  _svc_display_name_ = "Template for Python Service"

  def __init__ (self, args):
    win32serviceutil.ServiceFramework.__init__ (self, args)
    self.hWaitStop = win32event.CreateEvent (None, 0, 0, None)
    ServiceThread ()

  def SvcStop (self):
    self.ReportServiceStatus (win32service.SERVICE_STOP_PENDING)
    win32event.SetEvent (self.hWaitStop)

  def SvcDoRun (self):
    while 1:
      result = win32event.WaitForSingleObject (self.hWaitStop, 5000)
      if result == win32event.WAIT_TIMEOUT:
        pass
        # do whatever you want
      else:
        print "Service stopped"
        break

if __name__ == '__main__':
  win32serviceutil.HandleCommandLine (Service)

