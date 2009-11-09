from urllib2 import urlopen
import time
from SysTrayIcon import SysTrayIcon
from threading import Thread

hover_text = "Netmonitor"
menu_options = tuple()

RUNNING = True
ok_icon = r"E:\svn\ant-trunk\Python\sandbox\netmonitor\OK.ico"
down_icon = r"E:\svn\ant-trunk\Python\sandbox\netmonitor\down.ico"


class NetMonitor(object):
    def __init__(self):
        self.sti = SysTrayIcon(down_icon, hover_text, menu_options, on_quit=self.bye, default_menu_index=1)
        checker = Thread(target=self.loop)
        checker.start()
        self.sti.show()
    
    def bye(self, sysTrayIcon): 
        global RUNNING
        RUNNING = False
    
    def url_up(self, url):
        try:
            conn = urlopen(url)
            conn.close()
            return True
        except:
            return False

    def switch_icon(self, icon, hover_text):
        self.sti.icon = icon
        self.sti.hover_text = hover_text
        self.sti.refresh_icon()

    def run(self):
        if self.url_up("http://www.google.com") or self.url_up("http://www.plus.net"):
            self.switch_icon(ok_icon, "Connection OK")
        else:
            self.switch_icon(down_icon, "Connection down")

    def loop(self):
        time.sleep(5)
        while RUNNING:
            self.run()
            time.sleep(15)

def main():
    nm = NetMonitor()
    nm.start()

if __name__ == "__main__":
    main()

