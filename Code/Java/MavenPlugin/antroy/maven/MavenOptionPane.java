package antroy.maven;

import java.io.*;
import java.util.*;
import org.gjt.sp.jedit.*;
import javax.swing.*;
import javax.swing.border.*;
import javax.xml.xpath.*;
import org.xml.sax.InputSource;
import org.w3c.dom.*;
import java.awt.*;
import java.awt.event.*;

public class MavenOptionPane extends AbstractOptionPane {
    
    private MavenConfiguration config = MavenConfiguration.getInstance();
    
    public MavenOptionPane(){
        super("Maven");
    }
    
    public void _init() {
        
        DefaultListModel goalListModel = new DefaultListModel();
        
        JList goalList = new JList(goalListModel);
        
        for (String goal : config.getCommonGoals()){
            goalListModel.addElement(goal);
        }
        
        JPanel goalPanel = new JPanel(new BorderLayout());
        goalPanel.setBorder(new TitledBorder("Common Goals"));    
        JPanel goalButtons = new JPanel();
        JButton goalAdd = new JButton("Add");
        goalAdd.addActionListener(getGoalAddAction(goalList));
        goalButtons.add(goalAdd);
        JButton goalRemove = new JButton("Remove");
        goalRemove.addActionListener(getGoalRemoveAction(goalList));
        goalButtons.add(goalRemove);
        
          
        DefaultListModel projListModel = new DefaultListModel();
        
        JList projList = new JList(projListModel);
        
        for (File file : config.getProjectFiles()){
            projListModel.addElement(file);
        }
        
        JPanel projPanel = new JPanel(new BorderLayout());
        projPanel.setBorder(new TitledBorder("Project Descriptors"));        
        JPanel projButtons = new JPanel();
        JButton projAdd = new JButton("Add");
        projAdd.addActionListener(getProjectAddAction(projList));
        projButtons.add(projAdd);
        JButton projRemove = new JButton("Remove");
        projRemove.addActionListener(getProjectRemoveAction(projList));
        projButtons.add(projRemove);
      
        Dimension dim = new Dimension(200, 200);
        goalList.setPreferredSize(dim);
        projList.setPreferredSize(dim);
        
        JScrollPane goalPane = new JScrollPane(goalList);
        JScrollPane projPane = new JScrollPane(projList); 
        
        goalPane.setMinimumSize(dim);
        projPane.setMinimumSize(dim);
        
        goalPanel.add(goalPane, BorderLayout.CENTER);
        projPanel.add(projPane, BorderLayout.CENTER);
        goalPanel.add(goalButtons, BorderLayout.SOUTH);
        projPanel.add(projButtons, BorderLayout.SOUTH);
        
        addComponent(goalPanel);
        addComponent(projPanel);
        
    }

    public void _save(){
        config.save();
        
        for (MavenPanel panel : MavenPanel.instanceMap.values()){
            panel.refresh();
        }
        
    }
    
    private ActionListener getGoalAddAction(final JList list){
        
        ActionListener out = new ActionListener(){
            public void actionPerformed(ActionEvent e){
                String newGoal = Macros.input(null, "Enter new Goal:");
                
                if (newGoal == null) return;
                
                DefaultListModel model = (DefaultListModel) list.getModel();
                
                int index = list.getSelectedIndex() + 1;
                if (index < 0){
                    index = model.getSize();
                }
                
                model.add(index, newGoal);
                config.getCommonGoals().add(index, newGoal);
            }
        };
        
        return out;
    }
    
    
    private ActionListener getGoalRemoveAction(final JList list){
        
        ActionListener out = new ActionListener(){
            public void actionPerformed(ActionEvent e){
                DefaultListModel model = (DefaultListModel) list.getModel();
                
                int index = list.getSelectedIndex();
                if (index < 0){
                    return;
                }
                
                model.remove(index);
                config.getCommonGoals().remove(index);
            }
        };
        
        return out;
    }
    
    
    private ActionListener getProjectAddAction(final JList list){
        
        ActionListener out = new ActionListener(){
            public void actionPerformed(ActionEvent e){
                
                JFileChooser chooser = new JFileChooser();
                javax.swing.filechooser.FileFilter filter = new javax.swing.filechooser.FileFilter(){
                    public boolean accept(File f){
                        
                        if (f.isDirectory()){
                            return true;
                        }
                        
                        if (f.getName().equals("project.xml")){
                            return true;
                        }
                        
                        return false;
                    }
                    
                    public String getDescription(){
                        return "Maven Project Descriptors";
                    }
                };
                
                chooser.setFileFilter(filter);
                int returnVal = chooser.showOpenDialog(null);
                
                if(returnVal != JFileChooser.APPROVE_OPTION) {
                   return;
                }
                
                File chosen = chooser.getSelectedFile();
                
                if (chosen == null) return;
                
                DefaultListModel model = (DefaultListModel) list.getModel();
                
                int index = list.getSelectedIndex() + 1;
                if (index < 0){
                    index = model.getSize();
                }
                
                model.add(index, chosen);
                config.getProjectFiles().add(index, chosen);
            }
        };
        
        return out;
    }
    
    
    private ActionListener getProjectRemoveAction(final JList list){
        
        ActionListener out = new ActionListener(){
            public void actionPerformed(ActionEvent e){
                DefaultListModel model = (DefaultListModel) list.getModel();
                
                int index = list.getSelectedIndex();
                if (index < 0){
                    return;
                }
                
                model.remove(index);
                config.getProjectFiles().remove(index);
            }
        };
        
        return out;
    }
    
    
}
