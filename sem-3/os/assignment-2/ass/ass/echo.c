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
#include "global.c"
void echo(char *token)
{
  char *temp;
  char *t;
    char str1[1];
    str1[0]=34;

    token=strtok(NULL,str1);

    while(token!=NULL)
    {
      printf("token is %s\n",token);
      t=strtok(token," \t'");
      while(t!=NULL){
        if(t[0] == '$')
        {
          temp=(char*)malloc(sizeof(char)*100);
            strcpy(temp,t+1);
            temp=getenv(temp);
            printf("%s ",temp);
        }
        else
        {
            printf("%s ",t);
        }
        t=strtok(NULL," \t'");
        }
        token=strtok(NULL,str1);

    }
    printf("\n");
}
