# Parse output from Live Http Headers to produce actions.
import sys

app_template = r"""
from orb import *
import orb.parsers as parsers

base_url = "http://localhost:8080"
dump_file = r"c:\0\app.html"

def main():
    web_env = Web(base_url, 
                    dumper=parsers.get_dump_page_parser(dump_file))
    
    chain = Chain()
    
%s
    
    web_env.run(chain)
    
if __name__ == "__main__":
    main()

"""

def parse(from_file, to_file):
    fh = file(from_file)
    lines = fh.readlines()
    fh.close()
    
    triples = []
    
    for line in lines:
        triple = parse_line(line)
        if triple:
            triples.append(triple)
        
    buff = []
    format_triples(triples, buff)
    out = app_template % "\n".join(buff)
    
    fh_out = file(to_file, 'w')
    fh_out.write(out)
    fh_out.close()
    
def format_triples(triples, buff):
    count = 0
    param_template =  "    params_%d = %s"
    action_template = '    chain.add(Action("%s", %smethod="%s"))' 
    
    for triple in triples:
        count += 1
        param_str = ''
        if len(triple[2]) > 0:
            buff.append(param_template % (count, repr(triple[2])))
            param_str = "params_%d, " % count
        else:
            param_str = ""
        buff.append(action_template % (triple[1], param_str, triple[0]))
        buff.append("    ")
            
def parse_line(line):
    parts = line.split()
    
    part_count = len(parts)
    
    if (part_count < 2):
        return False
    
    req_type = parts[0].strip()
    req_url = parts[1].strip()
    
    params = {}
    
    if req_type == "POST" and part_count > 2:
        param_parts = parts[2].split('&')
        for part in param_parts:
            pair = part.split('=', 2)
            params[pair[0]] = pair[1]
        
    return (req_type, req_url, params)
    
if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) > 1:
        parse(*args)
