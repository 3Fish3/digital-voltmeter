# V2.3 真实元器件与封装开发记录

日期：2026-10-23（America/New_York）。开发分支：`feature/v2.3-real-footprints`。基线：`origin/main` 的 `138980f`。本阶段只完善原理图中的料号属性、封装分配和验证工具；没有创建 PCB、布线、Gerber 或采购订单。

## 完成范围

| 项目 | 结果 | 证据范围 |
| --- | --- | --- |
| 64个现有电路位号 | 60个已分配可解析封装，4个保留阻塞 | 见[逐位号BOM](component-footprint-bom.csv)和[焊盘核验](evidence/footprint-verification.json) |
| 封装种类 | 16种；其中5种为本项目专用封装 | 见[项目封装库说明](../../../hardware/v2.3/V23Draft.pretty/README.md) |
| 直插/贴片 | 53个直插；D1～D4、Q1、U4、U5为便于手焊的贴片 | 仍须实物试装，不以封装编号替代可焊性验证 |
| MPN/厂家属性 | 60个已分配位号已写入原理图的`MPN`、`Manufacturer`字段 | KiCad原生BOM见[evidence/native-bom.csv](evidence/native-bom.csv) |
| 连接 | 64元件、47命名网、183接线、5 NC、3供电声明未改变 | [网表核验](evidence/netlist-verification.json) |
| ERC | KiCad 10.0.6报告0项违规（沿用4项既有忽略规则） | [ERC原始JSON](evidence/erc.json)；不能证明电气性能 |
| 自动化 | 21项测试通过 | [原始日志](evidence/regression-tests.log) |
| PCB准入 | **未达到** | U1、M1、F1/F2、D1～D4仍阻塞；尚无PCB DRC和实物装配 |

## 已实施的封装

| 位号 | MPN | KiCad封装 | 关键依据 |
| --- | --- | --- | --- |
| U2 | MCP6002-I/P | `Package_DIP:DIP-8_W7.62mm` | Microchip DS20001733L，8脚PDIP、P2.54、7.62mm排距 |
| U3 | SN74AHCT125N | `V23Draft:TI_N14_PDIP-14_W7.62mm_P2.54mm` | TI N封装图MPDI002 Rev C，最大本体19.94×7.19mm；通用库庭院18.30mm不足，故建立专用封装 |
| U4 | SN74LVC1G125DBVR | `Package_TO_SOT_SMD:SOT-23-5_HandSoldering` | TI DBV 5脚、P0.95mm；采用加长手焊焊盘 |
| U5 | TPS2115APW | `Package_SO:TSSOP-8_4.4x3mm_P0.65mm` | TI PW0008A，本体4.3～4.5×2.9～3.1mm、P0.65mm |
| U6 | TL431BCLP | `V23Draft:TL431BCLP_TI_LP0003A_Inline_P1.27mm` | TI LP0003A/4215214-C：直引脚P1.27±0.13、孔0.85mm、本体最大5.21×4.19mm |
| Q1 | AO3401A | `V23Draft:AO3401A_SOT-23_GSD_HandSoldering` | 原厂1=G、2=S、3=D；封装焊盘直接命名为G/S/D，与现有符号一致 |
| Q2 | 2N3904BU | `V23Draft:2N3904BU_TO-92_Inline_EBC` | onsemi 1=E、2=B、3=C；TO-92直插、P1.27、孔0.75mm |
| J1 | TE 5787834-1 | `Connector_USB:USB_B_TE_5787834_Vertical` | Rev C图按2.50mm比例尺实测信号孔纵向中心距≈3.21mm（2.705+0.505链），与库3.2mm一致 |
| D1～D4 | BAS116H,115 | `Diode_SMD:D_SOD-123F` | 1=K/2=A与现有Device:D一致；25°C漏电5nA、150°C 80nA、VR75V、IF215mA、Ptot375mW；本体最大3.6×1.7mm，库庭院4.4×2.3mm |
| J2～J4 | Phoenix 1715721 | `TerminalBlock_Phoenix:...MKDS-1,5-2-5.08_1x02_P5.08mm_Horizontal` | 原厂P5.08、焊脚0.9×0.9、推荐孔1.3mm；库封装P5.08/孔1.3mm |
| J5～J7 | Samtec TSW-105/103/104-07-G-S | `Connector_PinHeader_2.54mm:PinHeader_1x0N_P2.54mm_Vertical` | 原厂0.025in方针、P2.54、-07直针A10.92/B2.54/C5.84mm |
| R1～R44（R6除外） | YAGEO MFR-25系列 | `Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal` | 本体L6.3±0.5、D2.4±0.2、线径0.55～0.60mm；孔0.8mm |
| R6 | YAGEO ZOR-25-R-52-0R | 同上轴向电阻封装 | ZOR-25专属尺寸L6.3±0.5、D2.3±0.3、线径0.60±0.05mm |
| C1/C2/C5～C9 | KEMET C320C104K5R5TA | `V23Draft:C320C104K5R5TA_Radial_L5.08mm_W3.18mm_P2.54mm` | L≤5.08、T≤3.18、H≤5.84、P2.54±0.78、F0.51mm；项目专用封装 |
| C3/C4 | Panasonic EEUFR1H100 | `Capacitor_THT:CP_Radial_D5.0mm_P2.00mm` | D5、L11、P2.0；有极性电容，装配须核对极性 |
| C10/C11 | KEMET R82DC3100AA50J | `Capacitor_THT:C_Rect_L7.2mm_W2.5mm_P5.00mm` | L7.2(+0.2/−0.5)、T2.5(+0.1/−0.5)、P5±0.4、线径0.5±0.05mm |

