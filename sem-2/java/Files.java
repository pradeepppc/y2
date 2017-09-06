import java.util.*;
import java.io.*;
public class Files{
	public static void main(String args[]){
		File f = null;
		String[] str = {"file1.txt","file2.txt"};
		try{
		for(String s:str)
		{	
		f = new File(s);
		boolean bo = f.canExecute();
		String ss = f.getAbsolutePath();
		System.out.println(ss +  ":"+ bo);
			}
		
		}
		catch(Exception e){
		
			e.printStackTrace();
		}

		}
}
