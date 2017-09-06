#include<stdio.h>
int main()
{
	int a,b;
	scanf("%d %d",&a ,&b);
	int count=0;
	while(a)
	{
	if(a >= b)
	{
	count = count + b;
	a = a - b;
	a = a+1;
			}
	else
		{
		count = count + a;	
		break;
			}
		
	}
	printf("%d",count);
	return 0;
}
