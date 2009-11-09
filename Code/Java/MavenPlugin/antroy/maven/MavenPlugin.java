/*
 * $Date: 2005/02/04 08:02:22 $
 * $Author: ant-roy $
 *
 * Copyright (C) 2002 Anthony Roy
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
package antroy.maven;

import org.gjt.sp.jedit.*;
import java.io.*;

public class MavenPlugin extends EditPlugin {
 
public static final String MAVEN_PROPS_PATH = System.getProperty("user.home") + "/.jedit/maven/maven_projects.properties";
public static final File MAVEN_PROPS_FILE;

static {
    
    MAVEN_PROPS_FILE = new File(MAVEN_PROPS_PATH);
    
    if (!MAVEN_PROPS_FILE.exists()){
        MAVEN_PROPS_FILE.getParentFile().mkdirs();
    }
    
}    
  /**
   * Method called by jEdit to finalize the plugin.
   */
  public void stop() {
  }

}
