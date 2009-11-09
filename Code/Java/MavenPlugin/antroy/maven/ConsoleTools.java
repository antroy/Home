package antroy.maven;

import java.util.*;
import org.gjt.sp.jedit.*;
import console.*;

public class ConsoleTools {

    private View view;
    private Map<String, String> pathMap;
    
    public ConsoleTools(View view){
        this.view = view;
        this.pathMap = pathMap;
        
    }
    
    void consoleRun(MavenProject project, String goal){
        String p = project.getBasePath();
        
        runInSystemShell("cd " + p);
        
        try{
            Thread.sleep(500);
        } catch (InterruptedException ex){}
        
        runInSystemShell("maven " + goal);
    }
    
    void runInSystemShell(String command){
        
         // Open the console if it isn't already open
        view.getDockableWindowManager().addDockableWindow("console");
    
        // Obtain the console instance
        Console console = (Console) view.getDockableWindowManager().getDockable("console");
    
        // Set the shell to use
        Shell _shell = Shell.getShell("System");
        console.setShell(_shell);
    
        // Run the command
        console.run(_shell,console,command);

    }

    
}

