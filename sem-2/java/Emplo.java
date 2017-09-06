import java.io.*;
import java.lang.*;
import java.util.*;
public class Emplo{
	private String name;
	private String address;
	private int number;
	public Emplo(String name,String address,int number){
	this.number = number;
	this.name = name;
	this.address  =address;
		}

	public void mailcheck(){
		System.out.println("Mailing a check to" + this.name + " " + this.address);
		}
	public String tostring(){
	
		return name + " "+ address +  " " + number; 
		}
	public String getname(){
		return name;
		
		}
	public String getaddress(){
		return address;
		}
	public int getnumber(){
		return number;
		}
}
