import urllib2, cookielib, sys, re, itertools, csv
from urllib2 import Request, HTTPError, URLError
from urllib import urlencode
from threading import Thread


# Global functions.

def _assertion_count(parser_dict):
    """This function counts the parsers which are actually assertions in the given dictionary"""
    count = 0
    values = parser_dict.values()

    for p in values:
        try:
            if p.assertion:
                count += 1
        except:
            pass
            
    return count



class Web(object):
    """The Web class represents the environment you are running against.

    An instance of this class is required in order to run Actions."""
    def __init__(self, base_url, verbose=False, parameter_dict=None, default_parser_dict=None, **kw):
        """Creates a new Web object.

        The parameters are as follows:
            base_url - the base URL from which Action urls will
                be relative to.
            verbose - if set to True, debugging information will
                be output.
            default_parser_dict - a dictionary of parsers which
                will be applied to the html output of the Action.
            Any remaining keyword arguments are added to the default_parser_dict dictionary.
            """
        self.base_url = base_url
        self.verbose = verbose
        
        self.current_url = ""
        self.current_page = ""
        self.current_headers = {}
        #self.current_output = {}
        
        if parameter_dict is None:
            parameter_dict = {}
        self.parameter_dict = parameter_dict
            
        if default_parser_dict is None:
            default_parser_dict = {}
        self.parsers = default_parser_dict
        self.parsers.update(kw)
        self.assertions_expected = 0
        self.assertion_results = []
        
        policy = cookielib.DefaultCookiePolicy(rfc2965=True)
        cj = cookielib.CookieJar(policy)
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        
    def run(self, runnable, abort_on_error=False, input_dict=None):
        """This method takes the input runnable (Action or Chain object)
        and runs it in the current Web environment. There is an optional 
        'input_dict' parameter that takes a dictionary as input to the Action
        or Chain being run. This is useful if you need to run a sequence of Chain
        or Action objects, and want to pass the output from one into the next.
        
        Note that output from running an Action is a dictionary with the same 
        keys as the Action's parser dictionary with values equal to the 
        corresponding parsers output. Any default parsers in the Web environment 
        are appended to each Action's parser dictionary. Running a Chain provides 
        the last Action's (optionally postprocessed) output.

        There is also an optional 'abort_on_error' parameter which is set to False by
        default. On a server error, by default the run method will return None allowing
        scripts to recover, or abort depending on requirements. If set to True, sys.exit(1)
        is called.

        """

        self.assertions_expected = self.assertion_count(runnable)

        if hasattr(runnable, 'disabled') and runnable.disabled == True:
            return {}

        try:
            if isinstance(runnable, Action):
                return self._run_action(runnable, input_dict)
            elif isinstance(runnable, Chain):
                return self._run_chain(runnable, input_dict)
            else:
                raise TypeError, "The runnable parameter for the run() method must be an Action or Chain object."
        except HTTPError, ex:
            print "Request to go to URL %s resulted in Error Code %d" % (ex.geturl(), ex.code)
            if abort_on_error:
                sys.exit(1)
            return None
        except URLError, ex:
            code, message = ex.args[0].args
            print "URL could not be opened: %s. Error code: %s" % (message, code)
            if abort_on_error:
                sys.exit(1)
            return None
            
    def add_default_parser(self, key, parser):
        self.parsers[key] = parser
    
    def add_default_assertion(self, key, parser):
        parser.assertion = True
        self.parsers[key] = parser
            
    def assertion_count(self, runnable):
        out = _assertion_count(self.parsers)
        out += runnable.assertion_count()

        return out


    def print_results(self):
        """
        Prints the results of any assertions that were run to std out.
        """
        print "\n TEST RESULTS:- \n"
        successCount = 0
        for k, g in itertools.groupby(self.assertion_results, lambda x: x[0]):
            print "%s:" % k
            for x in g:
                test, success, mssg = x[1], x[2], x[3]
                print "\t%s - %s" % (test, ("FAILED", "OK")[success]),
                print mssg and mssg or ''
                if success: 
                    successCount += 1
        total_assertions = self.assertions_expected

        print "Total number of assertions that should have run:", total_assertions
        print "Number of assertions that actually ran:", len(self.assertion_results)
        print "Number of successful assertions:", successCount


        if successCount == total_assertions:
            print "\nAll tests Succeeded!"
        else:
            print 
            print "WARNING - %d tests Failed." % (len(self.assertion_results) - successCount)
            print "        - %d tests did not run." % (total_assertions - len(self.assertion_results))


    def _run_chain(self, chain, input_dict=None):
        output = None
        
        for action, post_processor in chain:
            output_dict = self._run_action(action, input_dict)
            output = output_dict
            if post_processor:
                input_dict = post_processor(action, output_dict)
                output = input_dict
                #self.current_output = output
            
        return output
    
    def _run_action(self, action, input_dict):
        action.verbose = self.verbose
        if self.verbose:
            print "Running Action: %s" % action.rel_url
            print "parser_dict", [k for k,v in action.parser_dict.iteritems()]
            
        full_url = self.base_url + action.rel_url
        
        query = action.getQuery(self.parameter_dict, input_dict)
        page = self._fetch_page(full_url, query, action)
        out = self._parse_page(full_url, page, action)
        
        #self.current_output = out

        return out
        
    def _fetch_page(self, full_url, query, action):
        if self.verbose:
            print "Fetching: %s" % full_url
            print "Query: %s" % query
        
        url  = ""
        
        if action.method == "POST":
            url = Request(full_url)
            url.add_data(query)
        elif action.method in ["GET", "HEAD"]:
            url = "%s?%s" % (full_url, query)
        else:
            raise NotImplementedError
        
        resp = self.opener.open(url)
        page = resp.read()
        resp.close()
    
        self.current_url = resp.geturl()
        self.current_page = page
        self.current_headers = resp.info()

        return page
        
    def _parse_page(self, url, page, action):
        parser_dict = self.parsers.copy()
        parser_dict.update(action.parser_dict)

        out = action.extra_output

        for k, v in parser_dict.iteritems():
            if self.verbose:
                print "Parser %s (%s) running." % (k, v.__name__)
            
            assertion = False

            try:
                assertion = v.assertion
            except:
                pass
            
            parse_output = v(page)

            
            if not parse_output == None:
                out[k] = parse_output
    
            if assertion:
                result, mssg = False, ''
                if type(parse_output) == bool:
                    result = parse_output
                else:
                    result, mssg = parse_output
                    
                if result == True:
                    self.assertion_results.append((url, k, True, mssg))
                    if self.verbose:
                        print "%s: OK %s" % (k, mssg and "[%s]" % mssg or '')
                else: 
                    self.assertion_results.append((url, k, False, mssg))
                    if self.verbose:
                        print "%s: FAILED %s" % (k, mssg and "[%s]" % mssg or '')

        return out
        
        

