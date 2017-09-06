#include <stdio.h>
#include <limits.h>
int ans[100][100] = {0};
int s[100][100]  = {0};

int func(int arr[],int left,int right)
{
	if (left == right)
	{
		return  0;

	}
	int i;
	int min = INT_MAX;
	int count;
	for(i=left;i<right;i++)
	{
		count = 0;
		//int ans1,ans2;
		if(ans[left][i] != 0)
		{
				//count = count + ans[left][i];
		}
		else
		{
			ans[left][i] = func(arr,left,i);

		}	
		count = count + ans[left][i];

		if(ans[i+1][right] != 0)
		{

		}
		else
		{
			ans[i+1][right] = func(arr,i+1,right);

		}
		count = count + ans[i+1][right] + arr[left-1]*arr[i]*arr[right];


		//count = func(arr,left,i) + func(arr,i+1,right) + arr[left-1]*arr[i]*arr[right];
		if (count < min)
		{
			min = count;
			s[left][right] = i;

		}	
	}

	return min;

}
void printparen(int left,int right)
{
	if (left == right)
		printf("A%d",left);
	else
	{
		printf("(");	
		printparen(left,s[left][right]);
		printparen(s[left][right]+1,right);
		printf(")");
	}

}
int main()
{
	/* code */
	int arr[] = {5,10,3,12,5,50,60};
	int n = sizeof(arr)/sizeof(arr[0]);
	printf("min cost is %d\n",func(arr,1,n-1));
	printparen(1,n-1);
	printf("\n");
	return 0;
}