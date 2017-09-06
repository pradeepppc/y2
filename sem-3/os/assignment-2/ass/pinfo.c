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
void pinfo(char *token)
{
	int flag1 = 0;
	char *tok1 = token;
	char buffer[100];

	token = strtok(NULL," ");

	if (token == NULL)
	{
		flag1 = 1;
	}
	char path[500];
	char path2[500];
	strcpy(path,"/proc/");

	if(flag1 == 1)
	{
		int pid = getpid();
		if(pid < 0)
		{
			printf("error in proccess id\n");
			return;
		}
		sprintf(buffer,"%d",pid);
		//buffer = itoa(pid,10);
		strcat(path,buffer);


	}
	else
	{

		strcat(path,token);	
	}
	strcpy(path2,path);
	strcat(path,"/stat");
	strcat(path2,"/exe");

	int fd;
	fd = open(path,O_RDONLY);
	if(fd < 0)
	{
		printf("Given proccess doesnt exist in system\n");
		return;
	}
	char buf[10000];
	read(fd,buf,153);
	char **arr;
	arr = (char **)malloc(100 * sizeof(char *));
	char *to;
	to = strtok(buf," ");
	int i=0;
	while(to != NULL)
	{

		arr[i] = to;

		i++;
		to = strtok(NULL," ");
	}

	printf("pid--%s\n",arr[0]);
	printf("Process Status --%s\n",arr[2]);
	printf("memory- %s\n",arr[24]);
	char bu[500];
	int rlink = readlink(path2,bu,499);
	printf("Executable Path -- %s\n",bu);


}
