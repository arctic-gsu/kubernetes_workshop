# Kubernetes:

Contents:
1. What is container? What is kubernetes? Feature of Kubernetes
2. Kubernetes Architecture
3. Master node and Worker Node
4. Master components and Worker components
5. Docker basics
6. Containerizing our application
7. Two container one host communication, using docker compose - two different services communication
8. Using docker image in kubernetes: kubectl
9. Setup for kubeadmin
10. Workflow of a Pod
11. Multiple container in single pod
12. Creating a ML Porject and Deploying in kubernetes

## What is container? What is kubernetes? Feature of Kubernetes

### What is container?
A container is a lightweight package that contains an application's code, libraries, configuration files, and dependencies.
### What is Kubernetes?
- Open source container orchestration framework, developed by google </br>
- Manages containers, i.e. help manage application with 100-1000's of containers with various environments </br>

#### What problems does kubernetes solve? What are the task of an orchestration tool?

Rise of microservices caused rise of container technologies. Managing those containers across multiple environment is difficult, so these needs container orchestration technologies. </br>
<img src="https://github.com/arctic-gsu/kubernetes_workshop/assets/33342277/c3fa43b1-916e-4e89-896f-ad06871c8a8c" width="300">

### Features:
1. High availability or no downtime
2. Scalibility or high performance
3. Disaster recovery - backup and restore - server explode, data missing, then this system must have some technology to store its latest snapshot

## Kubernetes Architecture
- It has atleast one master node and other are worker nodes </br>
- Worker nodes has kubelet process, which makes it possible for cluster to communicate and run application processes </br>
- Workers have different number of containers </br>
- Worker node is where your services are running
- Master node runs several kubernetes processes that are absolutely necessary for running kubernetes clusters properly

