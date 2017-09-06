#include<stdio.h>
#include<string.h>
int main()
{
	
	char a[5001];
	scanf("%s",a);
	int i=0;
	int flag = 0;
	for(i=0;a[i] != '\0' ; i++)
	{
		if(a[i] == '0' && flag == 0)
		{
			
			flag = 1;
			}
		else if(a[i+1] == '\0' && flag == 0)
		{
		
			}
		else
		{
			printf("%c",a[i]);
			}

		}
	printf("\n");
	return 0;
}
