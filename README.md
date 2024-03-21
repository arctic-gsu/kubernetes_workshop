Agenda;
1. containerization - docker
2. 2 container 1 host communication
3. docker compose - 2 difference services communication
4. kubectl
5. kubenetes architecture
6. kubeview


A containerization journey

1. containerize a single app
2. run multicontainer application
3. best pratices
4. deploying into k8s

Docker basics:
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


need remote desktop:
k8s-ctrls04.rs.gsu.edu:82
you should land into Docker getting started page

write Dockerfile:
```
hpcshruti@k8s-ctrls04:~/kubenetes_dir/app$ cat Dockerfile 
FROM node:18-alpine
WORKDIR /app
COPY . .
RUN yarn install --production
CMD ["node", "src/index.js"]
```
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
document is running in:
```
http://k8s-ctrls04.rs.gsu.edu:82/tutorial/
```


checking in browser
![Screenshot 2024-03-19 at 1 15 38 PM](https://github.com/arctic-gsu/kubernetes_workshop/assets/33342277/b337a400-92bd-4c39-8108-ee268c7c04bc)

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

open https://labs.play-with-k8s.com/ and start an instance
```
git clone https://github.com/collabnix/kubelabs.git
```

look into bootstrap.sh
```
[node1 kubelabs]$ cat bootstrap.sh 
## Script to setup K8s Cluster

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

copy and paste in all worker nodes
```
kubeadm join 192.168.0.18:6443 --token j12itj.s873eteysrd8we2y --discovery-token-ca-cert-hash sha256:c78cb3840531be0deea863ae7c9af3e16c20f4220835077d525451d893678cc1 
it will Initializing machine ID from random generator in worker nodes
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
