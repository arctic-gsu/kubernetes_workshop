get the private key named user01<\br>
```
chmod 700 user01
```
Adjusting the ownership and permissions
```
ssh-keygen -p -m PEM -f user01
```
login the cluster
```
ssh -i user01 hpcuser01@k8s-ctrls04.rs.gsu.edu
```
