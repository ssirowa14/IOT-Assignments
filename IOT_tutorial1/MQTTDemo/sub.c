#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "MQTTClient.h"
#define ADDRESS     "tcp://localhost:1883"
#define CLIENTID    "ExampleClientSub"
#define TOPIC       "Temperature"
#define TOPIC2		"Humidity"
#define PAYLOAD     "Hello World!"
#define QOS         1
#define TIMEOUT     10000L
volatile MQTTClient_deliveryToken deliveredtoken;
long temp=0, humid=0;
void delivered(void *context, MQTTClient_deliveryToken dt)
{
    printf("Message with token value %d delivery confirmed\n", dt);
    deliveredtoken = dt;
}
int msgarrvd(void *context, char *topicName, int topicLen, MQTTClient_message *message)
{
    int i;
    char* payloadptr;
    printf("Message arrived\n");
    printf("     topic: %s\n", topicName);
    printf("   message: ");
    payloadptr = message->payload;
    for(i=0; i<message->payloadlen; i++)
    {
        putchar(*payloadptr++);
    }
    payloadptr = message->payload;
    int var = 0;
    for(int i=0; payloadptr[i] != '\0'; i++){
    	var = var*10 + payloadptr[i]-'0';
    }
    putchar('\n');
    printf("Parsed Integer: %d\n", var);
    if(!strcmp("Temperature", topicName)){
    	temp = var;
    	if(temp > 28){
    		printf("AC Switched ON\n");
    	}
    	else if(temp <=23){
    		printf("AC Switched OFF\n");
    	}
    }
    else if(!strcmp("Humidity", topicName)){
    	humid = var;
    	if(humid > 50){
    		printf("AC Switched ON\n");
    	}
    	else if(humid >=40 && temp >= 24){
    		printf("AC Switched ON\n");
    	}
    }
    MQTTClient_freeMessage(&message);
    MQTTClient_free(topicName);
    return 1;
}
void connlost(void *context, char *cause)
{
    printf("\nConnection lost\n");
    printf("     cause: %s\n", cause);
}
int main(int argc, char* argv[])
{
    MQTTClient client;
    MQTTClient_connectOptions conn_opts = MQTTClient_connectOptions_initializer;
    int rc;
    int ch;
    MQTTClient_create(&client, ADDRESS, CLIENTID,
        MQTTCLIENT_PERSISTENCE_NONE, NULL);
    conn_opts.keepAliveInterval = 20;
    conn_opts.cleansession = 1;
    MQTTClient_setCallbacks(client, NULL, connlost, msgarrvd, delivered);
    if ((rc = MQTTClient_connect(client, &conn_opts)) != MQTTCLIENT_SUCCESS)
    {
        printf("Failed to connect, return code %d\n", rc);
        exit(EXIT_FAILURE);
    }
    printf("Subscribing to topic %s\nfor client %s using QoS%d\n\n"
           "Press Q<Enter> to quit\n\n", TOPIC, CLIENTID, QOS);
    MQTTClient_subscribe(client, TOPIC, QOS);
    MQTTClient_subscribe(client, TOPIC2, QOS);
    do
    {
        ch = getchar();
    } while(ch!='Q' && ch != 'q');
    MQTTClient_disconnect(client, 10000);
    MQTTClient_destroy(&client);
    return rc;
}