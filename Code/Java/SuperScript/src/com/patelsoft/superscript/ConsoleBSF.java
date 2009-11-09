/*
 * ConsoleBeanShell.java - Executes commands in jEdit's BeanShell interpreter
 * :tabSize=8:indentSize=8:noTabs=false:
 * :folding=explicit:collapseFolds=1:
 *
 * Copyright (C) 2000, 2001 Slava Pestov
 *
 * This program is free software; you can redistribute it and/or
 * modify it under the terms of the GNU General Public License
 * as published by the Free Software Foundation; either version 2
 * of the License, or any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
 */

package com.patelsoft.superscript;

//{{{ Imports
import bsh.*;
import console.*;
import java.io.PrintWriter;
import java.io.StringWriter;
import org.gjt.sp.jedit.BeanShell;
import org.gjt.sp.jedit.jEdit;
import org.gjt.sp.jedit.View;
import org.gjt.sp.util.Log;
import org.apache.bsf.*;

//}}}

public class ConsoleBSF extends Shell{
	//{{{ ConsoleBeanShell constructor
	public ConsoleBSF() {
		super("BSF");
	} //}}}

	//{{{ printInfoMessage() method
	public void printInfoMessage(Output output) {
		output.print(null,jEdit.getProperty("console.bsf.info"));
	} //}}}

	//{{{ printPrompt() method
	/**
	 * Prints a prompt to the specified console.
	 * @param output The output
	 */
	public void printPrompt(Console console, Output output) {
		BSFController controller = BSFController.getInstance();
		
		String prompt = jEdit.getProperty("console.bsf.prompt") + "-" + 
				controller.getCurrentLanguage() + "> ";
		
		output.writeAttrs(
			ConsolePane.colorAttributes(console.getInfoColor()),
			prompt);
		output.writeAttrs(null," ");
	} //}}}

	//{{{ execute() method
	public void execute(Console console, String input, Output output,
		Output error, String command) {
		View view = console.getView();

		BSFController controller = BSFController.getInstance();
		String out = "";
		
		if (command.startsWith("%") && command.trim().length() > 1){
			out = runInternalCommand(command, view);
		} else {
			out = controller.evalOrExecute(view, command);
		}
		
		output.writeAttrs(
			ConsolePane.colorAttributes(console.getInfoColor()),
			out);
		output.writeAttrs(null,"\n");

		output.commandDone();
		error.commandDone();
	} //}}}

	String runInternalCommand(String command, View view){
		String[] split = command.split("\\s");
		String commandName = split[0].substring(1);
		
		if (commandName.length() == 0){
			return "Invalid Command";
		}
		
		String[] args = new String[split.length - 1];
		System.arraycopy(split, 1, args, 0, args.length);
		
		return CommandRegister.REGISTER.getCommand(commandName).exec(view, args);
	}
	
	//{{{ stop() method
	public void stop(Console console) {
	} //}}}

	//{{{ waitFor() method
	public boolean waitFor(Console console) {
		return true;
	} //}}}
}
