import java.util.*;
import java.io.*;
public class Console{
	public static void main(String args[]) throws IOException{
		InputStreamReader cin = null;
	try{
		cin  = new InputStreamReader(System.in);
		char c;
		do{
		c = (char) cin.read();
		System.out.print(c + "\n");
		
				}while(c != 'q');
		}
		finally{
			if(cin != null)
			{
				cin.close();	
				}
				}
	
	}

} 
