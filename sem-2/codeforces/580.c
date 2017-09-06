#include<stdio.h>
int main()
{
	int n;
	scanf("%d",&n);
	int  i;
	long long int a[1000000];
	int maxlength = -1;
	for(i=0;i<n;i++)
	{	
		scanf("%lld",&a[i]);
	
		}
	int count = 0;
	for(i=0;i<n;i++)
	{
		if(a[i+1] >= a[i])
		{
			count++;
			}
		else
			{
			
			if(count > maxlength)
				maxlength = count;
			count = 0;	
				}
	
		}
	printf("%d\n",maxlength+1);
	return 0;

}
