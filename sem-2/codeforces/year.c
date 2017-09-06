#include<stdio.h>
int check(int num)
{
	int a[4];
	int i;
	for(i=0;i<4;i++)
		{
			a[i] = num % 10;
			num = num / 10;
			}
	if(a[0] == a[1] || a[0] == a[2] || a[0] == a[3] || a[1] == a[2] || a[1] == a[3] || a[2] == a[3])
		return 0;
	else
		return 1;
}
int main()
{
	int y;
	scanf("%d",&y);
	int k=y+1;
	while(1)
	{
		if(check(k) == 1)
			break;
		else
			{}
		k++;
			}
	printf("%d\n",k);
	return 0;
}
