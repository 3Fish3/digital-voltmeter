# 双通道数字电压表项目交接文档

版本：V2.0  
日期：2026-09-20  
用途：将本文件和最新 KiCad 文件一起交给新的 ChatGPT/Codex 对话，继续完成原理图复核、模块化整理、PCB 布局布线与生产前检查。

---

## 1. 给新对话的直接任务指令

请继续处理我的双通道数字电压表 KiCad 项目。先阅读本交接文档，再检查我上传的最新工程文件；不要从零重新设计，也不要覆盖已经完成的修改。

工作要求：

1. 先用 KiCad 实际打开最新 `.kicad_sch`，确认没有解析错误。
2. 运行 ERC，并逐项解释错误和警告；不要直接批量忽略。
3. 核对 STM32F103C8T6 Blue Pill 模块 J1 的 40 针映射与自定义封装。
4. 核对全部元件的值、符号、封装和极性。
5. 将原理图按电源、MCU、ADC、两路模拟前端、显示、UART、输入端子分区整理，使其像独立模块一样易读，但不要改变已经确定的电气连接。
6. 完成 PCB 后运行 DRC，检查模块间距、USB 插拔空间、端子方向、丝印和安装可操作性。
7. 无法从文件确认的机械尺寸必须要求我测量实物，不得凭空保证。
8. 未通过 ERC、DRC、实物尺寸核对和样机测试前，不得声称设计“保证可用”。

优先目标：先让原理图可以稳定打开并通过关键电气检查，再进行美化和 PCB。

---

## 1.1 应随交接文档一起提供的文件

优先把下面的完整压缩包上传到新对话：

```text
STM32F103C8T6-BluePill-KiCad-package-v2.zip
```

压缩包内应包含：

```text
digital-voltmeter-pcb(2).kicad_sch
fp-lib-table
DigitalVoltmeter.pretty/
└── BluePill_STM32F103C8T6.kicad_mod
STM32F103C8T6-BluePill-design-notes.md
```

原理图单独文件名为：

```text
digital-voltmeter-pcb(2).kicad_sch
```

应使用已经修正 Blue Pill 内部符号前缀的最新版本。不要使用浏览器先前自动重命名的旧副本，例如：

```text
digital-voltmeter-pcb(2) (1).kicad_sch
```

---

## 2. 项目目标

项目是一台课程设计级双通道数字电压表：

- 两路 `0～5 V DC` 单端输入；
- 两路共地、非隔离；
- 控制器为 STM32F103C8T6 Blue Pill 模块；
- ADC 为 ADC0832，双通道、8 位；
- MCP6002 双运放作为两路输入缓冲；
- 74AHCT125 用于 ADC 数字接口缓冲和电平处理；
- OLED 显示；
- UART 与上位机通信；
- BNC 为面板安装，通过短同轴线接到 PCB 上的两位端子；
- 主电源为稳定 `+5 V`；
- Blue Pill 使用 3.3 V 逻辑；
- ADC 电源经 FB1 滤波形成 `ADC_5V`。

ADC0832 的名义分辨率：

```text
5 V / 256 = 19.53125 mV/LSB
```

课程验收可暂定为室温、预热和校准后，全量程误差约不超过 `±50 mV`，但这只是目标，不是已经实测得到的性能。

---

## 3. 已确定的电气结构

### 3.1 两路模拟前端

两个通道应保持完全对称：

```text
BNC/输入端子
    ↓
10 kΩ 串联限流
    ↓
输入节点 ── 10 MΩ ── GND
    │
    ├── 1N4148 钳位到 +5 V
    └── 1N4148 钳位到 GND
    ↓
MCP6002 电压跟随器
    ↓ BUF_CHx
3.3 kΩ 串联电阻
    ↓ ADC_CHx
1 µF 对地
    ↓
ADC0832 输入
```

关键要求：

- 运放输出网和 ADC 输入网必须分开；
- 3.3 kΩ 电阻不能被导线旁路；
- 运放反馈必须从运放输出直接回本通道反相输入，不能跨过 3.3 kΩ；
- 建议网络名为 `BUF_CH1`、`BUF_CH2`、`ADC_CH1`、`ADC_CH2`。

### 3.2 ADC0832 与电源

- U1：ADC0832，DIP-8；
- 主 `+5V` 经 FB1 到 `ADC_5V`；
- C2 10 µF 和 C3 100 nF 应跨接 `ADC_5V` 与 GND；
- FB1 应使用低直流电阻磁珠，不能随意用大电阻代替；
- ADC 电源同时影响测量满量程，调试时应测量 ADC 实际供电电压。

