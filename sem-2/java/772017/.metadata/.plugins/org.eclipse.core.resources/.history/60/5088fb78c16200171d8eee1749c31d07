import java.util.*;
class Dog implements Comparator <Dog> ,Comparable <Dog>{
	private String name;
	private int age;
	Dog(){
		
	}
	Dog(String a, int num){
		this.age = num;
		this.name = a;
		
	}
	public String getName(){
	return name;	
	}
	public int getAge(){
		return age;
	}
	public int compareTo(Dog d){
		return this.name.compareTo(d.getName());
	}
	public int compare(Dog d , Dog d1){
		return d.age - d1.age;
		}
}
public class Example {
public static void main(String args[]){
	List<Dog> list = new ArrayList<Dog>();
	list.add(new Dog("hello" , 45));
	list.add(new Dog("kmdnjajd" , 2));
	list.add(new Dog("cac",4));
	Collections.sort(list);
	for(Dog a:list)
	{
		System.out.println(a.getName() + " ,");
	}
	System.out.println("\n");
	Collections.sort(list,new Dog());
	for(Dog j : list)
	{
		System.out.println(j.getName() + " " + j.getAge());
	}
	System.out.println("\n");
}

}
