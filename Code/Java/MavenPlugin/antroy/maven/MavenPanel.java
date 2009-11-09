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



public class MavenPanel {
 
    static Map<View, MavenPanel> instanceMap = new HashMap<View, MavenPanel>();
    
    private JList list;
    private DefaultListModel listModel;
    private JTree tree;
    private HistoryTextField textfield;
    private View view;
    private ConsoleTools console;
    private MavenParser parser;

    private JComponent viewComponent;
    
    private MavenPanel(View view){
        this.view = view;
        console = new ConsoleTools(view);
        parser = new MavenParser();
        
        createComponents();
        initializeComponents();
        addListeners();
        layoutComponents();
        refresh();
    }
    
    public static MavenPanel getInstance(View v){
        
        MavenPanel instance = instanceMap.get(v);
        
        if (instance == null){
            instance = new MavenPanel(v);
            instanceMap.put(v, instance);
        } 
        
        return instance;
    }
    
    public void refresh(){
        parser.reparse();
        DefaultTreeModel model = (DefaultTreeModel) tree.getModel();
        DefaultMutableTreeNode root = (DefaultMutableTreeNode) model.getRoot();
        
        root.removeAllChildren();
        model.reload();
        
        for (MavenProject project : parser.getProjects()){
            DefaultMutableTreeNode n = new DefaultMutableTreeNode(project);
            model.insertNodeInto(n, root, root.getChildCount());
            
            for (String goal : project.getGoals()){
                
                DefaultMutableTreeNode leaf = new DefaultMutableTreeNode(goal);
                model.insertNodeInto(leaf, n, n.getChildCount());
            }
        }
        
        tree.expandRow(0);
                
        listModel.removeAllElements();
        
        for (String goal : parser.getCommonGoals()) {
            listModel.addElement(goal);
        }
        
        tree.repaint();
    }
    
    private void layoutComponents(){
        
        JScrollPane scrollPane = new JScrollPane(tree);
        JScrollPane listScrollPane = new JScrollPane(list); 
        
        Dimension minimumSize = new Dimension(100, 50);
        listScrollPane.setMinimumSize(minimumSize);
        scrollPane.setMinimumSize(minimumSize);
        
        JSplitPane split = new JSplitPane(JSplitPane.VERTICAL_SPLIT,
                true,
                listScrollPane,
                scrollPane);
        split.setPreferredSize(new Dimension(200,200));
        split.setOneTouchExpandable(true);
        
        JSplitPane topPanel = new JSplitPane(JSplitPane.VERTICAL_SPLIT,
                false,
                textfield,
                split);
        
        viewComponent = topPanel;
    }
    
    public JComponent getViewComponent(){
        return viewComponent;
    }
    
    private void createComponents(){
        
        DefaultMutableTreeNode top = new DefaultMutableTreeNode("Maven");
        tree = new JTree(top);
        
        listModel = new DefaultListModel();
        list = new JList(listModel);
        list.setSelectionMode(ListSelectionModel.SINGLE_SELECTION);
        list.setBackground(new Color(213, 238, 210));
       
        
    }
    
    private void initializeComponents(){
        setActions(tree);
         
        textfield = new HistoryTextField("Maven Goal Field");
        
        HistoryModel histModel = textfield.getModel();
        if (histModel.getSize() > 0){
            textfield.setText(histModel.getItem(0));
            textfield.selectAll();
        }
        
        
        textfield.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent evt){
                textfield.addCurrentToHistory();
                TreePath path = tree.getSelectionPath();
                if (path != null && path.getPathCount() >= 2) {
                    DefaultMutableTreeNode treeNode = (DefaultMutableTreeNode) path.getPathComponent(1);
                    console.consoleRun((MavenProject) treeNode.getUserObject(),
                                       textfield.getText());
                } else {
                    Macros.message(null, "No project selected!");
                }
            }
        });
        
        
    }

    
    
