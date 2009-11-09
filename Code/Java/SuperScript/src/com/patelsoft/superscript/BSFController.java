package com.patelsoft.superscript;

import java.io.*;
import org.gjt.sp.jedit.*;
import org.gjt.sp.util.*;
import javax.swing.*;
import java.util.Vector;
import java.util.Hashtable;
import java.util.Enumeration;
import java.awt.*;
import org.apache.bsf.*;
import java.awt.event.*;
import java.lang.reflect.Field;
import com.patelsoft.util.Logger;
import org.gjt.sp.jedit.gui.OptionsDialog;
import javax.swing.border.TitledBorder;
import java.util.StringTokenizer;
import java.util.List;

public class BSFController 
{
	private SuperScriptStream stdout=new SuperScriptStream(System.out),stderr= new SuperScriptStream(System.err);
	private Logger log = new Logger();
	private boolean pendingInitialization=true;
    private String currentLanguage = "beanshell";
    
    private static BSFController instance = new BSFController();

    private BSFController(){}
    
    public static BSFController getInstance(){
        return instance;
    }
    
    
    public void setCurrentLanguage(String lang){
        currentLanguage = lang;
    }
    
    public String getCurrentLanguage(){
        return currentLanguage;
    }
    
    
	String[] getAllLanguages(View view) throws BSFException
	{
		SuperScriptPlugin.loadBSFManager(view);
		try
		{
			Field registeredEngines = SuperScriptPlugin.bsfmanager.getClass().getDeclaredField("registeredEngines");
			registeredEngines.setAccessible(true);
			Hashtable lang2Engines = (Hashtable)registeredEngines.get(SuperScriptPlugin.bsfmanager);

			log.log(Logger.DEV,this,"Got Lang2Engines "+lang2Engines);

			Enumeration enumeration = lang2Engines.keys();
			Vector languages = new Vector();
			while(enumeration.hasMoreElements())
			{
				languages.addElement(enumeration.nextElement());
			}

			log.log(Logger.DEV,this,"See final languages "+ languages);

			return (String[])languages.toArray(new String[0]);
		}
		catch(Exception e)
		{
			log.log(Log.ERROR,this,e);
			return new String[0];
		}
	}


	public String executeScript(View view) throws BSFException
	{
		return this.executeScript(view, view.getTextArea().getText(),view.getBuffer().getName());
	}

	public String executeScript(View view, String script,String filename) throws BSFException
	{
		return this.executeScript(view, script, filename,getCurrentLanguage(),false);
	}

	String executeScript(View view,String script,String filename, String lang, boolean execFromMacro) throws BSFException
	{
		log.log(Logger.DEV, getClass(), "Entering executeScript");

		ClassLoader old = Thread.currentThread().getContextClassLoader();
		log.log(Logger.DEV, this.getClass(), "Setting CL to the new one in executeScript. Old is " + old);
		Thread.currentThread().setContextClassLoader(getClass().getClassLoader());
		log.log(Logger.DEV,this.getClass(),"After setting CL in executeScript");


		if(!execFromMacro)
		{
			stdout.setActive(true);
			stderr.setActive(true);
		}

		try
		{
			SuperScriptPlugin.loadBSFManager(view);
			SuperScriptPlugin.bsfmanager.exec(lang,filename,1,1,script);
			if(!execFromMacro)
			{
				return stdout.toString();
			}
		}
		catch(BSFException exp)
		{
			// log.log(Log.DEBUG, this.getClass(), "Caught BSFException in executeScript " + exp);
			log.log(Log.ERROR,this.getClass(),exp.getMessage());
			log.log(Logger.DEV, this.getClass(), "exp.getTargetException() " + exp.getTargetException());
			log.log(Logger.DEV, this.getClass(), "targetexception.getMessage() " + (exp.getTargetException() != null?exp.getTargetException().getMessage():null));
			//log.log(Log.ERROR,this,"Now printing target exception");
			//log.log(Log.ERROR,this,exp.getTargetException().getMessage());
			if(!execFromMacro)
			{
				return printError(view,exp);
			}
			throw exp;
		}
		finally
		{
			Thread.currentThread().setContextClassLoader(old);

			log.log(Logger.DEV,this.getClass(),"See contents of stdout in executeScript " + stdout);
			if(!execFromMacro)
			{
				stdout.reset();
				stderr.reset();
				stdout.setActive(false);
				stderr.setActive(false);
				// System.setErr(oldErrStream);
				// System.setOut(oldOutStream);
			}
			log.log(Logger.DEV, this.getClass(), "Leaving executeScript");
		}
        
        return "";
	}

