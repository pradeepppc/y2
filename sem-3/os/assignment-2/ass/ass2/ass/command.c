#include<stdio.h>
#include<stdlib.h>
#include<errno.h>
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
void purecom(char command[])
{
    char *token;
    token=strtok(command," \t");
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
        exit(EXIT_FAILURE);
    }
    else if(strcmp(token,"pinfo") == 0)
    {
      pinfo(token);
    }
    else
    {
        char *argv[100];
        //printf("purecom command is %s\n",commandget1);
        parse(commandget1,argv);
            //child process
        if(execvp(argv[0],argv)<0)
        {
          perror("ERROR :exec failed");
          //exit(1);
          exit(EXIT_FAILURE);
        }
    }


}
