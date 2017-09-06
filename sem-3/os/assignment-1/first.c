#include<stdio.h>
#include<stdlib.h>
#include<fcntl.h>
#include<unistd.h>
#include<sys/stat.h>
#include<sys/types.h>
int main(int argc,char *argv[]){
	int fd;
	//fd is the file discriptor for the file to open
	if(argc != 2)
	{
	return 0;//exit if wrong command
		}
	fd = open(argv[1],O_RDWR);
	if(fd < 0)
	{
		printf("failed to open\n");
		exit(1);

	}
	struct stat filestat;
	int x = stat(argv[1],&filestat);
	if(x < 0)
	{
	exit(1);
	}
	long long int text_size = filestat.st_size;
	text_size = text_size - 1;	
	printf("size : \t\t%lld bytes\n" ,  text_size);

	char buf;
	long long int i;

	int dir = mkdir("Assignment" ,0700);
	if(dir < 0)
	{
	printf("directory not created\n");
	exit(1);
		}
	int fd2 = open("Assignment/output.txt",O_CREAT | O_EXCL | O_RDWR);
	if(fd2 < 0)
	{

		printf("error\n");
		exit(1);
		}

	int xhm = chmod("Assignment/output.txt" , 0600);
	if(xhm < 0)
	{
		printf("error\n");
		exit(1);
		}
	int cc;

	for(i= text_size-1;i>=0;i--)
	{
	lseek(fd,i,SEEK_SET);
	cc = read(fd,&buf,1);
	int flag = 0;
	//printf("printing char %c \n",buf);
	if(buf <= 90 && buf >= 65)
	{
	buf = buf + 32;
	flag = 1;
		}
	if(flag == 0){
	if(buf >= 97 && buf <= 122)
	{
		buf = buf - 32;
		}
	
	}

	cc = write(fd2,&buf,1);
	}
	
	close(fd2);
	close(fd);
	return 0;
	
}
