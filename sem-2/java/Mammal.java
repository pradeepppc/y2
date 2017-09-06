package animals;
import java.io.*;
public class Mammal implements Animal{
	public void eat(){
	System.out.println("eat");
		}
	public void travel(){
		System.out.println("travel");
		}
	public int mam(){
		return 0;
		}
	public static void main(String args[]){
		Mammal m = new Mammal();
		m.eat();
		m.travel();

		}	
}