Figure showing Kubernetes Cluster Architecture
![Screenshot 2024-03-20 at 11 06 45 AM](https://github.com/arctic-gsu/kubernetes_workshop/assets/33342277/2e001376-e22c-472a-b701-714b249dfef2)

## Master node and Worker Node</br>

### Master components:</br>
Master node runs several kubernetes processes, that are essential for managing and running kubernetes cluster.
Master node doesnot need many resources as compared to worker nodes because they are handling only handful functions. The master node consists of following:

##### Kube API Server:</br>
- API is entry point to kubernetes cluster</br>
- Primary management component of k8s</br>
- Orchestrates all operations within a cluster</br>
- API Server is like gatekeeper, which is trying to understand status of server, i.e. worker nodes can know the status of the server from API server
- KubeAPI server fetches periodic report from kubelet to monitor status of nodes and containers in them

##### Controllers: </br>
- Controller manager - manages all these controllers, Keeps account of what is happening in the cluster, whether something needs to be repaired or maybe container dies and has to be restarted </br>
- Node Controllers - Takes care of Nodes, responsible for onboarding new nodes on a cluster, availability of nodes</br>
- Replica controller - ensures container are running at all times</br>

##### Kube Scheduler: </br>
- Identifies right node to place a container, based on container resource requirement, also looks at policy and contraints, tolerations etc</br>
  
##### ETCD Cluster</br>
- Its a Databse under master node. High availability key value store. Holds the current state of the kubernetes cluster. Backup is made from these etcd snapshots.</br>

#### Virtual network </br>
- enables worker node, master node communication </br>


Check components of master node
```
hpcshruti@k8s-ctrls04:~$ kubectl get componentstatus
Warning: v1 ComponentStatus is deprecated in v1.19+
NAME                 STATUS    MESSAGE                         ERROR
scheduler            Healthy   ok                              
controller-manager   Healthy   ok                              
etcd-0               Healthy   {"health":"true","reason":""}   
```

### Worker components:
- Manages all activities, have higher workloads, acutally are much bigger and have more resources
- Sending reports about the status of the worker node and containers to master nodes

#### kubelet 
- Kubelet is a node-level agent that helps with container management and orchestration in a Kubernetes cluster
- Is present in each node of the cluster, Listen to API server, and deploy, destroys containers
- KubeAPI server fetches periodic report from kubelet to monitor status of nodes and containers in them

#### kubectl
- Kubectl is a command-line tool that allows users to run commands against Kubernetes clusters
- API Server is like gatekeeper, which is trying to understand status of server
- API Server is always interacted whenever we use kubectl command

#### Kubeproxy 
- Now, how frontend talks to backend/mysql? 
- If someone from outside wants to access cluster then kube proxy does it

#### Pods:
- Scheduling unit of kubernetes(Elementary component)
- Creates abstraction over containers
- Usually 1 Application per Pod
- Each Pod gets its own IP address
- Runs one or more containers
- Are ephemeral, can die easily, if pod ran out of resources or anything, or application crashes, it will die, we will have to reconfigure ip address if pod dies and if we have to restart
<img width="500" alt="Screenshot 2024-03-21 at 3 11 36 AM" src="https://github.com/arctic-gsu/kubernetes_workshop/assets/33342277/bdf65dc1-d01c-4eee-92f3-f19ffc146907">

#### Service:
- Permanent IP address
- Lifecycle of Pod and Service are not connected
- Now, because of service, ip address will stay and we dont have to change it
- Has 2 types of service, one is external service, and another is internal service but has ip as 124.41.501.2:8080, which is not good for developing application, ingress comes into play
- Types of service:
    - ClusterIP (default): Internal clients send requests to a stable internal IP address
    - NodePort: Clients send requests to the IP address of a node on one or more nodePort values that are specified by the Service
    - LoadBalancer: Clients send requests to the IP address of a network load balancer
  
#### Ingress:
- now url looks like myapp.com
- so request first goes to ingress and then to the service
<img width="200" height="300" alt="Screenshot 2024-03-21 at 3 11 36 AM" src="https://github.com/arctic-gsu/kubernetes_workshop/assets/33342277/09d56b00-e2aa-439b-b01b-ec1017f18e2d">

   

## Docker basics:
<img width="1070" alt="Screenshot 2024-03-15 at 1 41 53 PM" src="https://github.com/arctic-gsu/kubernetes_workshop/assets/33342277/565d7040-c9ad-4e5d-8098-6fc19745a6ce">

Install docker in your system and run the following command, goto localhost:82 a browser should open
```
sudo docker run -d -p 82:80 docker/getting-started
```
command description: 
- docker run: starting a container
- docker/getting-started: docker image
- 82:80 host:port

I am running in k8s cluster (docker with only sudo can run here)
```
hpcshruti@k8s-ctrls04:~$ sudo docker run -d -p 82:80 docker/getting-started
Unable to find image 'docker/getting-started:latest' locally
latest: Pulling from docker/getting-started
c158987b0551: Pull complete 
1e35f6679fab: Pull complete 
cb9626c74200: Pull complete 
b6334b6ace34: Pull complete 
f1d1c9928c82: Pull complete 
9b6f639ec6ea: Pull complete 
ee68d3549ec8: Pull complete 
33e0cbbb4673: Pull complete 
4f7e34c2de10: Pull complete 
Digest: sha256:d79336f4812b6547a53e735480dde67f8f8f7071b414fbd9297609ffb989abc1
Status: Downloaded newer image for docker/getting-started:latest
35647727e3013ba8cd8ac0d419512b33cfe9917f330f5f3bbdf88b37198a0aaf
```

<img width="411" alt="Screenshot 2024-03-15 at 1 40 13 PM" src="https://github.com/arctic-gsu/kubernetes_workshop/assets/33342277/54b171c6-9106-4d46-a997-a66de0e62f17">

#### check the app in browser
[in local]
```
localhost:82
```
[in remote desktop]
```
k8s-ctrls04.rs.gsu.edu:82
```
you should land into Docker getting started page
```
http://k8s-ctrls04.rs.gsu.edu:82/tutorial/
```


checking in browser
![Screenshot 2024-03-19 at 1 15 38 PM](https://github.com/arctic-gsu/kubernetes_workshop/assets/33342277/b337a400-92bd-4c39-8108-ee268c7c04bc)


#### get the app
Either clone this repo you will have app.zip file inside it: </br>
so unzip it using 
```
unzip app.zip
```

OR if you have docker then do:
```
wget http://localhost:82/assests/app.zip
```
you must have the app folder now.

## Containerizing our application
moving app into kubenetes_dir and creating a Dockerfile inside app directory:
```
hpcshruti@k8s-ctrls04:~/kubenetes_dir/app$ cat Dockerfile 
FROM node:18-alpine
WORKDIR /app
COPY . .
RUN yarn install --production
EXPOSE 3000
CMD ["node", "src/index.js"]
```
build docker
```
docker build -t basic_app:1.0 .
```
run docker 
```
docker run -d -p 3000:3000 basic_app:1.0
```
check whether your app is working or not in browser 

<img width="1786" alt="Screenshot 2024-03-22 at 6 16 19 AM" src="https://github.com/arctic-gsu/kubernetes_workshop/assets/33342277/86ca8b9e-7ef4-4a7e-a20d-062871c6b792">

kill the port 3000, otherwise it will conflict:
```
(base) sshrestha8@ARCs-MacBook-Pro app % docker ps

CONTAINER ID   IMAGE           COMMAND                  CREATED          STATUS          PORTS                            NAMES
3e394770bbe6   basic_app:1.0   "docker-entrypoint.s…"   25 seconds ago   Up 24 seconds   50/tcp, 0.0.0.0:3000->3000/tcp   practical_torvalds

(base) sshrestha8@ARCs-MacBook-Pro app % docker stop 3e394770bbe6
```

## Two container one host communication, using docker compose - two different services communication


#### making our app interact with the mysql service

write compose file
```
hpcshruti@k8s-ctrls04:~/kubenetes_dir/app$ cat compose.yaml 
services:
  app:
    image: node:18-alpine 
    command: sh -c "yarn install && yarn run dev"
    ports:
      - 3000:3000
    working_dir: /app
    volumes:
      -  ./:/app
    networks:
      - mynet
    environment:
      MYSQL_HOST: mysql
      MYSQL_USER: root
      MYSQL_PASSWORD: secret
      MYSQL_DB: todos


  mysql:
    image: mysql:8.0
    volumes:
      - todo-mysql-data:/var/lib/mysql
    environment:
      MYSQL_ROOT_PASSWORD: secret 
      MYSQL_DATABASE: todos
    networks:
      - mynet


volumes:
  todo-mysql-data:

networks:
  mynet:
```

build the compose file:
```
docker compose up -d --build
```
you should see
```
[+] Running 2/2
 ⠿ Container app-mysql-1  Running                                                                                                                                                                                                                         
 ⠿ Container app-app-1    Started   
```
verify using docker compose ps
```
hpcshruti@k8s-ctrls04:~/kubenetes_dir/app$ sudo docker compose ps
NAME                IMAGE               COMMAND                  SERVICE             CREATED             STATUS              PORTS
app-app-1           node:18-alpine      "docker-entrypoint.s…"   app                 41 minutes ago      Up About a minute   0.0.0.0:3000->3000/tcp, :::3000->3000/tcp
app-mysql-1         mysql:8.0           "docker-entrypoint.s…"   mysql               41 minutes ago      Up 41 minutes       3306/tcp, 33060/tcp
```
it shows backend and database, mysql is database and node is backend


and mysql is running in 
```
http://k8s-ctrls04.rs.gsu.edu:3000/
```
If you refresh , the list in todo will be there, as we are mounting volume
![Screenshot 2024-03-19 at 1 16 54 PM](https://github.com/arctic-gsu/kubernetes_workshop/assets/33342277/444ccb16-fe74-43fb-93a2-7ef5316bf726)

Now, we have container 1, getting started, always wanted to keep up

and app is in another container which can be accessed through port 3000
![Screenshot 2024-03-19 at 2 28 39 PM](https://github.com/arctic-gsu/kubernetes_workshop/assets/33342277/d551bbc5-9d94-4f9b-90c2-22bd89f705ab)

##### We now want to run the same application in kubernetes:
In docker we have containers where our application is running, but in kubernetes we have pods where we can have one or more containers(container is inside a pod)

![Screenshot 2024-03-19 at 2 32 13 PM](https://github.com/arctic-gsu/kubernetes_workshop/assets/33342277/9c92f555-6978-4e4f-b1b4-2cd08a88efa2)


Login into arcdocker, which is our container registry, username and password are your gsu username and password
```
(base) sshrestha8@ARCs-MacBook-Pro app % docker login arcdocker.rs.gsu.edu
Authenticating with existing credentials...
Login Succeeded
```

tag it and push it to arcdocker
```
(base) sshrestha8@ARCs-MacBook-Pro app % docker tag basic_app:1.0 arcdocker.rs.gsu.edu/basic_app:1.0
(base) sshrestha8@ARCs-MacBook-Pro app % docker push arcdocker.rs.gsu.edu/basic_app:1.0
The push refers to repository [arcdocker.rs.gsu.edu/basic_app]
26d7ce54dd04: Pushed 
2dc453868043: Pushed 
e7f70e494320: Pushed 
e79172ab9ca5: Pushed 
884adc00e5c1: Pushed 
d5d73638bf28: Pushed 
d4fc045c9e3a: Pushed 
1.0: digest: sha256:a7dd29f9698b56445ec124c9949256428c9afa92aebd819b6448734b2e1a18be size: 1787
```


## Using docker image in kubernetes: kubectl
login to kubectl:
```
ssh -i private_key username@k8s-ctrls04.rs.gsu.edu
```


checking kubectl versions and nodes
```
hpcshruti@k8s-ctrls04:~/kubenetes_dir/app$ kubectl version
Kustomize Version: v4.5.7

hpcshruti@k8s-ctrls04:~/kubenetes_dir/app$ kubectl get nodes
NAME          STATUS   ROLES           AGE    VERSION
k8s-ctrls02   Ready    <none>          32d    v1.26.0
k8s-ctrls03   Ready    <none>          382d   v1.26.0
k8s-ctrls04   Ready    control-plane   437d   v1.26.0
```
k8s-ctrls02, k8s-ctrls03, k8s-ctrls04: these are our kubernetes clusters so it has kubernetes already installed in it.

running our pushed docker image from arcdocker in kubernetes cluster and naming it basic-app-kube:
```
hpcshruti@k8s-ctrls04:~$ kubectl run --image=arcdocker.rs.gsu.edu/basic_app:1.0 basic-app-kube --port=3000
pod/basic-app-kube created
```
kubectl is a command talking to kubernetes api server (simple way to run docker image in kubernetes)

get pods:
```
hpcshruti@k8s-ctrls04:~/kubenetes_dir/app$ kubectl get po
NAME                                                READY   STATUS             RESTARTS       AGE
basic-app-kube                                      1/1     Running             0              35s```
if you ready status is 0/1, it failed, check if you have docker hub login credentials correct, and also if you have pushed and used correct versions
```
expose image pod on kubernetes:
```
hpcshruti@k8s-ctrls04:~$ kubectl expose pod basic-app-kube --type=NodePort --port=3000
service/basic-app-kube exposed
```

check the port:
```
kubectl get svc basic-app-kube
```
This command will show you the details of the service. Look for the "Port(s)" column; it will show something like 3000:XXXXX, where XXXXX is the node port assigned to your service. This is the port you will use to access your application from outside the cluster.
```
hpcshruti@k8s-ctrls04:~$ kubectl get svc basic-app-kube
NAME               TYPE       CLUSTER-IP      EXTERNAL-IP   PORT(S)          AGE
basic-app-kube   NodePort   10.102.203.244   <none>        3000:32077/TCP   29s
```
goto k8s-ctrls04.rs.gsu.edu:32077 in your remote browser

<img width="1786" alt="Screenshot 2024-03-22 at 7 38 20 AM" src="https://github.com/arctic-gsu/kubernetes_workshop/assets/33342277/a42b4bdd-044d-4154-b83e-6972b8fd9fb0">



## Setup for kubeadmin

#### Setting up 5 nodes kubernetes cluster:

open https://labs.play-with-k8s.com/ and start an instance
```
[node1 ~]$ git clone https://github.com/collabnix/kubelabs.git

[node1 ~]$ cd kubelabs
```


look into bootstrap.sh
```
[node1 kubelabs]$ cat bootstrap.sh
kubeadm init --apiserver-advertise-address $(hostname -i) --pod-network-cidr 10.5.0.0/16
kubectl apply -f https://raw.githubusercontent.com/cloudnativelabs/kube-router/master/daemonset/kubeadm-kuberouter.yaml
```
explaining the command:
```
kubeadm init : initializes a Kubernetes control-plane node and execute the below phases

The “init” command executes the following phases:

preflight                    Run pre-flight checks
kubelet-start                Write kubelet settings and (re)start the kubelet
certs                        Certificate generation
  /ca                          Generate the self-signed Kubernetes CA to provision identities for other Kubernetes components
  /apiserver                   Generate the certificate for serving the Kubernetes API
  /apiserver-kubelet-client    Generate the certificate for the API server to connect to kubelet
  /front-proxy-ca              Generate the self-signed CA to provision identities for front proxy
  /front-proxy-client          Generate the certificate for the front proxy client
  /etcd-ca                     Generate the self-signed CA to provision identities for etcd
  /etcd-server                 Generate the certificate for serving etcd
  /etcd-peer                   Generate the certificate for etcd nodes to communicate with each other
  /etcd-healthcheck-client     Generate the certificate for liveness probes to healthcheck etcd
  /apiserver-etcd-client       Generate the certificate the apiserver uses to access etcd
  /sa                          Generate a private key for signing service account tokens along with its public key
kubeconfig                   Generate all kubeconfig files necessary to establish the control plane and the admin kubeconfig file
  /admin                       Generate a kubeconfig file for the admin to use and for kubeadm itself
  /kubelet                     Generate a kubeconfig file for the kubelet to use *only* for cluster bootstrapping purposes
  /controller-manager          Generate a kubeconfig file for the controller manager to use
  /scheduler                   Generate a kubeconfig file for the scheduler to use
control-plane                Generate all static Pod manifest files necessary to establish the control plane
  /apiserver                   Generates the kube-apiserver static Pod manifest
  /controller-manager          Generates the kube-controller-manager static Pod manifest
  /scheduler                   Generates the kube-scheduler static Pod manifest
etcd                         Generate static Pod manifest file for local etcd
  /local                       Generate the static Pod manifest file for a local, single-node local etcd instance
upload-config                Upload the kubeadm and kubelet configuration to a ConfigMap
  /kubeadm                     Upload the kubeadm ClusterConfiguration to a ConfigMap
  /kubelet                     Upload the kubelet component config to a ConfigMap
upload-certs                 Upload certificates to kubeadm-certs
mark-control-plane           Mark a node as a control-plane
bootstrap-token              Generates bootstrap tokens used to join a node to a cluster
kubelet-finalize             Updates settings relevant to the kubelet after TLS bootstrap
  /experimental-cert-rotation  Enable kubelet client certificate rotation
addon                        Install required addons for passing Conformance tests
  /coredns                     Install the CoreDNS addon to a Kubernetes cluster
  /kube-proxy                  Install the kube-proxy addon to a Kubernetes cluster
```

initialize the master node:
```
kubeadm init --apiserver-advertise-address $(hostname -i) --pod-network-cidr 10.5.0.0/16
```

look for kube join command and copy it, you will add this kube join to other worker nodes.
```
kubeadm join 192.168.0.13:6443 --token c6a5q8.zx11bw566y6lvoch \
        --discovery-token-ca-cert-hash sha256:df10aae9e466eaf94e2cdbaf966976aae43cc067133ccab66d0c5b1f88a56a3d
```
you should see below output after join in each node :
```
W0322 11:46:26.235363    2656 initconfiguration.go:120] Usage of CRI endpoints without URL scheme is deprecated and can cause kubelet errors in the future. Automatically prepending scheme "unix" to the "criSocket" with value "/run/docker/containerd/containerd.sock". Please update your configuration!
[preflight] Running pre-flight checks
        [WARNING FileAvailable--etc-kubernetes-kubelet.conf]: /etc/kubernetes/kubelet.conf already exists
[preflight] The system verification failed. Printing the output from the verification:
KERNEL_VERSION: 4.4.0-210-generic
OS: Linux
CGROUPS_CPU: enabled
CGROUPS_CPUACCT: enabled
CGROUPS_CPUSET: enabled
CGROUPS_DEVICES: enabled
CGROUPS_FREEZER: enabled
CGROUPS_MEMORY: enabled
CGROUPS_PIDS: enabled
CGROUPS_HUGETLB: enabled
CGROUPS_BLKIO: enabled
        [WARNING SystemVerification]: failed to parse kernel config: unable to load kernel module: "configs", output: "", err: exit status 1
        [WARNING Port-10250]: Port 10250 is in use
        [WARNING FileAvailable--etc-kubernetes-pki-ca.crt]: /etc/kubernetes/pki/ca.crt already exists
        [WARNING FileContent--proc-sys-net-bridge-bridge-nf-call-iptables]: /proc/sys/net/bridge/bridge-nf-call-iptables does not exist
[preflight] Reading configuration from the cluster...
[preflight] FYI: You can look at this config file with 'kubectl -n kube-system get cm kubeadm-config -o yaml'
[kubelet-start] Writing kubelet configuration to file "/var/lib/kubelet/config.yaml"
[kubelet-start] Writing kubelet environment file with flags to file "/var/lib/kubelet/kubeadm-flags.env"
[kubelet-start] Starting the kubelet
[kubelet-start] Waiting for the kubelet to perform the TLS Bootstrap...

This node has joined the cluster:
* Certificate signing request was sent to apiserver and a response was received.
* The Kubelet was informed of the new secure connection details.

Run 'kubectl get nodes' on the control-plane to see this node join the cluster.
```
check for nodes:

```
[node1 kubelabs]$ kubectl get nodes
NAME    STATUS     ROLES           AGE    VERSION
node1   NotReady   control-plane   105s   v1.27.2
node2   NotReady   <none>          11s    v1.27.2
```

check for service:
```
[node1 kubelabs]$ kubectl get svc
NAME         TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE
kubernetes   ClusterIP   10.96.0.1    <none>        443/TCP   3m28s
```

Establish networking: for pod networking kuberouter needs to be installed. 
```
[node1 kubelabs]$ kubectl apply -f https://raw.githubusercontent.com/cloudnativelabs/kube-router/master/daemonset/kubeadm-kuberouter.yaml
configmap/kube-router-cfg created
daemonset.apps/kube-router created
serviceaccount/kube-router created
clusterrole.rbac.authorization.k8s.io/kube-router created
clusterrolebinding.rbac.authorization.k8s.io/kube-router created
```

do in node 1:
```
kubeadm join 192.168.0.18:6443 --token j12itj.s873eteysrd8we2y --discovery-token-ca-cert-hash sha256:c78cb3840531be0deea863ae7c9af3e16c20f4220835077d525451d893678cc1 
it will show RTNETLINK answers: File exists in master nodes
```

copy and paste in all worker nodes. in the left side you will see, add instance, click on it and your new instance will be started
```
[node2 ~]$ kubeadm join 192.168.0.18:6443 --token j12itj.s873eteysrd8we2y --discovery-token-ca-cert-hash sha256:c78cb3840531be0deea863ae7c9af3e16c20f4220835077d525451d893678cc1
```

start another i.e. 3rd node and do the same
now in node1, you should see:
```
[node1 kubelabs]$ kubectl get nodes
NAME    STATUS   ROLES           AGE     VERSION
node1   Ready    control-plane   24m     v1.27.2
node2   Ready    <none>          3m45s   v1.27.2
node3   Ready    <none>          30s     v1.27.2
```

Likewise do it for 4th and 5th node. 
Now you have 5 nodes kubernetes cluster

After 5 nodes creation:
```
[node1 kubelabs]$ kubectl get nodes
NAME    STATUS     ROLES           AGE     VERSION
node1   Ready      control-plane   28m     v1.27.2
node2   Ready      <none>          7m43s   v1.27.2
node3   Ready      <none>          4m28s   v1.27.2
node4   NotReady   <none>          8s      v1.27.2
node5   NotReady   <none>          4s      v1.27.2
```

left panel shows our 5 kubernetes cluster

<img width="318" alt="Screenshot 2024-03-21 at 4 39 28 AM" src="https://github.com/arctic-gsu/kubernetes_workshop/assets/33342277/563fe3d5-abea-407b-b4f6-c132ae23a496">
where node 1 is master and all other are worker nodes.


## Workflow of a Pod:

<img width="851" alt="Screenshot 2024-03-21 at 5 09 18 AM" src="https://github.com/arctic-gsu/kubernetes_workshop/assets/33342277/706ca7ce-ca27-4e95-a3db-18c6a5985334">

- Pod is defined using json manifest </br>
- Manifest file has decalred/desired state and has container specs, networking specs and other additional information
- Basically kubectl applies the manifest and creates the pods
- API Server: kubectl send manifest to API server, API server validate manifests syntax and checks for any error
- Pod Scheduler: assigns pod to suitable worker node, scheduler takes account of resource, availability node affinity rule and scheduling constraints
- Container creation: assigned worker node recieves pods specification and initiates creating container insides the pod, it pulls the container images specified in the pod and starts the container
- Pod Status: pod goes through different status phases: pending, running, failed etc
- monitoring and logging: to track the status of the resources realted to the pod
- Every pod in the kubernetes cluster gets a ip address
- And different services use different ports

Every pod can talk to another pod through this address
![Screenshot 2024-03-21 at 9 41 37 AM](https://github.com/arctic-gsu/kubernetes_workshop/assets/33342277/5f965654-0edb-4bac-8cd6-a3a264cf6405)

Intra pod communication:
When multiple container running inside a pod, they share same namespace and communicate using localhost.

Pod manifest file;

create a manifest file and name it manifest.yaml
```
apiVersion: v1
kind: Namespace
metadata:
 name: ns2
---
apiVersion: v1
kind: Pod
metadata:
 name: basic-app
 namespace: ns2
spec:
 containers:
 - name: basic-app-container
   image: arcdocker.rs.gsu.edu/basic_app:1.0
```
apply the manifest file
```
hpcshruti@k8s-ctrls04:~/kubenetes_dir$ kubectl apply -f manifest.yaml 
namespace/ns2 created
pod/todo-list created
```
check what are inside your namespace
```
check namespace:
kubectl get ns

output:
NAME               STATUS   AGE
ns2                Active   54s
```
you pod is under namespace ns2

it doesnot appear when you do "kubectl get po"

```
hpcshruti@k8s-ctrls04:~/kubenetes_dir$ kubectl get po 
NAME                                                READY   STATUS    RESTARTS   AGE
basic-app-kube                                      1/1     Running   0              29m

```
Remember, this basic-app-kube is from before, but after you append command -n ns2, it shows, the recently create one "basic-app" that is under namespace ns2:
```
hpcshruti@k8s-ctrls04:~/basic_app_folder$ kubectl get po -n ns2
NAME        READY   STATUS    RESTARTS   AGE
basic-app   1/1     Running   0          85s

```
expose port
```
hpcshruti@k8s-ctrls04:~/basic_app_folder$ kubectl expose pod basic-app -n ns2 --type=NodePort --port=3000 --selector=app=basic-app
service/basic-app exposed
```
look for services
```
hpcshruti@k8s-ctrls04:~/kubenetes_dir$ kubectl get svc
NAME                                                      TYPE           CLUSTER-IP       EXTERNAL-IP     PORT(S)                      AGE
```
see our todo-list service is not showing up, remember to put -n for namespace
```
hpcshruti@k8s-ctrls04:~/basic_app_folder$ kubectl get svc -n ns2
NAME        TYPE       CLUSTER-IP       EXTERNAL-IP   PORT(S)          AGE
basic-app   NodePort   10.99.124.83     <none>        3000:31541/TCP   26s

```
see that your port is listening on 31541
goto http://k8s-ctrls04.rs.gsu.edu:31541/
and you will see your app running

<img width="1790" alt="Screenshot 2024-03-21 at 11 58 30 AM" src="https://github.com/arctic-gsu/kubernetes_workshop/assets/33342277/14df0d79-90e4-4e6e-af48-c85428691818">

## Multiple container in single pod:
We will create a namespace ns3, create a Pod with two containers, the first named todo-list using a Docker image srutsth/todo and a second container based on prom/promethrus:v2.30.3 docker image and container exposed to port 9090

```
hpcshruti@k8s-ctrls04:~/kubenetes_dir$ sudo nano multi_container.yaml

```
write this to your multi_container.yaml file
```
apiVersion: v1
kind: Namespace
metadata:
  name: ns3
---
apiVersion: v1
kind: Pod
metadata:
  name: multi-container-pod
  namespace: ns3
spec:
  containers:
  - name: todo-list
    image: srutsth/todo
    ports:
    - containerPort: 3000
  - name: prometheus
    image: prom/prometheus:v2.30.3
    ports:
    - containerPort: 9090
```
deploy this yaml file, check pod in ns3 namespace to see if both the containers inside the pod "multi-container-pod" are running, should be 2/2 if both are running
```
hpcshruti@k8s-ctrls04:~/kubenetes_dir$ kubectl apply -f multi_container.yaml 
namespace/ns3 created
pod/multi-container-pod created
hpcshruti@k8s-ctrls04:~/kubenetes_dir$ kubectl get po -n ns3
NAME                  READY   STATUS    RESTARTS   AGE
multi-container-pod   2/2     Running   0          57m
```


## Creating a ML Porject and Deploying in kubernetes

Be sure to first create virtual env, and install all the requirements
if you have not created virutal environment yet:
```
mkdir venv
python3 -m venv my_venv
source my_venv/bin/activate
```

see your requirements.txt file
```
(my_venv) hpcshruti@k8s-ctrls04:~/my_project$ cat requirements.txt 
blinker==1.7.0
click==8.1.7
flask==3.0.2
importlib-metadata==7.1.0
itsdangerous==2.1.2
Jinja2==3.1.3
joblib==1.3.2
MarkupSafe==2.1.5
numpy==1.24.4
scikit-learn==1.3.2
scipy==1.10.1
threadpoolctl==3.4.0
werkzeug==3.0.1
zipp==3.18.1
```
install the requirements
```
pip install -r requirements.txt
```

write a ml script and name it ml_script.py
```
(my_venv) hpcshruti@k8s-ctrls04:~/my_project$ cat ml_script.py 
from sklearn.linear_model import LinearRegression
import joblib
import numpy as np

X = np.array([[600], [800], [1000], [1200], [1400]])  # Features (square footage)
y = np.array([150000, 180000, 210000, 240000, 270000])  # Targets (price)

model=LinearRegression()
model.fit(X,y)

joblib.dump(model,'model.pkl')
```

run: python ml_script.py to get model.pkl
write flask for accessing through ip
```
(my_venv) hpcshruti@k8s-ctrls04:~/my_project$ cat flask_app.py 
from flask import Flask, request, jsonify
import joblib

app = Flask(__name__)

model = joblib.load('model.pkl')

@app.route('/predict',methods=['POST'])
def predict():
    data = request.get_json(force=True)
    prediction = model.predict([[700]])
    return jsonify({'prediction':prediction[0]})

if __name__ == '__main__':
    app.run(debug=True)
```




Containerizing our app:
```
(my_venv) hpcshruti@k8s-ctrls04:~/my_project$ nano Dockerfile 
FROM python:3.8-slim

WORKDIR /usr/src/app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

ENV FLASK_APP=flask_app.py
ENV FLASK_RUN_HOST=0.0.0.0

CMD ["flask","run"]
```

build docker file
```
(my_venv) hpcshruti@k8s-ctrls04:~/my_project$ sudo docker build -t my_project:1.0 .

(my_venv) hpcshruti@k8s-ctrls04:~/my_project$ sudo docker run -d -p 5000:5000 my_project:1.0
1a44547298b2d727891ee3e9707206dc88b834693a618883808195f0b90b2254
```
check if docker container is running with command docker ps
```
(my_venv) hpcshruti@k8s-ctrls04:~/my_project$ sudo docker ps
CONTAINER ID   IMAGE                    COMMAND                  CREATED          STATUS          PORTS                                       NAMES
1a44547298b2   my_project:1.0           "flask run"              15 seconds ago   Up 14 seconds   0.0.0.0:5000->5000/tcp, :::5000->5000/tcp   elegant_joliot
27eb65a4091b   srutsth/todo:1.0         "docker-entrypoint.s…"   21 hours ago     Up 21 hours     0.0.0.0:3001->3000/tcp, :::3001->3000/tcp   exciting_jones
35647727e301   docker/getting-started   "/docker-entrypoint.…"   6 days ago       Up 6 days       0.0.0.0:82->80/tcp, :::82->80/tcp           youthful_montalcini
```
curl to send post request
```
(my_venv) hpcshruti@k8s-ctrls04:~/my_project$ curl -X POST -H "Content-Type: application/json" -d '{"square_feet": 1000}' http://localhost:5000/predict
{"prediction":165000.00000000006}
```
we see the prediction value, so we can assure that our docker container is working

Now, create a registrysecret file to store your credentials, I am naming it myregistrysecret
```
kubectl create secret docker-registry myregistrysecret \
  --docker-server=arcdocker.rs.gsu.edu \ # Your Docker registry's server address
  --docker-username=*** \ # Your Docker registry username
  --docker-password=*** \ # Your Docker registry password
  --docker-email=*** # Your email
```

Deploying into kubernetes. Write the deployment file.
```
(my_venv) hpcshruti@k8s-ctrls04:~/my_project$ cat mydeployment.yaml 
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-project-app
spec:
  replicas: 2
  selector:
    matchLabels:
      app: my-project-app
  template:
    metadata:
      labels:
        app: my-project-app
    spec:
      containers:
      - name: my-project-app-container
        image: arcdocker.rs.gsu.edu/my_project:1.0 # Your private image
        ports:
        - containerPort: 5000
      imagePullSecrets:
      - name: myregistrysecret
```
deploy the yaml file
```
kubectl apply -f mydeployment.yaml 
```
remember for accessing port from outside this cluster you have to expose the port, for developement we can do this by nodeport, but for production we need to do it from loadbalancer
```
(my_venv) hpcshruti@k8s-ctrls04:~/my_project$ cat service.yaml 
apiVersion: v1
kind: Service
metadata:
  name: my-project-app-service
spec:
  type: NodePort
  selector:
    app: my-project-app
  ports:
  - protocol: TCP
    port: 5000
    targetPort: 5000
```
deploy the service
```
(my_venv) hpcshruti@k8s-ctrls04:~/my_project$ kubectl apply -f service.yaml 
service/my-project-app-service created
```
query for svc
```
(my_venv) hpcshruti@k8s-ctrls04:~/my_project$ kubectl get svc
NAME                                                      TYPE           CLUSTER-IP       EXTERNAL-IP     PORT(S)                      AGE
my-project-app-service                                    NodePort       10.100.98.55     <none>          5000:30910/TCP               1s
todo-app                                                  NodePort       10.110.225.48    <none>          3000:31313/TCP               23h
```
see our our service is there you can also check for deployments by </br>
kubectl get deployment </br>
and pod by:</br>
kubectl get pod</br>
</br>
curl to see if our kubernetes deployment is working or not
```
(my_venv) hpcshruti@k8s-ctrls04:~/my_project$ curl -X POST -H "Content-Type: application/json" -d '{"square_feet": 1000}' http://k8s-ctrls04.rs.gsu.edu:30910/predict
{"prediction":165000.00000000006}
```
