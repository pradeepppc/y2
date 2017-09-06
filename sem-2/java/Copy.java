import java.io.*;
import java.util.*;
public class Copy{
	public static void main(String args[]) throws IOException {
		FileInputStream in = null;
		FileOutputStream out = null;
		try{
			in = new FileInputStream("input.txt");
			out = new FileOutputStream("output.txt");
			int i;
			while( (i= in.read()) != -1)
			{
				out.write(i);
			
				}
		
			}
		finally{
			if(in != null)
				in.close();
			if(out != null)
				out.close();
		
		}	
	}
}
