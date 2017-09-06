import java.util.*;
public class Datedemo1{
	public static void main(String args[])
	{
		Date date = new Date();
		String str = String.format("%tc",date);
		System.out.println(str);
	}

}
