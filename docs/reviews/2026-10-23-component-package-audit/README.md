# V2.3 元器件与真实封装续审（只读）

审查日期：2026-10-23，America/New_York。范围：64个现有电路位号，以及核心板排母和已确认的15.8mm外跨。

**型号更正：** 用户随后确认实际主控为 **STM32F103C8T6 Blue Pill**。先前误记为 F102；本报告的 M1、管脚表和来源已改为 F103，F102 专属数据不再用于本项目。原理图、工程、蓝图、库和PCB均未修改；报告和原始检查证据归档于本目录，不构成采购BOM。

**后续实施：** 56个已具备足够证据的位号已在独立开发分支写入封装与MPN；本报告仍是开发前的64项审查快照。当前状态见[V2.3真实元器件与封装开发记录](../2026-10-23-v2.3-footprint-development/README.md)。

## 状态和证据边界

主表“状态”按准确选型、实体引脚、完整尺寸及采购闭环共同判断。结果：**通过0、失败7、待确认57**。此前35个“通过”只是静态子项通过，本表另列“静态子项状态”保留该范围；不得将该35项误读成可打板结论。失败针对表中明确的直接套封装/停产新选型方案，不表示功能器件本身必然失效。

本轮补得原厂资料及准确料号销售入口，但多数采购证据仍为检索快照或此前记录，没有实时交期及批次闭环；不引用库存数量。部分外网下载受代理连接失败/HTTP403影响，完整图未取得的项保持待确认。

## 优先阻塞项

1. M1：用户已确认金属外表面跨距15.8mm。标准Blue Pill名义为2×20、P2.54、0.6in中心距；本块实板的针宽、中心距、克隆板版本、左右方向、USB伸出和底部高度待核。PA13/PA14只在独立SWD排针，不能用两条长排母替代，详见[板级复核](../2026-10-23-stm32f103-blue-pill-investigation.md)。
2. U1：TI DIP-8版本为Obsolete；在产SOIC-14版本保留ADC0832功能，机械图已补齐，供货与图符重映射仍待批准。
3. Q1/Q2：原生XML引脚为G/S/D、B/C/E，候选Footprint为数字1/2/3；当前直接赋封装会失配，列失败。
4. D1–D4：当前每位号为两脚独立二极管；BAV199为三脚串联双管，直接逐位号赋封装失败。新查BAS116H单管方向仅列待审，不修改现图。
5. U6：TI LP0003A直引脚示例孔φ0.85，通用库孔φ0.75；针距相同不足以批准，需成品孔公差核查和专用方案。
6. U3、F1/F2、USB、径向去耦电容等仍缺完整机械/装配或供货闭环；64项工程Footprint字段均空。
7. STM32F103C8T6：保留用户确认的 Blue Pill 主控。ST DS5319 Rev20 表47规定 ADC 时钟最大14MHz，表49的精度条件为 PCLK2=56MHz、ADC=14MHz；现有条件预算的时钟前提成立，但实际固件时钟树仍待核对。Blue Pill 的 PA13/PA14 只在独立 SWD 排针，5V 与 USB VBUS 直连，详见[板级复核](../2026-10-23-stm32f103-blue-pill-investigation.md)。

## 已确认机械基准与新增核对

