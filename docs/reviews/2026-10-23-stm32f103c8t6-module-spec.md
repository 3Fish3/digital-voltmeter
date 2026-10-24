# STM32F103C8T6 Blue Pill 模块规格记录（M1）

记录日期：2026-10-23（America/New_York）。本文是 M1 主控模块的正式规格登记，供原理图、封装与后续 PCB 使用。**规格来源分三类**：ST 原厂芯片手册、开源封装工程实测、用户实测；凡属"名义/待实测"的项均已标注，不作为已冻结尺寸。

## 1. 芯片规格（ST 原厂）

依据 ST **DS5319 Rev 20（2025-07）**：

| 项目 | 参数 |
| --- | --- |
| 型号 | STM32F103C8T6 |
| 内核 / 最高主频 | Arm Cortex-M3 / 72 MHz |
| 存储 | 64 KiB Flash、20 KiB SRAM |
| 裸片封装 | LQFP48，7 × 7 mm，P0.5 mm |
| 工作电源 | 2.0～3.6 V |
| ADC | 2 × 12 bit，C8 封装共 10 通道；VDDA / VREF+ 2.4～3.6 V |
| ADC 时钟上限 | 14 MHz |
| ADC 精度条件 | PCLK2 = 56 MHz、ADC = 14 MHz、R_AIN < 10 kΩ、VDDA 3～3.6 V、25 °C、校准后 |
| 通信 | 2 × I2C、3 × USART、2 × SPI、USB FS、CAN |
| 温度等级 | −40～+85 °C |
| PA0 / PA1 | ADC12_IN0 / ADC12_IN1；普通模拟输入，**不是** 5 V 容忍（FT）脚 |

## 2. 模块机械规格（M1）

| 项目 | 记录值 | 来源与状态 |
| --- | --- | --- |
| 板卡 | STM32F103C8T6 Blue Pill 兼容板 | 芯片身份已确认；具体克隆板厂家/板号待定 |
| 外形 | 约 53 × 23 mm | 第三方资料名义值 |
| 排针形式 | 两条 1 × 20 单排，P2.54 mm | 开源封装与参考图一致 |
| **两排中心距 D** | **15.24 mm（设计锁定）** | 用户实测 15.8 mm 外跨换算 + 开源封装焊盘实测 15.24 mm；残余不确定性 ≤0.08 mm |
| 每排首末中心跨度 | 48.26 mm（(20−1)×2.54） | 开源封装实测 |
| 排针建议钻孔 | Ø1.016 mm | 开源封装焊盘 |
| 用户实测金属外侧跨距 | **15.8 mm** | 用户千分尺实测，端点为左右排针金属外表面 |
| 板载 LDO | 原厂参考图 RT9193-33；克隆板常见 AMS1117-3.3、TX6211B | 实物丝印待核 |
| 晶振 | 8 MHz HSE；部分板另有 32.768 kHz LSE | 实板待核 |
| USB 接口 | Micro-USB，部分克隆板为 USB-C | 实物待核；伸出包络未测 |
| 板底元件高度 | 未测 | 装配叠高待实测 |

**D 的推导与锁定依据**：用户实测两排金属外表面跨 **15.8 mm**（千分尺，端点已确认）。中心距 `D = 15.8 − w`（w 为单根针沿跨排方向宽度）：

| 针宽 w | 换算 D | 与 15.24 偏差 |
| --- | --- | --- |
| 0.64 mm（0.025″ 标准方针） | 15.16 mm | −0.08 mm |
| 0.56 mm | 15.24 mm | 0 |

开源封装 `BluePill_STM32F103C.kicad_mod` 的焊盘中心独立测得 **15.24 mm**。两种针宽下 D 都落在 15.16～15.24 mm，**最大偏差 0.08 mm**。排母孔 Ø1.0 mm、方针宽 0.64 mm，单边径向余量约 0.18 mm，0.08 mm 偏差可被吸收。因此 **D 采用 15.24 mm 作为设计锁定值**，残余 ±0.08 mm 不确定性已记录，不再作为阻塞项。

## 3. M1 引脚映射（逻辑脚 → 模块排针孔）

封装命名：A 排 pad 1～20 = A1～A20；B 排 pad 40～21 = B1～B20（即 B1 = pad 40）。

