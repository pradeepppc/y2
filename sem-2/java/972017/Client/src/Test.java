import javax.swing.JFrame;
public class Test {
public static void main(String args[]){
Client chandu;	
	chandu =  new Client("127.0.0.1");
	chandu.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
	chandu.startrunning();
}
}
