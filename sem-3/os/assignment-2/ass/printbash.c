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
void prbash()
{
	struct utsname data;
	char s[100];
	int r=gethostname(s,100);
	if(r<0)
	{
		//ERROR HANDLING
		printf("Unable to get hostname\n");
		exit(1);
	}
	r=uname(&data);
	if(r<0)
	{
		//ERROR HANDLING
		printf("Error in uname\n");
		exit(1);
	}
	printf("<%s@%s:~%s>",s,data.sysname,presentdir);
	return ;
}
