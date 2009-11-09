import wx
import os
import sys
import  wx.lib.rcsizer  as rcs
from wx import ImageFromStream

ID_SAVE_BUTTON = wx.NewId()
wx.InitAllImageHandlers()


class NoteTaker(wx.App):
    #BG_COL = "#4361eb"
    #BG_COL = "#9ad"
    BG_COL = "#67e"

    def __init__(self, b, fh):
        self.filehandler = fh
        wx.App.__init__(self, b)
    
    def OnInit(self):
        self.frame = wx.Frame(None, -1, "To Do")
        icon = wx.Icon("images/icon.ico", wx.BITMAP_TYPE_ICO)
        self.frame.SetIcon(icon)
        self.frame.Bind(wx.EVT_CLOSE, self.Exit)
        self.frame.SetBackgroundColour(col(NoteTaker.BG_COL))
        
        self.textBox = wx.TextCtrl(self.frame, 50, "", style=wx.TE_MULTILINE)
        
        self.textBox.SetForegroundColour(col("#fff"))
        self.textBox.SetBackgroundColour(col(NoteTaker.BG_COL))
        font = wx.Font(10, wx.FONTFAMILY_SWISS, wx.NORMAL, wx.BOLD)
        self.textBox.SetFont(font)
        
        self.setupToolbar()
        self.Bind(wx.EVT_TEXT, self.EnableSave, id=50)
        
        for line in self.filehandler.getLines():
            self.textBox.WriteText(line)
        
        
        self.SetTopWindow(self.frame)
        self.frame.Show(True)
        
        self.textBox.SetInsertionPoint(0)
        self.tb.EnableTool(10, False)
        
        return True
        
    def setupToolbar(self):
        self.tb = self.frame.CreateToolBar( wx.TB_HORIZONTAL | wx.NO_BORDER | wx.TB_FLAT | wx.TB_TEXT)
        self.tb.SetBackgroundColour(col(NoteTaker.BG_COL))
        
        saveImage = wx.Image("images/save.gif", wx.BITMAP_TYPE_GIF).ConvertToBitmap()
        self.tb.AddSimpleTool(10, saveImage, "Save", "Save to file")
        self.Bind(wx.EVT_TOOL, self.Save, id=10)
        
        self.tb.Realize()
        
        
    def Save(self, evt):
        self.filehandler.clear()
        for i in range(self.textBox.GetNumberOfLines()):
            self.filehandler.addLine(self.textBox.GetLineText(i))
        self.filehandler.save()
        self.tb.EnableTool(10, False)

    def EnableSave(self, evt):
        self.tb.EnableTool(10, True)
        
    def Exit(self, evt):
        self.Save(evt)
        sys.exit(0)
        
def col(hexVal):
    
    if (hexVal.startswith("#")):
        hexVal = hexVal[1:]
        
    if (len(hexVal) == 3):
        hexVal = hexVal[0]*2 + hexVal[1]*2 + hexVal[2]*2
    
    if (len(hexVal) != 6):
        return wx.Colour(red=255, green=255, blue=255)
    
    r = int(hexVal[0:2], 16)
    g = int(hexVal[2:4], 16)
    b = int(hexVal[4:6], 16)
    
    out = wx.Colour(red=r, green=g, blue=b)
    
    return out
    
    
class FileHandler(object):
    
    def __init__(self, path):
        self.path = path
        self.lines = []
        self.load()
    
    def __iter__(self):
        return iter(self.lines)
        
    def getLines(self):
        return self.lines
        
    def clear(self):
        self.lines = []
        
    def addLine(self, newText):
        self.lines.append(newText)
        
    def load(self):
        fileHandle = file(self.path)
        self.text = ""
        for line in fileHandle:
            self.lines.append(line)
        fileHandle.close()
        
    def save(self):
        fileHandle = file(self.path, 'w')
        for line in self.lines[0:len(self.lines)-1]:
            fileHandle.write(line)
            fileHandle.write('\n')
        fileHandle.write(self.lines[len(self.lines)-1])
        fileHandle.close()
        
def main(args):
    
    if (len(args) < 2):
        print "No File Specified!!"
        return
    
    path = os.path.abspath(args[1])
        
    if (not os.path.exists(path)):
        print "Path specified (", path, ") does not exist."
        return
    elif (not os.path.isfile(path)):
        print "Path specified (", path, ") is not a file."
        return
        
    applicationPath = os.path.dirname(__file__)
    os.chdir(applicationPath)
    
    fh = FileHandler(path)
    app = NoteTaker(False, fh)
    
    
    app.MainLoop()


main(sys.argv)