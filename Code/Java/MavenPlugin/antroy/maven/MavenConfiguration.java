package antroy.maven;

import java.util.*;
import java.io.*;

public class MavenConfiguration {
    
    private static final MavenConfiguration instance = new MavenConfiguration();
    
    private static final String GOAL_PROP = "maven.common.goal.";
    private static final String PROJECT_PROP = "maven.project.";
    
    private List<String> commonGoals;
    private List<File>   projectXmlFiles;  
    
    private MavenConfiguration(){
        refresh();
    }
    
    public static MavenConfiguration getInstance(){
        return instance;
    }
    
    public void refresh(){
        commonGoals = new LinkedList<String>();
        projectXmlFiles = new LinkedList<File>();  
        
        Properties props = new Properties();
        try{
            FileInputStream is = new FileInputStream(MavenPlugin.MAVEN_PROPS_FILE);
            props.load(is);
            is.close();
        } catch (IOException ex){
            
        }
        
        String goal = props.getProperty(GOAL_PROP + 0);
        
        for (int i = 1; goal != null; i++){
            commonGoals.add(goal);
            goal = props.getProperty(GOAL_PROP + i);
        }
        
        String proj = props.getProperty(PROJECT_PROP + 0);
        
        for (int i = 1; proj != null; i++){
            projectXmlFiles.add(new File(proj));
            proj = props.getProperty(PROJECT_PROP + i);
        }
        
    }
    
    public List<String> getCommonGoals(){
        return commonGoals;
    }
    
    public List<File> getProjectFiles(){
        return projectXmlFiles;
    }
    
    public void save(){
        Properties props = new Properties();
        
        int i = 0;
        
        for (String goal : commonGoals){
            props.setProperty(GOAL_PROP + i, goal);
            i++;
        }
        
        i = 0;
        
        for (File file : projectXmlFiles){
            props.setProperty(PROJECT_PROP + i, file.getAbsolutePath());
            i++;
        }
        
        try{
            FileOutputStream os = new FileOutputStream(MavenPlugin.MAVEN_PROPS_FILE);
            props.store(os, "Configuration saved by MavenConfiguration");
            os.close();
        } catch (IOException ex){
            ex.printStackTrace();
        }
        
    }
    
}
