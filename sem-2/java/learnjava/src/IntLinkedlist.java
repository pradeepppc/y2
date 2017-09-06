
public class IntLinkedlist {
	private Node head;
	public IntLinkedlist(int item){
			head = new Node();
			head.value = item;
			head.link = null;
			
	}
	public boolean nodeInsert(int item){
			Node n = new Node();
			n.value = item;
			n.link = head;
			head = n;
			return true;
	}
	public void PrintList(){
			Node temp = head;
			while(temp!=null){
					System.out.println(temp.value);
					temp = temp.link;
			}
			
	}
	public void listSort(){
			int c=0;
			Node a = head;
			while(a.link != null)
			{
					Node b= head;
					while(b.link != null)
					{
						if(b.value > b.link.value)
						{
							c = b.value;
							b.value = b.link.value;
							b.link.value  = c;
								
						}
						b = b.link;
					}
					a = a.link;
			}
	}
	public boolean delItem(int item){
		
		if(head.value == item)
		{
			head = head.link;
			return true;
		}
		else{
			Node p = new Node();
			Node q = new Node();
				q= head;
				p = head.link;
				while(p.value != item){
					q = p;
					p = p.link;	
				}
				if(p != null)
				{
				q.link = p.link;
				return true;
				}
				else
				{
				return false;	
					
				}
		}
	}
	class Node{
			private int value;
			private Node link;
			
	}
}
