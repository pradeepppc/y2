import java.util.*;
import java.io.*;
import java.lang.*;
public class Read{
	public static void main(String args[]){
		File f = null;
		String[] str;
		try{
		 f = new File("/tmp/user");
		 str  = f.list();
		for(String s : str){
			System.out.println(s + "\n");
			}

			}
		catch(Exception e){
		
			e.printStackTrace();
		
		}
	}

}
