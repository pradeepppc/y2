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
