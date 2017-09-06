import java.io.*;
public class Insufficient extends Exception{
	private double amount;
	public Insufficient(double amount){
	this.amount = amount;
	}
	public double getamount(){
	return amount;
	}
		
}

