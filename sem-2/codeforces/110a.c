#include<stdio.h>
int func(long long int l)
	{
		int count = 0;
		int flag=0;
		while(l>0)
		{
			int num = l %10;
			if(num == 4 || num == 7)
			{
			count++;
			}
			else
			{
				flag=1;
			}
			l= l/10;
			}
		return count;
	}	
int main()
{
	long long int n;
	scanf("%lld",&n);
	int ans = func(n);	
		if(ans == 4 || ans == 7 )
			printf("YES\n");
		else
			printf("NO\n");
	
			
	return 0;

}
