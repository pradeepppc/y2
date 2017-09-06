public class Main{
	public static void main(String args[]){
			

		/*Person p1  = new Person("chandu" , "123");
		Person p2  = new Person("nandu" , "321");
		PersonStack stack =  new PersonStack();
		stack.push(p1);
		stack.push(p2);
		System.out.println(stack.pop().toString());
		System.out.println(stack.pop().toString());
		}*/
		
		Intq q = new Intq();
		q.enq(3);
		System.out.println(q.deq());
	}
}