### 3.3 74AHCT125 数字接口

U2 使用 74AHCT125，供电为 +5 V：

- 三路缓冲 STM32 发往 ADC 的 `CS`、`CLK`、`DI`；
- 第四路缓冲 ADC 返回的 `DO`；
- `/OE` 为低有效，固定使能时应接 GND；
- U2 电源单元必须连接 +5 V 与 GND；
- C6 100 nF 应靠近 U2 电源脚。

使用的网络：

| 网络名 | 用途 |
|---|---|
| `ADC_CS_3V3` | STM32 侧片选 |
| `ADC_CLK_3V3` | STM32 侧时钟 |
| `ADC_DI_3V3` | STM32 到 ADC 数据 |
| `ADC_DO_5V` | ADC DOUT 至 U2D 输入 |
| `ADC_DO_BUF_5V` | U2D 输出至分压上臂 |
| `ADC_DO_3V3` | 分压中点至 STM32 |

DO 返回路径：

```text
ADC0832 DOUT
→ ADC_DO_5V
→ U2D
→ ADC_DO_BUF_5V
→ R7 10 kΩ
→ ADC_DO_3V3
→ STM32 PB14
```

R8 为 20 kΩ，下接 GND，与 R7 构成 5 V 到约 3.3 V 的分压。

默认状态电阻：

| 位号 | 数值 | 连接要求 |
|---|---:|---|
| R11 | 100 kΩ | `ADC_DO_5V` 下拉至 GND |
| R12 | 10 kΩ | `ADC_CS_3V3` 上拉至 +3.3 V |
| R13 | 100 kΩ | `ADC_CLK_3V3` 下拉至 GND |
| R14 | 100 kΩ | `ADC_DI_3V3` 下拉至 GND |

### 3.4 外部接口

- J4：OLED 四针接口；必须根据购买的 OLED 模块确认 VCC/GND/SCL/SDA 顺序；
- R9/R10：I²C 上拉 4.7 kΩ；若 OLED 模块自带合适上拉，可标为 DNP；
- J5：UART 四针接口，默认只使用 GND、TX、RX，剩余电源脚保持 NC，防止两个电源互顶；
- J6：两位主电源端子；
- J7/J8：两路面板 BNC 转接端子，每个端子一脚信号、一脚 GND。

---

## 4. STM32F103C8T6 的使用方式

本项目插入的是完整的 **STM32F103C8T6 Blue Pill 开发板模块**，不是裸 STM32F103C8T6 LQFP48 芯片。

如果后续改成裸芯片，则当前 J1 符号和封装全部不能使用，必须重新设计最小系统，包括 3.3 V 电源、去耦、复位、BOOT0/BOOT1、SWD、时钟和 LQFP48 封装。

### 4.1 J1 的 40 针映射

| J1 | Blue Pill | J1 | Blue Pill |
|---:|---|---:|---|
| 1 | VBAT | 2 | +3V3 |
| 3 | PC13 | 4 | GND |
| 5 | PC14 | 6 | +5V |
| 7 | PC15 | 8 | PB9 |
| 9 | PA0 | 10 | PB8 |
| 11 | PA1 | 12 | PB7 |
| 13 | PA2 | 14 | PB6 |
| 15 | PA3 | 16 | PB5 |
| 17 | PA4 | 18 | PB4 |
| 19 | PA5 | 20 | PB3 |
| 21 | PA6 | 22 | PA15 |
| 23 | PA7 | 24 | PA12 |
| 25 | PB0 | 26 | PA11 |
| 27 | PB1 | 28 | PA10 |
| 29 | PB10 | 30 | PA9 |
| 31 | PB11 | 32 | PA8 |
| 33 | NRST | 34 | PB15 |
| 35 | +3V3 | 36 | PB14 |
| 37 | GND | 38 | PB13 |
| 39 | GND | 40 | PB12 |

项目当前关键连接：

| 功能 | MCU 引脚 | J1 |
|---|---|---:|
| +3.3 V | +3V3 | 2 |
| GND | GND | 4 |
| +5 V | +5V | 6 |
| OLED SDA | PB7 | 12 |
| OLED SCL | PB6 | 14 |
| UART RX | PA10 | 28 |
| UART TX | PA9 | 30 |
| ADC DI | PB15 | 34 |
| ADC DO | PB14 | 36 |
| ADC CLK | PB13 | 38 |
| ADC CS | PB12 | 40 |

