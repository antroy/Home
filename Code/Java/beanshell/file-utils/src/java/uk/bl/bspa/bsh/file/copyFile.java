package uk.bl.bspa.bsh.file;

import bsh.*;
import java.io.*;
import java.util.zip.*;
import java.util.*;
import org.apache.commons.io.*;

/**
 * <p>
 * This class is a beanshell command module for copying files. 
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
 * <li><code>copyFile(String fromFile, String toFile)</code> Zips the specified folder into a file
 * in the parent directory.</li>
 * <li><code>copyFile(File fromFile, File toFile)</code>Zips the specified folder into a file in the parent
 * directory.</li>
 * </ul>
 */
public class copyFile {

    public static void invoke(Interpreter env, CallStack callstack, String from, String to){
        File fromFile = new File(from);
        File toFile = new File(to);
        invoke(env, callstack, fromFile, toFile);
    }
    
    public static void invoke(Interpreter env, CallStack callstack, File from, File to){
        try {
            FileUtils.copyFile(from, to);
        } catch (IOException ex){
            ex.printStackTrace();
        }
    }
}
