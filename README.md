# Kubernetes:
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

## Kubenetes Architecture
- It has atleast one master node and other are worker nodes </br>
- Worker nodes has kubelet process, which makes it possible for cluster to communicate and run application processes </br>
- Workers have different number of containers </br>
- Worker node is where your services are running
- Master node runs several kubernetes processes that are absolutely necessary for running kubernetes clusters properly

Figure showing Kubernetes Cluster Architecture
![Screenshot 2024-03-20 at 11 06 45 AM](https://github.com/arctic-gsu/kubernetes_workshop/assets/33342277/2e001376-e22c-472a-b701-714b249dfef2)

### Master node and Worker Node</br>

#### Master components:</br>
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

#### Worker components:
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


### Agenda;
1. Docker basics
2. 2 container 1 host communication, using docker compose - 2 different services communication
3. kubectl 
4. kubenetes architecture
5. kubeview
6. Setting up 5 nodes kubernetes cluster
7. Pod Concepts:
    1. Pod Deployment
    2. Multi Container
    3. Pod Networking
    4. Inter-Pod and Intra Pod Networking
    5. Pod Lifecycle
    6. Pod Manifest File
   

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
```
wget http://localhost:82/assests/app.zip
```

#### containerizing our application
moving app into kubenetes_dir and a Dockerfile inside app:
```
hpcshruti@k8s-ctrls04:~/kubenetes_dir/app$ cat Dockerfile 
FROM node:18-alpine
WORKDIR /app
COPY . .
RUN yarn install --production
CMD ["node", "src/index.js"]
```

## Two container one host communication, using docker compose - 2 different services communication

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

[+] Running 2/2
 ⠿ Container app-mysql-1  Running                                                                                                                                                                                                                         
 ⠿ Container app-app-1    Started   

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


## kubectl
running docker image in kubernetes:
```
kubectl run --image=srutsth/todo todolist-app --port=3000
```

k8s-ctrls02, k8s-ctrls03, k8s-ctrls04: these are our kubernetes clusters so it has kubernetes already installed in it.

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
kubectl is a command talking to kubernetes api server (simple way to run docker image in kubernetes)

get pods:
```
hpcshruti@k8s-ctrls04:~/kubenetes_dir/app$ kubectl get po
NAME                                                READY   STATUS             RESTARTS       AGE
todolist-app                                        0/1     ImagePullBackOff   0              72s
```
if you ready status is 0/1, it failed, check if you have docker hub login credentials correct, and also if you have pushed and used correct versions
```
sudo docker build -t srutsth/todo:1.0 .
sudo docker run -d -p 3000:3000 srutsth/todo:1.0
sudo docker push srutsth/todo:1.0
```
run again, 
```
hpcshruti@k8s-ctrls04:~/kubenetes_dir/app$ kubectl run --image=srutsth/todo:1.0 todo-app-1 --port=3000
pod/todo-app-1 created
```
then check again,
```
hpcshruti@k8s-ctrls04:~/kubenetes_dir/app$ kubectl get po
NAME                                                READY   STATUS             RESTARTS       AGE
todo-app-1                                          1/1     Running            0              72s
```

running image on kubernetes:
```
hpcshruti@k8s-ctrls04:~$ kubectl expose pod todo-app --type=NodePort --port=3000
service/todo-app exposed
```

check the port:
```
kubectl get svc todo-app
```
This command will show you the details of the service. Look for the "Port(s)" column; it will show something like 3000:XXXXX, where XXXXX is the node port assigned to your service. This is the port you will use to access your application from outside the cluster.
```
hpcshruti@k8s-ctrls04:~$ kubectl get svc todo-app
NAME       TYPE       CLUSTER-IP      EXTERNAL-IP   PORT(S)          AGE
todo-app   NodePort   10.110.225.48   <none>        3000:31313/TCP   2m54s
```
goto k8s-ctrls04.rs.gsu.edu:31313 in your remote browser

<img width="1792" alt="Screenshot 2024-03-21 at 4 16 33 AM" src="https://github.com/arctic-gsu/kubernetes_workshop/assets/33342277/55c51f8b-a83a-4656-b92c-89fa13520927">



## Setting up 5 nodes kubernetes cluster:

open https://labs.play-with-k8s.com/ and start an instance
```
git clone https://github.com/collabnix/kubelabs.git
```


look into bootstrap.sh
```
[node1 kubelabs]$ cat bootstrap.sh
kubeadm init --apiserver-advertise-address $(hostname -i) --pod-network-cidr 10.5.0.0/16
kubectl apply -f https://raw.githubusercontent.com/cloudnativelabs/kube-router/master/daemonset/kubeadm-kuberouter.yaml
```
explaining the command:
```
[kubeadm init : initializes control plane in master node](https://github.com/collabnix/kubelabs/blob/master/kube101.md)
```

establish netowrking 
```
[node1 kubelabs]$ kubectl apply -f https://raw.githubusercontent.com/cloudnativelabs/kube-router/master/daemonset/kubeadm-kuberouter.yaml
configmap/kube-router-cfg created
daemonset.apps/kube-router created
serviceaccount/kube-router created
clusterrole.rbac.authorization.k8s.io/kube-router created
clusterrolebinding.rbac.authorization.k8s.io/kube-router created
```
check token 
```
kubeadm token list
TOKEN                     TTL         EXPIRES                USAGES                   DESCRIPTION                                                EXTRA GROUPS
6g3aej.kxqom616rhqivzkl   23h         2024-03-22T07:16:27Z   authentication,signing   The default bootstrap token generated by 'kubeadm init'.   system:bootstrappers:kubeadm:default-node-token
```

do in node 1:
```
token create --print-join-command --ttl 30m
kubeadm join 192.168.0.18:6443 --token j12itj.s873eteysrd8we2y --discovery-token-ca-cert-hash sha256:c78cb3840531be0deea863ae7c9af3e16c20f4220835077d525451d893678cc1 
it will show RTNETLINK answers: File exists in master nodes
```

copy and paste in all worker nodes. in the left side you will see, add instance, click on it and your new instance will be started
```
[node2 ~]$ kubeadm join 192.168.0.18:6443 --token j12itj.s873eteysrd8we2y --discovery-token-ca-cert-hash sha256:c78cb3840531be0deea863ae7c9af3e16c20f4220835077d525451d893678cc1
```
This will initializing machine ID from random generator.
```
Initializing machine ID from random generator.
W0321 07:36:45.369746    2424 initconfiguration.go:120] Usage of CRI endpoints without URL scheme is deprecated and can cause kubelet errors in the future. Automatically prepending scheme "unix" to the "criSocket" with value "/run/docker/containerd/containerd.sock". Please update your configuration!
[preflight] Running pre-flight checks
        [WARNING Swap]: swap is enabled; production deployments should disable swap unless testing the NodeSwap feature gate of the kubelet
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


now in your node1 do:  kubectl get nodes
```
[node1 kubelabs]$ kubectl get nodes
NAME    STATUS   ROLES           AGE     VERSION
node1   Ready    control-plane   22m     v1.27.2
node2   Ready    <none>          2m12s   v1.27.2
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
apiVersion:v1
kind: Namespace
metadata:
 name: ns2
---
apiVersion:v1
kind:Pod
metadata:
 name: todo-list
 namespace: ns2
spec:
 containers:
 - name: todo-list
   image: srutsth/todo
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
NAME        READY   STATUS    RESTARTS   AGE

```
but after you append command -n ns2, it shows, that is we have to give namespace:
```
hpcshruti@k8s-ctrls04:~/kubenetes_dir$ kubectl get po -n ns2
NAME        READY   STATUS    RESTARTS   AGE
todo-list   1/1     Running   0          2m5s
```
expose port
```
hpcshruti@k8s-ctrls04:~/kubenetes_dir$ kubectl expose pod todo-list -n ns2 --type=NodePort --port=3000 --selector=app=todo-list
service/todo-list exposed
```
look for services
```
hpcshruti@k8s-ctrls04:~/kubenetes_dir$ kubectl get svc
NAME                                                      TYPE           CLUSTER-IP       EXTERNAL-IP     PORT(S)                      AGE
todo-app                                                  NodePort       10.110.225.48    <none>          3000:31313/TCP               7h27m
```
see our todo-list service is not showing up, remember to put -n for namespace
```
hpcshruti@k8s-ctrls04:~/kubenetes_dir$ kubectl get svc -n ns2
NAME        TYPE       CLUSTER-IP       EXTERNAL-IP   PORT(S)          AGE
todo-list   NodePort   10.111.172.157   <none>        3000:32191/TCP   2m19s
```
see that your port is listening on 32191
goto http://k8s-ctrls04.rs.gsu.edu:32191/
and you will see your app running

<img width="1790" alt="Screenshot 2024-03-21 at 11 58 30 AM" src="https://github.com/arctic-gsu/kubernetes_workshop/assets/33342277/14df0d79-90e4-4e6e-af48-c85428691818">

## Multiple container in single pod:
We will create a namespace ns3, create a Pod with two containers, the first named todo-list using a Docker image srutsth/todo and a second container based on prom/promethrus:v2.30.3 docker image and container exposed to port 9090

```
hpcshruti@k8s-ctrls04:~/kubenetes_dir$ touch multi_container.yaml
touch: cannot touch 'multi_container.yaml': Permission denied
hpcshruti@k8s-ctrls04:~/kubenetes_dir$ sudo touch multi_container.yaml
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
