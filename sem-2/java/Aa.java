abstract class Anonym{
public abstract void mymethod();
}
public class Aa{
public static void main(String args[]){

	Anonym an = new Anonym(){
		public void mymethod(){
			System.out.println("hello hi everyone\n");
			}
	
	};
	an.mymethod();
}}
