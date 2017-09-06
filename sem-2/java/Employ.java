import java.io.*;
public class Employ{
	
	String name;
	int age;
	String designation;
	double salary;
	
	public Employ(String name){
	
		this.name = name;
	}
	
	public void empage(int empage){
		age = empage;

	}
	public void empdesignation(String empdesignation)
	{
		designation = empdesignation;
		
	}

	public void empsalary(double empsalary){
		salary = empsalary;
		}
	public void printemploy(){
		System.out.println("name ::" + name);
		System.out.println("age ::" + age);
		System.out.println("salary ::" + salary);
		System.out.println("designation ::" + designation);
	
		}
}
