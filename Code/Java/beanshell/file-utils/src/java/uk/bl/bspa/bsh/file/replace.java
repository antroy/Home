package uk.bl.bspa.bsh.file;

import bsh.*;
import java.io.*;
import java.util.zip.*;
import java.util.*;
import org.apache.commons.io.*;

/**
 * <p>
 * This class is a beanshell command module for replacing patterns within files.
 *  Note that this will probably fail for large files, since it sucks the entire 
 * file in before doing any substitution.
 * To use it, make sure that the 
 * bsh-utils jar file is in the classpath, and add the commands in the package.
 * For example, the following snippet dynamically adds the jar to the classpath,
 * and then add all commands in the package <code>uk.bl.bspa.bsh.file</code>:
 * </p>
 * <pre>
 * addClassPath("lib/bsh-utils.jar");
 * importCommands("uk.bl.bspa.bsh.file");
 * </pre>
 * <p>
 * The following commands are provided:
 * </p>
 * <ul>
 * <li><code>replace(String file, String find, String replace, boolean regex)</code> 
 * Replaces all instances of <i>find</i> with <i>replace</i> in the file <i>file</i>
 * and then saves it.
 * If regex is set to true, the find and replace strings are treated as regular expression
 * find and replace strings.</li>
 * <li><code>copy(File file, File todir)</code>
 * Replaces all instances of <i>find</i> with <i>replace</i> in the file <i>file</i>
 * and then saves it.
 * If regex is set to true, the find and replace strings are treated as regular expression
 * find and replace strings.</li>
 * 
 * </ul>
 */
public class replace {

    public static final String ENCODING = System.getProperty("file.encoding");
    
    public static void invoke(Interpreter env, CallStack callstack, Set fileset, Map replaceMap, boolean regex){
        for (Iterator it = fileset.iterator(); it.hasNext(); ){
            FileSet fs = (FileSet) it.next();
            invoke(env, callstack, fs, replaceMap, regex);
        }
    }
    
    public static void invoke(Interpreter env, CallStack callstack, FileSet fs, Map replaceMap, boolean regex){
        for (Iterator it = fs.files().iterator(); it.hasNext(); ){
            File file = (File) it.next();
            invoke(env, callstack, file, replaceMap, regex);
        }
    }
    
    public static void invoke(Interpreter env, CallStack callstack, Set files, String find, String replace, boolean regex){
        for (Iterator it = files.iterator(); it.hasNext(); ){
            File file = (File) it.next();
            invoke(env, callstack, file, find, replace, regex);
        }
    }
    
    public static void invoke(Interpreter env, CallStack callstack, String file, String find, String replace, boolean regex){
        File f = new File(file);
        invoke(env, callstack, f, find, replace, regex);
    }
    
    public static void invoke(Interpreter env, CallStack callstack, File file, String find, String replace, boolean regex){
        Map replaceMap = new HashMap();
        replaceMap.put(find, replace);
        invoke(env, callstack, file, replaceMap, regex);
    }
    
    public static void invoke(Interpreter env, CallStack callstack, String file, Map replaceMap, boolean regex){
        File f = new File(file);
        invoke(env, callstack, f, replaceMap, regex);
    }
    
    public static void invoke(Interpreter env, CallStack callstack, File file, Map replaceMap, boolean regex){
        for (Iterator it = replaceMap.keySet().iterator(); it.hasNext(); ){
            String find = (String) it.next();
            String replace = (String) replaceMap.get(find);
            
            if (replace == null){
                System.err.println("Replacement value for " + find + "is null. Replacing with *NULL* instead");
                replace = "*NULL*";
            }
            
            if (regex){
                replaceRegex(file, find, replace);
            } else {
                replaceString(file, find, replace);
            }
        }
    }
    
    private static void replaceString(File file, String find, String replace){
        try {
            String inText = FileUtils.readFileToString(file, ENCODING);
            
            StringBuffer out = new StringBuffer();
            int fromIndex = 0;
            
            for(;;){
                int index = inText.indexOf(find, fromIndex);
                if (index == -1){
                    out.append(inText.substring(fromIndex, inText.length()));
                    break;
                }
                
                out.append(inText.substring(fromIndex, index));
                out.append(replace);
                fromIndex = index + find.length();
            }
            
            FileUtils.writeStringToFile(file, out.toString(), ENCODING);
        } catch (IOException ex){
            ex.printStackTrace();
        }
    }
    
    private static void replaceRegex(File file, String find, String replace){
        try {
            String inText = FileUtils.readFileToString(file, ENCODING);
            String outText = inText.replaceAll(find, replace);
            FileUtils.writeStringToFile(file, outText, ENCODING);
        } catch (IOException ex){
            ex.printStackTrace();
        }
    }
}
