import java.awt.*;
import java.awt.event.*;
import javax.swing.*;
public class Gui extends JFrame{
	private JButton reg;
	private JButton cus;
	public Gui(){
		super("The title");
		setLayout(new FlowLayout());
		
		reg = new JButton("regular");
		add(reg);
		
		Icon b = new ImageIcon(getClass().getResource("b.png"));
		Icon x = new ImageIcon(getClass().getResource("x.png"));
		cus = new JButton("custom" , b);
		cus.setRolloverIcon(x);
		add(cus);
		Handle hand = new Handle();
		reg.addActionListener(hand);
		cus.addActionListener(hand);
	}
	private class Handle implements ActionListener{
		public void actionPerformed(ActionEvent ev){
			JOptionPane.showMessageDialog(null,(String)ev.getActionCommand());
			
		}
		
	}
}
