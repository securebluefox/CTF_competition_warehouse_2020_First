#include <string.h>
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>

#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <sys/types.h>
#include <sys/wait.h>

#define RANDOM "/dev/urandom"
#define SIZE  8
#define ESIZE 10

static const char en85[] = {
	'0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
	'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J',
	'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
	'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd',
       	'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 
	'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 
	'y', 'z', '!', '#', '$', '%', '&', '(', ')', '*', 
	'+', '-', ';', '<', '=', '>', '?', '@', '^', '_',
	'`', '{', '|', '}', '~'
};

void encode_85(char *buf, int *out_bytes, const unsigned char *data, int bytes)
{
  *out_bytes = 0;
  while (bytes) {
    unsigned acc = 0;
    int cnt;
    for (cnt = 24; cnt >= 0; cnt -= 8) {
      unsigned ch = *data++;
      acc |= ch << cnt;
      if (--bytes == 0)
        break;
    }
    for (cnt = 4; cnt >= 0; cnt--) {
      int val = acc % 85;
      acc /= 85;
      buf[cnt] = en85[val];
    }
    buf += 5;
    *out_bytes += 5;
  }
  *buf = 0;
}

int perform_challenge(int sock) {
  int result;
  unsigned char rand[SIZE];
  unsigned char buff[64] = { 0 };

  char * why85 = NULL;
  why85 = malloc((SIZE * 5) / 4);
  if (why85 == NULL)
  {
    printf("unable to allocate memory!\n");
    return -1;
  }

  FILE * f = fopen(RANDOM, "r");
  if (f == NULL) 
  {
    printf("unable to open random ...\n");
    return -1;
  }

  result = fread(rand, 1, SIZE, f);
  if (result != SIZE) 
  {
    printf("unable to read proper # of bytes\n");
    return -1;
  }

  int outlen = 0;
  encode_85(why85, &outlen, rand, SIZE);
  if (outlen != (SIZE * 5)/4)
  {
    printf("encoding error!\n");
    return -1;
  }

  printf("solution: %s\n", why85);
  send(sock, "Guess the random number!\n", strlen("Guess the random number!\n"), 0);

  while (1) 
  {
    int res = recv(sock, buff, 64, 0);
    
    if (res <= 0) 
    {
      printf("Unable to read input!\n");
      return -1;
    }

    else 
    {
      printf("Received: %s vs Have: %s\n", buff, why85);
      int i;
      for (i = 0; i < ESIZE; i++)
      {
	// If the passwords don't match, no point in continuing. 
        if ((int)buff[i] != (int)why85[i])
          break;
	sleep(1); // easy way to prevent brute force attacks 
      }

      if (i == ESIZE) 
      {
	#ifdef FLAG
	send(sock, FLAG, strlen(FLAG), 0);
	#else
        send(sock, "Wow, you did it!, now try it on the server!\n", 
	     strlen("Wow, you did it!, now try it on the server!\n"), 0);
	#endif
	return 0;
      }

      else
      {
        send(sock, "Better luck next time!\n", 
	     strlen("Better luck next time!\n"), 0);
      }
    }
  }
}

int main(int argc, char * argv) {
  int serverSocket, newSocket;
  struct sockaddr_in serverAddr;
  struct sockaddr_storage serverStorage;
  socklen_t addr_size;
  pid_t pid[50];

  //Create the socket. 
  serverSocket = socket(PF_INET, SOCK_STREAM, 0);
  serverAddr.sin_family = AF_INET;
  serverAddr.sin_port = htons(7799);
  serverAddr.sin_addr.s_addr = INADDR_ANY;
  
  memset(serverAddr.sin_zero, '\0', sizeof(serverAddr.sin_zero));
  bind(serverSocket, (struct sockaddr *) &serverAddr, sizeof(serverAddr));

  if(listen(serverSocket,50)==0)
    printf("Listening\n");
  else
    printf("Error\n");

  pthread_t tid[60];
  int i = 0;

  while(1)
    {
      addr_size = sizeof(serverStorage);
      newSocket = accept(serverSocket, (struct sockaddr *) &serverStorage, &addr_size);
      int pid_c = 0;
      
      if ((pid_c = fork())==0) 
      {
        perform_challenge(newSocket);
        close(newSocket);
      }
      else
      {
        pid[i++] = pid_c;
        if( i >= 49)
        {
          i = 0;
          while(i < 50)
            waitpid(pid[i++], NULL, 0);
          i = 0;
        }
      }
    }

  return 0;
}