完整逐位号型号、厂家、封装和采购链接见[component-footprint-bom.csv](component-footprint-bom.csv)。列出的销售页面只证明公开料号存在，实时库存、批次和交期必须在采购前重新确认。

## 项目专用封装

新增项目库[V23Draft.pretty](../../../hardware/v2.3/V23Draft.pretty/)和[fp-lib-table](../../../hardware/v2.3/fp-lib-table)：

- `AO3401A_SOT-23_GSD_HandSoldering`：沿用KiCad已验证的手焊SOT-23几何，只把焊盘英文字母与AO3401A原厂1/2/3脚定义绑定。
- `2N3904BU_TO-92_Inline_EBC`：沿用KiCad已验证的TO-92 inline几何，焊盘E/B/C与onsemi 1/2/3脚定义绑定。
- `TL431BCLP_TI_LP0003A_Inline_P1.27mm`：P1.27，孔0.85mm；焊盘加大到1.5mm便于手焊，孔值采用TI示例。
- `C320C104K5R5TA_Radial_L5.08mm_W3.18mm_P2.54mm`：按KEMET最大本体与P2.54建立；孔0.8mm，适配0.51mm标称引线。
- `TI_N14_PDIP-14_W7.62mm_P2.54mm`：沿用DIP-14的P2.54/排距7.62与焊盘，按TI N封装扩大Fab/庭院到最大19.94mm本体。

自定义封装的KiCad SVG导出结果为成功：[导出日志](evidence/footprint-svg-export.log)。这些是待PCB阶段复核的设计输入，不是已完成的制造封装；生成SVG未纳入仓库。

C3/C4已按有极性铝电解的物理封装分配焊盘，但现有原理图仍使用`Device:C`无极性图符。网表脚1在`SYS_5V`/`VANA`、脚2在`GND`，与封装正负极方向相符；PCB前仍应将原理图图符或极性标识改为明确的有极性表示，并人工复核。

## 保留的4个阻塞位号

| 位号 | 原因 | 不会怎么做 |
| --- | --- | --- |
| U1 | TI ADC0832CCN/NOPB为停产PDIP-8；SOIC-14候选需要重建14脚图符且公开页缺货 | 不把14脚SOIC直接套到8脚图符，不替换ADC功能 |
| M1 | 具体Blue Pill克隆板、实际针宽/两排中心距、USB包络未实测；PA13/PA14只在独立SWD排针 | 不猜15.24mm或15.8mm为焊孔中心距，不省略SWD连接 |
| F1/F2 | 0251001.MXL为候选；熔断额定、I²t、启动浪涌及PICO II轴向焊脚成形未闭合 | 不用普通电阻封装代替保险丝 |

## 验证结果与证据

### PR #1 审查

PR #1 的隔离提交为`93fa411`，相对`origin/main`的`138980f`只增加检查工具、测试和说明，未改动硬件。专用测试4项通过，生成的名义/录入测试SVG均有40个中心标记；补齐`.tmp`网表夹具后全仓24项测试全部通过。未合并PR。

