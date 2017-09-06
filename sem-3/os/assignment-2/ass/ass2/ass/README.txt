First we take the command as input in the form of string and tokenize it .
Then according to the commands first we create child process with fork
If there is no & in the end of the command then parent will wait until the child process is done .




Directory Structure

.
├── cd.c
├── cd.h
├── command.c
├── command.h
├── echo.c
├── echo.h
├── global.c
├── global.h
├── ls.c
├── ls.h
├── main.c
├── main.h
├── makefile
├── parse.c
├── parse.h
├── pinfo.c
├── pinfo.h
├── printconsole.
├── printconsole.c
├── printconsole.h
├── pw.c
├── pw.h
├── README.txt
├── run
├── set.c
├── set.h
├── split.c
└── split.h

To Execute:

1) Run "make" command .
2) run "./run" the shell will appear.
