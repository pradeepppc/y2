class outer{
	private int num = 175;
	class inner{
		public int getnum(){

			return num;
			}
	
	}

}
public class Inner{
 	public static void main(String args[]){
		outer o = new outer();
		outer.inner in = o.new inner();
		System.out.println(in.getnum());
		//System.out.println(o.num); num cannot be used as it is a private in outer.
		}


}

