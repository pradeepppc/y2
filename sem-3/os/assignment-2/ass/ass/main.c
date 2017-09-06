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

void  parse(char *line, char **argv)
{
  //printf("command is %s\n",line);
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

int main()
{
    strcpy(initialdir,getenv("PWD"));

    //    if(1)
    while(1)
    {
        amp=0;
        prbash();
        commandget=(char*)malloc(sizeof(char)*100);
        commandget1=(char*)malloc(sizeof(char)*100);
        scanf(" %[^\n]s",commandget);
      //  printf("command is %s\n",commandget);
        strcpy(commandget1,commandget);
        if(commandget[strlen(commandget)-1] == '&')
        {
            amp=1;
            commandget[strlen(commandget)-1] = 0;
        }

        split(commandget);
        free(commandget);
    }
    return 0;
}
