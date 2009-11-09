package antroy.maven;


import java.awt.*;
import java.awt.event.*;
import java.util.*;
import java.io.*;

import javax.swing.*;
import org.gjt.sp.jedit.*;
import console.*;


public class SubversionTools {

    private View view;
    private ConsoleTools console;
    
    public SubversionTools(View view){
        this.view = view;
        this.console = new ConsoleTools(view);
    }
    
    
    public JMenu getMenu(final String path){
        
            JMenu svnMenu = new JMenu("SVN");
            
            JMenuItem svnCommit = new JMenuItem("SVN Commit");
            svnCommit.addActionListener(new ActionListener(){
                public void actionPerformed(ActionEvent e){
                    svnCommit(path);
                }
            }); 
            
            JMenuItem svnUpdate = new JMenuItem("SVN Update");
            svnUpdate.addActionListener(new ActionListener(){
                public void actionPerformed(ActionEvent e){
                    svnUpdate(path);
                }
            }); 
            
            JMenuItem svnAdd = new JMenuItem("SVN Add");
            svnAdd.addActionListener(new ActionListener(){
                public void actionPerformed(ActionEvent e){
                    
                    Buffer buff = view.getEditPane().getBuffer();
                    
                    String addCmd = "add " + '"' + buff.getPath() + '"';
                    svnCommand(addCmd, path);
                }
            }); 
            
            JMenuItem svnStatus = new JMenuItem("SVN Status");
            svnStatus.addActionListener(new ActionListener(){
                public void actionPerformed(ActionEvent e){
                    svnCommand("status", path);
                }
            }); 
            
            svnMenu.add(svnStatus);
            svnMenu.add(svnUpdate);
            svnMenu.add(svnCommit);
            svnMenu.add(svnAdd);
            
            return svnMenu;
    }
    
    
    void svnUpdate(String path){
        svnCommand("update", path);
    }
    
    void svnCommit(final String path){
        final JDialog commitDialog = new JDialog(view, "Commit Message");
        
        final JTextArea commitArea = new JTextArea(10,40);
        commitArea.setLineWrap(true);
        
        commitDialog.getContentPane().add(commitArea, BorderLayout.CENTER);
        
        JPanel buttPan = new JPanel();
        
        ActionListener al = new ActionListener(){
            public void actionPerformed(ActionEvent e){   
            
                if (e.getActionCommand().equals("OK")){
                    File temp = null;
                    try {
                        temp = File.createTempFile("svnCommit",".txt");
                        
                        BufferedWriter out = new BufferedWriter(new FileWriter(temp));
                        String txt = commitArea.getText();
                        out.write(txt, 0, txt.length());
                        out.close();
                    } catch (IOException ex){
                    }
                    
                    String command = "commit -F " + '"' + temp.getAbsolutePath() + '"';
                    svnCommand(command, path);
                }         
                
                int x = (int) commitDialog.getLocation().getX();
                int y = (int) commitDialog.getLocation().getY();
                
                jEdit.setIntegerProperty("svn.commit.dialog.x", x);
                jEdit.setIntegerProperty("svn.commit.dialog.y", y);
                
                commitDialog.setVisible(false);
                commitDialog.dispose();
            }
        };
        
        JButton ok = new JButton("OK");
        ok.addActionListener(al);
        
        JButton cancel = new JButton("Cancel");
        cancel.addActionListener(al);
        
        buttPan.add(ok, BorderLayout.WEST);
        buttPan.add(cancel, BorderLayout.EAST);
        commitDialog.getContentPane().add(buttPan, BorderLayout.SOUTH);
        
        commitDialog.pack();
        
        int x = jEdit.getIntegerProperty("svn.commit.dialog.x", 0);
        int y = jEdit.getIntegerProperty("svn.commit.dialog.y", 0);
        commitDialog.setLocation(x, y);
        
        commitDialog.setVisible(true);    
    }
    
    void svnCommand(String command, String dir){
        console.runInSystemShell("cd " + dir);
        console.runInSystemShell("svn " + command);
    }

    
}

