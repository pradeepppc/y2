import java.util.*;
public class Test{
public static <T extends Comparable<T>>T max(T a1,T a2, T a3){
T max = a1;
if(a2.compareTo(max)  > 0)
	max = a2;
if(a3.compareTo(max) > 0)
	max  =a3;	
return max;
}
public static void main(String args[]){
System.out.printf("%d\n",max(3,4,5));

System.out.printf("%f\n",max(3.30,4.15,5.1561));
System.out.printf("%s\n",max("hello","hellos","hellop"));

}

}
