import java.util.*;
public class Main {
public static void main(String args[]){
	LinkedList l = new LinkedList();
	l.add(new Integer(5));
	l.add(new Integer(-56));
	l.add(new Integer(48));
	l.add(new Integer(485));
	l.add(new Integer(-15));
	Comparator r = Collections.reverseOrder();
	Iterator i  = l.iterator();
	while(i.hasNext()){
		System.out.println(i.next() + " ");
	}
	System.out.println("\n");
	Collections.sort(l);
	i = l.iterator();
	while(i.hasNext()){
		System.out.println(i.next() + " ");
	}
	System.out.println("\n");
	Collections.sort(l,r);
	i = l.iterator();
	while(i.hasNext()){
		System.out.println(i.next() + " ");
	}
	Collections.shuffle(l);
	i = l.iterator();
	System.out.println("\n");
	while(i.hasNext()){
		System.out.println(i.next() + " ");
	}
	System.out.println("\n");
	System.out.println("minimum :" + Collections.min(l) + "\n");
	System.out.println("maximum :" + Collections.max(l) + "\n");
}
}
