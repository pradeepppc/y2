all :
	gcc -c pinfo.c -o pinfo.o
	gcc -c printconsole.c -o printconsole.o
	gcc -c pw.c -o pw.o
	gcc -c cd.c -o cd.o
	gcc -c command.c -o command.o
	gcc -c echo.c -o echo.o
	gcc -c global.c -o global.o
	gcc -c ls.c -o ls.o
	gcc -c main.c -o main.o

	gcc *.o -o run
clean :
	rm -r *.o
	
