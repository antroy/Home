package antroy.maven;

import javax.swing.tree.*;
import javax.swing.*;
import java.awt.*;

public class MavenTreeRenderer extends DefaultTreeCellRenderer {
    Icon goalIcon = new ImageIcon(
            MavenTreeRenderer.class.getResource("images/goal.png"));
    Icon projectIcon = new ImageIcon(
            MavenTreeRenderer.class.getResource("images/project.png"));

    public MavenTreeRenderer() {
    }

    public Component getTreeCellRendererComponent(
                        JTree tree,
                        Object value,
                        boolean sel,
                        boolean expanded,
                        boolean leaf,
                        int row,
                        boolean hasFocus) {

        super.getTreeCellRendererComponent(
                        tree, value, sel,
                        expanded, leaf, row,
                        hasFocus);
        if (leaf) {
            setIcon(goalIcon);
        } else {
            setIcon(projectIcon);
        }

        return this;
    }
}
