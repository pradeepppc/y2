import java.util.*;
public class Employ implements java.io.Serializable{
public String name;
public String address;
public transient int SSN;
public int num;
public void mailcheck(){
System.out.println("mailing a check to " + name + " " + address + "\n");
}
}
