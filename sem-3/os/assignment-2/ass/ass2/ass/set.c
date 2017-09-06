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