class DataManager(object):
    """The DataManager is responsible for reading data from a CSV
    File. The first row of the file should be the keys of the 
    dictionary, and subsequent rows the values.
    """
    def __init__(self, filename):
        self.__data_list = []
        self.__count = 0
        
        fh = None
        
        if isinstance(filename, str):
            fh = file(filename)
        else:
            fh = filename
            
        reader = csv.DictReader(fh)
        for data in reader:
            self.__data_list.append(data)
        fh.close()
        
    
    def __iter__(self):
        return (x for x in self.__data_list)
    
    def __str__(self):
        return str(self.__data_list)
        

class BatchRunner(object):
    def __init__(self, base_url, threaded=False, verbose=False, parsers=None, **kw):
        self.base_url = base_url
        self.verbose = verbose
        self.threaded = threaded
        if parsers == None:
            parsers = {}
        self.parsers = parsers
        self.parsers.update(kw)
    
    def run(self, runnable, data_manager, print_results=False):
        for data in data_manager:
            web_runner = WebRunner(self.base_url, runnable, self.verbose, data, self.parsers)
            web_runner.print_results_on_exit = print_results
            if self.threaded:
                web_runner.start()
            else:
                web_runner.run()
    
class WebRunner(Thread):
    def __init__(self, base_url, runnable, verbose=False, parameter_dict=None, default_parser_dict=None):
        Thread.__init__(self)
        self.web_obj = Web(base_url, verbose, parameter_dict, default_parser_dict)
        self.runnable = runnable
        self.print_results_on_exit = False
            
    def run(self):
        self.web_obj.run(self.runnable)
        if self.print_results_on_exit:
            self.web_obj.print_results()
        
            
