import java.util.*;
public class Main {
public static void main(String args[]){
		ArrayList ar = new ArrayList();
		ar.add("a");
		ar.add("b");
		ar.add("c");
		Iterator i = ar.iterator();
		while(i.hasNext()){
			Object o = i.next();
			System.out.println(o + " ");
		}
		System.out.println("\n");
		ListIterator it =  ar.listIterator();
		while(it.hasNext()){
			Object l = it.next();
			it.set(l + "+");
			//System.out.println(o + " ");
		}
		i = ar.iterator();
		while(i.hasNext()){
			 Object k = i.next();
			//System.out.println(o + " ");
			System.out.println(k + " ");
		}
		System.out.println("\n");
		while(it.hasPrevious()){
			System.out.println(it.previous() + " ");
				
		}
		System.out.println("\n");
}
}