### 4.2 Blue Pill 自定义封装

项目库：

```text
DigitalVoltmeter.pretty
```

封装：

```text
DigitalVoltmeter:BluePill_STM32F103C8T6
```

当前采用的名义尺寸：

- 模块 PCB：23 mm × 53 mm；
- 两排各 20 针；
- 纵向针距：2.54 mm；
- 两排中心距：17.78 mm；
- 通孔焊盘：2.0 mm；
- 钻孔：1.0 mm；
- USB 位于 1/2 脚一端；
- 封装包含 USB 方向丝印和扩展 Courtyard。

这些尺寸来自常见 Blue Pill 板型。克隆板可能不同，制板前必须测量手中实物，重点确认两排中心距、板长、板宽、USB 突出方向、复位键位置和背面元件高度，并打印 1:1 纸样试插。

### 4.3 Blue Pill 电源风险

常见 Blue Pill 的 +5 V 针与 USB 5 V 直接连接。不要同时使用 USB 供电和 PCB 外部 +5 V 供电，除非已经确认具体模块有可靠的隔离或防反灌设计。

---

## 5. 已经完成的修改

以下内容已经写入最新原理图文件，但新对话仍应在 KiCad 中复核：

1. 主电源网络统一使用 `+5V`。
2. ADC 的 DI、DO、CLK、CS 网络名已统一。
3. 两路模拟前端的 3.3 kΩ 串联电阻与 ADC 输入电容结构已按设计意图调整。
4. FB1 改为磁珠用途。
5. J5 UART 电源脚保持 NC。
6. U2D 用于 ADC DO 返回缓冲，R7/R8 构成分压。
7. 增加 R11～R14 默认状态电阻。
8. 大部分通孔元件已设置封装。
9. 错误地分配给 `#PWR02` 的 TQFP-44 封装已清除，并将其修正为 +5 V 电源符号。
10. J1 从通用 2×20+MountingPin 连接器改为项目专用 Blue Pill 40 针符号。
11. J1 的 MP 引脚已删除。
12. J1 已绑定项目专用 Blue Pill 封装。
13. J1 内部引脚名已改为实际 Blue Pill 功能名。
14. 已创建 `fp-lib-table` 和 `DigitalVoltmeter.pretty`。

---

## 6. 最近发生的 KiCad 解析错误

旧下载文件曾出现错误：

```text
无效的符号单元名前缀
Conn_02x20_Odd_Even_MountingPin_1_1
```

原因：外层符号已改名为：

```text
DigitalVoltmeter:BluePill_STM32F103C8T6
```

但内部图形单元仍保留旧连接器前缀。

最新文件已经把内部单元修正为：

```text
BluePill_STM32F103C8T6_1_1
```

文本级检查结果：

- 旧错误前缀已从自定义符号中移除；
- KiCad S-expression 括号平衡；
- 自定义符号有 40 个引脚；
- 引脚功能与预期映射一致；
- 自定义封装有 40 个唯一焊盘；
- 焊盘编号完整覆盖 1～40；
- 压缩包完整性测试通过。

注意：这些是文本结构检查。当前执行环境没有 `kicad-cli`，所以没有完成原生 KiCad 解析、ERC 或 DRC。新对话必须首先实际打开文件验证。

浏览器可能把重复下载文件重命名为：

```text
digital-voltmeter-pcb(2) (1).kicad_sch
```

不要继续使用含旧错误的下载副本。应重新下载最新项目包并解压到新目录，避免系统继续打开旧文件。

---

## 7. 当前封装表

| 元件 | 当前/推荐封装 |
|---|---|
| U1 ADC0832 | `Package_DIP:DIP-8_W7.62mm` |
| U2 74AHCT125 | `Package_DIP:DIP-14_W7.62mm` |
| U3 MCP6002 | `Package_DIP:DIP-8_W7.62mm` |
| R1～R14 | `Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal` |
| D1～D4 | `Diode_THT:D_DO-35_SOD27_P7.62mm_Horizontal` |
| C1、C4，1 µF | `Capacitor_THT:C_Disc_D5.0mm_W2.5mm_P5.00mm`，采购前核实实际器件尺寸 |
| C3、C5、C6，100 nF | `Capacitor_THT:C_Disc_D5.0mm_W2.5mm_P5.00mm` |
| C2、C8，10 µF | `Capacitor_THT:CP_Radial_D5.0mm_P2.00mm` |
| C7，100 µF | `Capacitor_THT:CP_Radial_D6.3mm_P2.50mm` |
| J1 Blue Pill | `DigitalVoltmeter:BluePill_STM32F103C8T6` |
| J4 OLED | `Connector_PinSocket_2.54mm:PinSocket_1x04_P2.54mm_Vertical` |
| J5 UART | `Connector_PinSocket_2.54mm:PinSocket_1x04_P2.54mm_Vertical` |
| J6/J7/J8 | `TerminalBlock_Phoenix:TerminalBlock_Phoenix_MKDS-1,5-2_1x02_P5.00mm_Horizontal` |
| FB1 | 暂用轴向通孔封装，采购前按实际磁珠尺寸修改 |

