
#include<unistd.h>
#include<stdlib.h>
#include<errno.h>
#include<string.h>
#include<dirent.h>
#include<sys/types.h>
#include<sys/stat.h>
#include<fcntl.h>
#include <sys/utsname.h>
#include<time.h>
#include<pwd.h>
#include<grp.h>
#include "pw.h"
#include "cd.h"
#include "command.h"
#include "echo.h"
#include "global.h"
#include "ls.h"
#include "pinfo.h"
#include "printconsole.h"
#include<stdio.h>
#include "parse.h"
#include "set.h"
#include "split.h"
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
                                perror("ERROR");
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
                                perror("ERROR");

			//printf(ANSI_COLOR_BLUE "%s" ANSI_COLOR_RESET "\n",tok);

		}
		else
		{
			perror("ERROR");
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
					printf("ERROR");
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
				printf("ERROR");
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
			perror("ERROR");
		}
		//print that file name if exist
	}
	return;

}
