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

void dump_tm (struct tm *t);
char initialdir[100];
char presentdir[100]={0};
char *commandget;
int flag;
#define ANSI_COLOR_RED     "\x1b[31m"
#define ANSI_COLOR_GREEN   "\x1b[32m"
#define ANSI_COLOR_YELLOW  "\x1b[33m"
#define ANSI_COLOR_BLUE    "\x1b[34m"
#define ANSI_COLOR_MAGENTA "\x1b[35m"
#define ANSI_COLOR_CYAN    "\x1b[36m"
#define ANSI_COLOR_RESET   "\x1b[0m"
void setpath()
{
	int i,j;
	char temp[100];
	getcwd(temp,100);
	if(strlen(initialdir)==strlen(temp))
	{
		presentdir[0]=0;
	}
	else if(!strlen(initialdir)<strlen(temp))
	{
		for(i=strlen(initialdir),j=0;i<strlen(temp);i++,j++)
		{
			presentdir[j]=temp[i];
		}
	}
}

void split(char command[])
{
	char *token,*temp;
	char *save1,*save2;
	token=strtok_r(command, ";",&save1);
	while(token!=NULL)
	{
		//    printf("%s\n",token);
		temp=token;
		purecom(token);
		token=strtok_r(NULL,";",&save1);
	}
}


int main()
{
	strcpy(initialdir,getenv("PWD"));

	//    if(1)
	while(1)
	{
		flag=0;
		prbash();
		commandget=(char*)malloc(sizeof(char)*100);
		scanf(" %[^\n]s",commandget);
		if(commandget[strlen(commandget)-1]=="&")
		{
			flag=1;

		}

		split(commandget);
		free(commandget);
	}
	return 0;
}
