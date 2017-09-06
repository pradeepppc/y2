import java.util.*;
public class general {
public static < E > void printArray(E[] array){
	for(E el:array){
		System.out.printf("%s ",el);
	}
	System.out.println();
	}
public static void main(String args[]){
	Integer[] intarr = {1,2,3,4,5,6};
	Double[] darr = {1.1,2.2,3.3,4.1,5.5,6.6};
	printArray(intarr);
	System.out.println("\n");
	printArray(darr);
}

}
