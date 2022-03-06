#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <MQTTClient.h>
#include <unistd.h>
#include <time.h>
#define ADDRESS     "tcp://localhost:1883"
#define CLIENTID    "ExampleClientPub1"
#define TOPIC       "Temperature"
// #define PAYLOAD     "Hello World!"
#define QOS         1
#define TIMEOUT     10000L
volatile MQTTClient_deliveryToken deliveredtoken;
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
    payloadptr = (char*) message->payload;
    for(i=0; i<message->payloadlen; i++)
    {
        putchar(*payloadptr++);
    }
    putchar('\n');
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
    MQTTClient_message pubmsg = MQTTClient_message_initializer;
    MQTTClient_deliveryToken token;
    int rc;
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
    srand(time(0));
    int upper = 35;
    int lower = 15;
    while(1){
        int var = (rand() % (upper - lower + 1)) + lower;
        char PAYLOAD[64];
        sprintf(PAYLOAD, "%d", var);
        printf("\nRandom Integer: %s\n", PAYLOAD);
        pubmsg.payload = (void*) PAYLOAD;
        pubmsg.payloadlen = strlen(PAYLOAD);
        pubmsg.qos = QOS;
        pubmsg.retained = 0;
        deliveredtoken = 0;
        MQTTClient_publishMessage(client, TOPIC, &pubmsg, &token);
        printf("Waiting for publication of %s\n"
                "on topic %s for client with ClientID: %s\n",
                PAYLOAD, TOPIC, CLIENTID);
        sleep(3);
    }
    while(deliveredtoken != token);
    MQTTClient_disconnect(client, 10000);
    MQTTClient_destroy(&client);
    return rc;
}