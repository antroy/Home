package uk.bl.bspa.bsh.file;

import bsh.*;
import java.io.*;
import java.util.zip.*;
import java.util.*;
import org.apache.commons.io.*;
import org.apache.commons.io.filefilter.*;

public class FileSet {
    Set includes = new HashSet();
    Set excludes = new HashSet();
    File dir;
    
    public FileSet(String dir){
        this.dir = new File(dir);
    }
    
    public FileSet(File dir){
        this.dir = dir;
    }
    
    public void include(String pattern, boolean recurse){
        includes.add(new Include(dir, pattern, recurse));
    }
    
    public void include(String pattern){
        includes.add(new Include(dir, pattern, false));
    }
    
    public void exclude(String pattern){
        excludes.add(new Exclude(pattern));
    }
    
    public void clear(){
        includes.clear();
        excludes.clear();
    }
    
    public Set files(){
        Set out = new HashSet();
        
        for (Iterator it = includes.iterator(); it.hasNext(); ){
            Include inc = (Include) it.next();
            out.addAll(inc.getFiles());
        }
        
        for (Iterator it = excludes.iterator(); it.hasNext(); ){
            Exclude exc = (Exclude) it.next();
            exc.removeExcludedFilesFromSet(out);
        }
        
        return out;
    }
    
    class Include {
        File dir;
        FileFilter filter;
        boolean recurse;
        
        public Include(File dir, String pattern, boolean recurse){
            this.dir = dir;
            this.recurse = recurse;
            filter = new PatternFilter(pattern);
        }
        
        public Set getFiles(){
            return getFiles(dir);
        }
        
        private Set getFiles(File folder){
            Set out = new HashSet();
            File[] files = folder.listFiles(filter);
            
            for(int i = 0; i < files.length; i++){
                File f = files[i];
                out.add(f);
            }
            
            if (recurse){
                File[] folders = folder.listFiles((FileFilter) DirectoryFileFilter.INSTANCE);
                
                for(int i = 0; i < folders.length; i++){
                    File f = folders[i];
                    out.addAll(getFiles(f));
                }
            }
            
            return out;
        }
        
    }
    
    class Exclude {
        PatternFilter filter;
        
        public Exclude(String pattern){
            filter = new PatternFilter(pattern);
        }
        
        public void removeExcludedFilesFromSet(Set includes){
            for (Iterator it = includes.iterator(); it.hasNext(); ){
                File file = (File) it.next();
                
                if (filter.accept(file)){
                    it.remove();
                }
            }
        }
        
    }
}