class Chain(list):
    """The Chain class represents a sequence of Action objects that should be 
    run in order. When run, each Action is run in turn, and any associated 
    post_processors are applied to the output from the Action."""
    def add(self, obj, post_processor=None):
        """This method takes either an Action or another Chain as the first parameter
        and adds them to this chain. If the object is an Action, and the optional
        post_processor is provided, then the post_processor is associated with the Action.
        
        Note that post_processors must take two parameters, an Action object and 
        a dictionary and should return another dictionary.
        """
        if isinstance(obj, Action):
            self.append((obj, post_processor))
        elif isinstance(obj, Chain):
            self.extend(obj)
        else:
            raise TypeError

    def assertion_count(self):
        count = 0
        for action, proc in self:
            count += action.assertion_count()
            
        return count
            
class Action(object):
    """This class defines a request to be run against a Web environment.
    The most important parameter is the relative_url which is appended to 
    the base_url of the Web environment. 
    
    The optional params parameter
    should be a dictionary of the key-value pairs to be sent as the request 
    parameters. 
    
    The parsers optional parameter should be a dictionary of
    parser callables that take a string (the page fetched from the URL) as 
    their only parameter, and returns a value. The output from running the 
    Action is a dictionary with the same keys as the parsers dictionary with 
    values equal to the corresponding parsers output. Note that parsers can 
    be either straight parsers for extracting data from a page, or assertions 
    which report True or False on the content of a page. The latter must be 
    callables with the attribute 'assertion' set to True.
    
    The initializer optional parameter should be a callable which takes an Action
    object and a dictionary as input parameters. It is used for changing the state
    of the action given input from a previous action. It could be used to add 
    parsers for example, or additional parameters.
    
    The method defaults to POST, but can be set to GET.
    
    Any additional keyword arguments should be parsers, as they are added to 
    the parser dictionary."""
    def __init__(self, relative_url, params=None, param_prefix=None, overrides=None, parsers=None, 
                                method="POST", **kw):
        self.rel_url = relative_url
        if params is None:
            params = []
        self.params = params
        
        if overrides is None:
            overrides = {}
        self.overrides = overrides
        
        self.param_prefix = param_prefix
            
        self.method = method
        self.extra_output = {}
        
        if parsers is None:
            parsers = {}
        self.parser_dict = parsers
        self.parser_dict.update(kw)
    
    def assertion_count(self):

        return _assertion_count(self.parser_dict)
        
    def getQuery(self, parameter_dict, additional_overrides):
        def rem_prefix(s):
            if self.param_prefix and s.startswith(self.param_prefix):
                return s[len(self.param_prefix) + 1:]
            return s
        
        def filterParams(param_dict, prefix_filter=lambda x: x):
            filtered = [(prefix_filter(k), v) for k, v in param_dict.iteritems() 
                                             if prefix_filter(k) in self.params]
            return dict(filtered)
            
        parameters = filterParams(parameter_dict, rem_prefix)
                                                     
        parameters.update(self.overrides)
        if additional_overrides:
            parameters.update(additional_overrides)
        
        parameters = filterParams(parameters)
            
        out = urlencode(parameters)
        
        if self.verbose:
            paramstr =  "\n=====  Parameter List  =====\n"
            paramstr += "%s\n"
            paramstr += "----------------------------\n"
            print paramstr % out
        
        return out

        
    def add_parser(self, key, parser):
        """Method for adding additional parsers to the Action."""
        self.parser_dict[key] = parser
        
    def add_assertion(self, key, parser):
        """Method for adding additional assertions to the Action."""
        parser.assertion = True
        self.add_parser(key, parser)
        


__all__ = ('Web', 'Chain', 'Action', 'DataManager', 'BatchRunner')        

# ================================================================
# ==                     T E S T S                              ==
# ================================================================


def run_test():
    webEnv = Web("http://antroy.homelinux.net/", {}, verbose=True)

    def isBobHome(page):
        return page.find("BOB") >= 0

    ass = isBobHome
    ass.assertion = True

    print "About to run action"
    act = Action('', bob_home=ass)
    webEnv.run(act)

if __name__ == "__main__":
    _globals = dict(globals())
    tests = [v for k,v in _globals.iteritems() if k.endswith("test")]
    
    for test in tests:
        test()

