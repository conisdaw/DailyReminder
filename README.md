# DailyReminder

DailyReminder这个是我昨天晚上突发奇想做的，就做了这个项目。

该项目使用Python 3.12.4开发。

## 如何使用

### 前期准备

去[阿里云百炼](https://click.aliyun.com)获取API_KEY，在钉钉创建一个群，添加自定义机器人获取dingtalk_webhook，安全配置可以直接使用IP地址

### 使用

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python ./main.py
```

