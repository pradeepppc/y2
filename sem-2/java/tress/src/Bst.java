
public class Bst {

	private Node root;
	public Bst(){
		
			root = null;
	}
	public boolean Insert(Person item){
		Node n = new Node(); 
		n.data = item;
		n.lc = null;
		n.rc = null;
		if(root == null)
		{
		root = n;
		return true;
		}
		Node p = root;
		Node q = root;
		while(p != null)
		{
			q = p;
			if(item.getName().compareTo(p.data.getName()) < 0)
				p = p.lc;
			else
				p = p.rc;
			
		}
		if(item.getName().compareTo(q.data.getName()) < 0)
			q.lc = n;
		else
			{q.rc = n;}
		
		
		return true;
	}
	public Node findParent(String name){
			Node p = root;
			Node q = root;
			do{
				if(name.compareTo(q.data.getName()) == 0)
					break;
				p = q;
				if(name.compareTo(q.data.getName()) < 0)
						q = q.lc;
				else
					q = q.rc;
				
			}while(q != null);
			System.out.println(">>" + p.data.getName());
			if(q != null)
				return p;
			else
				return null;
	}
	
	public Person getData(Node n){
		return n.data;
		
	}
	public void showAll(Node n){
		if(n != null)
		{
			System.out.println(n.data.getName() + " /n");
			showAll(n.lc);
			showAll(n.rc);
		}
			
	}
	public Node findNode(String find){
		Node c = root;
		while(c != null){
		if(c.data.getName().compareTo(find) < 0)
			{c= c.rc;}
		else if(c.data.getName().compareTo(find) > 0)
			{c =c.lc;}
		else
			break;
		}
		return c;
		
	}
	
	class Node{
		private Node lc;
		private Node rc;
		private Person data;
	}
	
	
	}