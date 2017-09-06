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
void ls2(char *tok)
{
	int flag = 0;
	int flag1 = 0;
	if(strcmp(tok,"-l") == 0)
	{
		flag = 1;
	}
	else if((strcmp(tok,"-la") == 0) || (strcmp(tok,"-al") == 0))
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
		if(flag == 1)
			flag1 = 1;
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
		int total = 0;

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
				printf("%lu ",fileStat.st_nlink);
				printf("%s ",pw->pw_name);
				printf("%s ",gr->gr_name);
				//printf("%lu ",fileStat.st_nlink);
				printf("%ld ",fileStat.st_size);
				
				total = total + (int)(fileStat.st_size/1024);
				
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
			printf("total %d\n",total);

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
			char def[500];
                        char com[500];
                        getcwd(def,400);
                        strcat(def,"/");
                        strcat(def,tok);
                        //printf("%s\n",def);
                        int x = chdir(def);
                        //printf("after\n");
                        if(x < 0)
                                printf("error\n");
			if(flag1 == 1)
                        strcpy(com,"ls -l");
			else
				strcpy(com,"ls -la");
                        char * t;
                        t = strtok(com," ");
			t = strtok(NULL," ");
                        ls2(t);
                        int r = chdir("..");
                        if(r < 0)
                                printf("error\n");

			//printf(ANSI_COLOR_BLUE "%s" ANSI_COLOR_RESET "\n",tok);

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
		tok = strtok(NULL," ");
		if(strcmp(tok,"-l") == 0)
		{
		char b[4];
		char *po;
		strcpy(b,"-la");
		po = strtok(b," ");
		ls2(po);
		return;
			}
	}
	else if((strcmp(tok,"-l")==0) || (strcmp(tok,"-la") == 0) || (strcmp(tok,"-al") == 0))
	{
		//call ls -la or ls -l
		ls2(tok);
	}
	else{
		// yet to write
		flag = 3;
		//printf("flag3\n");
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
		struct stat fff;
		stat(tok,&fff);
		if(S_ISREG(fff.st_mode))
		{
			printf(ANSI_COLOR_GREEN "%s" ANSI_COLOR_RESET "\n",tok);
		}
		else if(S_ISDIR(fff.st_mode))
		{
			
			char def[500];
			char com[500];
			getcwd(def,400);
			strcat(def,"/");
			strcat(def,tok);
			//printf("%s\n",def);
			int x = chdir(def);
			//printf("after\n");
			if(x < 0)
				printf("error\n");
			strcpy(com,"ls");
			char * t;
			t = strtok(com," ");
			ls(t);
			int r = chdir("..");
			if(r < 0)
				printf("error\n");
			//getcwd(def,400);
			//printf("%s\n",def);
			//printf(ANSI_COLOR_BLUE "%s" ANSI_COLOR_RESET "\n",tok);
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
void  parse(char *line, char **argv)
{
	while (*line != '\0') {       /* if not the end of line ....... */
		while (*line == ' ' || *line == '\t' || *line == '\n')
			*line++ = '\0';     /* replace white spaces with 0    */
		*argv++ = line;          /* save the argument position     */
		while (*line != '\0' && *line != ' ' &&
				*line != '\t' && *line != '\n')
			line++;             /* skip the argument until ...    */
	}
	*argv = '\0';                 /* mark the end of argument list  */
}
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