package com.patelsoft.superscript;

	//Imports
		import javax.swing.text.StyleConstants;
		import javax.swing.text.BadLocationException;
		import org.gjt.sp.jedit.*;
		import org.gjt.sp.util.*;
		import org.gjt.sp.jedit.gui.HistoryTextField;
		import javax.swing.*;
		import java.awt.*;
		import java.awt.event.*;
		import org.apache.bsf.BSFException;
		import javax.swing.text.SimpleAttributeSet;
		import javax.swing.text.Document;
		import com.patelsoft.util.*;
	//End of Imports


public class BSFPanel extends JPanel
{
	private static Logger log = new Logger();
	JPanel toolbar;
	View view;
	SuperScriptPlugin superscript;
	JComboBox listOfLanguages;
	HistoryTextField txtCommand;
	JTextPane tpOutput;
	boolean jythonhack;


	public BSFPanel(View view,SuperScriptPlugin superscript) throws BSFException
	{
		this.view = view;
		this.superscript = superscript;
		setLayout(new BorderLayout());
		toolbar = new JPanel(new BorderLayout());
		setUp();
		add(toolbar,BorderLayout.NORTH);
	}

	private void setUp() throws BSFException
	{

		Action executeScriptAction = new AbstractAction("Execute Script")
									 {
										 public void actionPerformed(ActionEvent event)
										 {
											 try
											 {
												 superscript.executeScript(view,BSFPanel.this);
											 }
											 catch(BSFException e)
											 {
												 log.log(Log.ERROR,this,e);
											 }
										 }
									 };

		JPanel btnSet1 = new JPanel();

		btnSet1.add(new JButton(executeScriptAction));

		listOfLanguages= new JComboBox(superscript.getAllLanguages(view));
		listOfLanguages.setSelectedIndex(0);
		listOfLanguages.setSelectedItem(jEdit.getProperty("SuperScript.lastLanguage","NotInTheList"));
		listOfLanguages.addItemListener(new ItemListener(){
			public void itemStateChanged(ItemEvent evt)
			{
				if(evt.getStateChange() == ItemEvent.SELECTED)
				{
					String lang= (String)evt.getItem();
					jEdit.setProperty("SuperScript.lastLanguage",lang);
					if(lang.equals("jython") && !jythonhack)
					{
						if(jEdit.getBooleanProperty("superscript.jythonhack"))
						{
							log.log(Logger.DEV,this.getClass(),"Running Jython Hack");
							JythonHack.loadJython();
							jythonhack=true;
						}
					}
				}
			}});

		//Hack jython is jython is the lastselected language

		if(jEdit.getProperty("SuperScript.lastLanguage","").equals("jython") && jEdit.getBooleanProperty("superscript.jythonhack"))
		{
			log.log(Logger.DEV,this.getClass(),"Running Jython Hack");
			JythonHack.loadJython();
			jythonhack=true;
		}

		btnSet1.add(listOfLanguages);

		toolbar.add(BorderLayout.WEST,btnSet1);

		//Setup the Command Textbox
		txtCommand = new HistoryTextField("SuperScripthistory",false,true);
		//txtCommand.setColumns(80);
		txtCommand.setRequestFocusEnabled(true);
		txtCommand.addActionListener(new ActionListener()
		{
			public void actionPerformed(ActionEvent evt)
			{
					superscript.evalOrExecute(view,txtCommand.getText(),BSFPanel.this);
					txtCommand.setText("");
			}
		});

		Box boxCmd = new Box(BoxLayout.Y_AXIS);
		Dimension dim = txtCommand.getPreferredSize();
		dim.width = Integer.MAX_VALUE;
		txtCommand.setMaximumSize(dim);
		boxCmd.add(Box.createGlue());
		boxCmd.add(txtCommand);
		boxCmd.add(Box.createGlue());
		toolbar.add(BorderLayout.CENTER,boxCmd);

		//Setup tpOutput
		tpOutput = new JTextPane();

		add(new JScrollPane(tpOutput),BorderLayout.CENTER);

		//add clear button

		Box boxSetEnd = new Box(BoxLayout.Y_AXIS);

		JButton btnClear = new JButton("Clear Output");
		btnClear.addActionListener(new ActionListener()
		{
			public void actionPerformed(ActionEvent e)
			{
				try
				{
					Document doc = tpOutput.getDocument();
					doc.remove(0,doc.getLength());
				}
				catch(BadLocationException exp)
				{
					log.log(Log.ERROR,this,exp);
				}
			}
		}
		);

		boxSetEnd.add(Box.createGlue());
		boxSetEnd.add(btnClear);
		boxSetEnd.add(Box.createGlue());
		toolbar.add(BorderLayout.EAST,boxSetEnd);

	}

	public String getCurrentLanguage()
	{
		return (String)listOfLanguages.getSelectedItem();
	}

	public void printOutput(String output)
	{
		Document doc = tpOutput.getDocument();
		try
		{
			log.log(Logger.DEV, this.getClass(), "Printing to BSFPanel " + output);
			doc.insertString(doc.getLength(),output,new SimpleAttributeSet());
			tpOutput.setCaretPosition(doc.getLength());
		}
		catch(BadLocationException e)
		{
			log.log(Log.ERROR,this,e);
		}
	}

	public void printError(String error)
	{
		Document doc = tpOutput.getDocument();
		try
		{
			SimpleAttributeSet errorAttr = new SimpleAttributeSet();
			errorAttr.addAttribute(StyleConstants.Foreground, Color.red);
			doc.insertString(doc.getLength(),error,errorAttr);
		}
		catch(BadLocationException e)
		{
			log.log(Log.ERROR,this,e);
		}
	}

	public void printQuestion(String command)
	{
		Document doc = tpOutput.getDocument();
		try
		{
			SimpleAttributeSet commandAttr = new SimpleAttributeSet();
			commandAttr.addAttribute(StyleConstants.Foreground, Color.green);
			doc.insertString(doc.getLength(),"-> "+command,commandAttr);
		}
		catch(BadLocationException e)
		{
			log.log(Log.ERROR,this,e);
		}
	}
}//End of class BSFPanel
