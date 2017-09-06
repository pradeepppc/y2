import javax.swing.*;
import java.awt.*;
import java.awt.event.*;
public class gui extends JFrame{
	private JComboBox box;
	private JLabel picture;
	
	private static String[] filename = {"b.png" ,"x.png"};
	private Icon[] pics = {new ImageIcon(getClass().getResource(filename[0])) ,new ImageIcon(getClass().getResource(filename[1])) };
	public gui(){
			super("The title");
			setLayout(new FlowLayout());
			box  = new JComboBox(filename);
			box.addItemListener(
			new ItemListener(){
				public void itemStateChanged(ItemEvent ev){
					if(ev.getStateChange() == ItemEvent.SELECTED)
					{
						picture.setIcon(pics[box.getSelectedIndex()]);
						
					}
				}
					
			});
			add(box);
			picture  = new JLabel(pics[0]);
			add(picture);
	}
}
