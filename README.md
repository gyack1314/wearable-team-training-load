# 跨设备运动负荷归因与团队训练周计划

本项目保存本地演练业务资料及其输入检查工具。全部资料为合成记录，不包含真实用户资料。资料说明见 docs/data-contract.md，数值条款见 data/terms.json。

## 运行环境

使用 Python 3.11 标准库，无第三方运行依赖。Linux 容器基础镜像按摘要固定，支持离线使用已缓存镜像。

```sh
python -m inputkit data
python -m unittest discover -s tests -v
python -m compileall -q inputkit tests
```

输入工具只检查字段、数值类型、物理主键及声明的引用。它返回每类记录的数量，业务推断、办理结果和后续状态不由该检查判定。现有检查不覆盖新的业务能力。

## 容器运行

```sh
docker build -t local-service-inputs .
docker run --rm local-service-inputs
docker run --rm local-service-inputs python -m unittest discover -s tests -v
```

新的资料批次遵守相同列定义与单位。原始数据和合同记录应保留，运行期间生成的业务状态可使用独立目录，实际入口与使用说明随项目能力维护。
