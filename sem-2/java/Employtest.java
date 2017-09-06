import java.io.*;
public class Employtest{

	public static void main(String args[]){
	Employ empone = new Employ("chandu");
	Employ emptwo = new Employ("nandu");
	empone.empage(18);
	emptwo.empage(12);
	empone.empdesignation("soft");
	emptwo.empdesignation("soft");
	empone.empsalary(100000000);
	emptwo.empsalary(100000000);
	empone.printemploy();
	System.out.println("\n\n");
	emptwo.printemploy();
	}

}
