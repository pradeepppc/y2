import java.io.*;
import java.lang.*;
import java.util.*;
class Outer{
int num;
private class Inner{
	
	public void print(){
		System.out.println("This is a inner class\n");
		}
}

	public void inner(){
	Inner in = new Inner();
	in.print();
	}

}

public class Myclass{
public static void main(String args[]){
	Outer o = new Outer();
	o.inner();
}

}