| 对象 | 原厂或实测 | 本机库/当前记录 | 结论与下一步 |
| --- | --- | --- | --- |
| 核心板两排外跨 | 用户千分尺实测15.8mm，测量端点已对图确认 | [设计报告第6.4节](../../design-report.md#64-核心板排母与机械参数记录)及[测量示意图](../../../pictures/coreboard-pin-row-outside-measurement.jpg) | 外跨已确认；需实际针宽换算D，并核同排针距和针数 |
| Harwin候选排母 | M20-7822046：20位/P2.54，推荐孔φ1.02±0.05 | 通用排母孔φ1.00、pad1.70×1.70 | 孔径工艺待核；实际模块是否20针/P2.54待确认 |
| U1 SOIC-14 | NPA0014B物理p36：L8.788–9.195、W7.391–7.595、含脚10.01–10.64、H2.362–2.642、P1.270mm | 14 pad，P1.27，左右pad中心距9.30，pad2.05×0.60；本体庭院x±4/y±4.75 | 庭院覆盖所列最大本体；14脚定义和实际供货仍需落实 |
| U6直引脚 | LP0003A物理p72–73，P1.27±0.13、示例孔φ0.85 | TO-92_Inline P1.27、孔φ0.75 | 孔径不同；最大引脚截面对角约0.698，φ0.75仅余0.052直径间隙，未计孔公差 |
| U3 DIP-14 | N14完整机械公差尚缺 | 通用库P2.54/排距7.62/孔φ0.8；庭院总长18.30 | 必须对准确N14最大长度再核包络，当前不批准 |
| R6 ZOR-25 | 原厂专属表：L6.3±0.5/D2.3±0.3/线径0.60±0.05 | 孔φ0.8、孔距10.16、庭院宽3.00 | 最大本体宽2.6可被庭院覆盖；原厂历史目录与当前批次适配待核 |
| J5/J6/J7 | Samtec -07目录A10.92/B2.54/C5.84；P2.54，单排塑胶宽标称2.48 | 5/3/4孔，首末跨度10.16/5.08/7.62；孔φ1.00、pad1.70×1.70 | 标称针距相符；完整公差、配对插深、G镀层供货仍待核 |

注意：Harwin推荐的0.64mm方针是候选排母适配条件，不是当前核心板公针实测值。Samtec目录-LL锁紧脚推荐孔不适用于直接判定当前无-LL料号。

## F103/Blue Pill 管脚对应（不是排母销售孔号）

来源：ST DS5319 Rev20 表5（pp28–33）与 Blue Pill 参考图。A/B 编号以 USB 端在上、从顶面看为准；P3/P4 为两条 20 针长排，SWD 为独立 4 针。下表把逻辑网络、MCU LQFP48 引脚和标准 Blue Pill 实体位置放在同一条证据链中。

| M1逻辑编号 | 功能 | 网络 | F103C8T6_LQFP48管脚 | Blue_Pill实体位置 | 证据范围 |
|---|---|---|---|---|---|
| 1 | 模块5V输入 | SYS_5V | 板载LDO输入；不是MCU裸片管脚 | 右侧B3；与USB VBUS同一5V网络 | 参考图直连，实板连续性待核 |
| 2 | 模块3V3 | 3V3 | VDD:24/36/48；VDDA:9 | 左侧A18或右侧B1 | 板载LDO输出，实板轨与LDO型号待核 |
| 3 | 模块GND | GND | VSS:23/35/47；VSSA:8 | 左侧A19/A20或右侧B2 | 标准孔位；实板连续性与去耦待核 |
| 4 | PB0 | MCU_CS | 18 | 左侧A13 | ST表5与参考板图对应 |
| 5 | PB1 | MCU_CLK | 19 | 左侧A14 | ST表5与参考板图对应 |
| 6 | PB10 | MCU_DI | 21 | 左侧A15 | ST表5与参考板图对应 |
| 7 | PB11 | MCU_DO | 22 | 左侧A16 | ST表5与参考板图对应 |
| 8 | PB12 | MCU_BUF_ENABLE_H | 25 | 右侧B20 | ST表5与参考板图对应 |
| 9 | PA0/ADC12_IN0 | MON_VANA | 10 | 左侧A5 | PA0不是FT 5V容忍脚；仅限0～VDDA |
| 10 | PA1/ADC12_IN1 | MON_REF | 11 | 左侧A6 | PA1不是FT 5V容忍脚；仅限0～VDDA |
| 11 | PA9/USART1_TX | UART_TX | 30 | 右侧B15 | ST表5与参考板图对应 |
| 12 | PA10/USART1_RX | UART_RX | 31 | 右侧B14 | ST表5与参考板图对应 |
| 13 | PA13/SWDIO | SWDIO | 34 | 独立4针SWD排针第2脚 | 不在两条20针长排；必须单独对接 |
| 14 | PA14/SWCLK | SWCLK | 37 | 独立4针SWD排针第3脚 | 不在两条20针长排；必须单独对接 |
| 15 | NRST | NRST | 7 | 左侧A17 | 板载复位网络；J5可引出 |
| 16 | PB6/I2C1_SCL | I2C_SCL | 42 | 右侧B7 | ST表5与参考板图对应 |
| 17 | PB7/I2C1_SDA | I2C_SDA | 43 | 右侧B6 | ST表5与参考板图对应 |

注意：标准板孔位已核，但本块克隆板的丝印方向、LDO、USB 接口及导通仍需实物确认。PA13/PA14 不在 A/B 长排，若仅焊两条排母，底板 J5 的 SWDIO/SWCLK 没有通路。

## 全部64个位号审查表

| 位号 | 现图标注 | 准确型号或候选 | 厂家 | 封装 | 原厂尺寸或关键距离_mm | 厂家资料 | 采购证据 | 建议KiCad_Footprint | 引脚核查 | 尺寸核查 | 状态 | 缺口与建议 | 静态子项状态 | 采购核查范围 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| U1 | ADC0832 | ADC0832CCN/NOPB（不建议新选）；ADC0832CCWM/NOPB（在产方向候选） | Texas Instruments | 原方案PDIP-8；备选SOIC-14宽体NPA | NPA0014B原厂PDF物理p36：本体长8.788～9.195、宽7.391～7.595；含脚10.01～10.64；高2.362～2.642；P1.270 | ADC-DIP；ADC-SO；ADC-DS | ADC-SALE；TI公开页缺货 | 原方案Package_DIP:DIP-8_W7.62mm；备选Package_SO:SOIC-14W_7.5x9mm_P1.27mm（NPA0014B图已核，图符/采购待批准） | 14脚为1CS/3CH0/5CH1/7GND/8DI/10DO/12CLK/14VCC；其余NC；现8脚定义不能直接套用 | 14脚候选实际库：P1.27、两侧焊盘中心距9.30、pad2.05×0.60；本体庭院边界x±4.00/y±4.75，可覆盖上述最大本体；尚未批准改用14脚 | 失败 | 失败针对停产TI DIP-8新采购方案和14脚直接套8脚图符。保留ADC0832功能的SOIC-14方向已补机械图；准确现货、完整14脚图符和装配仍待批准。 | 失败 | 准确料号公开目录/既有检索证据；本轮未闭合实时交货、批次及渠道可追溯性 |
| U2 | MCP6002 | MCP6002-I/P（候选） | Microchip | PDIP-8、300mil | 脚距2.54；原厂PDIP图C04-018-P Rev E；本体D8.839～10.16、E1 6.096～7.112 | MCP-DS | MCP-SALE | Package_DIP:DIP-8_W7.62mm | 1OUTA/2INA-/3INA+/4VSS/5INB+/6INB-/7OUTB/8VDD，与现图一致 | 本机脚距2.54、排距7.62、孔0.8；需按DIP正常成形插装 | 待确认 | 只通过候选静态选型/封装核查；零点摆幅、失调、负载稳定性与整机精度仍属电气验证。 | 通过 | 准确料号公开目录/既有检索证据；本轮未闭合实时交货、批次及渠道可追溯性 |
| U3 | 74AHCT125 | SN74AHCT125N（候选） | Texas Instruments | PDIP-14，N | 脚距2.54、排距7.62候选；原厂N14最大外形/引脚公差仍需补核 | AHCT-DS | AHCT-SALE；TI原厂准确料号检索标缺货，公开分销页仍需核供货 | Package_DIP:DIP-14_W7.62mm | OE1/4/10/13；A2/5/9/12；Y3/6/8/11；GND7/VCC14，与现图一致 | 本机14焊盘、脚距2.54、排距7.62、孔0.8；完整N14公差未闭合；另实读通用库庭院长18.30，必须取得N14原厂最大本体长度后再核包络，不能只核针距 | 待确认 | 不得用74HC125替代AHCT；需补准确N14机械图和采购批次。 | 待确认 | 准确料号公开目录/既有检索证据；本轮未闭合实时交货、批次及渠道可追溯性 |
| U4 | 74LVC1G125 | SN74LVC1G125DBVR（候选） | Texas Instruments | SOT-23-5，DBV，0.95mm脚距 | 本体标称2.9×1.6；含脚标称2.9×2.8；高≤1.45；脚距0.95 | LVC-DS | LVC-SALE | Package_TO_SOT_SMD:SOT-23-5_HandSoldering | 1OE/2A/3GND/4Y/5VCC，与现图一致 | 本机相邻脚距0.95，手焊焊盘1.56×0.65；DBV图可对应 | 待确认 | 保留必要易手焊贴片；部分上电/OE时序不能由封装匹配认定通过。 | 通过 | 准确料号公开目录/既有检索证据；本轮未闭合实时交货、批次及渠道可追溯性 |
| U5 | TPS2115A | TPS2115APW（候选，管装；PWR为卷带变体） | Texas Instruments | TSSOP-8，PW0008A | 本体4.3～4.5×2.9～3.1；含脚6.2～6.6；高≤1.2；脚距0.65 | TPS-DS | TPS-SALE | Package_SO:TSSOP-8_4.4x3mm_P0.65mm | 1STAT/2D0/3D1/4ILIM/5GND/6IN2/7OUT/8IN1，与现图一致 | 本机8焊盘、脚距0.65；焊盘1.475×0.4，左右中心距5.725 | 待确认 | 当前候选未发现直插版；保留TSSOP-8并检查手焊能力。反向电流/切换动态另需验证。 | 通过 | 准确料号公开目录/既有检索证据；本轮未闭合实时交货、批次及渠道可追溯性 |
| U6 | TL431BCLP | TL431BCLP（候选） | Texas Instruments | TO-92/LP，商业温度等级 | LP0003A，4215214/C 04/2025，PDF物理p72–73：本体宽4.44～5.21、厚3.17～4.19、高4.32～5.34；直引脚P1.27±0.13，长≥12.7 | TL-DS | TL-SALE | Package_TO_SOT_THT:TO-92_Inline（LP图已核，孔径/成品孔公差待确认） | TI LP为1K/2A/3REF；现图1与3同网、2接地，一致 | TI直引脚示例孔φ0.85/pad1.07×1.50；通用TO-92_Inline孔φ0.75/pad1.05×1.50，P1.27相同但孔径不同；不能批准为原厂等同封装 | 待确认 | LP订货表为BULK，仍应核到货为直引脚；原厂引脚最大截面0.55×0.43，对角约0.698mm，φ0.75仅余约0.052mm直径间隙（未计孔公差）。优先按TIφ0.85示例提出专用封装方案，用户批准后再建。 | 待确认 | 准确料号公开目录/既有检索证据；本轮未闭合实时交货、批次及渠道可追溯性 |
| M1 | BLUE_PILL_LOGICAL | STM32F103C8T6 Blue Pill（标准模块结构；具体克隆板厂家/版本未知） | 板级厂家待定；MCU为ST | Blue Pill 2×20长排针＋独立4针SWD＋底板两条1×20直插排母 | 标准板名义约53×23；2×20、P2.54、名义0.6in排中心距15.24。用户确认金属外表面跨距15.8；按0.64针宽换算中心距15.16，实板中心距仍待核 | ST-F103；ST-F103-DS；BLUE-PILL-SCH；BLUE-PILL-BOARD；具体板号/克隆板机械图仍缺 | ST-F103-SALE仅覆盖裸芯片；Blue Pill为通用无品牌模块，准确板卡SKU及货源待确认 | 模块专用封装待确认；标准名义2×20、P2.54、0.6in仅作候选；排母候选见第6.4节 | M1的17个逻辑端点已对应到F103 LQFP48和标准Blue Pill孔位；PA13/PA14只在独立4针SWD排针，不在长排。见coreboard-pin-mapping.csv | MCU LQFP48：7.0 BSC×7.0 BSC本体，9.0 BSC含脚，P0.5，H≤1.6。Blue Pill长排名义15.24中心距；用户外跨15.8不能直接当孔距 | 待确认 | 保持STM32F103C8T6。用实物核对每排20针、针宽/中心距、LDO、USB类型和VDDA连续性；PA13/14需独立SWD对接。5V与USB VBUS直连，底板供电时禁止插板载USB。详细见[板级复核](../2026-10-23-stm32f103-blue-pill-investigation.md)。 | 待确认 | 裸芯片有ST原厂销售证据；实际核心板型号/货源未确认 |
| J1 | USB-B ADAPTER POWER | 5787834-1（TE候选；需批准竖插方向） | TE Connectivity | USB 2.0 Type-B母座、竖插直插 | 原厂修订C工程图需完整核对板边/固定脚/高度；本机读到信号焊孔2.5mm横距 | TE-DS；LUM-DS作为淘汰对照 | TE标Active但公开页not currently available；即时供货待核 | Connector_USB:USB_B_TE_5787834_Vertical | 1VBUS/2D-/3D+/4GND/SH外壳与现图定义可对应；本机两个SH焊盘 | 本机信号孔0.92、外壳孔2.3；完整原厂孔位和板边伸出未闭合 | 待确认 | 本机另有Lumberg 2411 02封装，但原厂明确Obsolete，不作为常见新选型。TE候选需检查竖插空间与真实货源。 | 待确认 | 准确料号公开目录/既有检索证据；本轮未闭合实时交货、批次及渠道可追溯性 |
| J2 | EXT +5V/GND | 1715721 / MKDS 1,5/2-5,08（候选） | Phoenix Contact | 两位5.08mm直插螺钉端子 | W10.16×L9.8；离板高13.8；焊脚长3.5；脚0.9×0.9；推荐孔1.3 | PHX-DS | 原厂商业订货页存在；分销现货未直验 | TerminalBlock_Phoenix:TerminalBlock_Phoenix_MKDS-1,5-2-5.08_1x02_P5.08mm_Horizontal | 1=EXT+5V，2=GND；两个非极性触点的网络编号可对应 | 本机P5.08、孔1.3、焊盘2.6×2.6，与原厂推荐匹配 | 待确认 | 只通过该候选静态物理接口核查；J3/J4面板BNC及线缆另须选型，不在现64个PCB元件中。 | 通过 | 准确料号公开目录/既有检索证据；本轮未闭合实时交货、批次及渠道可追溯性 |
| F1 | FUSE MPN BLOCKED | 0251001.MXL（候选，额定尚未批准） | Littelfuse | PICO II 251，轴向直插、1A | 原厂系列标称D2.8×L7.11；孔距/弯脚及公差待补核 | 原厂251资料入口：https://www.littelfuse.com/products/fuses-overcurrent-protection/fuses/axial-radial-thru-hole-fuses/pico-fuses-axial-radial-thru-hole-fuses/251/0251001 | FUSE-SALE；准确料号公开销售页存在，实时交货未确认 | 待定：需专用PICO II封装，未创建 | 非极性两端可对应 | 不套普通电阻封装；本机未找到已核原厂图的同型专用封装 | 待确认 | 需联合验证额定、熔断I²t、启动浪涌、热态阻值及0.25Ω路径预算；0.128Ω仅系列名义冷阻值，不能当最坏值。 | 待确认 | 准确料号公开目录/既有检索证据；本轮未闭合实时交货、批次及渠道可追溯性 |
| F2 | FUSE MPN BLOCKED | 0251001.MXL（候选，额定尚未批准） | Littelfuse | PICO II 251，轴向直插、1A | 原厂系列标称D2.8×L7.11；孔距/弯脚及公差待补核 | 原厂251资料入口：https://www.littelfuse.com/products/fuses-overcurrent-protection/fuses/axial-radial-thru-hole-fuses/pico-fuses-axial-radial-thru-hole-fuses/251/0251001 | FUSE-SALE；准确料号公开销售页存在，实时交货未确认 | 待定：需专用PICO II封装，未创建 | 非极性两端可对应 | 不套普通电阻封装；本机未找到已核原厂图的同型专用封装 | 待确认 | 需联合验证额定、熔断I²t、启动浪涌、热态阻值及0.25Ω路径预算；0.128Ω仅系列名义冷阻值，不能当最坏值。 | 待确认 | 准确料号公开目录/既有检索证据；本轮未闭合实时交货、批次及渠道可追溯性 |
| Q1 | AO3401A candidate | AO3401A（候选） | Alpha & Omega Semiconductor | SOT-23-3 P沟道MOSFET | SOT23原厂机械图和本机1.9mm同侧脚距需最终逐项核查 | AO-DS；现存AO3401A Rev3.1 PDF只有5页电气资料，未含完整SOT23机械图 | AO-SALE | Package_TO_SOT_SMD:SOT-23_Handsoldering | 现图G/S/D为字母脚；候选实体需明确G→1/S→2/D→3后审签 | 本机数字焊盘1/2/3；当前字母引脚不能直接映射；原生XML确认当前引脚名与候选数字焊盘编号集合不同，直接赋通用封装失败 | 失败 | 失败范围仅为当前字母脚直接套数字焊盘。必须先批准数字脚映射；单PMOS导通后的双向路径不由封装审查关闭。 | 失败 | 准确料号公开目录/既有检索证据；本轮未闭合实时交货、批次及渠道可追溯性 |
| R1 | 100k 1% | MFR-25FBF52-100K（候选） | YAGEO | 1/4W、±1%轴向直插金属膜 | L6.3±0.5；D2.4±0.2；线径0.55±0.05 | MFR-DS | R-100K | Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal | 非极性；1/2与现图两端一致 | 本机孔0.8、孔距10.16；散装直引线需按该孔距整形 | 待确认 | 只通过该候选的静态规格/引脚与封装资料核查；未分配进工程。 | 通过 | 准确料号公开目录/既有检索证据；本轮未闭合实时交货、批次及渠道可追溯性 |
| R2 | 680R 1% | MFR-25FBF52-680R（候选） | YAGEO | 1/4W、±1%轴向直插金属膜 | L6.3±0.5；D2.4±0.2；线径0.55±0.05 | MFR-DS | R-680R | Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal | 非极性；1/2与现图两端一致 | 本机孔0.8、孔距10.16；散装直引线需按该孔距整形 | 待确认 | 只通过该候选的静态规格/引脚与封装资料核查；未分配进工程。 | 通过 | 准确料号公开目录/既有检索证据；本轮未闭合实时交货、批次及渠道可追溯性 |
| R3 | 20R 1% | MFR-25FBF52-20R（候选） | YAGEO | 1/4W、±1%轴向直插金属膜 | L6.3±0.5；D2.4±0.2；线径0.55±0.05 | MFR-DS | R-20R | Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal | 非极性；1/2与现图两端一致 | 本机孔0.8、孔距10.16；散装直引线需按该孔距整形 | 待确认 | 只通过该候选的静态规格/引脚与封装资料核查；未分配进工程。 | 通过 | 准确料号公开目录/既有检索证据；本轮未闭合实时交货、批次及渠道可追溯性 |
| R4 | 1R 1% | MFR-25FBF52-1R（候选） | YAGEO | 1/4W、±1%轴向直插金属膜 | L6.3±0.5；D2.4±0.2；线径0.55±0.05 | MFR-DS | R-1R | Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal | 非极性；1/2与现图两端一致 | 本机孔0.8、孔距10.16；散装直引线需按该孔距整形 | 待确认 | 只通过该候选的静态规格/引脚与封装资料核查；未分配进工程。 | 通过 | 准确料号公开目录/既有检索证据；本轮未闭合实时交货、批次及渠道可追溯性 |
| R5 | 4k7 1% BLEED | MFR-25FBF52-4K7（候选）；MFR-25FRF52-4K7（包装候选） | YAGEO | 1/4W、±1%轴向直插金属膜 | L6.3±0.5；D2.4±0.2；线径0.55±0.05 | MFR-DS | R-4K7；R-4K7-ALT | Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal | 非极性；1/2与现图两端一致 | 本机孔0.8、孔距10.16；散装直引线需按该孔距整形 | 待确认 | 补得另一包装候选的准确分销页面；本轮未取得实时可交货确认。先核YAGEO订货编码和到货引线，再决定，未替换。 | 待确认 | 准确料号公开目录/既有检索证据；本轮未闭合实时交货、批次及渠道可追溯性 |
| R6 | 0R SHIELD option | ZOR-25-R-52-0R（候选） | YAGEO | 轴向直插跳线 | ZOR-25：L6.3±0.5、D2.3±0.3、引线长28±2.0、线径0.60±0.05；原厂历史目录p38 | ZOR-DS，原厂ZOR-25专属表，非MFR系列尺寸代用 | ZOR-SALE | Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal | 非极性1/2可对应 | 通用库孔0.8/孔距10.16、庭院宽3.00，可覆盖所列最大本体D2.6；引线需整形，孔公差和当前批次适配待核 | 待确认 | 已补专属ZOR原厂尺寸表，待核历史目录版本与准确SKU/当前批次；屏蔽连接方案未改变。 | 待确认 | 准确料号公开目录/既有检索证据；本轮未闭合实时交货、批次及渠道可追溯性 |
| C1 | 100n | C320C104K5R5TA（候选） | KEMET/YAGEO | 径向MLCC，100nF/50VDC/X7R/±10% | 本体L≤5.08、T≤3.18、H≤5.84；P2.54±0.78；线径0.51+0.1/-0.025 | C320-DS | C320-SALE | 待确认：需要按原厂图核对/建立该径向件封装，未创建 | 非极性1/2一致 | 未找到已完成原厂尺寸逐项验证的本机对应封装；不能按外观套圆片封装 | 待确认 | 优先直插；需确认成形后的2.54mm脚距、安装离板高度与本体最大包络。供应商安装高度与原厂本体H不是同一基准。 | 待确认 | 准确料号公开目录/既有检索证据；本轮未闭合实时交货、批次及渠道可追溯性 |
| C2 | 100n | C320C104K5R5TA（候选） | KEMET/YAGEO | 径向MLCC，100nF/50VDC/X7R/±10% | 本体L≤5.08、T≤3.18、H≤5.84；P2.54±0.78；线径0.51+0.1/-0.025 | C320-DS | C320-SALE | 待确认：需要按原厂图核对/建立该径向件封装，未创建 | 非极性1/2一致 | 未找到已完成原厂尺寸逐项验证的本机对应封装；不能按外观套圆片封装 | 待确认 | 优先直插；需确认成形后的2.54mm脚距、安装离板高度与本体最大包络。供应商安装高度与原厂本体H不是同一基准。 | 待确认 | 准确料号公开目录/既有检索证据；本轮未闭合实时交货、批次及渠道可追溯性 |
| C3 | 10u candidate | EEUFR1H100（候选） | Panasonic | 径向有极性铝电解，10uF/50V/±20% | 标称D5、L11、脚距2.0 | FR-DS | FR-SALE | Capacitor_THT:CP_Radial_D5.0mm_P2.00mm | 建议1=正极SYS_5V或VANA，2=GND；方向可对应 | 本机P2.0、孔0.8匹配标称间距；最大外形及最终引线公差仍需复核 | 待确认 | 现图为无极性电容图符且介质/ESR未冻结；需批准采用极性器件，并补启动/切换条件和实时采购确认。 | 待确认 | 准确料号公开目录/既有检索证据；本轮未闭合实时交货、批次及渠道可追溯性 |
| C4 | 10u candidate | EEUFR1H100（候选） | Panasonic | 径向有极性铝电解，10uF/50V/±20% | 标称D5、L11、脚距2.0 | FR-DS | FR-SALE | Capacitor_THT:CP_Radial_D5.0mm_P2.00mm | 建议1=正极SYS_5V或VANA，2=GND；方向可对应 | 本机P2.0、孔0.8匹配标称间距；最大外形及最终引线公差仍需复核 | 待确认 | 现图为无极性电容图符且介质/ESR未冻结；需批准采用极性器件，并补启动/切换条件和实时采购确认。 | 待确认 | 准确料号公开目录/既有检索证据；本轮未闭合实时交货、批次及渠道可追溯性 |
| C5 | 100n | C320C104K5R5TA（候选） | KEMET/YAGEO | 径向MLCC，100nF/50VDC/X7R/±10% | 本体L≤5.08、T≤3.18、H≤5.84；P2.54±0.78；线径0.51+0.1/-0.025 | C320-DS | C320-SALE | 待确认：需要按原厂图核对/建立该径向件封装，未创建 | 非极性1/2一致 | 未找到已完成原厂尺寸逐项验证的本机对应封装；不能按外观套圆片封装 | 待确认 | 优先直插；需确认成形后的2.54mm脚距、安装离板高度与本体最大包络。供应商安装高度与原厂本体H不是同一基准。 | 待确认 | 准确料号公开目录/既有检索证据；本轮未闭合实时交货、批次及渠道可追溯性 |
| J3 | CH0 SIG/GND | 1715721 / MKDS 1,5/2-5,08（候选） | Phoenix Contact | 两位5.08mm直插螺钉端子 | W10.16×L9.8；离板高13.8；焊脚长3.5；脚0.9×0.9；推荐孔1.3 | PHX-DS | 原厂商业订货页存在；分销现货未直验 | TerminalBlock_Phoenix:TerminalBlock_Phoenix_MKDS-1,5-2-5.08_1x02_P5.08mm_Horizontal | 1=SIG，2=GND；两个非极性触点的网络编号可对应 | 本机P5.08、孔1.3、焊盘2.6×2.6，与原厂推荐匹配 | 待确认 | 只通过该候选静态物理接口核查；J3/J4面板BNC及线缆另须选型，不在现64个PCB元件中。 | 通过 | 准确料号公开目录/既有检索证据；本轮未闭合实时交货、批次及渠道可追溯性 |
| R10 | 180k 1% | MFR-25FBF52-180K（候选） | YAGEO | 1/4W、±1%轴向直插金属膜 | L6.3±0.5；D2.4±0.2；线径0.55±0.05 | MFR-DS | R-180K | Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal | 非极性；1/2与现图两端一致 | 本机孔0.8、孔距10.16；散装直引线需按该孔距整形 | 待确认 | 只通过该候选的静态规格/引脚与封装资料核查；未分配进工程。 | 通过 | 准确料号公开目录/既有检索证据；本轮未闭合实时交货、批次及渠道可追溯性 |
| R11 | 1M2 1% | MFR-25FBF52-1M2（候选） | YAGEO | 1/4W、±1%轴向直插金属膜 | L6.3±0.5；D2.4±0.2；线径0.55±0.05 | MFR-DS | R-1M2 | Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal | 非极性；1/2与现图两端一致 | 本机孔0.8、孔距10.16；散装直引线需按该孔距整形 | 待确认 | 只通过该候选的静态规格/引脚与封装资料核查；未分配进工程。 | 通过 | 准确料号公开目录/既有检索证据；本轮未闭合实时交货、批次及渠道可追溯性 |
| D1 | LOW-LEAKAGE BLOCKED | BAV199-7-F（每通道一只双管候选，不是每位号一只） | Diodes Incorporated | SOT-23-3、内部串联双二极管 | 原厂本体L2.8～3.0、W1.2～1.4；三脚结构 | BAV-DS | BAV-SALE | Package_TO_SOT_SMD:SOT-23_Handsoldering（必须先重建双管映射） | 拟实体1=GND、3=SENSE_CH0、2=VANA；现单管图符仅K1/A2 | 三脚双管与两脚独立图符不一致；不能直接赋该封装 | 失败 | 失败针对BAV199直接赋给现单管位号。若要保留每位号两脚直插，需另核在产低漏电单管；目前不将未追溯货源或1N4148直接等同替代。另找到Nexperia BAS116H,115/C74210（SOD123F单管）待审方向：厂家Production、LCSC检索有供货指示而DigiKey缺货；完整机械图、脚序、漏电/VF条件仍待核，未替换。 | 失败 | 准确料号公开目录/既有检索证据；本轮未闭合实时交货、批次及渠道可追溯性 |
| D2 | LOW-LEAKAGE BLOCKED | BAV199-7-F（每通道一只双管候选，不是每位号一只） | Diodes Incorporated | SOT-23-3、内部串联双二极管 | 原厂本体L2.8～3.0、W1.2～1.4；三脚结构 | BAV-DS | BAV-SALE | Package_TO_SOT_SMD:SOT-23_Handsoldering（必须先重建双管映射） | 拟实体1=GND、3=SENSE_CH0、2=VANA；现单管图符仅K1/A2 | 三脚双管与两脚独立图符不一致；不能直接赋该封装 | 失败 | 失败针对BAV199直接赋给现单管位号。若要保留每位号两脚直插，需另核在产低漏电单管；目前不将未追溯货源或1N4148直接等同替代。另找到Nexperia BAS116H,115/C74210（SOD123F单管）待审方向：厂家Production、LCSC检索有供货指示而DigiKey缺货；完整机械图、脚序、漏电/VF条件仍待核，未替换。 | 失败 | 准确料号公开目录/既有检索证据；本轮未闭合实时交货、批次及渠道可追溯性 |
| R12 | 220R | MFR-25FBF52-220R（候选） | YAGEO | 1/4W、±1%轴向直插金属膜 | L6.3±0.5；D2.4±0.2；线径0.55±0.05 | MFR-DS | R-220R | Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal | 非极性；1/2与现图两端一致 | 本机孔0.8、孔距10.16；散装直引线需按该孔距整形 | 待确认 | 只通过该候选的静态规格/引脚与封装资料核查；未分配进工程。 | 通过 | 准确料号公开目录/既有检索证据；本轮未闭合实时交货、批次及渠道可追溯性 |
| C10 | 100n | R82DC3100AA50J（候选） | KEMET/YAGEO | 径向PET薄膜，100nF/63VDC/±5% | L7.2+0.2/-0.5；T2.5+0.1/-0.5；H6.5+0.1/-0.5；P5±0.4；线径0.5±0.05 | R82-DS | R82-SALE | Capacitor_THT:C_Rect_L7.2mm_W2.5mm_P5.00mm | 非极性1/2一致 | 本机P5、孔0.75；标称外形一致，公差包络与引线整形需样件复核 | 待确认 | 作为保持100nF功能的直插候选；额定为63VDC/40VAC，不把销售标题40V误读为40VDC；库存及电气预算待确认。 | 待确认 | 准确料号公开目录/既有检索证据；本轮未闭合实时交货、批次及渠道可追溯性 |
| J4 | CH1 SIG/GND | 1715721 / MKDS 1,5/2-5,08（候选） | Phoenix Contact | 两位5.08mm直插螺钉端子 | W10.16×L9.8；离板高13.8；焊脚长3.5；脚0.9×0.9；推荐孔1.3 | PHX-DS | 原厂商业订货页存在；分销现货未直验 | TerminalBlock_Phoenix:TerminalBlock_Phoenix_MKDS-1,5-2-5.08_1x02_P5.08mm_Horizontal | 1=SIG，2=GND；两个非极性触点的网络编号可对应 | 本机P5.08、孔1.3、焊盘2.6×2.6，与原厂推荐匹配 | 待确认 | 只通过该候选静态物理接口核查；J3/J4面板BNC及线缆另须选型，不在现64个PCB元件中。 | 通过 | 准确料号公开目录/既有检索证据；本轮未闭合实时交货、批次及渠道可追溯性 |
| R14 | 180k 1% | MFR-25FBF52-180K（候选） | YAGEO | 1/4W、±1%轴向直插金属膜 | L6.3±0.5；D2.4±0.2；线径0.55±0.05 | MFR-DS | R-180K | Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal | 非极性；1/2与现图两端一致 | 本机孔0.8、孔距10.16；散装直引线需按该孔距整形 | 待确认 | 只通过该候选的静态规格/引脚与封装资料核查；未分配进工程。 | 通过 | 准确料号公开目录/既有检索证据；本轮未闭合实时交货、批次及渠道可追溯性 |
| R15 | 1M2 1% | MFR-25FBF52-1M2（候选） | YAGEO | 1/4W、±1%轴向直插金属膜 | L6.3±0.5；D2.4±0.2；线径0.55±0.05 | MFR-DS | R-1M2 | Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal | 非极性；1/2与现图两端一致 | 本机孔0.8、孔距10.16；散装直引线需按该孔距整形 | 待确认 | 只通过该候选的静态规格/引脚与封装资料核查；未分配进工程。 | 通过 | 准确料号公开目录/既有检索证据；本轮未闭合实时交货、批次及渠道可追溯性 |
| D3 | LOW-LEAKAGE BLOCKED | BAV199-7-F（每通道一只双管候选，不是每位号一只） | Diodes Incorporated | SOT-23-3、内部串联双二极管 | 原厂本体L2.8～3.0、W1.2～1.4；三脚结构 | BAV-DS | BAV-SALE | Package_TO_SOT_SMD:SOT-23_Handsoldering（必须先重建双管映射） | 拟实体1=GND、3=SENSE_CH1、2=VANA；现单管图符仅K1/A2 | 三脚双管与两脚独立图符不一致；不能直接赋该封装 | 失败 | 失败针对BAV199直接赋给现单管位号。若要保留每位号两脚直插，需另核在产低漏电单管；目前不将未追溯货源或1N4148直接等同替代。另找到Nexperia BAS116H,115/C74210（SOD123F单管）待审方向：厂家Production、LCSC检索有供货指示而DigiKey缺货；完整机械图、脚序、漏电/VF条件仍待核，未替换。 | 失败 | 准确料号公开目录/既有检索证据；本轮未闭合实时交货、批次及渠道可追溯性 |
| D4 | LOW-LEAKAGE BLOCKED | BAV199-7-F（每通道一只双管候选，不是每位号一只） | Diodes Incorporated | SOT-23-3、内部串联双二极管 | 原厂本体L2.8～3.0、W1.2～1.4；三脚结构 | BAV-DS | BAV-SALE | Package_TO_SOT_SMD:SOT-23_Handsoldering（必须先重建双管映射） | 拟实体1=GND、3=SENSE_CH1、2=VANA；现单管图符仅K1/A2 | 三脚双管与两脚独立图符不一致；不能直接赋该封装 | 失败 | 失败针对BAV199直接赋给现单管位号。若要保留每位号两脚直插，需另核在产低漏电单管；目前不将未追溯货源或1N4148直接等同替代。另找到Nexperia BAS116H,115/C74210（SOD123F单管）待审方向：厂家Production、LCSC检索有供货指示而DigiKey缺货；完整机械图、脚序、漏电/VF条件仍待核，未替换。 | 失败 | 准确料号公开目录/既有检索证据；本轮未闭合实时交货、批次及渠道可追溯性 |
| R16 | 220R | MFR-25FBF52-220R（候选） | YAGEO | 1/4W、±1%轴向直插金属膜 | L6.3±0.5；D2.4±0.2；线径0.55±0.05 | MFR-DS | R-220R | Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal | 非极性；1/2与现图两端一致 | 本机孔0.8、孔距10.16；散装直引线需按该孔距整形 | 待确认 | 只通过该候选的静态规格/引脚与封装资料核查；未分配进工程。 | 通过 | 准确料号公开目录/既有检索证据；本轮未闭合实时交货、批次及渠道可追溯性 |
| C11 | 100n | R82DC3100AA50J（候选） | KEMET/YAGEO | 径向PET薄膜，100nF/63VDC/±5% | L7.2+0.2/-0.5；T2.5+0.1/-0.5；H6.5+0.1/-0.5；P5±0.4；线径0.5±0.05 | R82-DS | R82-SALE | Capacitor_THT:C_Rect_L7.2mm_W2.5mm_P5.00mm | 非极性1/2一致 | 本机P5、孔0.75；标称外形一致，公差包络与引线整形需样件复核 | 待确认 | 作为保持100nF功能的直插候选；额定为63VDC/40VAC，不把销售标题40V误读为40VDC；库存及电气预算待确认。 | 待确认 | 准确料号公开目录/既有检索证据；本轮未闭合实时交货、批次及渠道可追溯性 |
| C6 | 100n U2 | C320C104K5R5TA（候选） | KEMET/YAGEO | 径向MLCC，100nF/50VDC/X7R/±10% | 本体L≤5.08、T≤3.18、H≤5.84；P2.54±0.78；线径0.51+0.1/-0.025 | C320-DS | C320-SALE | 待确认：需要按原厂图核对/建立该径向件封装，未创建 | 非极性1/2一致 | 未找到已完成原厂尺寸逐项验证的本机对应封装；不能按外观套圆片封装 | 待确认 | 优先直插；需确认成形后的2.54mm脚距、安装离板高度与本体最大包络。供应商安装高度与原厂本体H不是同一基准。 | 待确认 | 准确料号公开目录/既有检索证据；本轮未闭合实时交货、批次及渠道可追溯性 |
| C7 | 100n U1 | C320C104K5R5TA（候选） | KEMET/YAGEO | 径向MLCC，100nF/50VDC/X7R/±10% | 本体L≤5.08、T≤3.18、H≤5.84；P2.54±0.78；线径0.51+0.1/-0.025 | C320-DS | C320-SALE | 待确认：需要按原厂图核对/建立该径向件封装，未创建 | 非极性1/2一致 | 未找到已完成原厂尺寸逐项验证的本机对应封装；不能按外观套圆片封装 | 待确认 | 优先直插；需确认成形后的2.54mm脚距、安装离板高度与本体最大包络。供应商安装高度与原厂本体H不是同一基准。 | 待确认 | 准确料号公开目录/既有检索证据；本轮未闭合实时交货、批次及渠道可追溯性 |
| C8 | 100n U3 | C320C104K5R5TA（候选） | KEMET/YAGEO | 径向MLCC，100nF/50VDC/X7R/±10% | 本体L≤5.08、T≤3.18、H≤5.84；P2.54±0.78；线径0.51+0.1/-0.025 | C320-DS | C320-SALE | 待确认：需要按原厂图核对/建立该径向件封装，未创建 | 非极性1/2一致 | 未找到已完成原厂尺寸逐项验证的本机对应封装；不能按外观套圆片封装 | 待确认 | 优先直插；需确认成形后的2.54mm脚距、安装离板高度与本体最大包络。供应商安装高度与原厂本体H不是同一基准。 | 待确认 | 准确料号公开目录/既有检索证据；本轮未闭合实时交货、批次及渠道可追溯性 |
| C9 | 100n U4 | C320C104K5R5TA（候选） | KEMET/YAGEO | 径向MLCC，100nF/50VDC/X7R/±10% | 本体L≤5.08、T≤3.18、H≤5.84；P2.54±0.78；线径0.51+0.1/-0.025 | C320-DS | C320-SALE | 待确认：需要按原厂图核对/建立该径向件封装，未创建 | 非极性1/2一致 | 未找到已完成原厂尺寸逐项验证的本机对应封装；不能按外观套圆片封装 | 待确认 | 优先直插；需确认成形后的2.54mm脚距、安装离板高度与本体最大包络。供应商安装高度与原厂本体H不是同一基准。 | 待确认 | 准确料号公开目录/既有检索证据；本轮未闭合实时交货、批次及渠道可追溯性 |
| R20 | 47k | MFR-25FBF52-47K（候选） | YAGEO | 1/4W、±1%轴向直插金属膜 | L6.3±0.5；D2.4±0.2；线径0.55±0.05 | MFR-DS | R-47K | Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal | 非极性；1/2与现图两端一致 | 本机孔0.8、孔距10.16；散装直引线需按该孔距整形 | 待确认 | 只通过该候选的静态规格/引脚与封装资料核查；未分配进工程。 | 通过 | 准确料号公开目录/既有检索证据；本轮未闭合实时交货、批次及渠道可追溯性 |
| R21 | 47k | MFR-25FBF52-47K（候选） | YAGEO | 1/4W、±1%轴向直插金属膜 | L6.3±0.5；D2.4±0.2；线径0.55±0.05 | MFR-DS | R-47K | Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal | 非极性；1/2与现图两端一致 | 本机孔0.8、孔距10.16；散装直引线需按该孔距整形 | 待确认 | 只通过该候选的静态规格/引脚与封装资料核查；未分配进工程。 | 通过 | 准确料号公开目录/既有检索证据；本轮未闭合实时交货、批次及渠道可追溯性 |
| R22 | 47k | MFR-25FBF52-47K（候选） | YAGEO | 1/4W、±1%轴向直插金属膜 | L6.3±0.5；D2.4±0.2；线径0.55±0.05 | MFR-DS | R-47K | Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal | 非极性；1/2与现图两端一致 | 本机孔0.8、孔距10.16；散装直引线需按该孔距整形 | 待确认 | 只通过该候选的静态规格/引脚与封装资料核查；未分配进工程。 | 通过 | 准确料号公开目录/既有检索证据；本轮未闭合实时交货、批次及渠道可追溯性 |
| R23 | 100R | MFR-25FBF52-100R（候选） | YAGEO | 1/4W、±1%轴向直插金属膜 | L6.3±0.5；D2.4±0.2；线径0.55±0.05 | MFR-DS | R-100R | Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal | 非极性；1/2与现图两端一致 | 本机孔0.8、孔距10.16；散装直引线需按该孔距整形 | 待确认 | 只通过该候选的静态规格/引脚与封装资料核查；未分配进工程。 | 通过 | 准确料号公开目录/既有检索证据；本轮未闭合实时交货、批次及渠道可追溯性 |
| R24 | 100R | MFR-25FBF52-100R（候选） | YAGEO | 1/4W、±1%轴向直插金属膜 | L6.3±0.5；D2.4±0.2；线径0.55±0.05 | MFR-DS | R-100R | Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal | 非极性；1/2与现图两端一致 | 本机孔0.8、孔距10.16；散装直引线需按该孔距整形 | 待确认 | 只通过该候选的静态规格/引脚与封装资料核查；未分配进工程。 | 通过 | 准确料号公开目录/既有检索证据；本轮未闭合实时交货、批次及渠道可追溯性 |
| R25 | 100R | MFR-25FBF52-100R（候选） | YAGEO | 1/4W、±1%轴向直插金属膜 | L6.3±0.5；D2.4±0.2；线径0.55±0.05 | MFR-DS | R-100R | Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal | 非极性；1/2与现图两端一致 | 本机孔0.8、孔距10.16；散装直引线需按该孔距整形 | 待确认 | 只通过该候选的静态规格/引脚与封装资料核查；未分配进工程。 | 通过 | 准确料号公开目录/既有检索证据；本轮未闭合实时交货、批次及渠道可追溯性 |
| R26 | 10k | MFR-25FBF52-10K（候选） | YAGEO | 1/4W、±1%轴向直插金属膜 | L6.3±0.5；D2.4±0.2；线径0.55±0.05 | MFR-DS | R-10K | Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal | 非极性；1/2与现图两端一致 | 本机孔0.8、孔距10.16；散装直引线需按该孔距整形 | 待确认 | 只通过该候选的静态规格/引脚与封装资料核查；未分配进工程。 | 通过 | 准确料号公开目录/既有检索证据；本轮未闭合实时交货、批次及渠道可追溯性 |
| R27 | 47k | MFR-25FBF52-47K（候选） | YAGEO | 1/4W、±1%轴向直插金属膜 | L6.3±0.5；D2.4±0.2；线径0.55±0.05 | MFR-DS | R-47K | Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal | 非极性；1/2与现图两端一致 | 本机孔0.8、孔距10.16；散装直引线需按该孔距整形 | 待确认 | 只通过该候选的静态规格/引脚与封装资料核查；未分配进工程。 | 通过 | 准确料号公开目录/既有检索证据；本轮未闭合实时交货、批次及渠道可追溯性 |
| R28 | 47k | MFR-25FBF52-47K（候选） | YAGEO | 1/4W、±1%轴向直插金属膜 | L6.3±0.5；D2.4±0.2；线径0.55±0.05 | MFR-DS | R-47K | Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal | 非极性；1/2与现图两端一致 | 本机孔0.8、孔距10.16；散装直引线需按该孔距整形 | 待确认 | 只通过该候选的静态规格/引脚与封装资料核查；未分配进工程。 | 通过 | 准确料号公开目录/既有检索证据；本轮未闭合实时交货、批次及渠道可追溯性 |
| R29 | 47k | MFR-25FBF52-47K（候选） | YAGEO | 1/4W、±1%轴向直插金属膜 | L6.3±0.5；D2.4±0.2；线径0.55±0.05 | MFR-DS | R-47K | Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal | 非极性；1/2与现图两端一致 | 本机孔0.8、孔距10.16；散装直引线需按该孔距整形 | 待确认 | 只通过该候选的静态规格/引脚与封装资料核查；未分配进工程。 | 通过 | 准确料号公开目录/既有检索证据；本轮未闭合实时交货、批次及渠道可追溯性 |
| R30 | 100R | MFR-25FBF52-100R（候选） | YAGEO | 1/4W、±1%轴向直插金属膜 | L6.3±0.5；D2.4±0.2；线径0.55±0.05 | MFR-DS | R-100R | Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal | 非极性；1/2与现图两端一致 | 本机孔0.8、孔距10.16；散装直引线需按该孔距整形 | 待确认 | 只通过该候选的静态规格/引脚与封装资料核查；未分配进工程。 | 通过 | 准确料号公开目录/既有检索证据；本轮未闭合实时交货、批次及渠道可追溯性 |
| R31 | 10k | MFR-25FBF52-10K（候选） | YAGEO | 1/4W、±1%轴向直插金属膜 | L6.3±0.5；D2.4±0.2；线径0.55±0.05 | MFR-DS | R-10K | Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal | 非极性；1/2与现图两端一致 | 本机孔0.8、孔距10.16；散装直引线需按该孔距整形 | 待确认 | 只通过该候选的静态规格/引脚与封装资料核查；未分配进工程。 | 通过 | 准确料号公开目录/既有检索证据；本轮未闭合实时交货、批次及渠道可追溯性 |
| R32 | 100k | MFR-25FBF52-100K（候选） | YAGEO | 1/4W、±1%轴向直插金属膜 | L6.3±0.5；D2.4±0.2；线径0.55±0.05 | MFR-DS | R-100K | Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal | 非极性；1/2与现图两端一致 | 本机孔0.8、孔距10.16；散装直引线需按该孔距整形 | 待确认 | 只通过该候选的静态规格/引脚与封装资料核查；未分配进工程。 | 通过 | 准确料号公开目录/既有检索证据；本轮未闭合实时交货、批次及渠道可追溯性 |
| R33 | 10k | MFR-25FBF52-10K（候选） | YAGEO | 1/4W、±1%轴向直插金属膜 | L6.3±0.5；D2.4±0.2；线径0.55±0.05 | MFR-DS | R-10K | Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal | 非极性；1/2与现图两端一致 | 本机孔0.8、孔距10.16；散装直引线需按该孔距整形 | 待确认 | 只通过该候选的静态规格/引脚与封装资料核查；未分配进工程。 | 通过 | 准确料号公开目录/既有检索证据；本轮未闭合实时交货、批次及渠道可追溯性 |
| R40 | 68R 1% | MFR-25FBF52-68R（候选） | YAGEO | 1/4W、±1%轴向直插金属膜 | L6.3±0.5；D2.4±0.2；线径0.55±0.05 | MFR-DS | R-68R | Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal | 非极性；1/2与现图两端一致 | 本机孔0.8、孔距10.16；散装直引线需按该孔距整形 | 待确认 | 只通过该候选的静态规格/引脚与封装资料核查；未分配进工程。 | 通过 | 准确料号公开目录/既有检索证据；本轮未闭合实时交货、批次及渠道可追溯性 |
| R41 | 1k 1% | MFR-25FBF52-1K（候选） | YAGEO | 1/4W、±1%轴向直插金属膜 | L6.3±0.5；D2.4±0.2；线径0.55±0.05 | MFR-DS | R-1K | Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal | 非极性；1/2与现图两端一致 | 本机孔0.8、孔距10.16；散装直引线需按该孔距整形 | 待确认 | 只通过该候选的静态规格/引脚与封装资料核查；未分配进工程。 | 通过 | 准确料号公开目录/既有检索证据；本轮未闭合实时交货、批次及渠道可追溯性 |
| R42 | 10k 1% | MFR-25FBF52-10K（候选） | YAGEO | 1/4W、±1%轴向直插金属膜 | L6.3±0.5；D2.4±0.2；线径0.55±0.05 | MFR-DS | R-10K | Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal | 非极性；1/2与现图两端一致 | 本机孔0.8、孔距10.16；散装直引线需按该孔距整形 | 待确认 | 只通过该候选的静态规格/引脚与封装资料核查；未分配进工程。 | 通过 | 准确料号公开目录/既有检索证据；本轮未闭合实时交货、批次及渠道可追溯性 |
| R43 | 10k 1% | MFR-25FBF52-10K（候选） | YAGEO | 1/4W、±1%轴向直插金属膜 | L6.3±0.5；D2.4±0.2；线径0.55±0.05 | MFR-DS | R-10K | Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal | 非极性；1/2与现图两端一致 | 本机孔0.8、孔距10.16；散装直引线需按该孔距整形 | 待确认 | 只通过该候选的静态规格/引脚与封装资料核查；未分配进工程。 | 通过 | 准确料号公开目录/既有检索证据；本轮未闭合实时交货、批次及渠道可追溯性 |
| R44 | 1k 1% | MFR-25FBF52-1K（候选） | YAGEO | 1/4W、±1%轴向直插金属膜 | L6.3±0.5；D2.4±0.2；线径0.55±0.05 | MFR-DS | R-1K | Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal | 非极性；1/2与现图两端一致 | 本机孔0.8、孔距10.16；散装直引线需按该孔距整形 | 待确认 | 只通过该候选的静态规格/引脚与封装资料核查；未分配进工程。 | 通过 | 准确料号公开目录/既有检索证据；本轮未闭合实时交货、批次及渠道可追溯性 |
| Q2 | NPN_EN MPN BLOCKED | 2N3904BU（候选） | onsemi | TO-92-3直插NPN | 准确BU引线成形及公差待核；不能仅凭TO-92名称确认 | NPN-DS；已读onsemi原厂PDF提取版Rev3 2024-10：p1脚序、p6订购、p7 CASE135AN、p8 CASE135AR | NPN-SALE | Package_TO_SOT_THT:TO-92_Inline（待核BU图） | 已核原厂1=E/2=B/3=C；现图E/B/C须映射到1/2/3；不得自动按位置替换 | 本机1.27mm脚距/孔0.75；准确BU机械图未闭合；原生XML确认当前引脚名与候选数字焊盘编号集合不同，直接赋通用封装失败 | 失败 | 失败范围仅为当前字母脚直接套数字焊盘。NPN具体型号和驱动条件待批准；不同TO-92三极管脚序不可混用。 | 失败 | 准确料号公开目录/既有检索证据；本轮未闭合实时交货、批次及渠道可追溯性 |
| J5 | SWD NO POWER IN | TSW-105-07-G-S（候选） | Samtec | 1×5直插公排针 | P2.54；5针首末跨度10.16；0.025英寸公针；-07目录A10.92/B2.54/C5.84；单排塑胶宽标称2.48 | SAM5；SAM-CAT | SAM5 | Connector_PinHeader_2.54mm:PinHeader_1x05_P2.54mm_Vertical | 1Vref/2GND/3SWDIO/4SWCLK/5NRST；须与实际对端线序核对 | 本机实际5孔，P2.54、孔1.00、pad1.70×1.70；目录标称针距对应，精确公差、配对接触深度与G镀层供货仍待核 | 待确认 | 保持1Vref/2GND/3SWDIO/4SWCLK/5NRST，核实际调试器线序及1脚用途。目录的φ1.02±0.03推荐孔出现在-LL锁紧脚选项，不能直接推给当前无-LL料号。 | 待确认 | 准确料号公开目录/既有检索证据；本轮未闭合实时交货、批次及渠道可追溯性 |
| J6 | TTL 3V3 NO POWER PIN | TSW-103-07-G-S（候选） | Samtec | 1×3直插公排针 | P2.54；3针首末跨度5.08；0.025英寸公针；-07目录A10.92/B2.54/C5.84；单排塑胶宽标称2.48 | SAM3；SAM-CAT | SAM3 | Connector_PinHeader_2.54mm:PinHeader_1x03_P2.54mm_Vertical | 1TX/2RX/3GND；须与实际对端线序核对 | 本机实际3孔，P2.54、孔1.00、pad1.70×1.70；目录标称针距对应，精确公差、配对接触深度与G镀层供货仍待核 | 待确认 | 保持1TX/2RX/3GND，核对端TX/RX交叉。目录的φ1.02±0.03推荐孔出现在-LL锁紧脚选项，不能直接推给当前无-LL料号。 | 待确认 | 准确料号公开目录/既有检索证据；本轮未闭合实时交货、批次及渠道可追溯性 |
| J7 | OLED OPTIONAL | TSW-104-07-G-S（候选） | Samtec | 1×4直插公排针 | P2.54；4针首末跨度7.62；0.025英寸公针；-07目录A10.92/B2.54/C5.84；单排塑胶宽标称2.48 | SAM4；SAM-CAT | SAM4 | Connector_PinHeader_2.54mm:PinHeader_1x04_P2.54mm_Vertical | 1VCC/2GND/3SCL/4SDA；须与实际对端线序核对 | 本机实际4孔，P2.54、孔1.00、pad1.70×1.70；目录标称针距对应，精确公差、配对接触深度与G镀层供货仍待核 | 待确认 | 保持1VCC/2GND/3SCL/4SDA，核具体OLED模块针序、自带上拉与插接高度。目录的φ1.02±0.03推荐孔出现在-LL锁紧脚选项，不能直接推给当前无-LL料号。 | 待确认 | 准确料号公开目录/既有检索证据；本轮未闭合实时交货、批次及渠道可追溯性 |

## 电气审查与原始检查的沿用范围

此前原生KiCad 10.0.6导出网表及ERC原始结果现随报告归档：64电路件、47命名网、183接线、5NC、3供电声明；ERC报告0项违规，忽略规则为single_global_label、four_way_junction、simulation_model_issue、footprint_filter。原始command-1.json/command-2.json记录工具参数。本轮未重跑ERC，工程哈希相同后沿用该次结果。

TPS2115A切换/反向供电、ADC0832掉电数字路径、MCP6002零点/满量程、TL431动态稳定性及二极管全温漏电和保护配合仍需电气验证。封装对照、条件计算和ERC分别记录，均不作为整机可用结论。

## 未应用的可审查替代方向

| 对象 | 候选方案 | 已得证据 | 剩余条件 |
| --- | --- | --- | --- |
| U1 | ADC0832CCWM/NOPB，SOIC14 | TI原厂Active、NPA0014B图、完整14脚功能定义 | TI公开页检索缺货；落实可追溯供货、批准14脚图符；保持ADC0832功能 |
| D1–D4 | 保留BAV199-7-F，每通道一只双管 | 现存Diodes原厂图及串联结构 | 用户批准后重建器件单元/位号与三脚映射 |
| D1–D4 | Nexperia BAS116H,115，四只单管，SOD123F | 原厂Production；准确LCSC C74210销售入口；DigiKey该料号检索缺货 | 原厂完整图、两脚极性、漏电/VF/温度及可交货证据待补；未认定直接兼容 |
| R5 | MFR-25FRF52-4K7，4.7k/1%/0.25W包装候选 | 准确DigiKey和Arrow目录；功能值与原候选相同 | 准确包装编码、引线成形与实时交货待核 |
| U6 | 保持TI TL431BCLP，按LP0003A直引脚示例提出专用孔位 | 原厂φ0.85孔、P1.27及最大引脚截面已得 | 用户审定后才能创建或修改封装；同时核板厂成品孔公差 |

## 资料索引

主表资料键对应如下。前轮资料沿用时已注明检索/本地文件范围；新增资料没有证据支持的参数均留待确认。

- **ST-F103**：ST STM32F103C8官方产品页 — https://www.st.com/en/microcontrollers-microprocessors/stm32f103c8.html
- **ST-F103-DS**：ST DS5319 Rev20，2025-07；表2、表5、表47～50、表62 — https://www.st.com/resource/en/datasheet/stm32f103c8.pdf
- **ST-F103-SALE**：ST商城准确料号STM32F103C8T6；裸芯片证据，不是板卡货源 — https://estore.st.com/en/products/microcontrollers-microprocessors/stm32-32-bit-arm-cortex-mcus/stm32-mainstream-mcus/stm32f1-series/stm32f103/stm32f103c8.html
- **BLUE-PILL-SCH**：Blue Pill原始参考图，2016-01-26 — https://stm32-base.org/assets/pdf/boards/original-schematic-STM32F103C8T6-Blue_Pill.pdf
- **BLUE-PILL-BOARD**：STM32-base通用Blue Pill资料页 — https://stm32-base.org/boards/STM32F103C8T6-Blue_Pill.html
- **BLUE-PILL-SPACE**：2×20、0.6in插座装配说明；仅作名义布局 — https://github.com/LieBtrau/electronics-design-data/wiki/STM32-Blue-Pill

- **ADC-DIP**：TI ADC0832CCN/NOPB: OBSOLETE; public page out of stock — https://www.ti.com/product/ADC0832-N/part-details/ADC0832CCN/NOPB
- **ADC-SO**：TI ADC0832CCWM/NOPB: ACTIVE, NPA 14; public page out of stock — https://www.ti.com/product/ADC0832-N/part-details/ADC0832CCWM/NOPB
- **ADC-DS**：TI SNAS531B, pin diagrams Figure 2 and Figure 5 — https://www.ti.com/lit/ds/symlink/adc0832-n.pdf
- **ADC-SALE**：DigiKey exact 14-pin SKU; listed as not normally stocked — https://www.digikey.com/en/products/detail/texas-instruments/ADC0832CCWM-NOPB/182196
- **MCP-DS**：Microchip DS20001733L, page 1 pinout and pages 29–30 PDIP drawing — [仓库内原厂资料](../../../references/datasheets/mcp6002.pdf)
- **MCP-SALE**：DigiKey MCP6002-I/P exact SKU; indexed sale page, live inventory not verified — https://www.digikey.com/en/products/detail/microchip-technology/MCP6002-I-P/500875
- **AHCT-DS**：TI SCLS264R, N/PDIP-14 — https://www.ti.com/lit/ds/symlink/sn74ahct125.pdf
- **AHCT-SALE**：DigiKey SN74AHCT125N exact SKU; seller/lot must be checked — https://www.digikey.com/en/products/detail/texas-instruments/SN74AHCT125N/375798
- **LVC-DS**：TI SCES223U, DBV SOT-23-5 outline and pinout — https://www.ti.com/lit/ds/symlink/sn74lvc1g125.pdf
- **LVC-SALE**：LCSC C23654, exact SN74LVC1G125DBVR listing, indexed stock indication — https://www.lcsc.com/product-detail/C23654.html
- **TPS-DS**：TI TPS2115A, PW0008A outline — [仓库内原厂资料](../../../references/datasheets/tps2115a.pdf)
- **TPS-SALE**：DigiKey TPS2115APW exact listing, indexed stock indication — https://www.digikey.co.nz/en/products/detail/texas-instruments/TPS2115APW/1670931
- **TL-DS**：TI SLVS543S, Table 5-1 LP pinout and package drawings — [仓库内原厂资料](../../../references/datasheets/tl431.pdf)
- **TL-SALE**：TI TL431BCLP orderable part details — https://www.ti.com/product/TL431/part-details/TL431BCLP
- **AO-DS**：AOS AO3401A Rev 3.1, SOT23 top/bottom view — [仓库内原厂资料](../../../references/datasheets/ao3401a.pdf)
- **AO-SALE**：LCSC C15127, AOS AO3401A listing, indexed stock indication — https://www.lcsc.com/product-detail/C15127.html
- **NPN-DS**：onsemi 2N3904 family datasheet; exact BU lead form still needs final drawing verification — https://www.onsemi.com/pdf/datasheet/2n3904-d.pdf
- **NPN-SALE**：Newark 47T5757, exact 2N3904BU listing, indexed stock indication — https://www.newark.com/onsemi/2n3904bu/transistor-npn-40-v-0-2-a-to-92/dp/47T5757
- **BAV-DS**：Diodes DS30232 Rev 11-2, pages 1 and 4 — [仓库内原厂资料](../../../references/datasheets/BAV199-Diodes.pdf)
- **BAV-SALE**：DigiKey BAV199-7-F, indexed stock indication — https://www.digikey.com/en/products/detail/diodes-incorporated/BAV199-7-F/1033645
- **MFR-DS**：YAGEO MFR specification April 3, 2024 V4, page 3 dimensions — https://yageogroup.com/content/Resource%20Library/Datasheet/YAGEO-MFR_DATASHEET.pdf
- **ZOR-SALE**：DigiKey YAGEO ZOR-25-R-52-0R listing; original ZOR drawing not fully obtained — https://www.digikey.com/en/products/detail/yageo/ZOR-25-R-52-0R/18795
- **C320-DS**：KEMET exact C320C104K5R5TA specification, generated October 19, 2026 — https://search.kemet.com/component-documentation/download/specsheet/C320C104K5R5TA
- **C320-SALE**：DigiKey C320C104K5R5TA exact listing, indexed stock indication — https://www.digikey.com/en/products/detail/kemet/C320C104K5R5TA/818040
- **R82-DS**：KEMET exact R82DC3100AA50J specification, generated October 23, 2026 — https://search.kemet.com/component-documentation/download/specsheet/R82DC3100AA50J
- **R82-SALE**：Newark 68X3241 exact listing; immediate inventory not established — https://www.newark.com/kemet/r82dc3100aa50j/cap-0-1-f-40v-5-pet-radial/dp/68X3241
- **FR-DS**：Panasonic exact EEUFR1H100 product specification — https://industrial.panasonic.com/ww/products/pt/aluminum-cap-lead/models/EEUFR1H100
- **FR-SALE**：LCSC C178701 exact listing; real-time quantity not verified — https://www.lcsc.com/product-detail/C178701.html
- **TE-DS**：TE 5787834-1 active product, engineering drawing 5787834 revision C — https://www.te.com/en/product-5787834-1.html
- **LUM-DS**：Lumberg 2411 02 original datasheet explicitly says Obsolete — https://downloads.lumberg.com/datenblaetter/en/2411_02.pdf
- **PHX-DS**：Phoenix 1715721 MKDS 1,5/2-5,08 official dimensions — https://www.phoenixcontact.com/en-us/products/pcb-terminal-block-mkds-15-2-508-1715721
- **SAM3**：Samtec TSW-103-07-G-S exact manufacturer listing — https://www.samtec.com/products/tsw-103-07-g-s
- **SAM4**：Samtec TSW-104-07-G-S exact manufacturer listing — https://www.samtec.com/products/tsw-104-07-g-s
- **SAM5**：Samtec TSW-105-07-G-S exact manufacturer listing — https://www.samtec.com/products/tsw-105-07-g-s
- **SOCKET-DS**：Harwin M20-7822046 exact manufacturer product — https://www.harwin.com/products/M20-7822046
- **SOCKET-DWG**：Harwin M20-782 technical drawing, rev 11, August 3, 2026 — https://content.harwin.com/asset/53851ba8-b32e-4ac5-a0c5-09d9271c0c0a/DRG-00385-Technical-Drawing-Datasheet-M20-782-pdf.pdf
- **SOCKET-SALE**：DigiKey Harwin M20-7822046 listing, indexed stock indication — https://www.digikey.com/en/products/detail/harwin-inc/M20-7822046/3727872
- **R-100K**：Exact YAGEO MFR-25FBF52-100K sale listing; indexed observation — https://www.digikey.com/en/products/detail/yageo/MFR-25FBF52-100K/13473
- **R-680R**：Exact YAGEO MFR-25FBF52-680R sale listing; indexed observation — https://www.digikey.com/en/products/detail/yageo/MFR-25FBF52-680R/9138201
- **R-20R**：Exact YAGEO MFR-25FBF52-20R sale listing; indexed observation — https://www.digikey.com/en/products/detail/yageo/MFR-25FBF52-20R/12661
- **R-1R**：Exact YAGEO MFR-25FBF52-1R sale listing; indexed observation — https://www.digikey.com/en/products/detail/yageo/MFR-25FBF52-1R/9138095
- **R-4K7**：Exact YAGEO MFR-25FBF52-4K7 sale listing; indexed observation — https://www.digikey.com/en/products/detail/yageo/MFR-25FBF52-4K7/9138176
- **R-180K**：Exact YAGEO MFR-25FBF52-180K sale listing; indexed observation — https://www.digikey.com/en/products/detail/yageo/MFR-25FBF52-180K/9138057
- **R-1M2**：Exact YAGEO MFR-25FBF52-1M2 sale listing; indexed observation — https://www.digikey.com/en/products/detail/yageo/MFR-25FBF52-1M2/9138071
- **R-220R**：Exact YAGEO MFR-25FBF52-220R sale listing; indexed observation — https://www.digikey.com/en/products/detail/yageo/MFR-25FBF52-220R/9138097
- **R-47K**：Exact YAGEO MFR-25FBF52-47K sale listing; indexed observation — https://www.digikey.com/en/products/detail/yageo/MFR-25FBF52-47K/9138173
- **R-100R**：Exact YAGEO MFR-25FBF52-100R sale listing; indexed observation — https://www.lcsc.com/product-detail/C6300650.html
- **R-10K**：Exact YAGEO MFR-25FBF52-10K sale listing; indexed observation — https://www.digikey.com/en/products/detail/yageo/MFR-25FBF52-10K/13219
- **R-68R**：Exact YAGEO MFR-25FBF52-68R sale listing; indexed observation — https://www.digikey.com/en/products/detail/yageo/MFR-25FBF52-68R/9138203
- **R-1K**：Exact YAGEO MFR-25FBF52-1K sale listing; indexed observation — https://www.digikey.com/en/products/detail/yageo/MFR-25FBF52-1K/13011
- **SAM-CAT**：Samtec TSW/HTSW原厂目录F-226，-07直针尺寸A10.92/B2.54/C5.84mm；只核标称值 — https://suddendocs.samtec.com/catalog_english/tsw_th.pdf
- **R-4K7-ALT**：DigiKey准确包装候选MFR-25FRF52-4K7，1/4W、4.7kΩ、1%，有切带/卷带目录，实时供货待核 — https://www.digikey.com/en/products/detail/yageo/MFR-25FRF52-4K7/9139057
- **FUSE-SALE**：TME准确料号0251001.MXL公开销售页；无本轮实时库存承诺 — https://www.tme.com/us/en-us/details/0251001.mxl/axial-fuses-super-fast/littelfuse/
- **BAS-DS**：Nexperia BAS116H原厂Rev3，2011-05-31；两脚SOD123F低漏电单管方向；完整机械图本轮仍未取得 — https://assets.nexperia.com/documents/data-sheet/BAS116H.pdf
- **BAS-PROD**：Nexperia BAS116H原厂页检索标Production — https://www.nexperia.com/product/BAS116H
- **BAS-SALE**：LCSC准确型号BAS116H,115，C74210；检索页面有库存指示，未复核实时数量 — https://www.lcsc.com/zh-TW/product-detail/C74210.html
- **BAS-SALE-2**：DigiKey准确型号BAS116H,115；检索标缺货可预订，渠道供应状态不同 — https://www.digikey.com/en/products/detail/nexperia-usa-inc/BAS116H-115/1163691
- **ZOR-DS**：YAGEO Leaded Resistors原厂目录，DigiKey托管，PDF物理p38：ZOR-25专属尺寸表；历史版次与当前批次适配待核 — https://media.digikey.com/pdf/Data%20Sheets/Yageo%20PDFs/Leaded%20Resistors.pdf

## 本轮产物与核验

- [CSV完整主表](component-package-audit-continued.csv)和[JSON结构化主表及资料索引](component-package-audit-continued.json)：64项。
- [核心板管脚对应CSV](coreboard-pin-mapping.csv)：17项逻辑→F103管脚与标准Blue Pill实体位置；PA13/PA14标注为独立SWD。
- [实际库几何及源文件哈希](continuation-footprint-geometry.json)：19个库封装。
- [续审核验结果](continuation-verification.json)：工程不变、64位号完整性及数量核验；[硬件哈希基线](continuation-hardware-before.json)覆盖7个原工程文件。

- [原生ERC报告](erc.json)、[原生XML网表](voltmeter-v2.3-draft.xml)、[蓝图比较结果](blueprint-check.json)、[图符清单](component-inventory.json)及[标签清单](label-inventory.json)。清单从原理图独立解析，不是MCP实测导出。
- [原网表导出命令记录](command-1.json)和[原ERC执行记录](command-2.json)保留当时的临时副本路径及原始退出码；这些路径用于说明来源，复核时使用下方归档入口。

## 归档证据复核

在仓库根目录执行以下命令，以现有只读核对脚本比较归档网表和当前蓝图。`PYTHONDONTWRITEBYTECODE=1`避免写入字节码；`--blueprint`指定当前蓝图，`--netlist`与`--inventory`指向本报告归档证据，脚本同时读取同目录的标签清单。

```bash
PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify_v2_3_netlist.py \
  --blueprint hardware/v2.3/connections-draft.json \
  --netlist docs/reviews/2026-10-23-component-package-audit/voltmeter-v2.3-draft.xml \
  --inventory docs/reviews/2026-10-23-component-package-audit/component-inventory.json
```

该命令核对连接数据；归档ERC仍按报告记录的工具版本和忽略规则解读。发布时未重新执行ERC、预算脚本或实物验证。
