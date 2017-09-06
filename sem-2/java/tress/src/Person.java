
public class Person {
	
private String name;
private int age;
public Person(String name , int age){
	this.age = age;
	this.name = name;	
}
public String getName(){
	
			return this.name;
}
public int getAge(){
	return this.age;
}
public void setAge(int num){
	age = num;
		
}
public String tostring(){
	return "name:" + name + " age :" + age + "\n" ; 
		
}
	
}
