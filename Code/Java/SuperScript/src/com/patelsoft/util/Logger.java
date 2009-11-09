package com.patelsoft.util;

	//Imports
import org.gjt.sp.util.Log;
	//End of Imports

  /**
    *    A Wrapper around jEdit's Logging mechnism to facilitate dynamic Logging of events.
    *
    *    @created 06 Jun 2003
    *    @author Jiger Patel
    *
    */

public class Logger
{
	public final static int DEV=0;
	private static int level=Log.NOTICE; //DEBUG


	public Logger()
	{
		super();

	}//End of Logger constructor

	public void log(int severity, Object source, Object message)
	{
		if(severity >=level)
		{
			//Since jEdit's Log class does not have custom logging options or extension points, we log DEV at DEBUG level but only when the LEVEL is set to DEV which serves both the purpose of logging and DEV level logging.
			if(severity == DEV)
			{
				Log.log(Log.DEBUG,source,message);
			}
			else
			{
				Log.log(severity,source,message);
			}
		}
	}

	public void setLevel(int level)
	{
		Logger.level = level;
	}

	public int getLevel()
	{
		return level;
	}


}//End of class Logger

