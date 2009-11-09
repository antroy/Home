class Options {
    var _options = Map()
    var _args = new ArrayList()

    def addOpt(name: String, value: String){
        _options(name) = value
    }

    def addArgs(args: 
}

class Action(dest: String, type: String){
    def dest = dest
    def type = type
}

class OptParse {
    
    var actionMap = Map()

    def get_opts(args: Array[String]){
        return null
    }

    def add_option(short_arg: String, long_arg: String, dest: String, type: String){
        actionMap(short_arg) = (dest, type)
        actionMap(long_arg) = (dest, type)
    }
}

object Parser {

    def main(args: Array[String]){
        var parser = new OptParse()
        parser.add_option("-p", "--pattern", "pattern")

        var options = parser.get_opts(args)
        println("Opts: " + options)

    }
}

