# Blue Pill 双排排母尺寸检验工具（V2.3）

用途：输出毫米制 1:1 SVG **针中心定位图**，帮助比对实物 Blue Pill 两条公排针的中心位置，**不是 KiCad Footprint、PCB 钻孔数据或制造文件**。

当前主控是 STM32F103C8T6 Blue Pill。标准参考板名义值为双排各 20 针、同排 2.54 mm、排中心距 15.24 mm；实际克隆板需要量测。此前实测 15.8 mm 是两侧针金属外表面的总跨距，**不等于排中心距**。两针等宽且沿跨排方向各为 w 时才有“中心距 = 外跨 - w”；不能将候选排母声称适配的 0.64 mm 方针当作已经测到的针宽。

名义预览：
```bash
python3 scripts/bluepill_fit_template.py --nominal-preview --output .tmp/bluepill/preview.svg
```

录入实际测量的数据才可生成测量图（下列数值**仅作命令格式示例，不是实测确认**）：
```bash
python3 scripts/bluepill_fit_template.py --center-mm 15.16 --pitch-mm 2.54 --pins-per-row 20 --output .tmp/bluepill/measured.svg
```

SVG 采用 USB 朝上、顶视图，A 排在左、B 排在右；请用打印软件设置实际大小/100%，关闭“适合页面”，并实测图中 10 mm 刻度。40 个标记只表示中心，不是焊孔直径或焊盘形状。须继续核对两排数量、实际针宽、中心距、USB 外伸、底部器件高度、排母选型和实物 1:1 试插。

**独立阻塞条件：** PA13/SWDIO 与 PA14/SWCLK 不在两条 20 针长排上，需要额外 SWD 连接；标准 Blue Pill 的 5V 针与 USB VBUS 相通，底板供电时不得同时将板载 USB 接入另一电源。上述事项必须在结构与电气验收时处理，本工具不做电源保护验证。

测试：
```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_bluepill_fit_template.py -v
```

**范围：** 只增添检查工具、测试和说明。V2.3 原理图、图符、64 项封装、BOM 和 PCB 不变。尚未取得实物尺寸或真实 PCB 制造准入。
