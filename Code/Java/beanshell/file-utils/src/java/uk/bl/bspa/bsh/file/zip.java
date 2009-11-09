package uk.bl.bspa.bsh.file;

import bsh.*;
import java.io.*;
import java.util.zip.*;
import java.util.*;

/**
 * <p>
 * This class is a beanshell command module for zipping folders into a zip archive. 
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
 * <li><code>zip(String folderPath)</code> Zips the specified folder into a file
 * in the parent directory.</li>
 * <li><code>zip(File folder)</code>Zips the specified folder into a file in the parent
 * directory.</li>
 * <li><code>zip(File fromFolder, File toFile)</code>Zips the specified folder into the 
 * specified zip file.</li>
 * <li><code>zip(String fromDir, String toFile)</code>Zips the specified folder into the 
 * specified zip file.</li>
 * </ul>
 */
public class zip {

    private static final String FILE_SEP = System.getProperty("file.separator","/");
    private static final String COMMENT = "Files Zipped by British Library Remote "
    		+ "Services Team beanshell zip utility.";
    
    public static void invoke(Interpreter env, CallStack callstack, String path){
        File file = new File(path);
        invoke(env, callstack, file);
    }
    
    
    public static void invoke(Interpreter env, CallStack callstack, File dir){
        File toFile = new File(dir.getAbsoluteFile().getParentFile(), dir.getName() + ".zip");
        // Test to ensure dir is a folder.
        invoke(env, callstack, dir, toFile);
    }
    
    
    public static void invoke(Interpreter env, CallStack callstack, String filePath, String toFile){
        File file = new File(filePath);
        File dir = new File(toFile);
        invoke(env, callstack, file, dir);
    }
    
    
    public static void invoke(Interpreter env, CallStack callstack, File file, File toFile){
        File toDir = toFile.getAbsoluteFile().getParentFile();
        if (!toDir.exists()){
            toDir.mkdirs();
        }
        
        if (!file.exists()){
            System.err.println("No such directory: " + file.getAbsolutePath());
            return;
        }
        
        List files = listFiles(file);
        
        try {
            ZipOutputStream os = new ZipOutputStream(new FileOutputStream(toFile));
            os.setMethod(ZipOutputStream.DEFLATED);
            os.setComment(COMMENT);
            int i = 5;
            for (Iterator it = files.iterator(); it.hasNext(); i++){
                File f = (File) it.next();
                String entryName = nameRelativeTo(f, file);
                
                ZipEntry entry = new ZipEntry(entryName);
                entry.setComment(COMMENT);
                entry.setSize(f.length());
                entry.setTime(f.lastModified());
                
                os.putNextEntry(entry);
                
                BufferedInputStream is = new BufferedInputStream(new FileInputStream(f));
                
                byte[] buffer = new byte[1024];
                while (true){
                    int bytesRead = is.read(buffer);
                    if (bytesRead == -1){
                        break;
                    }
                    os.write(buffer, 0, bytesRead);
                }
                
                is.close();
                os.closeEntry();
            }
            os.close();
            
        } catch(IOException ex){
            ex.printStackTrace();
        }
    }
    
    private static List listFiles(File file){
        List out = new LinkedList();
        if (file.isFile()){
            out.add(file);
        } else if (file.isDirectory()){
            File[] farr = file.listFiles();
            for(int i = 0; i < farr.length; i++){
                out.addAll(listFiles(farr[i]));
            }
        }
        
        return out;
    }
    
    private static String nameRelativeTo(File path, File context){
        String out = path.getAbsolutePath();
        String c = context.getAbsolutePath();
        
        if (out.startsWith(c)){
            out = out.substring(c.length());
        }
        
        if (out.startsWith(FILE_SEP)){
            out = out.substring(FILE_SEP.length());
        }
        
        return out.replace('\\','/');
    }
}
