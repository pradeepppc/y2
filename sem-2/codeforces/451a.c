#include<stdio.h>
int mini(int a,int b)
{
	if (a < b)
		return a;
	return b;
	}
int main()
{
	int n,m;
	scanf("%d %d",&n ,&m);
	if(mini(n,m) % 2 == 0)
	printf("Malvika");
	else
	printf("Akshat");	
	return 0;
	}
