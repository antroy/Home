import os.path as path, adapter
import zipfile
from zipfile import ZipFile, ZipInfo

class history:
    def __init__(self, page):
        self.page = page
        title = path.basename(page)
        
        self.historyfile = path.join(adapter.wiki_dir, title + "-history.zip")
        
    def addPage(self, text):
        mode = 'a'
        if not path.exists(self.historyfile):
            mode = 'w'
        elif not zipfile.is_zipfile(self.historyfile):
            print "Could not create history archive! Non-zip file exists in this location:", self.historyfile
            return
        
        entrycount = 0
        if mode == 'a':
            history = ZipFile(self.historyfile, 'r')
            entrycount = len(history.infolist())
            history.close()
            
        name = "v%s.txt" % entrycount
        
        history = ZipFile(self.historyfile, mode, zipfile.ZIP_DEFLATED)
        history.writestr(name, text)
        history.close()
        
    def getVersion(self, version):
        name = version + ".txt"
        history = ZipFile(self.historyfile, 'r')
        text = ""
        
        if name in history.namelist():
            text = history.read(name)
        
        return text
        
    def listVersions(self):
        out = []
        history = ZipFile(self.historyfile, 'r')
        
        for item in history.infolist():
            version = path.splitext(item.filename)[0]
            date = "%s-%02i-%02i %02i:%02i:%02i" % item.date_time
            pair = {'version': version, 'date': date}
            out.append(pair)
        
        history.close()
        return out
        
        
        
def main():
    name = 'Test'
    hist = history(name)
    text = """
    More old crap.
    """
    #hist.addPage(text)
    
    print "Entries: ", hist.listVersions()
    print "First entry: \n", hist.getVersion('v3')
    
    
if __name__ == '__main__':
    main()
    
    
 
