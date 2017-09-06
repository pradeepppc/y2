interface Message{
	String greet();
}

public class Ab{
public void desplay(Message m){

	System.out.println(m.greet() + "hello hi");

}
public static void main(String args[]){
	Ab n = new Ab();
	n.desplay(new Message(){
	public String greet(){
		return "assssk";
	}
		
		});
}
}
