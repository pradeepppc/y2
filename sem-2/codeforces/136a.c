#include<stdio.h>
int main()
{
	int n;
	scanf("%d",&n);
	int a[100];
	int ans[100];
	int i;
	for(i=0;i<n;i++)
	{
	scanf("%d",&a[i]);
	ans[a[i]] = i+1;
	}
	for(i=1;i<=n;i++)
		printf("%d ",ans[i]);
			return 0;
}
