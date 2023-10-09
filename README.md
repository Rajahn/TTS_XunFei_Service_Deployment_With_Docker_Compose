
# **TTS Service Deployment with Docker Compose**
![image](https://github.com/Rajahn/TTS_XunFei_Service_Deployment_With_Docker_Compose/assets/39303094/100198b9-dddb-4ef2-bf3e-dc11163d1b31)


## **1. Overview**

We have set up a deployment process based on Docker Compose to deploy and manage the TTS service and its related components. The primary components are **`tts_xunfei`** and **`dispatcher`**.

The motivation behind deploying in a cluster is to enhance the concurrency of the TTS model. A single TTS model accepts a piece of text and returns the generated audio. 

This process is blocking and is not conducive for other services to invoke. By adopting a cluster deployment approach, we can handle multiple requests simultaneously, thus enhancing throughput and responsiveness.

This project is just an example, since the xunfei service doesn't actually have concurrency issues, but it's for our own trained tts model, which simply need implements the tts_api interface, inputs the text, and generates and returns the binary data for the audio. 

## **2. `tts_xunfei`**

### **Functionality**

**`tts_xunfei`** is a Text-to-Speech (TTS) service offering two HTTP endpoints:

1. **`POST /tts`**: Generates audio from the provided text. This method returns the audio in binary data of a mp3 file.
2. **`GET /check_tts_status`**: Checks the current status of the TTS service to see if it's occupied.

### **Dockerization**

To ensure ease of deployment and scalability, we have containerized the service into a Docker container.

## **3. `dispatcher`**

### **Functionality**

Since we aim to run multiple **`tts_xunfei`** instances and balance the requests among them, we introduced **`dispatcher`**. Its role is to:

1. Receive TTS requests from clients.
2. Check the status of all **`tts_xunfei`** instances.
3. Redirect the request to an available **`tts_xunfei`** instance.

### **Dockerization**

Similar to **`tts_xunfei`**, for ease of deployment and scalability, we have also containerized **`dispatcher`** into a Docker container.

## **4. Managing Deployment with Docker Compose**

Docker Compose allows us to define and run multi-container applications using a single YAML file. Our **`docker-compose.yml`** file defines the following services:

1. Multiple **`tts_xunfei`** instances.
2. One **`dispatcher`** instance.

With a simple **`docker-compose up`** command, all these services will start and interconnect with each other. 
![image](https://github.com/Rajahn/TTS_XunFei_Service_Deployment_With_Docker_Compose/assets/39303094/ca67f98f-8df4-4771-89ec-1785dfb23cc3)

And check docker desktop for status
![image](https://github.com/Rajahn/TTS_XunFei_Service_Deployment_With_Docker_Compose/assets/39303094/c06966b0-0d6e-45f6-966a-06f1bf3bc1fc)




