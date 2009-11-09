//:folding=indent:collapseFolds=2:
package uk.bl.bspa.bsh.file;

import bsh.*;
import java.io.*;
import java.util.zip.*;
import java.util.*;
import java.util.regex.*;

/**
 * <p>
 * This class is a beanshell command module for unzipping zip files. To use it, 
 * make sure that the bsh-utils jar file is in the classpath, and add the 
 * commands in the package.
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
 * <li><code>unzip(String zipfile)</code> Unzips the specified file into the 
 * current directory.</li>
 * <li><code>unzip(File zipfile)</code>Unzips the specified file into the 
 * current directory.</li>
 * <li><code>unzip(File zipfile, File todir)</code>Unzips the specified file into the 
 * specified directory.</li>
 * <li><code>unzip(String zipfile, String todir)</code>Unzips the specified file into the 
 * specified directory.</li>
 * <li><code>unzip(Set zipfiles, String destination)</code>Unzips the specified files into the 
 * specified directory.</li>
 * <li><code>unzip(FileSet zipfiles, String destination)</code>Unzips the specified files into the 
 * specified directory.</li>
 * </ul>
 */
public class unzip {

    public static void invoke(Interpreter env, CallStack callstack, Set filesets, String dest){
        for (Iterator it = filesets.iterator(); it.hasNext(); ){
            FileSet fs = (FileSet) it.next();
            invoke(env, callstack, fs, dest);
        }
    }
    
    public static void invoke(Interpreter env, CallStack callstack, FileSet fs, String dest){
        File toDir = new File(dest);
        
        for (Iterator it = fs.files().iterator(); it.hasNext(); ){
            invoke(env, callstack, (File) it.next(), toDir);
        }
    }
    
    public static void invoke(Interpreter env, CallStack callstack, String path){
        File file = new File(path);
        System.out.println("F: " + file);
        invoke(env, callstack, file);
    }
    
    
    public static void invoke(Interpreter env, CallStack callstack, File file){
        File dir = file.getAbsoluteFile().getParentFile();
        invoke(env, callstack, file, dir);
    }
    
    
    public static void invoke(Interpreter env, CallStack callstack, String path, String toDir){
        File file = new File(path);
        File dir = new File(toDir);
        invoke(env, callstack, file, dir);
    }
    
    public static void invoke(Interpreter env, CallStack callstack, File file, File toDir){
        if (!toDir.exists()){
            toDir.mkdirs();
        }

        if (!file.exists()){
            System.err.println("No such file: " + file.getAbsolutePath());
            return;
        }

        if (!toDir.isDirectory()){
            //throw exception.
            return;
        }
                
        try {
            ZipFile zip = new ZipFile(file);
            for (Enumeration en = zip.entries(); en.hasMoreElements(); ){
                ZipEntry ze = (ZipEntry) en.nextElement();
                String name = ze.getName();
                
                if (name.endsWith("/")){
                    continue;
                }
                
                File toFile = new File(toDir, name);
                File parentDir = toFile.getParentFile();
                
                if (!parentDir.exists()){
                    parentDir.mkdirs();
                }
                
                BufferedInputStream is = new BufferedInputStream(zip.getInputStream(ze));
                BufferedOutputStream os = new BufferedOutputStream(
                                                new FileOutputStream(toFile));
                byte[] buffer = new byte[256];
                while (true){
                    int bytesRead = is.read(buffer);
                    if (bytesRead == -1){
                        break;
                    }
                    os.write(buffer, 0, bytesRead);
                }
                
                is.close();
                os.close();
            }
        } catch(IOException ex){
            ex.printStackTrace();
        }
    }
}
