package com.patelsoft.superscript;

	//Imports
		import java.io.PrintStream;
		import java.io.ByteArrayOutputStream;
		import com.patelsoft.util.Logger;
	//End of Imports

  /**
    *    A Output/Error Stream.
    *
    *    @created 09 Jun 2003
    *    @author Jiger Patel
    *
    */

public class SuperScriptStream  extends PrintStream
{
	private static Logger log = new Logger();
	PrintStream defStream;
	ByteArrayOutputStream bout;
	private boolean active;


	public SuperScriptStream(PrintStream defStream)
	{
		super(defStream);
		this.defStream = defStream;
		bout = new ByteArrayOutputStream();
	}//End of SuperScriptStream constructor

	public SuperScriptStream(PrintStream defStream, boolean active)
	{
		super(defStream);
		this.defStream = defStream;
		this.active = active;
		bout = new ByteArrayOutputStream();
	}//End of SuperScriptStream constructor

	public void setActive(boolean streamActive)
	{
		this.active = streamActive;
	}

	public boolean isActive()
	{
		return this.active;
	}

	public void write(byte[] buf, int off, int len)
	{
		log.log(Logger.DEV,this.getClass(),"Inside write of SuperScriptStream isActive" + isActive());
		if(!active)
		{
			defStream.write(buf,off,len);
		}
		else
		{
			bout.write(buf,off,len);
		}
	}

	public void write(String message)
	{
		this.write(message.getBytes(),0,message.length());
	}


	public void reset()
	{
		bout.reset();
	}

	public int size()
	{
		if(active)
		{
			return bout.size();
		}
		throw new RuntimeException("Getting the Size of Default Stream "+ defStream +" is not possible");
	}

	public String toString()
	{
		if(active)
		{
			return bout.toString();
		}
		else
		{
			return defStream.toString();
		}
	}

}//End of class SuperScriptStream

