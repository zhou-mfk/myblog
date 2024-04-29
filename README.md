# myblog

use python flask build a self blog system.

### poetry

use poetry manager python packages. you can use:

```shell
pip install poetry
```

or

```shell
pipx install poetry
```

use poetry install python dependencies package

```shell
poetry install
```

### pre-commit

use pre-commit check python code style.

```shell
pip install pre-commit
# or
pipx install pre-commit
```

In you project you use command init pre-commit hook at first.

```shell
pre-commit install
```

**.pre-commit-config.yaml** is a config use pre-commit. you can read details.

### mysql

mysql command use podman

```shell
podman run -itd -e TZ="Asia/Shanghai" -p 3306:3306 --privileged=true --mount type=bind,src=./mysql_data/data,dst=/var/lib/mysql -e MYSQL_USER=admin -e MYSQL_PASSWORD=redhat -e MYSQL_ROOT_PASSWORD=redhat --restart=always --name=mysql57 registry.access.redhat.com/rhscl/mysql-57-rhel7:latest
```

进入容器

```shell
podman exec -it mysql57 /bin/bash
```

连接 mysql

```shell
mysql -uroot -p
```

mysql command

```sql
--- 建库
create database myblog default character set utf8mb4 collate utf8mb4_unicode_ci;
create database test_myblog default character set utf8mb4 collate utf8mb4_unicode_ci;

--- 授权
grant all privilege on myblog.* to admin@'%';
grant all privilege on test_myblog.* to admin@'%';

```

### flask command

```shell
# in fish
set FALSK_APP wsgi.py
```

```shell
flask run
```
