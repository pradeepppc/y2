#include<stdio.h>
int main()
{
	long long int n;
	scanf("%lld",&n);
	long long int sum;
	if (n % 2 == 0)
		sum  = n/2;
	else
		sum = -(n+1)/2;
	printf("%lld\n",sum);
	return 0;
	}
