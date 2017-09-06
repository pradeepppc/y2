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
void purecom(char command[])
{
	char *token;
	token=strtok(command," ");
	//token2=strtok(token1,"\t");
	if(strcmp(token,"cd")==0)
	{
		//call cd()
		cd(token);
	}
	else if(strcmp(token,"pwd")==0)
	{
		pwd();
	}
	else if(strcmp(token,"ls") == 0)
	{
		//call ls
		ls(token);

	}
	else if(strcmp(token,"echo") == 0)
	{
		echo(token);
	}
	else if(strcmp(token,"exit") == 0)
	{
		// exit
		exit(1);
	}
	else if(strcmp(token,"pinfo") == 0)
	{
		pinfo(token);

	}
	else
	{
		char *argv[100];
		parse(commandget,argv);
		pid_t pid;
		int status;
		pid=fork();
		if(pid<0)
		{
			printf("ERROR in forking\n");
			exit(1);
		}
		else if(pid==0)
		{
			//child process
			if(execvp(*argv,argv)<0)
			{
				printf("ERROR :exec failed\n");
				exit(1);
			}
		}
		else
		{
			//printf("Parent");
			if(flag!=1)
			{
				//printf("No &");
				while(wait(&status) !=pid);
			}
		}
	}


}