- [PR #1专用测试原始日志](evidence/pr1-target-tests.log)
- [PR #1全仓24项测试日志](evidence/pr1-full-tests-with-fixtures.log)
- [PR提交列表](evidence/pr1-commits.txt)及[差异统计](evidence/pr1-diffstat.txt)；完整差异可用`git diff origin/main...origin/pr-1`复现
- 工具限制：只输出针中心检查图，不生成焊盘、孔径、PCB或电源保护；`15.8mm`仍不能直接当中心距。

### 开发分支验证

| 检查 | 原始结果 | 说明 |
| --- | --- | --- |
| KiCad ERC | 0 violations，4项既有忽略规则 | [erc.json](evidence/erc.json)；不等于电气可用 |
| 原生网表 | 64元件、47网、183接线、5 NC、3供电声明；蓝图一致 | [netlist-verification.json](evidence/netlist-verification.json) |
| 封装/焊盘 | 60个已分配封装均可解析，焊盘编号与符号引脚一致；4个未分配 | [footprint-verification.json](evidence/footprint-verification.json)；不是DRC |
| BOM交叉核对 | 64行；60个已分配项的封装、MPN、厂家与网表字段一致 | [bom-crosscheck.json](evidence/bom-crosscheck.json) |
| 原理图字段差异 | 56个位号、175个字段变化；未发现Footprint/MPN/Manufacturer/DesignStatus以外的字段变化 | [field-diff-summary.json](evidence/field-diff-summary.json)、[逐项差异](evidence/field-changes.json) |
| 硬件文件差异 | 基线6个跟踪文件：5个未变、原理图1个变更；新增1个库表和6个封装/说明文件 | [hardware-change-summary.json](evidence/hardware-change-summary.json) |
| 回归测试 | 21项通过 | [regression-tests.log](evidence/regression-tests.log) |
| KiCad BOM | 成功导出含MPN/厂家/封装的BOM | [native-bom.csv](evidence/native-bom.csv) |

ERC忽略项为`single_global_label`、`four_way_junction`、`simulation_model_issue`、`footprint_filter`。封装已写入的原理图仍不能证明器件可采购、尺寸可安装、焊盘适合板厂工艺或整机性能满足要求。

### 复现命令

在仓库根目录先把本次归档的三项夹具复制到`.tmp/v2.3-validation/`：

```bash
mkdir -p .tmp/v2.3-validation
cp docs/reviews/2026-10-23-v2.3-footprint-development/evidence/voltmeter-v2.3-draft.xml .tmp/v2.3-validation/
cp docs/reviews/2026-10-23-v2.3-footprint-development/evidence/component-inventory.json .tmp/v2.3-validation/
cp docs/reviews/2026-10-23-v2.3-footprint-development/evidence/label-inventory.json .tmp/v2.3-validation/
```

随后导出、检查并运行测试：

```bash
kicad-cli sch export netlist --format kicadxml --output .tmp/v2.3-validation/voltmeter-v2.3-draft.xml hardware/v2.3/voltmeter-v2.3-draft.kicad_sch
kicad-cli sch erc --format json --units mm --severity-all --exit-code-violations --output /tmp/v23-erc.json hardware/v2.3/voltmeter-v2.3-draft.kicad_sch
PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify_v2_3_netlist.py --blueprint hardware/v2.3/connections-draft.json --netlist .tmp/v2.3-validation/voltmeter-v2.3-draft.xml --inventory .tmp/v2.3-validation/component-inventory.json
PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify_v2_3_footprints.py --netlist .tmp/v2.3-validation/voltmeter-v2.3-draft.xml
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p 'test_*.py' -v
```

PR #1的隔离检查命令为`PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_bluepill_fit_template.py -v`；全部原始输出在`evidence/`中，不依赖本次开发分支的改动。

## PCB设计准入

当前**未达到PCB设计准入**。阻断条件按优先级：

1. U1没有可追溯的在产采购版本与相应14脚图符，不能生成可信的ADC封装。
2. M1未取得本块Blue Pill的针宽/中心距、USB位置和底面高度；两条20针排母没有覆盖PA13/PA14。
3. D1～D4的双管封装拓扑需要用户审定，不能用当前四只单管图符蒙混。
4. F1/F2额定与专用轴向封装未闭合，不能在保险丝选型前定板。
5. 60个封装只完成了符号引脚/焊盘编号和资料层面对照；没有PCB DRC、板厂DRC、装配干涉或手工焊接验证。

下一步应先用实物确认M1，再决定U1/D1～D4/F1/F2方案；所有方案经用户审定后，才能进入PCB创建与布局。
