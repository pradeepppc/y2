import java.util.*;
public class Main {
public static void main(String args[]){
	Enumeration days; 
	Vector v = new Vector();
	v.add("monday");
	v.add("tueday");
	v.add("wednesday");
	days  = v.elements();
	while(days.hasMoreElements()){
		
		System.out.println(days.nextElement());
	}
}
}
