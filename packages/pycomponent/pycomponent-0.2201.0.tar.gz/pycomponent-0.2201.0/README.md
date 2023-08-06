# pycomponent: Python 工程组件
- 即插即用
- version 采用 `v0.{arxiv月份}.{从0开始依次加1}`, 方便找到对应的某个版本
- 安装: `pip3 install pycomponent`

```bash
├── data_collect.py    # 数据收集/回流模块, 可以配置两种限制 1.剩余磁盘空间 2.收集的数目
├── dir_as_dict.py     # 把文件夹转换为 base64 的 json
└── transport_pack.py  # 把 obj 转换 pickle, 通过 msgpack 以二进制形式高效传输
```


