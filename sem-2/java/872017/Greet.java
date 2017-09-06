import java.net.*;
import java.io.*;
public class Greet{
public static void main(String args[]){

	String servername = args[0];
	int port = Integer.parseInt(args[1]);
	try{
		System.out.println("Connecting to " + servername + " on port  " + port);
		Socket client = new Socket(servername , port);
		System.out.println("just connected to " + client.getRemoteSocketAddress());
		OutputStream ou = client.getOutputStream();
		DataOutputStream out = new DataOutputStream(ou);
		out.writeUTF("Hello from other side \n");
		InputStream in = client.getInputStream();
		DataInputStream inp = new DataInputStream(in)	;
		System.out.println("Server says " + inp.readUTF());
		client.close();
	}catch(IOException e){
		e.printStackTrace();
		}
}

}
