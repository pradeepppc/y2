#include<stdio.h>
int main()
{
	int n,m;
	scanf("%d %d",&n ,&m);
	int count=n,i;
	for(i=0;;i++)
	{
		count--;

		if((i+1) % m == 0)
			count++;

		if(count == 0)
			break;
	
		}
	printf("%d",i+1);
	return 0;

}
