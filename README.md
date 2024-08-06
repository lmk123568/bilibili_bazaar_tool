# bilibili_bazaar_tool
基于 streamlit 的 b 站市集低价搜索工具

### 如何使用

下载打包压缩好的 [zip](https://github.com/lmk123568/bilibili_bazaar_tool/releases) 文件并解压，解压后双击运行 exe 文件

> ⚠ 请先登录 bilibili，获取 cookie，就可以利用该 cookie 模拟请求访问集市

### 如何打包

本项目用 pyinstaller 打包

```bash
pyinstaller -F --additional-hooks-dir=./hooks -i "bilibili-line.png" run_main.py
```

打包的关键点在于写好 hook，参考`./hooks/hook-streamlit.py`，将 streamlit 库以及 `main.py`、`bilibili.png` 等文件打包成单个 exe 文件
