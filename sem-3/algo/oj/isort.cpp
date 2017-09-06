#include<stdio.h>
#include<bits/stdc++.h>
using namespace std;
vector<int> ar;
void insertionSort(int n)
{
	int i, key, j;
	
	for (i = 1; i < n; i++)
	{
		int k = ar[i];
		j = i-1;
		while (j >= 0 && ar[j] > k)
		{
			//int temp = ar[j+1];
			ar[j+1] = ar[j];
			//ar[j] = temp;
			j--;
		}
		ar[j+1] = k;
	}
}
int main()
{
	int c=2;
	int i=0;
	char temp;
	 int n;
	     while((scanf("%d",&n)) != EOF)
		    {
		printf("%d\n",n);
		ar.push_back(n);
		i++;
		
			}
	
	int size=i;
       insertionSort(size);	
	for(i=0;i<size;i++){ 
		printf("%d ",ar[i]); 
	} 
	return 0;

}
