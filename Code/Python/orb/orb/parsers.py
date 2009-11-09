import os.path as path

def get_dump_page_parser(filename):
    """Returns a parser function that dumps the page into the file specified."""
    def increment():
        i = 0
        while True:
            yield i
            i += 1
    
    suffixIterator = None
    if filename.find('%d') >= 0:
        suffixIterator = increment()
        
    def dump_page_parser(page):
        fn = filename
                
        if suffixIterator:
            it = suffixIterator.next()
            fn = filename % it
        
        f = file(fn, 'w')
        f.write(page)
        f.close()
        
        return filename
    return dump_page_parser
    

__all__ = ('get_dump_page_parser')
    
# ================================================================
# ==                     T E S T S                              ==
# ================================================================


