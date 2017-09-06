public class Puppy{
	int age;
	public Puppy(String nam){
		
		System.out.println("hello" + nam);
		}

	public void setage(int num)
	{
		age = num;
	
		}
	public int getage(){
	
		System.out.println("Puppys age is : " + age);
		return age;
		}

	public static void main(String []args){
		Puppy mypup = new Puppy("po");
		mypup.setage(12);
		System.out.println("pup age is :" + mypup.getage() + " " + mypup.age);
		}
}
