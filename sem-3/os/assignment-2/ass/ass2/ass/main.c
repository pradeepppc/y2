
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







int main()
{
    strcpy(initialdir,getenv("PWD"));
	presentdir[0]=0;
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
