#include<stdio.h>
#include<math.h>
#include<stdlib.h>
int main()
{
	int N,i,j,m;
	printf("enter number of experments\n");
	scanf("%d",&m);
	printf("enter the number of steps\n");
	scanf("%d",&N);
	//int dis1=0,dis2=0;
	int ans = 0;
	for(j = 0;j<m;j++)
	{
	int dis1=0,dis2=0;
	for(i = 0;i<N;i++)
	{
	float x1 = (float)rand()/(float)(RAND_MAX/1);
	float x2 = (float)rand()/(float)(RAND_MAX/1);
	//printf("%f\n",x);
	if(x1 < 0.5)
	{
	
	dis1 = dis1 - 1;
		}
	else
	{
		dis1 = dis1 + 1;
		}

	if(x2 < 0.5)
	{
	dis2 = dis2 - 1;
		}
	else
	{
	dis2 = dis2 + 1;
	
		}

	
	}
	if(dis1 == dis2)
	ans++;	
	}
	double prob = (double)ans/m;
	printf("probability for their meeeting %lf\n",prob);
	return 0;


}
