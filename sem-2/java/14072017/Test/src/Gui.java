import java.awt.*;
import java.awt.event.*;
import javax.swing.*;
import javax.swing.event.*;
public class Gui extends JFrame{
	private JTextField jt;
	private JCheckBox italicbox;
	private JCheckBox boldbox;
	public Gui(){
			super("The Title");
			setLayout(new FlowLayout());
			
			jt = new JTextField("This is used to write" , 20);
			jt.setFont(new Font("Serif" , Font.PLAIN , 14));
			add(jt);
			italicbox = new JCheckBox("italic");
			boldbox = new JCheckBox("bold");
			add(italicbox);
			add(boldbox);
			handler hand =  new handler();
			italicbox.addItemListener(hand);
			boldbox.addItemListener(hand);
			
	}
	private class handler implements ItemListener{
		public void itemStateChanged(ItemEvent ev){
			Font f = null;
			if(boldbox.isSelected() && italicbox.isSelected())
			{
					f = new Font("Serif" , Font.ITALIC + Font.BOLD , 14);
			}else if(boldbox.isSelected()){
				
				f = new Font("Serif" , Font.BOLD , 14);
			}else if(italicbox.isSelected()){
				
				f = new Font("Serif" , Font.ITALIC , 14);	
			}else
			{
				f = new Font("Serif" , Font.PLAIN ,14);	
			}
			jt.setFont(f);	
		}
			
	}
}
