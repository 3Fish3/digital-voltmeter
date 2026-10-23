# KiCad MCP 接入检查点

- 完成时间：2026-10-23 01:56 EDT（America/New_York，UTC−04:00）。
- 任务：将原理图与 PCB MCP 工具接入本机 Codex。
- 仓库：`/home/kekeyuyu/projects/digital-voltmeter`，分支 `main`，跟踪 `origin/main`。

## 已完成与验证

- 使用 uv 独立工具环境安装 `mcp-server-kicad==0.21.1`；环境位于 `/home/kekeyuyu/.local/share/uv/tools/mcp-server-kicad/`，入口为 `/home/kekeyuyu/.local/bin/mcp-server-kicad`。未向系统 Python 安装依赖。
- 通过 `codex mcp add` 在 `/home/kekeyuyu/.codex/config.toml` 新增全局 `kicad` STDIO 服务。`codex mcp get kicad --json` 确认启用；逐项比较配置结构，除新增服务外所有原有配置保持一致，包括 `pi-web-access` 和 `pi-lens`。
- 固定 `KICAD_CLI_PATH=/usr/bin/kicad-cli`、`KICAD_PYTHON=/usr/bin/python3`；配置本机 7897 HTTP 和 7898 SOCKS5 代理，回环地址走 `NO_PROXY`。全局服务不绑定此项目的设计文件，每次调用传绝对路径。
- 从 PyPI 下载的 0.21.1 wheel 经 SHA-256 校验：`2d38fae3bd9c57f04d7e7784c16d8aa0320d3a0f7321614d1f4613aee6c68dc1`。与另一客户端已有的 `uvx mcp-server-kicad` 配置同源；未修改另一客户端配置。
- 实际 STDIO 初始化返回服务器 `kicad` / `0.21.1`，列出 109 个工具；`get_version` 返回 KiCad 10.0.6。
- 读取现行原理图：A1，67 个图符（含供电声明）、186 个局部标签、267 根线、7 个结点、5 个 NC。
- 在 `/tmp/digital-voltmeter-kicad-setup/` 的原理图副本中修改 R40 属性，再通过工具读取确认；对副本调用原生 ERC，报告 0 项。此项只验证工具调用与文件兼容性。
- 用本机 `pcbnew` 创建临时测试板，通过 MCP 添加 10 mm、0.25 mm 宽 F.Cu 走线并读回；原生 DRC 返回预期 `track_dangling` 警告，验证报告通路有效。
- 对 `hardware/v2.3/` 的全部 6 个文件比较前后 SHA-256，无修改、无新增文件。未创建项目正式 PCB。
- 验证记录：`.tmp/kicad-mcp-integration/` 中的 `probe-result.json`、`registration-report.json`、`tools.json`、`installed-packages.json` 和哈希基线。该目录为可重建的本地记录。

## 决策与工作区边界

- 复用现有客户端采用的 Python 包，使用固定版本独立安装；不引入 Node 版第二套服务器。
- 原仓库已有 README 修改、旧文档路径删除和新版本文档目录等未提交改动，另有 `docs/progress.md`、`docs/project-goals.md`。均保留；本任务不暂存、不提交、不修改 Git 引用。
- 收尾只读检查还观察到 `docs/design-report.md` 和 `docs/pin-connections.csv` 为未跟踪文件；这两项不是本任务创建，未修改。
- 本任务在项目中只新增本检查点及忽略目录 `.tmp/` 下的验证记录。
- 参考 OpenAI 官方 MCP 配置文档（`https://developers.openai.com/codex/mcp`）与固定版本包元数据/源码；依赖下载经过本机代理并保持 TLS 校验。

## 待完成与限制

- 当前运行会话的工具目录没有动态加载新服务；需重新打开本机 Codex 会话，再确认 `kicad` 出现在 `/mcp` 中。配置已注册及直接握手通过，与新会话是否实际加载分开记录。
- 尚未测试自动布线、Freerouting、全部 109 个工具或 GUI 实时联动。本次验证针对磁盘文件工具与原生检查调用。
- 上游 0.21.1 的包说明标注自 2026 年 10 月进入维护模式，仅接受安全与 KiCad 兼容性修复；本次采用固定版本并记录依赖版本。
- V2.3 仍为原理图草案，封装、器件选型及既有 P0 验收工作继续按 `docs/progress.md` 的问题表执行，现行设计见 `docs/design-report.md`。

## 恢复第一步与回退

1. 重新打开本机 Codex 会话，用 `/mcp` 检查 `kicad`，然后调用 `get_schematic_summary`，显式传入 `/home/kekeyuyu/projects/digital-voltmeter/hardware/v2.3/voltmeter-v2.3-draft.kicad_sch`。
2. 需要排查时，`codex mcp get kicad --json` 只读取该服务的启用状态、命令和环境设置；原理图入口见 `docs/design-report.md`，阻断条件见 `docs/progress.md`。
3. 需要撤回接入时，`codex mcp remove kicad` 仅移除名为 `kicad` 的 Codex 配置项；`uv tool uninstall mcp-server-kicad` 移除本次独立工具环境及其入口。两条命令均未执行，使用前按当时授权操作；不会更改电路文件。
