import ConfigParser

class config (ConfigParser.SafeConfigParser):
    def __init__(self, config_path):
        self.config_path = config_path
        self.read(config_path)
        
    def save(self):
        fh = open(config_path, 'w')
        parser.write(fh)

