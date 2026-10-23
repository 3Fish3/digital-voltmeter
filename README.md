# STM32＋ADC0832双通道数字电压表

课程设计项目：两路共地0～5V直流采集，使用STM32与ADC0832，配套显示、串口及平均降噪实验。文档按目标、进度和现行设计三个用途维护。

## 当前版本

当前为**V2.3受控原理图草案**，工程位于`hardware/v2.3/`。封装、采购BOM和PCB尚未定稿；保护、精度及实物验证仍待完成，当前不投板。最新状态与检查证据统一记录在进度文档。

## 从这里开始

1. [项目最初目标](docs/project-goals.md)：课程目的、原始功能和验收来源。
2. [当前进度与问题](docs/progress.md)：完成情况、问题及关闭条件、验证记录和下一步。
3. [最新设计报告](docs/design-report.md)：当前电路、接口、参数、预算与完整网络表。

维护方式见[文档导航](docs/README.md)。每次设计更新后完整重写同一份设计报告，变更过程与问题记入进度。

## 目录

- `docs/`：三份主文档、[逐引脚CSV](docs/pin-connections.csv)、旧BOM与阶段交接。
- `hardware/v2.3/`：KiCad草案、局部图符库、连接蓝图和[原理图PDF](hardware/v2.3/review/voltmeter-v2.3-draft.pdf)。
- `references/datasheets/`：本地数据手册和应用说明。
- `scripts/`、`tests/`：条件预算、网表核对工具及回归测试。
- `pictures/`：旧版板卡渲染、理想前端仿真图和Gerber包；与V2.3工程区分使用。
- `.tmp/`：本地计算、验证数据和文档整理快照，由`.gitignore`排除。

## 工具测试与本地验证数据

在仓库根目录可运行独立预算测试：

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_reference_sampling_budget.py -v
```

本次11项预算测试通过。另9项网表测试依赖`defusedxml`及`.tmp/v2.3-validation/`中的KiCad导出XML、独立元件清单与标签清单，当前缺少这三个文件。完整测试的前置条件、命令和证据范围见[进度验证记录](docs/progress.md#4-验证记录与复现)。
