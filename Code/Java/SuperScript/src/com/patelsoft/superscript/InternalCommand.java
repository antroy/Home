package com.patelsoft.superscript;

import org.gjt.sp.jedit.View;

public interface InternalCommand {
	
	String exec(View view, String[] args);
	
	String getDescription();
}
