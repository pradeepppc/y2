import java.io.*;
import java.util.*;
import java.lang.*;
public class Bankdemo{
	public static void main(String args[]){
	Check c = new Check(100);
	System.out.println("depositing 500 dollars \n");
	c.deposit(500.00);
	try{
	System.out.println("withdrawing 100 dollars \n");
	c.withdraw(100.00);
	System.out.println("balance is :" + c.getBalance() + "\n");
	System.out.println("withdrawing 600 dollars\n");
	c.withdraw(600.00);
	
	}
	catch(Insufficient e){
		
		System.out.println("Sorry you are short of " + e.getamount() + "\n");
		e.printStackTrace();	
	}
		}

}
