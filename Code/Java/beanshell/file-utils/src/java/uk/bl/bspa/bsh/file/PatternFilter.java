package uk.bl.bspa.bsh.file;

import bsh.*;
import java.io.*;
import java.util.regex.*;
import java.util.*;
import org.apache.commons.io.*;

public class PatternFilter implements FileFilter, FilenameFilter {

    Pattern pattern;
    
    public PatternFilter(String regex){
        pattern = Pattern.compile(regex);
    }
    
    public PatternFilter(Pattern regex){
        pattern = regex;
    }

    public boolean accept(File path){
        Matcher m = pattern.matcher(path.getAbsolutePath());
        return m.matches();
    }
    
    public boolean accept(File dir, String name){
        return accept(new File(dir, name));
    }
}
