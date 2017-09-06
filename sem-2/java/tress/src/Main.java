
public class Main {
public static void main(String args[]){
	Person p1 = new Person("chandu",45);
	Person p2 = new Person("nandu" , 46);
	Person p3 = new Person("hello" , 12);
	Person p4 = new Person("sncjnds" , 48);
	
	Bst tree = new Bst();
		 tree.Insert(p4);
		 tree.Insert(p2);
		 tree.Insert(p3);
		 tree.Insert(p1);
		 //tree.showAll(tree.findNode("hello"));
		 Person p = tree.getData(tree.findNode("hello"));
		 System.out.println(p.tostring());
}
}
