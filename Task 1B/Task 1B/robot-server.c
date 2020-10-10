/*
*****************************************************************************************
*
*        		===============================================
*           		Rapid Rescuer (RR) Theme (eYRC 2019-20)
*        		===============================================
*
*  This script is to implement Task 1B of Rapid Rescuer (RR) Theme (eYRC 2019-20).
*  
*  This software is made available on an "AS IS WHERE IS BASIS".
*  Licensee/end user indemnifies and will keep e-Yantra indemnified from
*  any and all claim(s) that emanate from the use of the Software or 
*  breach of the terms of this agreement.
*  
*  e-Yantra - An MHRD project under National Mission on Education using ICT (NMEICT)
*
*****************************************************************************************
*/

/*
* Team ID:			[ Team-ID ]
* Author List:		[ Names of team members worked on this file separated by Comma: Name1, Name2, ... ]
* Filename:			task_1a.py
* Functions:		readImage, solveMaze
* 					[ Comma separated list of functions in this file ]
* Global variables:	CELL_SIZE
* 					[ List of global variables defined in this file ]
*/


// Include necessary header files
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h> 
#include <arpa/inet.h>


// Constants defined
#define SERVER_PORT 3333
#define RX_BUFFER_SIZE 1024
#define TX_BUFFER_SIZE 1024

#define MAXCHAR 1000				// max characters to read from txt file

// Global variables
struct sockaddr_in dest_addr;
struct sockaddr_in source_addr;

char rx_buffer[RX_BUFFER_SIZE];		// buffer to store data from client
char tx_buffer[RX_BUFFER_SIZE];		// buffer to store data to be sent to client

char ipv4_addr_str[128];			// buffer to store IPv4 addresses as string
char ipv4_addr_str_client[128];		// buffer to store IPv4 addresses as string

int listen_sock,count=0,k=0,p=0,l=0;

char line_data[MAXCHAR];

FILE *input_fp, *output_fp;


/*
* Function Name:	socket_create
* Inputs:			dest_addr [ structure type for destination address ]
* 					source_addr [ structure type for source address ]
* Outputs: 			my_sock [ socket value, if connection is properly created ]
* Purpose: 			the function creates the socket connection with the server
* Example call: 	int sock = socket_create(dest_addr, source_addr);
*/
int socket_create(struct sockaddr_in dest_addr, struct sockaddr_in source_addr){

	int addr_family;
	int ip_protocol;

	dest_addr.sin_addr.s_addr = htonl(INADDR_ANY);
	dest_addr.sin_family = AF_INET;
	dest_addr.sin_port = htons(SERVER_PORT);
	addr_family = AF_INET;
	ip_protocol = IPPROTO_IP;

	int my_sock,sock,clilen;

	sock=socket(AF_INET,SOCK_STREAM,IPPROTO_IP);
	if(bind(sock , (struct sockaddr *) &dest_addr,sizeof(dest_addr))<0)
        {
        	printf("Binding Failed.");
        }
        
        else
        {
        	printf("Socket binded with port\n");
        }
        
        //lisetning
        
        listen(sock , 5);
        
        
        //accepting the connections
        
        clilen=sizeof(source_addr);
        my_sock=accept(sock , (struct sockaddr *) &source_addr,&clilen);
        if(my_sock<0)
        {
        	printf("Error establishing connection");
        }
        else
        {
        	printf("Connection established\n");
        }

	return my_sock;
}


/*
* Function Name:	receive_from_send_to_client
* Inputs:			sock [ socket value, if connection is properly created ]
* Outputs: 			None
* Purpose: 			the function receives the data from server and updates the 'rx_buffer'
*					variable with it, sends the obstacle position based on obstacle_pos.txt
*					file and sends this information to the client in the provided format.
* Example call: 	receive_from_send_to_client(sock);
*/
int receive_from_send_to_client(int sock){
	int i1,line;
       //Reading th message from client
	bzero(rx_buffer,RX_BUFFER_SIZE);
	i1=read(sock,rx_buffer,RX_BUFFER_SIZE);
	count=count+1;
	if(i1<0)
	{
		printf("Error on reading");
	}
	
	int file_num;
	file_num=(rx_buffer[0]-'0');
	
	if(file_num>0)	
	{
	while(file_num==l+1 && count==1 && file_num!=line_data[0]-'0')	
	{	
		fgets(line_data, MAXCHAR, input_fp);
		fgets(line_data, MAXCHAR, input_fp);
		l++;
	}
	}
	if(file_num!=line_data[0]-'0')
	l=l+1;
	char buffer[10][50];
	
	int x[100];
	int y[100];
	for(int i=0; i<100 ; i++)
	x[i] = 0,y[i] = 0;
	
	int j = 0;
	int i = 4;
	k=0;

	if(file_num==line_data[0]-'0'){
	while(i<strlen(line_data) && line_data[i]){
		while(line_data[i] != ',')
			x[j] = x[j]*10 + line_data[i++] - '0';
		i++;
		while(line_data[i] != ')')
			y[j] = y[j] * 10 + line_data[i++] - '0';
		i += 4;
		
		
		sprintf(buffer[k],"@(%d,%d)@",x[j],y[j]);
		k=k+1;
		j++;
	}
	}
	sprintf(buffer[k],"@%s@","$");
	k=k+1;
	//Sending a message to client
	bzero(tx_buffer,TX_BUFFER_SIZE);
	strncpy(tx_buffer,buffer[count-1],100);
	i1=write(sock,tx_buffer,strlen(tx_buffer));
	if(i1<0)
	{
		printf("Error on writing");
	}
	
	if(count==k)
	{
		
		count=0;
		k=0;
	}

	return 0;

}


int main() {

    char *input_file_name = "obstacle_pos.txt";
	char *output_file_name = "data_from_client.txt";

	// Create socket and accept connection from client
	int sock = socket_create(dest_addr, source_addr);

	input_fp = fopen(input_file_name, "r");

	if (input_fp == NULL){
		printf("Could not open file %s\n",input_file_name);
		return 1;
	}

	fgets(line_data, MAXCHAR, input_fp);
	
	output_fp = fopen(output_file_name, "w");

	if (output_fp == NULL){
		printf("Could not open file %s\n",output_file_name);
		return 1;
	}

	while (1) {

		// Receive and send data from client and get the new shortest path
		receive_from_send_to_client(sock);
		// NOTE: YOU ARE NOT ALLOWED TO MAKE ANY CHANGE HERE
		fputs(rx_buffer, output_fp);
		fputs("\n", output_fp);
		

	}

	return 0;
}

