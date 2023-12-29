# chat-server

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

### 新增自己的插件
#### 0.确定自己的需求
```
比如我们要一个三阶魔方还原教程，GPT的回答通常很垃圾，我们就需要定制插件
```

#### 1.新建一个插件文件，放到plugins目录下
#### three_rubik_cube_course_plugin.py
```python
import json

from .base_plugin import BasePlugin


class ThreeRubikCubeCoursePlugin(BasePlugin):

    def __init__(self):
        super().__init__()
        self.name = "three_rubik_cube_course"
        self.description = "Third Order Rubik's Cube Reduction Tutorial"
        self.params = {
            "type": "object",
            "properties": {},
        }

    def start(self, params):
        return json.dumps({
            "code": 0,
            "data": {
                '第一步': "https://v.douyin.com/i8sfHhmC",
                '第二步': "https://v.douyin.com/i8sfWfDo",
                '第三步': "https://v.douyin.com/i8sPdLH9",
                '第四步': "https://v.douyin.com/i8sP2XE3",
                '第五步': "https://v.douyin.com/i8sP6yDe",
                '第六步': "https://v.douyin.com/i8sPr3us",
                '第七步': "https://v.douyin.com/i8sPrHcN",
            },
            "message": "success"
        })
```

#### 2.注册到GPT
```python
# 在plugins文件夹下，有个__init__.py文件
from .three_rubik_cube_course_plugin import ThreeRubikCubeCoursePlugin as ThreeRubikCubeCoursePlugin

plugin_list = [
    ...,
    
    # 魔方还原教程
    ThreeRubikCubeCoursePlugin()
]
```

#### 3.我们已经完成了插件的编写和注册，你可以去问一下GPT，魔方还原的教程是什么