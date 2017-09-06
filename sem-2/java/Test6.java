public class Test6{

	public static void main(String args[]){
		String str1  = new String("hello");
		String str2 = new String("hey");
		String str3 = new String("hello");
		int x = str1.compareTo(str2);
		int y = str1.compareTo(str3);
		int z = str2.compareTo("hhhhhh");
		System.out.printf("%d %d %d",x ,y , z);
	
	}

}
