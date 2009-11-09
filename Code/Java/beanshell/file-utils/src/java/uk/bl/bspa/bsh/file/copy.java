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
 * <li><code>copy(String file, String todir)</code> Zips the specified folder into a file
 * in the parent directory.</li>
 * <li><code>copy(File file, File todir)</code>Zips the specified folder into a file in the parent
 * directory.</li>
 * </ul>
 */
public class copy {

    public static void invoke(Interpreter env, CallStack callstack, String from, String toDir){
        File fromFile = new File(from);
        File toFile = new File(toDir);
        invoke(env, callstack, fromFile, toFile);
    }
    
    
    public static void invoke(Interpreter env, CallStack callstack, File from, File toDir){
        try {
            if (from.isDirectory()){
                File[] files = from.listFiles();
                
                for(int i = 0; i < files.length; i++){
                    copyFromDir(files[i], toDir);
                }
            } else {
                copyFromDir(from, toDir);
            }
        } catch (IOException ex){
            ex.printStackTrace();
        }
    }
    
    private static void copyFromDir(File from, File to) throws IOException {
        if (from.isFile()){
            FileUtils.copyFileToDirectory(from, to);
            return;
        }
        
        if (from.isDirectory()){
            File[] files = from.listFiles();
            File nextTo = new File(to, from.getName());
            
            for(int i = 0; i < files.length; i++){
                copyFromDir(files[i], nextTo);
            }
        }
    }
}
