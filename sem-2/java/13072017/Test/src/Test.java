import java.awt.FlowLayout;
import java.awt.event.*;
import java.awt.*;
import javax.swing.*;
public class Test extends JFrame{
	private JTextField item1;
	private JTextField item2;
	private JTextField item3;
	private JPasswordField pas;
	public Test(){
		super("The title"); 
		setLayout(new FlowLayout());
		item1 = new JTextField(10);
		add(item1);
		item2 = new JTextField("enter text here");
		add(item2);
		item3 = new JTextField("This is not editable" , 20);
		item3.setEditable(false);
		add(item3);
		pas = new JPasswordField("pass");
		add(pas);
		hand h = new hand();
		item1.addActionListener(h);
		item2.addActionListener(h);
		item3.addActionListener(h);
		pas.addActionListener(h);
	}
	private class hand implements ActionListener{
		public void actionPerformed(ActionEvent event){
			String s = "";
			if(event.getSource() == item1)
				s= (String)event.getActionCommand();
			else if(event.getSource() == item2)
				s= (String)event.getActionCommand();
			else if(event.getSource() == item3)
				s= (String)event.getActionCommand();
			else if(event.getSource() == pas)
				s= (String)event.getActionCommand();
			JOptionPane.showMessageDialog(null, s);
		}
		
	}
}
