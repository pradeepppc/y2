#include<stdio.h>
#include<errno.h>
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
#include "pw.h"
#include "cd.h"
#include "command.h"
#include "echo.h"
#include "global.h"
#include "ls.h"
#include "pinfo.h"
#include "printconsole.h"
#include "parse.h"
#include "set.h"
#include "split.h"
void cd(char *token)
{
    char newdir[100];
    token=strtok(NULL," \t");
    while(token!=NULL)
    {
        char temp[100];
        getcwd(temp,100);
        if(strcmp(token,"..")==0 ) {
        if(strcmp(temp,initialdir)!=0)
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
            int x = chdir(newdir);
            if(x == -1)
            {
                //error handling
                perror("ERROR");
                exit(1);
            }
        }}
        else
        {
            strcpy(newdir,temp);
            strcat(newdir,"/");
            strcat(newdir,token);
            int x = chdir(newdir);
            if(x == -1)
            {
                //error handling
                perror("ERROR");
                exit(1);
            }
        }


        setpath();
        token=strtok(NULL," \t");
    }
}
