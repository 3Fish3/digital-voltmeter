# 双通道数字直流电压表 PCB

## 当前版本入口

**当前设计版本：V2.3受控原理图草案。** 文档同步和Git提交不升级设计版本；远端是否同步以实际提交与推送核验为准，仓库发布不表示硬件已验收。

当前新版工作目录为 [pcb_pcb_pcb/](pcb_pcb_pcb/README.md)，最新资料见 [V2.3受控原理图审查](pcb_pcb_pcb/docs/V2.3-controlled-schematic-review.md)与[继续整改依据](pcb_pcb_pcb/docs/V2.3-followup-evidence.md)。当前仍为原理图草案，封装未定、无PCB、无新版采购BOM，P0未关闭，禁止投板。

`digital-voltmeter-pcb/`、`new_pcb/` 与根目录 `docs/` 保留旧工程和历史资料；其中 `docs/bom.csv` 不是新版采购依据。下文仅为旧版说明，不用于定义新版电路或板框。

## 旧版V1.1说明（历史资料）

基于《现代电子综合训练——数字电压表项目全套填报材料（第6组方案 V1.1）》的 KiCad 硬件工程。

- 量程：CH1 / CH2 各 0–5 V 单极性直流
- ADC：ADC0832，双通道复用，准同步采集
- 主控：STM32F103C8T6 Blue Pill（可插拔）
- 模拟前端：MCP6002-P（DIP-8）双路缓冲 + 3.3 kΩ / 1 µF RC 低通
- 逻辑接口：74AHCT125（DIP-14）将 STM32 3.3 V 的 `CS` / `CLK` / `DI` 转换为 5 V；ADC `DO` 采用 20 kΩ / 10 kΩ 分压至 3.3 V
- 电源：面板 DC 输入与开关，经 LM2596 输出 5 V；ADC 支路采用磁珠（或 10 Ω）+ 10 µF + 100 nF 净化
- PCB：双层 FR-4、1.6 mm，初始目标板框 120 × 85 mm；BNC / DC 插座 / 电源开关为面板安装件

> 生产文件必须在原理图、封装、实物尺寸和 PCB DRC 全部确认后再导出。
