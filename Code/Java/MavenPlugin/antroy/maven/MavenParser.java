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

import javax.swing.*;
import javax.swing.tree.*;
import org.w3c.dom.*;
import javax.xml.parsers.*;
import java.awt.event.*;
import org.gjt.sp.jedit.*;
import org.gjt.sp.jedit.browser.*;
import org.gjt.sp.jedit.gui.*;
import java.awt.*;
import java.io.*;
import java.util.*;
import java.util.List;
import console.*;



public class MavenParser {
 
    private List<MavenProject> projects = new LinkedList<MavenProject>();
    private MavenConfiguration config   = MavenConfiguration.getInstance();  
    
    public MavenParser(){
        parse();
    }

    public List<String> getCommonGoals(){
        return config.getCommonGoals();
    }
    
    public List<MavenProject> getProjects(){
        return projects;
    }
    
    
    private void parse(){
        
        for (File filename : config.getProjectFiles()){
            if (filename.exists()){
                projects.add(getProject(filename));
            }
        }
    }

    public void reparse(){
        projects = new LinkedList<MavenProject>();
        config.refresh();
        parse();
    }
    
private MavenProject getProject(File f){
    
    Document doc = null;
    
    try {
        doc = DocumentBuilderFactory.newInstance().newDocumentBuilder().parse(f);
    } catch (Exception ex){
    }
    
    NodeList projectNodes = doc.getDocumentElement().getChildNodes();
    
    String name = "NO PROJECT NAME FOUND!";
    String description = "";
    
    for (int i = 0; i < projectNodes.getLength(); i++){
        Node n = projectNodes.item(i);
        if (n.getNodeName().equals("name")){
            name = n.getFirstChild().getNodeValue();
        } else if (n.getNodeName().equals("shortDescription")){
            description = n.getFirstChild().getNodeValue();
        }
    }
    
    MavenProject out = new MavenProject(f.getParent(), name, description);
    
    File mavenDotXml = new File(f.getParentFile(), "maven.xml");
    
    if (mavenDotXml.exists()){
        try {
            doc = DocumentBuilderFactory.newInstance().newDocumentBuilder().parse(mavenDotXml);
        } catch (Exception ex){
        }
        
        NodeList goalNodes = doc.getDocumentElement().getChildNodes();
        
        for (int i = 0; i < goalNodes.getLength(); i++){
            Node nextNode = goalNodes.item(i);
            
            if (nextNode.getNodeName().equals("goal")){
                NamedNodeMap attributes = nextNode.getAttributes();
                Node attName = attributes.getNamedItem("name");
                out.addGoal(attName.getNodeValue());
            }
        }
    }
    
    return out;
}
    

}
