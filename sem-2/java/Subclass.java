class Super_class{
	int num = 20;
	public void display(){
	System.out.println("hello hey");
	}

}

class Subclass extends Super_class{
	int num = 10;
	public void display(){
	System.out.println("This is sub class");
	}
	public void mymethod(){
		Subclass sub = new Subclass();
		sub.display();
		super.display();
		System.out.println(sub.num + "\n");
		System.out.println(super.num);
	}
	public static void main(String args[]){
		Subclass o =new Subclass();
		o.mymethod();
		}

}