---

## 8. 下一步必须完成的工作

### 8.1 第一优先级：文件与 ERC

1. 在新目录解压最新完整项目包。
2. 用本地 KiCad 打开 `.kicad_sch`。
3. 若仍报符号解析错误，记录完整错误、行号和 KiCad 版本，不要盲目重新命名整个符号。
4. 确认 J1 值为 `BluePill_STM32F103C8T6`。
5. 确认 J1 封装为 `DigitalVoltmeter:BluePill_STM32F103C8T6`。
6. 运行 ERC，保存报告。

### 8.2 第二优先级：电气复核

- 检查 R5/R6 是否确实串接在 `BUF_CHx` 与 `ADC_CHx` 之间；
- 检查两路 MCP6002 反馈没有交叉；
- 检查 U2 和 U3 的隐藏/独立电源单元；
- 检查 U2 四个 `/OE` 状态；
- 检查 U2D 输入输出方向；
- 检查 R7/R8 分压连接；
- 检查 ADC0832 模式引脚；
- 检查 C2/C7/C8 极性；
- 检查 D1～D4 方向；
- 检查 J4、J5、J6、J7、J8 实物针序；
- 检查所有 NC 标志只位于确实不用的引脚。

### 8.3 第三优先级：模块化整理

在不改变电气连接的前提下，把原理图分成以下区域：

1. 电源输入和滤波；
2. Blue Pill MCU 模块；
3. ADC0832 与数字缓冲；
4. 通道 1 模拟前端；
5. 通道 2 模拟前端；
6. OLED；
7. UART；
8. 外部输入端子。

区域之间优先用清晰网络标签连接，避免长导线穿过整个页面。两路模拟前端的布局应保持镜像或上下对齐，便于比较。

### 8.4 第四优先级：PCB

- 按实际 Blue Pill 测量值确认 J1 封装；
- 为 USB 插头、复位键和跳帽留出操作空间；
- 模拟输入与数字时钟走线分开；
- 100 nF 去耦尽量靠近芯片电源脚；
- ADC 输入 RC 元件靠近 ADC；
- 端子放在板边并标注 CH1/CH2、SIG/GND、+5V/GND；
- 有极性电容、二极管和电源端子必须有清晰丝印；
- 完成后运行 DRC；
- 输出 Gerber 前进行 1:1 打印试装。

---

## 9. 需要新对话交付的结果

最终希望得到：

- 可以正常打开的 KiCad 工程；
- 模块化整理后的原理图；
- ERC 报告及剩余警告说明；
- 元件值、符号、封装检查表；
- J1 针号—Blue Pill 引脚—网络名映射表；
- 经实物尺寸确认的 Blue Pill 封装；
- 原理图 PDF；
- PCB 文件；
- DRC 报告；
- Gerber 与钻孔文件；
- 生产前检查清单；
- 上电、校准、双通道测量与误差测试步骤。

---

## 10. 资料来源

- STMicroelectronics，STM32F103x8/xB 数据手册：  
  <https://www.st.com/resource/en/datasheet/stm32f103c8.pdf>
- STM32-base，Blue Pill 板型、尺寸、引脚表及供电提示：  
  <https://stm32-base.org/boards/STM32F103C8T6-Blue-Pill.html>

---

## 11. 安全和保证范围

- 本项目输入为 0～5 V DC、共地、非隔离；
- 当前钳位结构只能称为有限误接保护；
- 未做专项测试前，不应宣称能够安全承受 ±12 V；
- 首次通电应使用限流电源，建议先限制在 100～200 mA；
- 通电前检查 +5 V、+3.3 V、GND 是否短路；
- 不要默认所有 STM32 GPIO 都能承受 5 V；
- 不要同时通过 USB 和 PCB 外部 +5 V 给 Blue Pill 供电；
- 文本检查、ERC、DRC、实物尺寸验证和样机测试缺一不可。
