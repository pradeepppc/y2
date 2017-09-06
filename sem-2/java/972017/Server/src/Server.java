import java.io.*;
import java.util.*;
import java.net.*;
import java.awt.*;
import javax.swing.*;
import java.awt.event.*;
public class Server extends JFrame{
	private JTextField usertext;
	private JTextArea chatWindow;
	private ObjectOutputStream output;
	private ObjectInputStream input;
	private ServerSocket server;
	private Socket connection;

	public Server(){
			super("AI messenger");
			usertext = new JTextField();
			usertext.setEditable(false);
			usertext.addActionListener(
			new ActionListener(){
			public void actionPerformed(ActionEvent event){
				sendMessage(event.getActionCommand());
				usertext.setText("");
			}
			
			}
					
					);

			add(usertext, BorderLayout.NORTH);
			chatWindow = new JTextArea();
			add(new JScrollPane(chatWindow));
			setSize(300 , 150);
			setVisible(true);
		}
	public void startrunning(){
		try{
			server =  new ServerSocket(6789 , 5);
			while(true){
			try{
				waitforconnection();
				setupstreams();
				whilechatting();
				}catch(EOFException er){
					showMessage("\n  Server stopped");
				
					}finally{
					
						closeshit();
					}
			
			}

			}catch(IOException error){
				error.printStackTrace();
				}
		}
	private void waitforconnection() throws IOException{
		showMessage(" Waiting for someone to connect...... \n");
		connection =  server.accept();
		showMessage(" Your are connected to" + connection.getInetAddress().getHostName());
	}
	
	private void setupstreams()throws IOException{
		output = new ObjectOutputStream(connection.getOutputStream());
		output.flush();
		input = new ObjectInputStream(connection.getInputStream());
		showMessage("\n Streams are now setup \n ");
		}
	private void whilechatting() throws IOException{
		String message = "\n you can chat now \n";
		sendMessage(message);
		abletotype(true);
		do{	
				try{
					message = (String) input.readObject();	
					showMessage("\n" + message);
					}catch(ClassNotFoundException e){
						showMessage(" wtf is that \n");
						}

		
			}
			while(!message.equals("END"));
		}
	// closing the streams and the sockets after you are done or just name it as housekeeping work in java 
	private void closeshit(){
		showMessage("\n closing the connection \n");
		abletotype(false);
		try{
			output.close();
			input.close();
			connection.close();
			}catch(IOException eee){
				eee.printStackTrace();
				}
		}
	private void sendMessage(String message){
		try{
			output.writeObject("Server : " + message + "\n");
			output.flush();
			showMessage("Server : " + message + "\n");
			}catch(IOException i)
		{
			chatWindow.append("\n error \n"); 
				}
		
		}
	private void showMessage(final String text){
		SwingUtilities.invokeLater(
				new Runnable(){
					public void run(){
							chatWindow.append(text);
							}
				
						}
				
				
				);
	
		}
	private void abletotype(final boolean t){
	
		
		SwingUtilities.invokeLater(
				new Runnable(){
					public void run(){
							//chatWindow.append(text);
						usertext.setEditable(t);		
						}
				
						}
				
				
				);
		}

}
