<img width="851" alt="Screenshot 2024-03-21 at 5 09 18 AM" src="https://github.com/arctic-gsu/kubernetes_workshop/assets/33342277/0b4db5c2-ed6f-46e8-9788-a4704d5f8b54">
Agenda;
1. Docker basics
2. 2 container 1 host communication, using docker compose - 2 difference services communication
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

command
```
sudo docker run -d -p 82:80 docker/getting-started
```
docker run: starting a container
docker/getting-started: docker image
82:80 host:port

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

[need remote desktop]
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
## 2 container 1 host communication, using docker compose - 2 difference services communication

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

If we want to run hte same application in kubernetes:
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
sudo docker build -t srutsth/todo:1.0 .
sudo docker run -d -p 3000:3000 srutsth/todo:1.0
sudo docker push srutsth/todo:1.0

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

<img width="1792" alt="Screenshot 2024-03-21 at 4 16 33 AM" src="https://github.com/arctic-gsu/kubernetes_workshop/assets/33342277/55c51f8b-a83a-4656-b92c-89fa13520927">

## kubenetes architecture
### Master node and Worker Node

#### Master components:
Kube Scheduler: identifies right node to place a container, based on container resource requirement, also looks at policy and contraints, tolerations etc
ETCD Cluster: Stores whicih container is on which ships, when was it loaded etc. Its a Databse under master node. High availability key value store

Controllers: 
Node Controllers - Takes care of Nodes, responsible for onboarding new nodes on a cluster, availability of nodes
Replica controller - ensures container are running at all times
Controller manager - manages all these controllers

Kube API Server:
Primary management component of k8s
Orchestrates all operations within a cluster

check components of master node
```
hpcshruti@k8s-ctrls04:~$ kubectl get componentstatus
Warning: v1 ComponentStatus is deprecated in v1.19+
NAME                 STATUS    MESSAGE                         ERROR
scheduler            Healthy   ok                              
controller-manager   Healthy   ok                              
etcd-0               Healthy   {"health":"true","reason":""}   
```

#### Worker components:
Manages all activities
Sending reports about the status of the worker node and containers to master nodes
Known as kubelet and is present in each node of the cluster, Listen to API server, and deploy, destroys containers
KubeAPI server fetches periodic report from kubelet to monitor status of nodes and continer int hem

API Server is like gatekeeper, which is trying to understand status of server

API Serever is always interacted whenever we use kubectl command


Now, how frontend talks to backend/mysql? Kubeproxy helps
If someone from outside wantes to access cluster then kube proxy does it


Pods:
Scheduling unit of kubernetes(Elementary component)
Runs one or more containers

Kubernetes Cluster Architecture
![Screenshot 2024-03-20 at 11 06 45 AM](https://github.com/arctic-gsu/kubernetes_workshop/assets/33342277/2e001376-e22c-472a-b701-714b249dfef2)

KubeAPI server fetches periodic report from kubelet to monitor status of nodes and continer int hem

API Server is like gatekeeper, which is trying to understand status of server

API Server is always interacted whenever we use kubectl command

Now, how frontend talks to backend/mysql? Kubeproxy helps
If someone from outside wantes to access cluster then kube proxy does it


#### Pods:
Scheduling unit of kubernetes(Elementary component)
Runs one or more containers
<img width="1033" alt="Screenshot 2024-03-21 at 3 11 36 AM" src="https://github.com/arctic-gsu/kubernetes_workshop/assets/33342277/bdf65dc1-d01c-4eee-92f3-f19ffc146907">

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

start nother 3rd node and do the same
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


## Pod Concepts:

<img width="851" alt="Screenshot 2024-03-21 at 5 09 18 AM" src="https://github.com/arctic-gsu/kubernetes_workshop/assets/33342277/706ca7ce-ca27-4e95-a3db-18c6a5985334">
Pod is defined using json manifest
Manifest file has decalred /desired state
has container specs, networking specs and other additional infor
basically kubectl applied the manifest and creates the pods
API Server: kubectl send manifest to API server, API server validate manifests syntax and checks for any error
Pod Scheduler: assigns pod to suitable worker node, scheduler takes account of resource, availability node affinity rule and scheduling constraints
Container creation: assigned worker node recieves pods specification and initiates creating container insides the pod, it pulls the container images specified in the pod and starts the container
Pod Status: pod goes through different status phases: pending, running, failed etc
monitoring and logging: to track the status of the resources realted to the pod








