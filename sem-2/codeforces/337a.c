#include<stdio.h>
void heapify(int a[],int n,int i)
{
	int max = i;
	int left = 2*i+1,right = 2*i+2;
	if(left < n && a[left] > a[max])
		max = left;
	if(right < n && a[right] > a[max])
		max = right;
	if(max != i)
	{
		int temp= a[max];
		a[max] = a[i];
		a[i]  = temp;
		heapify(a,n,max);
		}
	

}
void sorti(int a[],int m)
{
	int i;	
	for(i=m/2-1;i>=0;i--)
		heapify(a,m,i);
	for(i=m-1;i>=0;i--)
	{
		int temp = a[i];
		a[i] = a[0];
		a[0]  = temp;
		heapify(a,i,0);
		}

}
int main()
{
	int n,m;
	scanf("%d %d",&n ,&m);
	int a[1000];
	int i;
	for(i=0;i<m;i++)
	{
		scanf("%d",&a[i]);
	}
	sorti(a,m);
	/*for(i=0;i<m;i++)
		printf("%d ",a[i]);
	printf("\n");*/
	int minim = 1000000;
	for(i=0;;i++)
	{
		if(i+n-1 >= m)
			break;
		int tt = a[i+n-1] - a[i];
		if(tt < minim)
			minim = tt;
		}
	printf("%d",minim);
	return 0;	

}
