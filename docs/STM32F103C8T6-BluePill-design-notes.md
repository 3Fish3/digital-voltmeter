# STM32F103C8T6 Blue Pill 模块设计说明

修订：2026-09-21 联合审查版。仅同步验证边界，未修改符号或封装。

本文件对应项目中的 `J1`。这里插入的是完整的 **STM32F103C8T6 Blue Pill 开发板模块**，不是裸 STM32F103C8T6 芯片。

## 已完成内容

- J1 已改为项目内嵌符号 `DigitalVoltmeter:BluePill_STM32F103C8T6`。
- J1 已绑定项目封装 `DigitalVoltmeter:BluePill_STM32F103C8T6`。
- 删除了原通用连接器的 Mounting Pin/MP 引脚。
- 40 个符号引脚已改成 Blue Pill 的实际功能名。
- 创建了项目封装库 `DigitalVoltmeter.pretty` 和 `fp-lib-table`。
- 封装包含 40 个通孔焊盘、模块外形、1 脚标识和 USB 方向提示。

## 40 针映射

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

本项目当前使用的关键脚：

| 功能 | Blue Pill 引脚 | J1 针号 |
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

## 封装机械参数

当前封装采用常见 Blue Pill 模块的名义尺寸：

- 模块 PCB：23 mm × 53 mm；
- 两排各 20 针，纵向针距 2.54 mm；
- 两排中心距：17.78 mm（当前采用的常见值，需实物复核）；
- 焊盘：2.0 mm，钻孔 1.0 mm；
- 首末针中心纵向距离：48.26 mm；
- USB 位于 1/2 脚一端，Courtyard 为 USB 插头留出额外空间。

Blue Pill 克隆板的板宽、排距、USB 位置和元件高度可能不同。送板前必须用实际购买的模块测量，并打印 1:1 封装纸样试插。若排距不是 17.78 mm，应修改封装中两排焊盘的 X 坐标。

## 电源注意事项

- Blue Pill 的 +5V 针通常与 USB 5V 直接相连。
- 不要同时从 USB 和外部 +5V 给模块供电，除非已经确认所用克隆板具有可靠的电源隔离/防反灌设计。
- MCU GPIO 以 3.3 V 逻辑工作；是否 5 V 容忍必须按具体引脚和工作模式查 STM32F103x8/xB 数据手册，不能默认所有脚都可直接承受 5 V。
- 首次通电前，用万用表检查 +5V、+3V3、GND 是否短路，限流电源建议先设为 100–200 mA。

## KiCad 使用方法

将以下内容放在同一个项目目录：

- `digital-voltmeter-pcb(2).kicad_sch`
- `fp-lib-table`
- `DigitalVoltmeter.pretty/BluePill_STM32F103C8T6.kicad_mod`

打开原理图后执行：

1. 检查 J1 的值为 `BluePill_STM32F103C8T6`。
2. 检查 J1 封装为 `DigitalVoltmeter:BluePill_STM32F103C8T6`。
3. 更新 PCB 前先运行 ERC。
4. 在封装编辑器中按实际模块尺寸复核两排中心距和 USB 方向。
5. PCB 更新后运行 DRC，再做 1:1 打印试装。

## 资料来源

- STMicroelectronics，STM32F103x8/xB 数据手册：<https://www.st.com/resource/en/datasheet/stm32f103c8.pdf>
- STM32-base，Blue Pill 板型、尺寸和引脚表：<https://stm32-base.org/boards/STM32F103C8T6-Blue-Pill.html>

## 当前验证范围

J1 为项目自定义编号，不是裸芯片管脚号。必须按实物顶视图逐针核对左右排、首尾、USB 端及装配方向，排除镜像和 180° 插反。USB END 与 Courtyard 只表示文件定义，尚未验证线缆插头空间。所有 J1 引脚目前为 passive，ERC 不能完整检出 MCU 方向冲突。

单独上传的封装须放入 DigitalVoltmeter.pretty，以匹配库表。任何模块插拔均须先断开全部供电、确认电容放电；未供电时移除测量输入和有源 UART 信号。两路 BNC、UART 与整板共地，不得连接不同电位。限流出现异常时应断电排查，不直接提高限流值。

已完成文本级结构校验：KiCad S-expression 括号平衡、J1 有 40 个引脚、封装有 40 个唯一焊盘且编号为 1–40。当前环境没有 `kicad-cli`，因此仍需在本地 KiCad 中打开文件并运行 ERC/DRC；本文件不替代实物尺寸验证和样机测试。
