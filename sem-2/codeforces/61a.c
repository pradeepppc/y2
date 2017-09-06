#include<stdio.h>
#include<string.h>
int main()
{	
	char a[1000],b[1000];
	scanf("%s",a);
	scanf("%s",b);
	int i;
	for(i=0;i<strlen(a);i++)
	{	
		if(a[i] == b[i])
		printf("0");
		else
			printf("1");
		}
	return 0;
}
