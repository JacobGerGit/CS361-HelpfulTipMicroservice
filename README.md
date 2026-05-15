# CS361-HelpfulTipMicroservice





### **Description of the Microservice:**



Using ZMQ, a context (socket container / manager) is created in order to create a socket, which is used to send and receive messages between programs. Once the socket is created, it is then bound to a specific PORT to listen for requests.



The microservice receives a list of helpful tips (minimum 2 unique items) from Unity as raw bytes (C# List -> Json -> bytes, then parsed back into Json on the microservice side and finally back into a list). random.choice from the random library is called on this list to select a random tip that is unique from the previous random tip to be returned as a Json string encoded as bytes again.





### **Required Packages:**



**Python**: json, random, pyzmq



pip install pyzmq



**import statements**:
import json

import random

import zmq



**Unity**: NuGet package manager, NetMQ, NewtonSoft



**using statements**:

using System.Collections.Generic;

using System;

using UnityEngine;

using TMPro;

using NetMQ;

using NetMQ.Sockets;

using Newtonsoft.Json.Linq;





### **Requesting Data:**



1. Create a request socket using NetMQ

Ex.
Declaration: private RequestSocket client;
In Awake(): client = new RequestSocket();

2. Connect to the same PORT as server

Ex.
Declaration: private const int PORT = 5555;
In Awake(): client.Connect($"tcp://127.0.0.1:{PORT}");

3. Create a list of string tips

Ex.
Declaration: private List<string> tips = new List<string>{"tip1","tip2","etc..."}

4. Using a helper class, wrap the list (so Unity's Json Utility can parse it) and convert to Json.

Ex.
In Awake(): listOfTipsAsJson = JsonUtility.ToJson(new TipListWrapper{tips = this.tips});
Helper Class:
\[System . Serializable]
public class TipListWrapper
{
public List<string> tips;
}



5. Send the Json string to the microservice

Ex.
In your GetTip() method: client.SendFrame(listOfTipsAsJson);





### **Receiving Data:**



1. Try to receive response from microservice.



&#x20;  Ex.

&#x20;  In GetTip() method: bool gotResponse = client.TryReceiveFrameString(TimeSpan.FromSeconds(2), out string responseAsJson);



&#x20;  If no response is received within 2 seconds, then the server/microservice/client has issues and needs debugging.

&#x20;  Otherwise,



2\. Parse from bytes to JObject.



&#x20;  Ex.

&#x20;  In GetTip() method: JObject parsedMessage = JObject.Parse(responseAsJson);



3\. Pull out the string value



&#x20;  Ex.

&#x20;  In GetTip() method: string serverTip = (string)parsedMessage\["tip"];



4\. Do work with your random string tip



&#x20;  Ex.

&#x20;  Declaration: \[SerializeField] private TextMeshProUGUI helpfulTipText; // Make sure you drag your TextMeshPro UI into the Unity inspector

&#x20;  In GetTip() method: helpfulTipText.text = serverTip;





### **UML sequence diagram:**



showing how requesting and receiving data works. Make it detailed enough that your teammates (and your grader) will understand.





### **Communication Contract:**



## **Communication Platform**

All team communication will be done through Discord. Important decisions, updates, and announcements must be posted in the main project channel so everyone can see them.



#### **Response Time Expectations**

Team members are expected to respond to messages within 24 hours. If unavailable, they should notify the team in advance.



#### **Unresponsive Member / Backup Plan**

If a team member is unresponsive for more than 72 hours without notice, their tasks will be reassigned to the rest of the team to avoid blocking progress.



#### **Meeting Participation**

Members are expected to attend scheduled meetings or notify the team ahead of time if they cannot attend. Key decisions will be summarized in Discord.



#### **Scope Control**

The team will prioritize completing core features first. Additional features or polish will only be added after core requirements are stable.



