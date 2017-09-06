#include<stdio.h>
void heapify(long long int a[],int i,int n);
long long int max(long long int a,long long int b)
{
	if(a > b)
		return a;
	return b;

}
void heapify(long long int a[],int i,int n)
{

	int left= 2*i+1;
	int right = 2*i+2;
	long long int ans = i;
	if(left < n && a[left] > a[i])
		ans = left;
	if(right < n && a[right] > a[ans])
		ans = right;
	if(ans != i)
	{
		long long int temp = a[i];
		a[i] = a[ans];
		a[ans] = temp;
		heapify(a,ans,n);
			}


}
void sortin(long long int a[],int n)
{
	int i;
	for(i=n/2-1;i>=0;i--)
		heapify(a,i,n);
	for(i=n-1;i>=0;i--)
	{
		long long int temp = a[i];
		a[i]= a[0];
		a[0] = temp;
		heapify(a,0,i);
		}


}
int check(long long int a,long long int b,long long int c)
{

	if(c < a+b && a < b+c && b < c+a)
	return 1;
	else
		return 0;
}
int main()
{
	int n;
	scanf("%d",&n);
	int i;
	long long int a[100000];
	for(i=0;i<n;i++)
		scanf("%lld",&a[i]);
	sortin(a,n);
	int flag=0;
	for(i=0;i<n-2;i++)
	{	
		int ans = check(a[i],a[i+1],a[i+2]);
		if (ans == 1)
			{
			flag= 1;
				break;
				}
		else
			{}
			}
	if(flag == 1)
		printf("YES\n");
	else
		printf("NO\n");
	return 0;
}
