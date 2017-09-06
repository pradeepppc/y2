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
#define ANSI_COLOR_RED     "\x1b[31m"
#define ANSI_COLOR_GREEN   "\x1b[32m"
#define ANSI_COLOR_YELLOW  "\x1b[33m"
#define ANSI_COLOR_BLUE    "\x1b[34m"
#define ANSI_COLOR_MAGENTA "\x1b[35m"
#define ANSI_COLOR_CYAN    "\x1b[36m"
#define ANSI_COLOR_RESET   "\x1b[0m"
void dump_tm (struct tm *t);
char initialdir[100];
char presentdir[100]={0};
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
void cd(char *token)
{
	char newdir[100];
	token=strtok(NULL," ");
	while(token!=NULL)
	{
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
void ls2(char *tok)
{
	int flag = 0;
	//char *kog  = tok;
	//comment 
	//kog = strtok(NULL," ");
	//comment
	if(strcmp(tok,"-l") == 0)
	{
		flag = 1;
	}//comment
	else if((strcmp(tok,"-la") == 0) || (strcmp(tok,"-al") == 0)) //comment
	{
		flag = 2;
	}
	tok = strtok(NULL," ");
	if(tok == NULL)
	{
		//pass
	}
	else if(strcmp(tok,"-a") == 0)
	{
	flag = 2;
		}
	else
	{
		flag = 3;
	}


	if (flag == 1 || flag == 2)
	{
		char temp[100];
		char buf[512];
		getcwd(temp,100);
		DIR *pointdir = opendir(temp);
		struct dirent *file;
		struct stat fileStat;


		while((file = readdir(pointdir)) != NULL)
		{
			char str[255];
			strncpy(str,file->d_name,254);
			str[254] = '\0';

			if((str[0] == '.') && (flag == 1))
			{
				// dont print in ls
			}
			else{

				sprintf(buf, "%s/%s",temp,file->d_name);
				stat(buf,&fileStat);
				char time_str[100] = "";
				struct passwd *pw = getpwuid(fileStat.st_uid);
				struct group  *gr = getgrgid(fileStat.st_gid);
				time_t now = time (NULL);
				struct tm tmfile, tmnow;
				localtime_r(&fileStat.st_mtime,&tmfile);    /* get struct tm for file */
				localtime_r(&now, &tmnow);


				printf( (S_ISDIR(fileStat.st_mode)) ? "d" : "-");
				printf( (fileStat.st_mode & S_IRUSR) ? "r" : "-");
				printf( (fileStat.st_mode & S_IWUSR) ? "w" : "-");
				printf( (fileStat.st_mode & S_IXUSR) ? "x" : "-");
				printf( (fileStat.st_mode & S_IRGRP) ? "r" : "-");
				printf( (fileStat.st_mode & S_IWGRP) ? "w" : "-");
				printf( (fileStat.st_mode & S_IXGRP) ? "x" : "-");
				printf( (fileStat.st_mode & S_IROTH) ? "r" : "-");
				printf( (fileStat.st_mode & S_IWOTH) ? "w" : "-");
				printf( (fileStat.st_mode & S_IXOTH) ? "x" : "-");
				printf(" ");
				printf("%s ",pw->pw_name);
				printf("%s ",gr->gr_name);
				printf("%d ",fileStat.st_nlink);
				printf("%d ",fileStat.st_size);
				if (tmfile.tm_year == tmnow.tm_year) {    /* compare year values  */
					strftime (time_str, sizeof (time_str), "%b %e %H:%M",
							&tmfile);   /* if year is current output date/time  */
					printf ("%s ",time_str);
				}
				else { /* if year is not current, output time/year */
					strftime (time_str, sizeof (time_str), "%b %e  %Y",
							&tmfile);
					printf ("%s ",time_str);
				}

				if(S_ISREG(fileStat.st_mode))
				{
					printf(ANSI_COLOR_GREEN "%s" ANSI_COLOR_RESET "\n",str);
				}
				else if(S_ISDIR(fileStat.st_mode))
				{

					printf(ANSI_COLOR_BLUE "%s" ANSI_COLOR_RESET "\n",str);
				}
				else
				{

					printf("%s\n",str);
				}

			}

		}	
		closedir(pointdir);

	}
	else if(flag == 3)
	{
		// yet to be written
		struct stat file;
		stat(tok,&file);
		if(S_ISREG(file.st_mode))
		{
			printf(ANSI_COLOR_GREEN "%s" ANSI_COLOR_RESET "\n",tok);
		}
		else if(S_ISDIR(file.st_mode))
		{

			printf(ANSI_COLOR_BLUE "%s" ANSI_COLOR_RESET "\n",tok);

		}
		else
		{
			printf("error file doesnt exist\n");
		}

	}

	return;

}
void ls(char *token)
{	
	char *tok = token;
	int flag = 0;
	tok = strtok(NULL," ");
	if(tok == NULL)
	{
		flag = 1;
	}
	else if(strcmp(tok,"-a") == 0)
	{
		flag = 2;
	}
	else if((strcmp(tok,"-l")==0) || (strcmp(tok,"-la") == 0) || (strcmp(tok,"-al") == 0))
	{
		//call ls -la or ls -l
		ls2(tok);
	}
	else{
		// yet to write
		flag = 3;
	}

	if(flag == 1 || flag == 2)
	{
		char temp[100];
		char buf[512];
		getcwd(temp,100);
		DIR *pointdir = opendir(temp);
		struct dirent *file;
		//struct stat filestat;

		while((file = readdir(pointdir)) != NULL)
		{
			char str[255];
			strncpy(str,file->d_name,254);
			str[254] = '\0';

			if((str[0] == '.') && (flag == 1))
			{
				// dont print in ls
			}
			else{
				struct stat filestat;
				stat(str,&filestat);

				if(S_ISREG(filestat.st_mode))
				{
					printf(ANSI_COLOR_GREEN "%s" ANSI_COLOR_RESET "\n",str);
				}
				else if(S_ISDIR(filestat.st_mode))
				{

					printf(ANSI_COLOR_BLUE "%s" ANSI_COLOR_RESET "\n",str);
				}
				else
				{
					printf("error file doesnt exist\n");
				}


			}
		} 
		closedir(pointdir);
	}
	else if(flag == 3)
	{
		//int fd = open(tok,O_RDWR);
		struct stat fff;
		stat(tok,&fff);
		if(S_ISREG(fff.st_mode))
			        {
					        printf(ANSI_COLOR_GREEN "%s" ANSI_COLOR_RESET "\n",tok);
						                        }
		        else if(S_ISDIR(fff.st_mode))
				        {

						        printf(ANSI_COLOR_BLUE "%s" ANSI_COLOR_RESET "\n",tok);
							                }
			        else
					        {
							                printf("error file doesnt exist\n");
									                }

		//print that file name if exist
	}
	return;

}
void pwd()
{
	printf("~%s\n",presentdir);
}
void purecom(char command[])
{
	char *token;
	token=strtok(command," ");
	if(strcmp(token,"cd")==0)
	{
		//call cd()
		cd(token);
	}
	else if(strcmp(token,"pwd")==0)
	{
		pwd();
	}
	else if(strcmp(token,"echo")==0)
	{
		while(token!=NULL)
		{
			//      printf("sub %s\n",token);
			token=strtok(NULL," ");
		}
	}
	else if(strcmp(token,"ls") == 0)
	{	
		//call ls
		ls(token);

	}
	else if(strcmp(token,"exit") == 0)
	{
		// exit
		exit(1);	
	}

}
void split(char command[])
{
	char *token,*subtoken,*temp;
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
int main()
{
	strcpy(initialdir,getenv("PWD"));
	char *command;
	//    if(1)
	while(1)
	{
		prbash();
		command=(char*)malloc(sizeof(char)*100);
		scanf(" %[^\n]s",command);
		split(command);
		free(command);
	}
	return 0;
}
