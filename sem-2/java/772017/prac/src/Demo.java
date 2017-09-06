import java.util.*;
import java.io.*;
public class Demo{
public static void main(String args[]){
Employ e  = new Employ();
e.name = "nandu";
e.address = "acdc";
e.SSN = 15;
e.num = 101;
try{
	FileOutputStream fileout = new FileOutputStream("/tmp/employ.ser");
	ObjectOutputStream out = new ObjectOutputStream(fileout);
	out.writeObject(e);
	out.close();
	fileout.close();
	System.out.println("done");
		}
	catch (IOException i){
	i.printStackTrace();
	}

}
}
