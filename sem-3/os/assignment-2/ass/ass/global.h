#ifndef GLOBAL
#define GLOBAL
void dump_tm (struct tm *t);
char initialdir[100];
char presentdir[100]={0};
char *commandget,*commandget1;
int amp;
#define ANSI_COLOR_RED     "\x1b[31m"
#define ANSI_COLOR_GREENY   "\x1b[32m"
#define ANSI_COLOR_GREEN   "\x1b[0m"
#define ANSI_COLOR_YELLOW  "\x1b[33m"
#define ANSI_COLOR_BLUE    "\x1b[34m"
#define ANSI_COLOR_MAGENTA "\x1b[35m"
#define ANSI_COLOR_CYAN    "\x1b[36m"
#define ANSI_COLOR_RESET   "\x1b[0m"
#endif
