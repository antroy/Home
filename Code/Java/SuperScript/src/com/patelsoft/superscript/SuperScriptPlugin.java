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

public class SuperScriptPlugin extends EditPlugin
{
	public final static String NAME = "superscript";
	static BSFManager bsfmanager;
	private SuperScriptStream stdout=new SuperScriptStream(System.out),stderr= new SuperScriptStream(System.err);
	private static Logger log = new Logger();
	private static boolean pendingInitialization=true;

	/*
		The jEdit startup routine calls this method for each loaded plugin. Plugins typically use this method to register information with the EditBus and perform other initialization
	*/
	public void start()
	{
		super.start();

		//Since SuperScript would have glob patterns set Dynamically. We cannot hardcode the glob pattern in any of the properties file. Thus we stimulate "macro-handler.superscript.glob".
		if(jEdit.getProperty("macro-handler.superscript.glob") == null)
		{
			jEdit.setProperty("macro-handler.superscript.glob",""); //This will make Macro Framework happy when the registeration is done.
		}
		Log.log(Log.DEBUG,this,"Registered SuperScript for " + jEdit.getProperty("macro-handler.superscript.glob"));

		System.setOut(stdout);
		System.setErr(stderr);

		Macros.registerHandler(new SuperScriptMacroHandler());
	}

	public void stop()
	{
		super.stop();
	}

/* 	public void createMenuItems(Vector menuItems)
	{
		menuItems.addElement(GUIUtilities.loadMenuItem("superscript"));
	}

	public void createOptionPanes(OptionsDialog dialog)
	{
		dialog.addOptionPane();
	} */

	static void loadBSFManager(View view) throws BSFException
	{
		if(bsfmanager == null)
		{
			log.log(Logger.DEV, SuperScriptPlugin.class, "BSF Manager is null going to load now.");
			bsfmanager = new BSFManager();
		}

		if(bsfmanager != null && pendingInitialization)
		{
			if(view != null)
			{
				bsfmanager.declareBean("view",view,View.class);
				EditPane ep = view.getEditPane();
				bsfmanager.declareBean("editPane",ep,EditPane.class);
				bsfmanager.declareBean("buffer",ep.getBuffer(),Buffer.class);
				bsfmanager.declareBean("textArea",ep.getTextArea(),org.gjt.sp.jedit.textarea.JEditTextArea.class);
				pendingInitialization = false;
			}
			//bsfmanager.declareBean("superscript",this,this.getClass());
		}
	}

