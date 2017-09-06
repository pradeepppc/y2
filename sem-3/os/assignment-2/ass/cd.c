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
void cd(char *token)
{
	char newdir[100];
	token=strtok(NULL," ");
	while(token!=NULL)
	{
		if(token=="$")
			break;
		char temp[100];
		getcwd(temp,100);
		if(strcmp(token,"..")==0)
		{
			int i;
			for(i=strlen(temp)-1;i>=0;i--)
			{
				if(temp[i]=='/')
				{
					temp[i]=0;
					break;
				}
			}
			strcpy(newdir,temp);
		}
		else
		{
			strcpy(newdir,temp);
			strcat(newdir,"/");
			strcat(newdir,token);
		}
		int x = chdir(newdir);
		if(x == -1)
		{
			//error handling
			printf("error in command cd\n");
			exit(1);
		}

		setpath();
		token=strtok(NULL," ");
	}
}
