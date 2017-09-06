#include<stdio.h>
#include<stdlib.h>
#include<unistd.h>
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
#include "parse.h"
#include "set.h"
#include "split.h"
void split(char command[])
{
    char *token,*temp;
    char *save1,*save2;
    token=strtok_r(command, ";",&save1);
    //printf("split command is %s\n",commandget1);
    while(token!=NULL)
    {
        //    printf("%s\n",token);
        temp=token;
        pid_t pid;
        int status;
        pid=fork();
        if(pid<0)
        {
          perror("ERROR in forking");
          //exit(1);
          exit(EXIT_FAILURE);
        }
        else
        {
          if(pid==0)
            purecom(token);
          else
          {
            if(amp!=1)
            {
                while(wait(&status) !=pid);
            }
          }

        }
        token=strtok_r(NULL,";",&save1);
      //  printf("while command is %s\n",commandget1);
    }
    //printf("split command is %s\n",commandget1);
}

