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
void prbash()
{
    struct utsname data;
    char s[100];
    int r=gethostname(s,100);
    if(r<0)
    {
        //ERROR HANDLING
        perror("Unable to get hostname");
        //exit(1);
        exit(EXIT_FAILURE);
    }
    r=uname(&data);
    if(r<0)
    {
        //ERROR HANDLING
        perror("Error in uname");
        //exit(1);
        exit(EXIT_FAILURE);
    }
    printf(ANSI_COLOR_RED"<"ANSI_COLOR_GREENY"%s"ANSI_COLOR_RESET"@"ANSI_COLOR_BLUE"%s:"ANSI_COLOR_YELLOW"~%s"ANSI_COLOR_RED">" ANSI_COLOR_RESET  ,s,data.sysname,presentdir);
    return ;
}
