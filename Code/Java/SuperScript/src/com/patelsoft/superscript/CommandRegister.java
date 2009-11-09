package com.patelsoft.superscript;

import java.util.*;
import org.gjt.sp.jedit.View;
import org.apache.bsf.*;

public final class CommandRegister {
	
    public static final CommandRegister REGISTER = new CommandRegister();
    
    private Map register = new HashMap();
    private Map aliasMap = new HashMap();
    BSFController controller = BSFController.getInstance();
    
    public CommandRegister getInstance(){
        return REGISTER;
    }
    
    private CommandRegister(){
        registerCommand(new HelpCommand(), "help");
        registerCommand(new SetLangCommand(), "set-lang");
        registerCommand(new ShowLangsCommand(), "show-langs");
        String[] runAliases = {"run-buffer", "rb"};
        registerCommand(new RunBufferCommand(), runAliases);
    }
    
    public void registerCommand(InternalCommand command, String[] name){
        for (int i=0; i < name.length; i++){
            aliasMap.put(name[i], name[0]);
        }
        register.put(name[0], command);
    }
    
    public void registerCommand(InternalCommand command, String name){
        String[] names = {name};
        registerCommand(command, names);
    }
    
    public boolean unregisterCommand(String name){
        return register.remove(name) != null;
    }
    
    public InternalCommand getCommand(String alias){
        Object name = aliasMap.get(alias);
        
        if (name == null) {
            return new HelpCommand("Your command was: " + alias);
        }
        
        return (InternalCommand) register.get(name);
    }
    
    private class ShowLangsCommand implements InternalCommand {
    
        public String getDescription(){
            return "Displays a list of supported languages.";
        }
        
        public String exec(View view, String[] args){
            
			StringBuffer out = new StringBuffer();
			try {
				String[] arr = controller.getAllLanguages(view);
				for (int i = 0; i < arr.length; i++){
					out.append(arr[i]);
					out.append("\n");
				}
				
				return out.toString();
			} catch (BSFException ex){
				return ex.getMessage();
			}
        }
	} 
        
    private class SetLangCommand implements InternalCommand {
    
        public String getDescription(){
            return "Sets the current language to the parameter value (if supported).";
        }
        
        public String exec(View view, String[] args){
			String[] arr = {};
			
			try {
				arr = controller.getAllLanguages(view);
			} catch (BSFException ex){
				return ex.getMessage();
			}
			
			String lang = args[0];
			
			for  (int i = 0; i < arr.length; i++){
				if (lang.equals(arr[i])){
					controller.setCurrentLanguage(lang);
					return "Language set to " + lang;
				}
			}
			
			return "Language " + lang + " not available!";
		}
    }
    
    private class RunBufferCommand implements InternalCommand {
    
        public String getDescription(){
            return "Run the current buffer as a script.";
        }
        
        public String exec(View view, String[] args){
            try {
				return controller.executeScript(view);
			} catch (BSFException ex){
				return ex.getMessage();
			}
        }
    }
    
    
    private class HelpCommand implements InternalCommand {
        String firstline = "";
        
        HelpCommand(){}
        
        HelpCommand(String firstLine){
            firstline = firstLine + "\n";
        }
        
        public String exec(View view, String[] args){
            StringBuffer out = new StringBuffer(firstline);
            
            out.append("The following commands are available:\n");
            
            Map aliases = getAliases();
            
            for (Iterator it = register.entrySet().iterator(); it.hasNext(); ){
                Map.Entry e = (Map.Entry) it.next();
                out.append("  ");
                List aliasList = (List) aliases.get(e.getKey());
                
                for (Iterator it2 = aliasList.iterator(); it2.hasNext(); ){
                    out.append(it2.next());
                    if (it2.hasNext()) out.append(", ");
                }
                
                InternalCommand ic = (InternalCommand) e.getValue();
                
                out.append(": ");
                out.append(ic.getDescription());
                out.append("\n");
            }
            
            return out.toString();
        }
	
        private Map getAliases(){
            Map out = new HashMap();
            
            for (Iterator it = aliasMap.entrySet().iterator(); it.hasNext(); ){
                Map.Entry e = (Map.Entry) it.next();
                List list = null;
                Object listObj = out.get(e.getValue());
                
                if (listObj == null) {
                    list = new LinkedList();
                    out.put(e.getValue(), list);
                } else {
                    list = (List) listObj;
                }
                
                list.add(e.getKey());
            }
            
            return out;
        }
        
        public String getDescription(){
            return "Prints out a help message giving possible internal command options.";
        }
    }
}
