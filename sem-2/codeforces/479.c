#include<stdio.h>
int max(int a,int b)
{
	if (a > b)
		return a;
	return b;
	}
int main()
{
	int a[3];
	int i;
	for(i=0;i<3;i++)
	{
		scanf("%d",&a[i]);
		}
	int ans1 = a[0]*a[1]+a[2];
	int ans2 = a[0]+a[1]*a[2];
	int ans3 = a[0]*a[1]*a[2];
	int ans4 = a[0]*(a[1]+a[2]);
	int ans5 = (a[0]+a[1])*a[2];
	int ans6 = a[0]+a[1]+a[2];
	printf("%d\n",max(ans1,max(ans2,max(ans3,max(ans4,max(ans5,ans6))))));
	return 0;

}
