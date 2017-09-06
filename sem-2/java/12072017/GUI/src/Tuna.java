import javax.swing.*;
import java.awt.*;
public class Tuna extends JFrame{
private JLabel item1;
public Tuna(){
	
		super("The title bar");
		setLayout(new FlowLayout());
		item1 = new JLabel("this is a sentance");
		item1.setToolTipText("This will show up on hovering");
		add(item1);
		
}

}
