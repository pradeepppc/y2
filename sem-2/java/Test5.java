public class Test5{

	public static void main(String args[]){
		StringBuffer buf = new StringBuffer("abcdefghikl");
		System.out.print(buf);
		buf.replace(3,8,"HEL");

		System.out.print("\n");
		System.out.print(buf);
		}

}
