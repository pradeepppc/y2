import java.util.*;
import java.io.*;
import java.lang.*;
public class Check{
	private double balance;
	private int number;
	public Check(int number){
	
	this.number = number;
		}
	public void deposit(double amount){
		balance += amount; 
		}

	public double getBalance(){
	
	return balance;
		}
	public int getNumber(){
		return number;
		}
	public void withdraw(double amount) throws Insufficient{
	
		if(amount <= balance)
		{
		balance  = balance  - amount;
			}
		else{
			double need  = amount - balance;
			throw new Insufficient(need);
			}

		}
}