| M1 逻辑号 | 功能 | 网络 | 模块孔位 |
| --- | --- | --- | --- |
| 1 | 5 V 输入（LDO 输入） | SYS_5V | B3（pad 38） |
| 2 | 3.3 V | 3V3 | A18（pad 18） |
| 3 | 地 | GND | A19（pad 19） |
| 4 | PB0 | MCU_CS | A13（pad 13） |
| 5 | PB1 | MCU_CLK | A14（pad 14） |
| 6 | PB10 | MCU_DI | A15（pad 15） |
| 7 | PB11 | MCU_DO | A16（pad 16） |
| 8 | PB12 | MCU_BUF_ENABLE_H | B20（pad 21） |
| 9 | PA0 | MON_VANA | A5（pad 5） |
| 10 | PA1 | MON_REF | A6（pad 6） |
| 11 | PA9 | UART_TX | B15（pad 26） |
| 12 | PA10 | UART_RX | B14（pad 27） |
| 13 | PA13 | SWDIO | **不在 40 针排**；独立 SWD 第 2 脚 |
| 14 | PA14 | SWCLK | **不在 40 针排**；独立 SWD 第 3 脚 |
| 15 | NRST | NRST | A17（pad 17） |
| 16 | PB6 | I2C_SCL | B7（pad 34） |
| 17 | PB7 | I2C_SDA | B6（pad 35） |

模块上其余 23 个孔（含未用 GPIO、多余 3.3 V/GND、VBAT 等）在封装中作为未使用机械孔保留，不接网络。

## 4. 供电与调试约束（必须遵守）

1. **USB 回灌**：Blue Pill 的 5 V 针与 USB VBUS、LDO 输入为同一网络，参考板无反向保护。由底板 5 V 供电时，**禁止同时插板载 USB**。
2. **3V3 反灌**：3.3 V 针是板载 LDO 输出，不应由底板外部电源直接反灌。
3. **独立 SWD**：PA13/PA14 只在板载 4 针 SWD 排针（3V3、SWDIO、SWCLK、GND）。底板 J5 需单独对接：J5.3→SWD 第 2 脚、J5.4→第 3 脚、J5.2→第 4 脚、J5.5→A17(NRST)；J5.1 仅作 3.3 V 电压感知，不可反向供电。
4. **VDDA**：参考板 VDDA 接 3.3 V 轨；克隆板 LDO 型号与去耦需实物核对。

## 5. 项目封装

- 封装：`V23Draft:BluePill_STM32F103C8T6_Module`
- 40 个通孔，P2.54，排距 15.24 mm，首末 48.26 mm，孔 Ø1.016 mm
- 文件：[BluePill_STM32F103C8T6_Module.kicad_mod](../../hardware/v2.3/V23Draft.pretty/BluePill_STM32F103C8T6_Module.kicad_mod)
- 交叉核对样本：[开源 BluePill 封装](2026-10-23-v2.3-footprint-development/evidence/opensource-BluePill_STM32F103C.kicad_mod)

## 6. 仍待实测的项

以下项目缺失时不得声称封装已冻结为实板尺寸：

- 本块克隆板单针宽度（仅用于把残余偏差从 ±0.08 mm 进一步收窄，不再是阻塞项）
- USB 接口类型与伸出包络
- 板底元件高度与排母叠高
- 板载 LDO 实际型号与 VDDA 走线

## 资料来源

- ST DS5319 Rev 20（2025-07），第 1、9、10、26～33、74～76、99 页
- [ST STM32F103C8 产品页](https://www.st.com/en/microcontrollers-microprocessors/stm32f103c8.html)
- [Blue Pill 原始参考原理图（VCC-GND，2016-01-26）](https://stm32-base.org/assets/pdf/boards/original-schematic-STM32F103C8T6-Blue_Pill.pdf)
- [STM32-base Blue Pill 板级资料](https://stm32-base.org/boards/STM32F103C8T6-Blue-Pill.html)
- 开源封装：[tomaskovacik/kicad-library BluePill_STM32F103C.kicad_mod](https://github.com/tomaskovacik/kicad-library/blob/master/BluePill_breakouts.pretty/BluePill_STM32F103C.kicad_mod)
- 用户实测：两排金属外表面 15.8 mm（千分尺）

本记录不是 PCB 封装批准或整机验收；实物公差核对与 PCB DRC 仍须完成。
