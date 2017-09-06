#include<stdio.h>
#include<stdlib.h>
#include<unistd.h>
#include<string.h>
#include<dirent.h>
#include<sys/types.h>
#include<sys/stat.h>
#include<fcntl.h>
#include <sys/utsname.h>
#include<time.h>
#include<pwd.h>
#include<grp.h>
void echo(char *token)
{
	char *temp;
	token=strtok(NULL," ");
	while(token!=NULL)
	{

		if(token[0] == '$')
		{

			temp=(char*)malloc(sizeof(char)*100);
			strcpy(temp,token+1);

			temp=getenv(temp);

			printf("%s ",temp);
		}
		else
		{
			printf("%s ",token);
		}
		token=strtok(NULL," ");
	}
	printf("\n");
}
