# 新版STM32＋ADC0832双通道电压表

这是现有仓库内的新版硬件工作目录，不是另建独立项目。新版资料、原理图、PCB和后续BOM集中在此，旧工程保持原位供参考，不覆盖、不直接沿用旧连接。

## 当前版本

- **当前本地最新设计：V2.3受控原理图草案**，工程位于 `hardware/v2.3/`。
- 文档同步不升级设计版本；V2.0～V2.2保留为历史候选或背景依据，不与V2.3混成采购版本。
- 尚未定稿：封装未定、无PCB、无新版采购BOM；保护与精度验证仍未完成，禁止投板。
- 远端同步状态以实际提交与推送核验为准；Git提交和仓库发布不升级设计版本，也不表示硬件已验收。

## 从这里开始

1. [V2.3受控原理图审查报告](docs/V2.3-controlled-schematic-review.md)、[继续整改依据](docs/V2.3-followup-evidence.md)：最新入口，现有ERC预设为0项，P0仍未关闭，禁止投板。
2. [原理图PDF](hardware/v2.3/review/voltmeter-v2.3-draft.pdf)、[KiCad项目](hardware/v2.3/voltmeter-v2.3-draft.kicad_pro)、[逐节点表](docs/v2.3-node-connections.md)：用于连接审查，不是封装或采购定稿。
3. [V2.2设计决策](docs/V2.2-design-decisions.md)、[参考误差预算](docs/reference_accuracy_budget.md)、[输入保护](docs/input_protection_circuit.md)、[电源最坏情况](docs/power_path_worst_case.md)：完整背景与计算前提。
4. [V2.1预算](docs/power-front-end-review-v2.1.md)、[V2.0-R0报告](docs/digital-voltmeter-v2-design-review.md)：历史候选，不与新图混成一个BOM。
5. [硬件候选方案](docs/hardware-v2-proposal.md)、[开源调研](docs/open-source-reuse-survey.md)：背景及证据边界。

## 目录

- `docs/`：设计报告与持续维护的审查资料。
- `references/datasheets/`：已取得的芯片资料及TL431应用说明；新增Diodes BAV199原厂PDF、STM32的Rev17第三方镜像（不是Rev20）。不能据此代替最终采购厂商资料。
- `hardware/v2.3/`：独立KiCad草案、局部图符库、JSON连接蓝图和审查PDF；无PCB。
- `scripts/`：预算计算和导出网表核对；核对脚本使用本机已有defusedxml，不代表仿真或实测。
- `tests/`：网表核对脚本的回归测试，依赖本地导出网表及MCP清单。
- `.tmp/calculations/`：可重建的前端候选计算。
- `.tmp/migration-manifest.json`：本次六项资料迁移记录及迁移时SHA-256，用于校验和恢复。文档随后进行了路径更新，最终哈希另记录在该清单中。

## 工具测试与本地验证数据

在本仓库根目录运行 `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_reference_sampling_budget.py -v`。当前本地20项工具测试通过：参考/采样预算11项、网表核对9项；这是算术与核对工具回归，不是硬件验收。网表核对依赖Python包 `defusedxml`，本次未新增安装依赖。

`.tmp/` 不随本次提交上传；本仓库为工作目录的发布快照。完整网表测试还需先在本地准备本仓库 `.tmp/v2.3-validation/` 中与当前原理图对应的 `voltmeter-v2.3-draft.xml`（KiCad导出）、`component-inventory.json` 和 `label-inventory.json`（MCP清单）。仅克隆仓库不足以运行这9项测试；缺少数据时会报错，不跳过检查。无需这些临时数据的预算测试可在本仓库根目录单独运行，命令见上文；完整20项含网表核对需上述本地临时数据。

## 固定需求

STM32＋ADC0832；两路0～5V单极性；输入阻抗≥1MΩ；≥20Hz完整双通道帧；五组平均次数实验；优先常见直插器件，必要处允许易焊贴片；新版独立USB口与外部5V，需防回灌。输入共地，不是电气隔离，不用于市电。

## 状态与下一步

现行使用边界见[掉电隔离范围](docs/poweroff-isolation-scope.md)：先烧录调试，再断开调试器，使用独立电源测量；不新增隔离芯片，维持既有64元件草案。带电SWD/TTL等外设在掉电主板上长连不属于允许使用状态；核心板原USB不与独立测量电源并接，不以物理遮挡/隔断或新增总线隔离作为必做项。两路输入限流钳位、电源防反接及双源互灌保护仍属硬件验收范围，PA0等板内异常掉电路径仍待验证。

以下原理图导出与ERC结果为既有记录，本次未重跑电气验证；推送前工具测试的本地结果与前置条件见上节。

已有V2.3受控原理图草案：64电路图符＋3个手动供电声明、47命名网、183已接电路引脚；实际导出一致、9项核对工具测试通过。核实正常供电来源并逐项声明后，原生ERC按现有预设为0项违规；P0未关闭，封装为空、未采购、不投板。参考监测方向及适配器供电已确认，准确器件、低端、输入保护、板内异常掉电与电源回流、原厂采样条件和实物性能仍需关闭。未完成SPICE或实物验收；尚无PCB，不适用PCB DRC。

旧工程与旧版清单不在本仓库发布范围内；`.tmp/` 为本地工作目录，不作为新版长期工程文件。
