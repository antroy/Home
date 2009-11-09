from pyparsing import *

def surround(template):
    def _out(s, loc, toks):
        return [template % t for t in toks]
    return _out

def parse(text):
    bold = QuotedString(quoteChar="'''")
    bold.setParseAction( surround("<b>%s</b>") )

    italics = QuotedString(quoteChar="''")
    italics.setParseAction( surround("<i>%s</i>") )

    bold_italic = QuotedString(quoteChar="'''''")
    bold_italic.setParseAction( surround("<b><i>%s</i></b>") )

    parser = bold_italic | bold | italics
    #parser = Optional(italics)

    #parsed_text = parser.scanString(text)
    parsed_text = parser.transformString(text)


    return parsed_text


res = parse("Test this is '''bold''' '''''bold-italic?''''', but this is ''italic''.")
print res


