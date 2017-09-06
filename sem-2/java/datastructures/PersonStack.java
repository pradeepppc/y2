public class PersonStack{
	private Person [] stack;
	private int top;
	private int size;
	public PersonStack(){
		top = -1;
		size = 50;
		stack = new Person [50];
		}
	public PersonStack(int size){
		top = -1;
		this.size = size;
		stack = new Person [this.size];	
		}
	public boolean push(Person item){
		if(!isFull())
		{top++;
		stack[top] = item;
		return true;}
		else
			return false;
		}
	public boolean isFull(){
		if(stack.length-1 == top)
		return true;
		else
		return false;	
		}
	public Person pop(){
		return stack[top--];

		}
	public boolean isEmpty(){
		if(top == -1)
			return true;
		else
			return false;
		}
}
