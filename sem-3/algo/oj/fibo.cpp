#include<stdio.h>
#include<bits/stdc++.h>
using namespace std;
long long int ar[100000]={0};
long long int ans(long long int n)
{
	if(n == 1)
	{
	ar[1] = 1;
	return 1;	
		}
	else if(n == 2)
	{
	ar[2] = 1;
	return 1;
		}
	else
	{
	if(ar[n] != 0)
		return ar[n];
	else
	{
	ar[n] = ans(n- 1) + ans(n- 2);
	return ar[n];
		}
		}

}
int main()
{
	long long int n;
	scanf("%lld",&n);
	long long int an = ans(n);
	printf("%lld\n",an);
	return 0;
	}
