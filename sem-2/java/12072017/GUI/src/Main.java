import javax.swing.*;
public class Main {
public static void main(String args[]){
		String s = JOptionPane.showInputDialog("enter first number");
		String r = JOptionPane.showInputDialog("enter secon number");
		int num1 = Integer.parseInt(s);
		int num2 = Integer.parseInt(r);
		int ans = num1 + num2;
		JOptionPane.showMessageDialog(null, "the sum is" + ans , "GUI",JOptionPane.PLAIN_MESSAGE);
}	
}