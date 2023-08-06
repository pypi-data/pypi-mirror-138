# Container Database Buddy - CoDaBuddy


> We use the buddy system. No more flyin' solo!
>
> You need somebody watching your back at all times!

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[*Rex Kwon Do - Napelon Dynamite*](https://youtu.be/Hzh9koy7b1E?t=94)

![LOGO_PLACEHOLDER](./docs/logo.png)
**This is a placeholder logo. Source: https://logomakr.com/**



A container native database setup, backup and restore solution

Maintainer: tim.bleimehl@dzd-ev.de

Status: Alpha (WIP - **do not use productive yet**)


[[_TOC_]]

# What is this (short)

CoDaBuddy helps you to automate setup and backup your database that is running in container environment (kubernetes, docker)

It relies heavily on configuration by labels ([docker-labels](https://docs.docker.com/config/labels-custom-metadata/), [kubernetes-labels](https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/))

This means you only have to attach the right labels to your database containers and they will be ready to use and included in your daily backup.


# Features

* Supported Databases:
    * Mysql
    * Postgres
* Automatic backup retentation management (Daily, Weekly, Monthly, Yearly)
* "Backup now!" wizard
* Compressed backup
* Auto create databases and users

# Basic Example

## Docker example
### Setup

Lets create a mysql/mariadb database via docker-compose

```yaml
version: "3.7"
services:
  mysql:
    image: mariadb:10
    ports:
      - 3306:3306
    container_name: mysql
    environment:
      - MYSQL_ROOT_PASSWORD=mysuperpw
    restart: unless-stopped
    labels:
      - "backup.dzd-ev.de/enabled=true"
      - "backup.dzd-ev.de/type=mysql"
      - "backup.dzd-ev.de/username=root"
      - "backup.dzd-ev.de/password=mysuperpw"
```

Note the `labels`; these will direct our CoDaBuddy instance.

Start the DB:

`docker-compose up -d`

Lets write some data into our new database

```bash
docker exec mysql /usr/bin/mysql -N -h127.0.0.1 -uroot -pmysuperpw -e "\
  CREATE DATABASE IF NOT EXISTS coda_test; \
  CREATE TABLE IF NOT EXISTS coda_test.my_table(id INT AUTO_INCREMENT, firstname VARCHAR(32), PRIMARY KEY (id)); \
  INSERT INTO coda_test.my_table(firstname) VALUES ('Anna'); \
  INSERT INTO coda_test.my_table(firstname) VALUES ('Thomas'); \
  commit;"
```

### Backup

Now we can install CoDaBuddy via

`pip3 install git+https://git.connect.dzd-ev.de/dzdtools/CoDaBuddy -U`

And lets backup our DB

`coda-backup docker`

Thats it. We now have a directory `./backups/` in front of us, with all databases backuped.

### Restore


## Kubernetes example

### Setup

First we create a sample postgres database container

`postgres-deployment.yaml`

```yaml
apiVersion: v1
kind: Service
metadata:
  name: postgres
spec:
  ports:
  - port: 5432
  selector:
    app: postgres
  clusterIP: None
---
apiVersion: apps/v1
kind: Deployment
metadata:
  labels:
    backup.dzd-ev.de/auto-create: true
    backup.dzd-ev.de/enabled: true
    backup.dzd-ev.de/password: supersavepw
    backup.dzd-ev.de/type: postgres
    backup.dzd-ev.de/username: postgres
  annotations:
    backup.dzd-ev.de/auto-create-databases: |-
      [{
          "database": "coda_ps_test",
          "user": "coda_test",
          "password": "super_save_pw"
        }]
spec:
  selector:
    matchLabels:
      workloadselector: postgres01
  serviceName: ""
  template:
    metadata:
      labels:
        workloadselector: postgres01
    spec:
      containers:
      - env:
        - name: POSTGRES_PASSWORD
          value: supersavepw
        image: postgres:12
        name: postgres01
        ports:
        - containerPort: 5432
          hostPort: 5432
          name: psport5432
```

`kubectl apply -f postgres-deployment.yaml`


### Setup Databases

Just for fun we now use the CoDaBuddy Docker Container `auto-create`-feature to create our user and database

`docker pull registry-gl.connect.dzd-ev.de:443/dzdtools/codabuddy`

`docker run --rm -it --network=host -v ~/.kube/config:/.kube/config registry-gl.connect.dzd-ev.de:443/dzdtools/codabuddy auto-create --debug kubernetes --all-namespaces`

This creates a new postgres user/role named `coda_test` with access to a newly created database named `coda_ps_test` as defined in our annotation `backup.dzd-ev.de/auto-create-databases`


ToDo-note:

> this is not working due to missing role auth
>
> results in `Error from server (Forbidden): pods is forbidden: User "system:serviceaccount:default:default" cannot list resource "pods" in API group "" at the cluster scope`
>
> `kubectl run codabuddy --restart=Never --rm -i --image=registry-gl.connect.dzd-ev.de:443/dzdtools/codabuddy -- auto-create --debug kubernetes --all-namespaces `


### Backup

Now we create a CronJob for CoDaBuddy to create a daily backup every night at 00:00

```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: CoDaBuddy-backupjob
spec:
  schedule: "0 0 * * *"
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: CoDaBuddy-backupjob
            image: registry-gl.connect.dzd-ev.de:443/dzdtools/codabuddy
            imagePullPolicy: Always
            volumeMounts:
            - mountPath: /backup
              name: backup-vol
            - mountPath: /.kube/config
              name: kubeconf-vol
            command:
            - backup
            - --all-namespaces
          restartPolicy: OnFailure
          volumes:
          - name: backup-vol
            hostPath:
              # path to store backups in the cluster host. This is obviously just a test setup. dont do that in productive
              path: /tmp/backup
              # this field is optional
              type: Directory
          - name: kubeconf-vol
            hostPath:
              # path to store the kube config. This is obviously just a test setup. dont do that in productive
              path: /home/myname/.kube/config
              # this field is optional
              type: Directory
```

DISCLAIMER/HINT: this is a simple alpha state POC. In future version there will be a more secure/regulated example to access to the kubernetes api via roles and kubectl proxy https://kubernetes.io/docs/tasks/run-application/access-api-from-pod/


# Planned features

* (WIP) Restore Wizard
* (WIP) Neo4j support
* (Planned) Database auth via Docker/kubernetes Secrets
* (Planned) Email notification
* (Planned) Docker Event listener / Kubectl hooks to react to container started/stopped
* (Planned) Backup compression optional
* (Idea) Switch to https://github.com/kubernetes-client/python and https://docker-py.readthedocs.io/en/stable/ (or create alternative modules)
* (Idea) restore by label (checked/executed when pod starts via https://kubernetes.io/docs/concepts/containers/container-lifecycle-hooks/) (needs a metadata store :/ )
* (Idea) Matrix notifications   
* (Idea) [Podman](https://podman.io/) support. Your help is greatly appreciated. Should be easy or maybe no work at all
* (Idea) [LCX](https://linuxcontainers.org/) support. Help needed!
* (Idea) Suppord pod with more than one container https://kubernetes.io/docs/tasks/debug-application-cluster/get-shell-running-container/#opening-a-shell-when-a-pod-has-more-than-one-container
* (Idea) Provide auto-create params in https://kubernetes.io/docs/concepts/configuration/configmap/ instead of k8s annotation
* (Idea) Improve human readable output by printing a tree structure (https://www.baeldung.com/java-print-binary-tree-diagram)
* (Idea) Encrypt backups
# Current ToDo / Known Issues

* write docs
* Timestamp is not in current timezone?
* Write example with proper productive access to Kubernetes API


# limitations

## Auto database creation

* All databases in one instance/container must have the same encoding and collation. Atm there is no way of configuring this on a per database level
* All databases in one instance/container must share on backup user. Atm there is no way of having multiple users to access different databases in one instance/container


# Docker Volumes Pathes


- `/var/run/docker.sock:/var/run/docker.sock`
  Is needed to access the docker API to find database containers to be backed up



- `/.kube/config`
  Is needed to access the kubernetes API to find database containers to be backed up. to be refined in future version

# Dev Notes

https://kubernetes.io/docs/tasks/run-application/run-single-instance-stateful-application/

Start Test Rancher K8s

```
docker run -d \
--restart=unless-stopped \
-p 80:80 -p 443:443 \
--privileged \
--name rancher \
-v /var/run/docker.sock:/var/run/docker.sock \
rancher/rancher:stable
```