String getFullName(File f){
    
    Document doc = null;
    
    try {
        doc = DocumentBuilderFactory.newInstance().newDocumentBuilder().parse(f);
    } catch (Exception ex){
    }
    
    NodeList projects = doc.getDocumentElement().getChildNodes();
    
    for (int i = 0; i < projects.getLength(); i++){
        Node n = projects.item(i);
        if (n.getNodeName().equals("name")){
            return n.getFirstChild().getNodeValue();
        }
    }
    return "NO PROJECT NAME FOUND!";
}
    
    private void addListeners(){
        
        MouseListener ml = new MouseAdapter() {
            public void mousePressed(MouseEvent e) {
                if (e.getClickCount() == 2){
                    TreePath path = tree.getSelectionPath();
                    if (path != null && path.getPathCount() >= 2) {
                        DefaultMutableTreeNode treeNode = (DefaultMutableTreeNode) path.getPathComponent(1);
                        
                        console.consoleRun((MavenProject) treeNode.getUserObject(), 
                                            list.getSelectedValue().toString());
                    } else {
                        Macros.message(null, "No project selected!");
                    }
                }
            }
        };
        
        list.addMouseListener(ml);
        
        KeyAdapter ka = new KeyAdapter(){
            public void keyReleased(KeyEvent e){
                
                if (e.getKeyCode() == KeyEvent.VK_ENTER){
                    TreePath path = tree.getSelectionPath();
                    if (path != null && path.getPathCount() >= 2) {
                        DefaultMutableTreeNode treeNode = (DefaultMutableTreeNode) path.getPathComponent(1);
                        console.consoleRun((MavenProject) treeNode.getUserObject(), 
                                            list.getSelectedValue().toString());
                    } else {
                        Macros.message(null, "No project selected!");
                    }
                }
            }
        };
        
        list.addKeyListener(ka);
    }
    
    
    
    private void setActions(final JTree tree){
        MouseListener ml = new MouseAdapter() {
        public void mousePressed(MouseEvent e) {
             TreePath selPath = tree.getPathForLocation(e.getX(), e.getY());
             int len = selPath.getPathCount();
             
             if(len > 2 && e.getClickCount() == 2) {
                 String goal = selPath.getPathComponent(len-1).toString();
                 
                 DefaultMutableTreeNode treeNode = (DefaultMutableTreeNode) selPath.getPathComponent(1);
                 MavenProject p = (MavenProject) treeNode.getUserObject();
                 console.consoleRun(p, goal);
             }
             if (e.isPopupTrigger()){
                 showRightContext(e, tree);
             }
         }
         public void mouseReleased(MouseEvent e) {
                 if (e.isPopupTrigger()){
                     showRightContext(e, tree);
                 }
         }
        };
        tree.addMouseListener(ml);
    
        KeyAdapter ka = new KeyAdapter(){
            public void keyReleased(KeyEvent e){
                
                 TreePath selPath = tree.getSelectionPath();
                 int len = selPath.getPathCount();
                     
                 if (len == 3 && e.getKeyCode() == KeyEvent.VK_ENTER){
                     Object[] path = selPath.getPath();
                     String goal = selPath.getPathComponent(len-1).toString();
                     DefaultMutableTreeNode treeNode = (DefaultMutableTreeNode) selPath.getPathComponent(1);
                     MavenProject p = (MavenProject) treeNode.getUserObject();
                     console.consoleRun(p, goal);
                 }
             }
        };
        
        tree.addKeyListener(ka);
        
    }
    
    private void showRightContext(final MouseEvent e, final JTree tree){
        JPopupMenu popup;
        popup = new JPopupMenu();
     
        TreePath selPath = tree.getPathForLocation(e.getX(), e.getY());
        tree.setSelectionPath(selPath);
        List<Component> items = new LinkedList<Component>();
    
        if (selPath.getPathCount() < 2) {
            JMenuItem item = new JMenuItem("build.properties");
            String build_props = System.getProperty("user.home") + "/build.properties";
            item.addActionListener(getOpenAction(build_props));
            items.add(item);
            
            item = new JMenuItem("Edit Project List");
            String maven_proj = MavenPlugin.MAVEN_PROPS_PATH;
            item.addActionListener(getOpenAction(maven_proj));
            items.add(item);
            
            item = new JMenuItem("Refresh");
            item.addActionListener(new ActionListener(){
                public void actionPerformed(ActionEvent e){
                    refresh();
                }
            });
            
            items.add(item);
            items.add(new JSeparator());
            
            items.add(new JSeparator());
            
            item = new JMenuItem("Help");
            item.addActionListener(new ActionListener(){
                public void actionPerformed(ActionEvent e){
                    StringBuffer sb = new StringBuffer();
                    sb.append("To execute a maven command, double click on it.\n\n");
                    sb.append("Various files associated with the projects can be opened by\n");
                    sb.append("right-clicking on a project name.\n\n");
                    sb.append("If the Project Viewer plugin is available, if you have a \n");
                    sb.append("project with the same name as the Maven project, then a menu item\n");
                    sb.append("will be available in the context menu to open that project.");
                    Macros.message(view, sb.toString());
                }
            });
            items.add(item);
        } else {
            String name = selPath.getPathComponent(1).toString();
            
            DefaultMutableTreeNode treeNode = (DefaultMutableTreeNode) selPath.getPathComponent(1);
                        
            MavenProject project = (MavenProject) treeNode.getUserObject();
            
            String p = project.getBasePath();
                
            items = getMenuItems(p, name);
        }
            
        for (Component menuItem : items){
            popup.add(menuItem);
        }
        
        if (items.size() > 0){
            popup.show(e.getComponent(),
                           e.getX(), e.getY());
        }
    }

    private ActionListener getOpenAction(final String path){
        
        ActionListener out = new ActionListener(){
                public void actionPerformed(ActionEvent e){
                    jEdit.openFile(view, path);
                }
            };
        return out;
    }

    private List<Component> getMenuItems(final String path, final String name){

        File dir = new File(path);
        String[] files = {"project.xml", "maven.xml", "plugin.jelly",
                          "project.properties", "plugin.properties"};
        List<Component> out = new LinkedList<Component>();
        
        if (jEdit.getPlugin("projectviewer.ProjectPlugin") != null){
            projectviewer.ProjectManager man = projectviewer.ProjectManager.getInstance();
            if (man.hasProject(name)){
                JMenuItem item = new JMenuItem("Open Project");
                item.addActionListener(new ActionListener(){
                    public void actionPerformed(ActionEvent e){
                        openProject(name);
                    }
                }); 
                out.add(item);
                          
            }
        }
        
        JMenuItem item = new JMenuItem("Browse Project Root");
        item.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent e){
                browseProject(path);
            }
        }); 
        out.add(item);
        
        out.add(new JSeparator());  
        
        out.addAll(addSubversionMenu(dir, path));
        
        for (String f : files){
            File next = new File(dir, f);
            if (!next.exists()){
                continue;
            } 
        
            JMenuItem iitem = new JMenuItem(f);
            iitem.addActionListener(getOpenAction(next.getAbsolutePath()));
            out.add(iitem);
        }
        
    
        return out;
    }
    
    private List<Component> addSubversionMenu(File dir, String path){
        
        List<Component> out = new LinkedList<Component>();
        
        File svnFolder = new File(dir, ".svn");
        
        if (svnFolder.exists() && svnFolder.isDirectory()){
            
            final SubversionTools sub = new SubversionTools(view);
            
            JMenu svnMenu = sub.getMenu(path);
            
            out.add(svnMenu);
            out.add(new JSeparator()); 
        }
        
        return out;
    }
    
    private void openProject(String name){
        Buffer[] buffers = jEdit.getBuffers();
        for (Buffer buf : buffers){
            if (buf.isDirty()){
                jEdit.saveAllBuffers(view, true);
                break;
            }
        }
        
        //new projectviewer.ProjectViewer(view);
        
        EditAction action = jEdit.getAction("projectviewer");
        action.invoke(view);
        
        projectviewer.ProjectViewer viewer = projectviewer.ProjectViewer.getViewer(view);
        viewer.setProject(projectviewer.ProjectManager.getInstance().getProject(name));
    }
    
    private void browseProject(String path){
        VFSBrowser.browseDirectory(view,path);
    }

    
        

}
