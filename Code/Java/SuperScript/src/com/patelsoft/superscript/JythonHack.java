package com.patelsoft.superscript;

//Imports
import org.python.core.*;
import org.python.util.*;
import org.gjt.sp.jedit.*;
import java.util.Properties;
import com.patelsoft.util.*;
//End of Imports

/**
  *    A Class to overcome Jython Classloading Issues with BSF.
  *
  *    @created 28 May 2003
  *    @author Jiger Patel
  *
  */

public class JythonHack
{
	private static Logger log = new Logger();

	public static void loadJython()
	{
		Properties props  = new Properties();
		Properties sysProperties  = System.getProperties();
		PythonInterpreter.initialize(sysProperties, props, new String[]{""});
		PySystemState sys  = Py.getSystemState();
		log.log(Logger.DEV, JythonHack.class, "Got sys " + sys +" sys.getCL() " + sys.getClassLoader());
		log.log(Logger.DEV, JythonHack.class, "Setting sys cl to " + JythonHack.class.getClassLoader());
		PluginJAR[] plugins = jEdit.getPluginJARs();
		for (int i=0;i<plugins.length;i++)
		{
			PySystemState.packageManager.addJar(plugins[i].getPath(), true);
		}
	}
}//End of class JythonHack

