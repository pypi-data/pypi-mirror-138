# YOLO to MongoDB

将 YOLO 格式的标注数据存入 MongoDB 数据库的小工具.

## 本地开发

```bash
python3 -m venv env
pip install -r requirements.txt
```

### 测试数据

将测试导入的数据放在 *demo/* 目录下.

### 安装调试

```bash
pip install -U -e .
yolo-to-mongo
```

### 发布命令

```bash
python setup.py sdist
yolo-to-mongo
```
