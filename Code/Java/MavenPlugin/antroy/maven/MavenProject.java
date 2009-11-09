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

import java.util.*;

public class MavenProject {
 
    private List<String> goalSet = new LinkedList<String>();
    private String basePath;
    private String name;
    private String description;
      
    public MavenProject(String basePath, String name, String description){
        this.basePath = basePath;
        this.name = name;
        this.description = description;
    }

    public String getName(){
        return name;
    }
    
    public String getDescription(){
        return description;
    }
    
    public String getBasePath(){
        return basePath;
    }
    
    public void addGoal(String goal){
        goalSet.add(goal);
    }
    
    public List<String> getGoals(){
        return goalSet;
    }
    
    public String toString() {
        return name;
    }
    
}
