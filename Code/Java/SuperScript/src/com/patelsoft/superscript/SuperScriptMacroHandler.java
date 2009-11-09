package com.patelsoft.superscript;

	//Imports
import org.gjt.sp.jedit.Macros;
import org.gjt.sp.jedit.View;
import org.apache.bsf.*;
import org.apache.bsf.util.*;
import com.patelsoft.util.*;
import org.gjt.sp.jedit.jEdit;
import org.gjt.sp.util.Log;
import java.io.File;

	//End of Imports

  /**
    *    A Macro handler for all SuperScript supported languages.
    *
    *    @created 06 Jun 2003
    *    @author Jiger Patel
    *
    */
//(?:(?:.)*.groovy|(?:.)*.gv|(?:.)*.js)
public class SuperScriptMacroHandler extends Macros.Handler
{
	private Logger log = new Logger();

	public SuperScriptMacroHandler()
	{
		super("superscript");
	}//End of SuperScriptMacroHandler constructor

	public Macros.Macro createMacro(String macroName, String path)
	{
		String label = Macros.Macro.macroNameToLabel(macroName);
		label = label.substring(0, label.length() - 3);
		return new Macros.Macro(this, macroName, label, path);
	}

	public void runMacro(View view, Macros.Macro macro)
	{
		try
		{
			String lang = BSFManager.getLangFromFilename(macro.getPath());

			SuperScriptPlugin superscript= (SuperScriptPlugin)jEdit.getPlugin("com.patelsoft.superscript.SuperScriptPlugin");

			log.log(Logger.DEV,this.getClass(),"Got superscript plugin instance from jEdit "+ superscript);

			String script = StringUtils.getContentAsString(new File(macro.getPath()).toURL());
			log.log(Logger.DEV, this.getClass(), "Got script " + script +" macro "+ macro);
			log.log(Logger.DEV,this.getClass(), "Got script in file "+ macro.getPath() +" "+ script);
			superscript.executeScript(view,script,macro.getPath(), lang, true,null);
		}
		catch(Exception e)
		{
			log.log(Log.ERROR, this.getClass(), e);
		}
	}//End of runMacro
}//End of class SuperScriptMacroHandler
