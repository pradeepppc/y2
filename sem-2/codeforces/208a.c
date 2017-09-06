#include<stdio.h>
#include<string.h>
int main()
{
	char a[300];
	scanf("%s",a);
	int i;
	int flag=0;
	int first = 0;
	for(i=0;i<strlen(a);i++)
	{
		if(a[i] == 'W')
			{
				if(a[i+1] == 'U' && a[i+2] == 'B')
				{
					i=i+2;
					flag= 1+flag;
					if(flag == 1 && first != 0)
						printf(" ");	
							
					}
				else
				{
					printf("%c",a[i]);
					flag = 0;
					first = 1;
					continue;
				
					}
				}	
			else
				{
				flag = 0;
				first = 1;
				printf("%c",a[i]);	
					}
	
			}
	return 0;


}