	String[] getAllLanguages(View view) throws BSFException
	{
		loadBSFManager(view);
		try
		{
			Field registeredEngines =bsfmanager.getClass().getDeclaredField("registeredEngines");
			registeredEngines.setAccessible(true);
			Hashtable lang2Engines = (Hashtable)registeredEngines.get(bsfmanager);

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

	public BSFPanel openDockable(View view) throws BSFException
	{
		return new BSFPanel(view,this);
	}

	public void executeScript(View view,BSFPanel bsfpanel) throws BSFException
	{
		this.executeScript(view, view.getTextArea().getText(),view.getBuffer().getName(),bsfpanel);
	}

	public void executeScript(View view, String script,String filename,BSFPanel bsfpanel) throws BSFException
	{
		this.executeScript(view, script, filename,bsfpanel.getCurrentLanguage(),false,bsfpanel);
	}

	void executeScript(View view,String script,String filename, String lang, boolean execFromMacro,BSFPanel bsfpanel) throws BSFException
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
			loadBSFManager(view);
			bsfmanager.exec(lang,filename,1,1,script);
			if(!execFromMacro)
			{
				printOutput(view,bsfpanel,stdout.toString());
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
				printError(view,bsfpanel,exp);
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
	}

	private void eval(View view,BSFPanel bsfpanel,String command) throws BSFException
	{
		log.log(Logger.DEV, this.getClass(), "Entering eval");
		loadBSFManager(view);
		printQuestion(view,bsfpanel,command+"\n");
		bsfmanager.declareBean("bsfpanel",bsfpanel,BSFPanel.class);
		log.log(Logger.DEV, this.getClass(), "Going for bsfmanager.eval see stdout.isActive " + stdout.isActive());
		Object obj = bsfmanager.eval(bsfpanel.getCurrentLanguage(),view.getBuffer().getName(),1,1,command);
		bsfmanager.undeclareBean("bsfpanel");
		printOutput(view,bsfpanel,stdout.toString());
		if(obj !=null && stdout.size() == 0) //Last condition is due to JS hack. Coz it prints to the sysout AND also returns object of type Undefined.
		{
			printOutput(view,bsfpanel,obj.toString() +"\n\n");
		}
		/* else
		{
				log.log(Logger.DEV, this.getClass(), "Leaving eval");
				throw new BSFException(BSFException.REASON_INVALID_ARGUMENT,"Return value from eval is NULL");
		} */
		log.log(Logger.DEV, this.getClass(), "Leaving eval");
	}


	void evalOrExecute(View view,String command,BSFPanel bsfpanel)
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
			this.eval(view,bsfpanel,command);
		}
		catch(BSFException e)
		{
			//One last chance
			try
			{
				this.executeScript(view, command,"<No Filename>",bsfpanel);
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
			bsfpanel.txtCommand.grabFocus();
			log.log(Logger.DEV, this.getClass(), "Leaving evalOrExecute");
		}
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

	void printOutput(View view,BSFPanel bsfpanel,String output)
	{
		if(bsfpanel != null)
		{
			bsfpanel.printOutput(output);
		}
	}

	void printQuestion(View view,BSFPanel bsfpanel,String question)
	{
		if(bsfpanel != null)
		{
			bsfpanel.printQuestion(question);
		}
	}


	void printError(View view,BSFPanel bsfpanel,String err)
	{
		if(bsfpanel != null)
		{
			bsfpanel.printError("\n"+err);
		}
	}

	void printError(View view,BSFPanel bsfpanel,BSFException exp)
	{
		printError(view,bsfpanel,exceptionToString((exp.getTargetException()==null?exp:exp.getTargetException())));
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

	public void declareVariable(View view, String varName, Object value) throws BSFException
	{
		if(!(varName == null || value == null))
		{
			loadBSFManager(view);
			bsfmanager.declareBean(varName,value, value.getClass());
		}
		else
		{
			if(bsfmanager != null)
			{
				BSFPanel bsfpanel = (BSFPanel)bsfmanager.lookupBean("bsfpanel");
				printError(view, bsfpanel, "Variable name or value is NULL. Ignoring variable declaration.\n");
			}
		}
	}

	public static SuperScriptOptionPane getSuperScriptOptionPane()
	{
		//We need to implement this method since SuperScriptOptionPane uses loadBsfManager and other non-static methods on SuperScript Plugin. If we make those methods as static then other code needs to be made static and thus creates a cyclical static hell. So we create a new instance of OptionPane. Let jEdit cache it if it wants.
		SuperScriptPlugin ssp = (SuperScriptPlugin)jEdit.getPlugin("com.patelsoft.superscript.SuperScriptPlugin");
		if(ssp != null)
		{
			return ssp.new SuperScriptOptionPane();
		}
		return null; //Shudn't happen
	}

	class SuperScriptOptionPane extends AbstractOptionPane
	{
		JCheckBox chkExtensions[];
		List vecext;
		JCheckBox chkLoadPluginJars;

		public SuperScriptOptionPane()
		{
			super(NAME);
			vecext = new Vector();
			String ext = jEdit.getProperty("superscript.macros.ext");
			if(ext != null)
			{
				StringTokenizer strtok = new StringTokenizer(ext,",");
				while(strtok.hasMoreTokens())
				{
					vecext.add(strtok.nextToken());
				}
			}
		}

		protected void _init()
		{
			try
			{
				JPanel pnlMain = new JPanel(new BorderLayout());

				loadBSFManager(jEdit.getActiveView());

				Field extensions =bsfmanager.getClass().getDeclaredField("extn2Lang");
				extensions.setAccessible(true);
				Hashtable extn2Lang = (Hashtable)extensions.get(bsfmanager);

				chkExtensions = new JCheckBox[extn2Lang.size()];

				Enumeration enumExt = extn2Lang.keys();
				for(int i=0;enumExt.hasMoreElements();i++)
				{
					String ext  = (String)enumExt.nextElement();
					String lang = (String)extn2Lang.get(ext);

					JCheckBox chk = new JCheckBox(lang +"("+ext+")");
					chk.setSelected(vecext.contains(ext));
					chk.setActionCommand(ext);
					chkExtensions[i] = chk;
				}

				JScrollPane scrollPane = new JScrollPane(new CheckboxList(chkExtensions));
				scrollPane.setBorder(new TitledBorder("Select Extensions to be recognised as Macro"));
				pnlMain.add(BorderLayout.CENTER,scrollPane);

				chkLoadPluginJars = new JCheckBox("Load Plugin Jars(Jython hack)", jEdit.getBooleanProperty("superscript.jythonhack"));

				pnlMain.add(chkLoadPluginJars,BorderLayout.SOUTH);

				addComponent((String)null,pnlMain,GridBagConstraints.CENTER);
			}
			catch(Exception e)
			{
				log.log(Log.ERROR,this.getClass(),e);
			}
		}

		public void save()
		{
			if(chkExtensions != null)
			{
				//Loop thru all the checkboxes and store languges selected and the glob patterns.
				StringBuffer strbuf = new StringBuffer();

				for(int i=0;i<chkExtensions.length;i++)
				{
					if(chkExtensions[i].isSelected())
					{
						strbuf.append(chkExtensions[i].getActionCommand()+",");
					}
				}

				if(strbuf.length() >0) //Strip of the last char.
				{
					strbuf.deleteCharAt(strbuf.length()-1);
				}

				jEdit.setProperty("superscript.macros.ext",strbuf.toString());
				if(strbuf.length() != 0)
				{
					jEdit.setProperty("macro-handler.superscript.glob","*.{"+strbuf.toString()+"}");
				}
				jEdit.setBooleanProperty("superscript.jythonhack",chkLoadPluginJars.isSelected());
			}


		}//End of method save

		//Inner Classes
			class CheckboxList extends JList
			{
				class CheckboxListCellRenderer implements ListCellRenderer
				{
					public Component getListCellRendererComponent(JList list, Object value, int index, boolean isSelected, boolean cellHasFocus)
					{
						JCheckBox box = (JCheckBox)value;
						box.setEnabled(isEnabled());
						box.setFont(getFont());
						box.setFocusPainted(false);
						box.setBorderPainted(true);
						box.setPreferredSize(new Dimension(box.getPreferredSize().width+20,box.getPreferredSize().height));
						//box.setBorder(isSelected ? UIManager.getBorder("List.focusCellHighlightBorder") : new EmptyBorder(1,1,1,1));
						return box;
					}
				}

				public CheckboxList(Object[] args)
				{
					super(args);
					setCellRenderer(new CheckboxListCellRenderer());
					addMouseListener(new MouseAdapter()
									 {
										 public void mousePressed(MouseEvent e)
										 {
											 int index = locationToIndex(e.getPoint());
											 if (index != -1)
											 {
												 JCheckBox box = (JCheckBox)getModel().getElementAt(index);
												 box.setSelected(!box.isSelected());
												 repaint();
											 }
										 }
									 });
					setFixedCellWidth(getMaximumSize().width*2);

				}
			}
		//End of Inner
	} //End of SuperScriptOptionPane
}//End of class SuperScript