	private String eval(View view,String command) throws BSFException
	{
		log.log(Logger.DEV, this.getClass(), "Entering eval");
		SuperScriptPlugin.loadBSFManager(view);
		Object obj = SuperScriptPlugin.bsfmanager.eval(getCurrentLanguage(),view.getBuffer().getName(),1,1,command);
		
        String out = stdout.toString();
		if(obj !=null && stdout.size() == 0) //Last condition is due to JS hack. Coz it prints to the sysout AND also returns object of type Undefined.
		{
			out += obj.toString();
		}
		/* else
		{
				log.log(Logger.DEV, this.getClass(), "Leaving eval");
				throw new BSFException(BSFException.REASON_INVALID_ARGUMENT,"Return value from eval is NULL");
		} */
		log.log(Logger.DEV, this.getClass(), "Leaving eval");
        
        return out;
	}


	String evalOrExecute(View view,String command)
	{
		log.log(Logger.DEV, this.getClass(), "Entering evalOrExecute");

		ClassLoader old = Thread.currentThread().getContextClassLoader();
		log.log(Logger.DEV,this.getClass(),"Going to set CL in evalOrExecute. Old CL is " + old);
		Thread.currentThread().setContextClassLoader(this.getClass().getClassLoader());
		log.log(Logger.DEV,this.getClass(),"After setting CL in evalOrExecute");

		// //initStreams();
		// PrintStream oldErrStream = System.err;
		// System.setErr(new PrintStream(stderr));
		// PrintStream oldOutStream = System.out;
		// System.setOut(new PrintStream(stdout));

		stderr.setActive(true);
		stdout.setActive(true);

		try
		{
			return this.eval(view,command);
		}
		catch(BSFException e)
		{
			//One last chance
			try
			{
				return this.executeScript(view, command,"<No Filename>");
			}
			catch(BSFException exp)
			{
				//printError(exp.getTargetException().toString());
				log.log(Log.ERROR, this.getClass(), exp);
			}
		}
		finally
		{
			log.log(Logger.DEV,this.getClass(),"Re-Setting the CL in Thread to "+ old);
			Thread.currentThread().setContextClassLoader(old);
			stdout.reset();
			stderr.reset();
			stdout.setActive(false);
			stderr.setActive(false);
			log.log(Logger.DEV, this.getClass(), "Leaving evalOrExecute");
		}
        
        return "ERROR";
	}

	private String exceptionToString(Throwable e)
	{
		if(e == null)
		{
			return null;
		}

		StringWriter strw = new StringWriter();
		if(e.getMessage() == null)
		{
			e.printStackTrace(new PrintWriter(strw));
		}
		else
		{
			strw.write(e.getMessage()+"\n");
		}
		return strw.toString();
	}


	String printError(View view,String err)
	{
		return "\n"+err;
	}

	String printError(View view,BSFException exp)
	{
		return printError(view,exceptionToString((exp.getTargetException()==null?exp:exp.getTargetException())));
	}

	public Logger getLog()
	{
		return log;
	}

	SuperScriptStream getOut()
	{
		return stdout;
	}

	SuperScriptStream getErr()
	{
		return stderr;
	}
}//End of class SuperScript
