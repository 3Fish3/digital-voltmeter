# 证据目录

本目录保存2026-10-23封装开发阶段的原始输出和结构化核验结果。文件由当前开发分支生成；未把`.tmp`、编辑器缓存或PCB数据加入版本控制。

| 文件 | 内容 |
| --- | --- |
| `workspace-status-before.txt`、`head-before.txt` | 开发开始前的工作区和基线提交 |
| `git-baseline.txt` | 开发分支、`origin/main`和PR #1提交号 |
| `pr1-*` | PR #1提交、实际差异、专用测试与补齐夹具后的24项测试输出 |
| `pr1-target-tests.log`、`pr1-full-tests-with-fixtures.log` | PR #1测试原始stdout/stderr合并日志 |
| `voltmeter-v2.3-draft.xml` | 开发后由KiCad 10.0.6导出的原生KiCad XML网表 |
| `component-inventory.json`、`label-inventory.json` | 用于回归比对的元件和标签清单；后两项由当前原理图与既有独立清单组成 |
| `netlist-verification.json` | 蓝图、XML、元件清单逐引脚比对结果 |
| `erc.json`、`erc.*.log` | ERC JSON及标准输出/错误输出 |
| `footprint-verification.json` | 61个已分配封装的解析、焊盘编号和孔径结构核对 |
| `j1-conflict.json`、`te-5787834-drawing-revC.png` | J1的TE Rev C图纸与KiCad封装孔位冲突记录及原图 |
| `open-item-assessments.md` | U1、F1/F2、M1、C3/C4 的完整评估与结论 |
| `datasheet-text/` | BAS116H、XD0832CC、Littelfuse 251 原厂PDF的文本提取（原始PDF的公开来源见评估文档，不入库以避免二进制与空白检查冲突） |
| `BAS116H-SOD123F-outline.png` | Nexperia SOD-123F 原厂封装图（本体3.6×1.7mm） |
| `TI-P8-PDIP-mechanical-4040082E.png`、`datasheet-text/TI-P-R-PDIP-T8-4040082E.txt` | TI P(R-PDIP-T8) 8脚PDIP原厂机械图与文本 |
| `j1-dimension-analysis.json` | J1 尺寸链像素测量记录（2.705+0.505=3.21mm） |
| `bom-crosscheck.json` | 逐位号BOM与网表中的封装、MPN、厂家交叉核对 |
| `field-diff-summary.json`、`field-changes.json` | 原理图相对基线只有封装/MPN/厂家/DesignStatus字段变化 |
| `native-bom.csv` | KiCad原生BOM导出，包含MPN、厂家和封装 |
| `regression-tests.log` | 21项测试原始日志 |
| `hardware-sha256-before.txt`、`hardware-sha256-after.txt` | 开发前后硬件文件完整哈希，供人工比较 |
| `hardware-change-summary.json` | 基线硬件文件的未变/变更/新增分类；排除本地会话文件 |

日志原样保留。记录中的`Found 0 violations`、`OK`或焊盘一致都只对应各自检查范围。
