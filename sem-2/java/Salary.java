import java.io.*;
public class Salary extends Emplo{
	private double salary;
	public Salary(String name,String address,int number,double salary){
		super(name,address,number);
		setsalary(salary);
		}
	public void mailcheck(){
	System.out.println("Within mail check of salary class");
	System.out.println("Mailing check to " + getname() + "with salary" + salary);
		
		}
	public double getsalary(){
		return salary;
		}
	public void setsalary(double salary){
		this.salary  =salary;
		}
}
