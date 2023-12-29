from config import CONFIG

from .search_engine_plugin import SearchEnginePlugin as SearchEnginePlugin
from .realtime_news_plugin import RealtimeNewsPlugin as RealtimeNewsPlugin
from .run_python_code_plugin import RunPythonCodePlugin as RunPythonCodePlugin
from .realtime_time_plugin import RealtimeTimePlugin as RealtimeTimePlugin
from .reward_author_plugin import RewardAuthorPlugin as RewardAuthorPlugin
from .design_software_plugin import DesignSoftwarePlugin as DesignSoftwarePlugin

"""
OpenAi会根据自己的需要, 自动调用插件的内容, 你要做的就是根据规则创建插件和维护插件
    1.创建插件文件
    2.继承BasePlugin
    3.实现属性和方法
    4.添加到plugin_list
"""

plugin_list = [
    # 生产环境需要selenium和chrome支持
    # SearchEnginePlugin(),
    # RealtimeNewsPlugin(),
    # 危险系数较高，不建议生产环境运行
    # RunPythonCodePlugin(),

    # 获取当前时间
    RealtimeTimePlugin(),
    # 打赏作者
    RewardAuthorPlugin(),
    # 常用设计软件的下载
    DesignSoftwarePlugin()
]