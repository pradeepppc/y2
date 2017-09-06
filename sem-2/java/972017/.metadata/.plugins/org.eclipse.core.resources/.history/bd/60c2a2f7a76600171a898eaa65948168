import java.io.*;
import java.net.*;
import java.awt.*;
import java.awt.event.*;
import javax.swing.*;
public class Client extends JFrame{
	private JTextField usertext;
	private JTextArea chatwindow;
	private ObjectOutputStream output;
	private ObjectInputStream input;
	private String message = "";
	private String serverip;
	private Socket connection;
	
	public Client(String host){
			super("ms g");
			serverip = host;
			usertext = new JTextField();
			usertext.setEditable(false);
			usertext.addActionListener(
				new ActionListener(){
					public void actionPerformed(ActionEvent event){
					senddata(event.getActionCommand());
					usertext.setText("");
					}});
					add(usertext , BorderLayout.NORTH);
					chatwindow  = new JTextArea();
					add(new JScrollPane(chatwindow) , BorderLayout.CENTER);
					setSize(300 , 150);
					setVisible(true);
					
	}
	public void startrunning(){
			try{
				connecttoserver();
				setupstreams();
				whilechatting();
			}catch(EOFException er){
				showmessage("Client terminated connection \n");
			}catch(IOException io){
				io.printStackTrace();
			}finally{
				closecrap();
			}
			
	}
	private void connecttoserver() throws IOException{
		showmessage("Attempting connection \n");
		connection  = new Socket(InetAddress.getByName(serverip) , 6789);
		showmessage("connected to : " + connection.getInetAddress().getHostName());
	} 
	private void setupstreams() throws IOException{
		output  = new ObjectOutputStream(connection.getOutputStream());
		output.flush();
		input  = new ObjectInputStream(connection.getInputStream());
		showmessage("Dude your streams are good to use now \n");	
	}
	private void whilechatting() throws IOException{
		abletotype(true);
		do{
			try{
				message = (String) input.readObject();
				showmessage("\n" +":" + message + "\n");
			}catch(ClassNotFoundException cl){
				
					showmessage(" untrusted contact \n");
			}
				
		}while(!message.equals("END"));
		
	}
	private void closecrap(){
		showmessage("\n closing the crap down \n");
		try{
			input.close();
			output.close();
			connection.close();
		}catch(IOException e){
				e.printStackTrace();
		}
			
	}
	private void senddata(String message){
		try{
			output.writeObject("Client - " + message + "\n");
			output.flush();
			showmessage("\nClient - " + message + "\n");	
		}catch(IOException i){
				chatwindow.append("\n something messed up \n");
		}
			
	}
	private void showmessage(final String str){
		SwingUtilities.invokeLater(
				new Runnable(){
					public void run(){
						
						chatwindow.append(str);
					}});
		
	}
	private void abletotype(final boolean r){
		SwingUtilities.invokeLater(
				new Runnable(){
					public void run(){
						usertext.setEditable(r);
							
					}
					
				}
				);
			
	}
	
}




























