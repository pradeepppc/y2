#include<stdio.h>
#include<stdlib.h>
#include<fcntl.h>
#include<unistd.h>
#include<sys/stat.h>
#include<sys/types.h>
void print(char st[])
{
	int u=0;
	for(u=0;st[u] !='\0';++u);
	write(STDOUT_FILENO, st, u);
	return;

}
int main(int argc , char *argv[])
{
	if(argc != 2)
	{
		exit(1);	
	}
	int ans = symlink("Assignment/output.txt","linkoutput.txt");
	if(ans == 0)
	{

	}
	else{
		exit(1);
	}
	struct stat dirstat,filestat,symstat;
	int ans1 = stat("Assignment",&dirstat);
	int ans2 = lstat("linkoutput.txt",&symstat);
	int ans3 = stat("Assignment/output.txt",&filestat);

	//checking directory created or not
	if(S_ISDIR(dirstat.st_mode))
	{
		print("Checking whether the directory has been created: Yes\n");
		
	}
	else
	{
		print("directory not created\n");
		exit(1);
	}
	//checking if regular file created
	if(S_ISREG(filestat.st_mode))
	{
		print("Checking whether the file has been created: Yes\n");
	}
	else
	{
		print("file not created\n");
		exit(1);

	}

	//checking if symbolic file created or not
	if(S_ISLNK(symstat.st_mode))
	{
		print("Checking whether the symlink has been created: Yes\n");
	}
	else
	{
		print("symlink not created\n");
		exit(1);
	}

	print("\n");

	//checking if the file content have been reversed or not

	int fd1 = open(argv[1],O_RDONLY);
	int fd2 = open("Assignment/output.txt",O_RDONLY);

	char buf1,buf2;

	long long int size = filestat.st_size - 1;
	long long int i;
	int flag = 0;
	struct stat givenstat;
	stat(argv[1] , &givenstat);
	if(givenstat.st_size != filestat.st_size)
	{
		flag = 1;
		}
	if(flag == 0)
	{
	for(i=size  ;i>=0 ;i--)
	{
		lseek(fd1,i,SEEK_SET);
		lseek(fd2,size-1-i,SEEK_SET);
		read(fd1,&buf1,1);	
		read(fd2,&buf2,1);
		if((buf1 <= 90 && buf1 >= 65) || (buf1 >= 97 && buf1 <= 122))
		{
			if((buf1 == (buf2 + 32)) || (buf2 == (buf1 + 32)))
			{}
			else
			{
				flag = 1;
				break;}

		}
		else
		{
			if(buf1 == buf2)
			{}
			else
			{
				flag = 1;
				break;
			}
		}

	}
	}
	if(flag == 1)
	{
		print("Checking whether file contents have been reversed and case-inverted: Yes\n");
	}
	else
	{
		print("Checking whether file contents have been reversed and case-inverted: No\n");
	}

	print("\n");

	//checking user permissions on file
	if(filestat.st_mode & S_IRUSR)
	{
		print("User has read permission on file: Yes\n");
	}
	else
	{
		print("User has read permission on file: No\n");
	}

	if(filestat.st_mode & S_IWUSR)
	{
		print("User has write permission on file: Yes\n");
	}
	else
	{
		print("User has write permission on file: No\n");
	}

	if(filestat.st_mode & S_IXUSR)
	{
		print("User has execute permission on file: Yes\n");
	}
	else
	{
		print("User has execute permission on file: No\n");
	}

	print("\n");
	//checking group permissions on the file
	if(filestat.st_mode & S_IRGRP)
	{
		print("Group has read permission on file: Yes\n");
	}
	else
	{
		print("Group has read permission on file: No\n");
	}
	if(filestat.st_mode & S_IWGRP)
	{
		print("Group has write permission on file: Yes\n");
	}
	else
	{
		print("Group has write permission on file: No\n");
	}
	if(filestat.st_mode & S_IXGRP)
	{
		print("Group has execute permission on file: Yes\n");
	}
	else
	{
		print("Group has execute permission on file: No\n");
	}
	print("\n");

	//checking other permissions on the file
	if(filestat.st_mode & S_IROTH)
	{
		print("Others has read permission on file: Yes\n");
	}
	else
	{
		print("Others has read permission on file: No\n");
	}
	if(filestat.st_mode & S_IWOTH)
	{
		print("Others has write permission on file: Yes\n");
	}
	else
	{
		print("Others has write permission on file: No\n");
	}
	if(filestat.st_mode & S_IXOTH)
	{
		print("Others has execute permission on file: Yes\n");
	}
	else
	{
		print("Others has execute permission on file: No\n");
	}
	print("\n");


	//checking user permissions on directory
	if(dirstat.st_mode & S_IRUSR)
	{
		print("User has read permission on directory: Yes\n");
	}
	else
	{
		print("User has read permission on directory: No\n");
	}

	if(dirstat.st_mode & S_IWUSR)
	{
		print("User has write permission on directory: Yes\n");
	}
	else
	{
		print("User has write permission on directory: No\n");
	}

	if(dirstat.st_mode & S_IXUSR)
	{
		print("User has execute permission on directory: Yes\n");
	}
	else
	{
		print("User has execute permission on directory: No\n");
	}

	print("\n");
	//checking group permissions on the directory
	if(dirstat.st_mode & S_IRGRP)
	{
		print("Group has read permission on directory: Yes\n");
	}
	else
	{
		print("Group has read permission on directory: No\n");
	}
	if(dirstat.st_mode & S_IWGRP)
	{
		print("Group has write permission on directory: Yes\n");
	}
	else
	{
		print("Group has write permission on directory: No\n");
	}
	if(dirstat.st_mode & S_IXGRP)
	{
		print("Group has execute permission on directory: Yes\n");
	}
	else
	{
		print("Group has execute permission on directory: No\n");
	}
	print("\n");
	// checking other permissions on the directory

	if(dirstat.st_mode & S_IROTH)
	{
		print("Others has read permission on directory: Yes\n");
	}
	else
	{
		print("Others has read permission on directory: No\n");
	}
	if(dirstat.st_mode & S_IWOTH)
	{
		print("Others has write permission on directory: Yes\n");
	}
	else
	{
		print("Others has write permission on directory: No\n");
	}
	if(dirstat.st_mode & S_IXOTH)
	{
		print("Others has execute permission on directory: Yes\n");
	}
	else
	{
		print("Others has execute permission on directory: No\n");
	}
	print("\n");
	close(fd1);
	close(fd2);
	return 0;

}









