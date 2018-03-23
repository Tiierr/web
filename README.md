# Simple API Server with Flask

## 简介

本项目是使用 flask 搭建一个 web 应用，提供了 5个 api接口。包括:

- 注册接口
- 登录接口
- 获取登录用户信息接口
- 修改用户登录信息接口
- 退出登录接口

登录 api 接口可选是否保存登录状态，默认保存1天，可选保存7天。

同一用户最多在3台不同设备进行登录。

## 开发环境

- deepin linux
- mongodb 2.6.0
- redis 4.0.1
- python 3.6.2

首先克隆该项目到你的 VPS 上：

```
$ cd /home
$ git clone https://github.com/RayYu03/web
```

安装并激活虚拟环境：

```
$ cd web
$ virtualenv --no-site-packages venv
$ source venv/bin/activate
```

安装依赖：

```
(venv) $ pip3 install -r requirements.txt
```

配置 config:

```
(venv) $ vim config.py
```

启动:

```
(venv) $ python3 manage.py runserver
```

## 用法


### 注册用户

其中 `username` 和 `password` 为必填参数

```
curl -i -H "Content-Type: application/json" -X POST -d '{"username":"rayyu","password":"rayyu"}' http://localhost:5000/api/register
```
![注册用户](http://ww1.sinaimg.cn/large/647dc635ly1fpmo9z0362j20sr095my6.jpg)

### 登录用户

其中 `username` 和 `password` 为必填参数, `days` 为可选参数（只能填7）

```
curl -i -H "Content-Type: application/json" -X POST -d '{"username":"rayyu","password":"rayyu"}' http://localhost:5000/api/login
```

![](http://ww1.sinaimg.cn/large/647dc635ly1fpmoaap9d0j20ss0bd75u.jpg)

登录成功会生成 `token`, 该 `token` 同时会添加到用户的信息中。

若用户产生的 `token` 数目已经超过三个, 则不允许该用户再进行登录，只能通过 `token` 进行访问,
或者注销后再进行登录。

### 查看用户信息

查看用户信息要使用登录时生成的 `token`

```
curl -i -H "Content-Type: application/json" -X  POST -d '{"token":"eyJhbGciOiJIUzI1NiIsImlhdCI6MTUyMTc4MDY3NywiZXhwIjoxNTIxODY3MDc3fQ.eyJ1c2VybmFtZSI6InJheXl1In0.RplvI0VaiXzRVcZ4ObffFY4ss11WLCbtJFRE7_sNPWA"}' http://localhost:5000/api/info
```
![查看用户信息](http://ww1.sinaimg.cn/large/647dc635ly1fpmobd5n16j20sw0aign0.jpg)

### 修改用户年龄

修改用户年龄要使用登录时生成的 `token` , 同时还需要 `age` 参数

```
curl -i -H "Content-Type: application/json" -X  POST -d '{"token":"eyJhbGciOiJIUzI1NiIsImlhdCI6MTUyMTc4MDY3NywiZXhwIjoxNTIxODY3MDc3fQ.eyJ1c2VybmFtZSI6InJheXl1In0.RplvI0VaiXzRVcZ4ObffFY4ss11WLCbtJFRE7_sNPWA", "age": 15 }' http://localhost:5000/api/update/age
```

![修改用户年龄](http://ww1.sinaimg.cn/large/647dc635ly1fpmobtb5pzj20sy09sdh7.jpg)

### 注销用户

注销用户要使用登录时生成的 `token`

```
curl -i -H "Content-Type: application/json" -X  POST -d '{"token":"eyJhbGciOiJIUzI1NiIsImlhdCI6MTUyMTc4MDY3NywiZXhwIjoxNTIxODY3MDc3fQ.eyJ1c2VybmFtZSI6InJheXl1In0.RplvI0VaiXzRVcZ4ObffFY4ss11WLCbtJFRE7_sNPWA"}' http://localhost:5000/api/logout
```

![注销用户](http://ww1.sinaimg.cn/large/647dc635ly1fpmoc369sbj20ss09sjsq.jpg)

注销用户时，会将用户的当前的 `token` 删除。

注销前：

![注销前](http://ww1.sinaimg.cn/large/647dc635ly1fpmoddftgaj20su0910tq.jpg)

注销后：

![注销后](http://ww1.sinaimg.cn/large/647dc635ly1fpmodqtbzuj20sn07c3z1.jpg)
