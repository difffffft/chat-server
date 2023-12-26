# mchst-server

### 系统需求

```
Python >= 3.8
```

### 安装依赖

```cmd
创建虚拟环境
python -m venv venv

激活虚拟环境
venv\Scripts\activate

安装依赖
pip install -r requirements.txt
```

### 本地运行

```cmd
激活虚拟环境
venv\Scripts\activate

python main.py
```

### 生成依赖

```
pip freeze > requirements.txt
``` 

### 支持Dockerfile部署（不包含mysql和redis环境）

```
构建镜像
docker build -t chat-server .

运行容器
docker run -dit --name chat-server -p 8080:8080 chat-server
```