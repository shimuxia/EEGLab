# Windows 本地统一官网交接

严颖课题组统一官网 V1 已可浏览。交给下一位执行者的工作是用户看过画廊后选定的视觉和交互修订。由一位执行者独占工作树，同一台 Windows 笔记本复用以下目录。

| 项目 | 位置或版本 |
|---|---|
| Windows 仓库 | `D:\AI-Agent-Workspace\Projects\YanYing-EEGLab-Merge\repo` |
| WSL 仓库 | `/mnt/d/AI-Agent-Workspace/Projects/YanYing-EEGLab-Merge/repo` |
| Windows QA（与 repo 同级） | `D:\AI-Agent-Workspace\Projects\YanYing-EEGLab-Merge\qa\codex-backend-visual-v1-20261119` |
| 本地分支 | `feat/yanying-codex-backend-visual-v1` |
| 开发基点 | `ef4720e90dfdd336c0ab4a62ccb1275127bb9c6a` |
| 后端提交 | `7d3d4b29b8b6e9b2e0b151d3ac95ceee9f46e893` |
| 完整视觉源码提交 | `e11630c52a6e32600bad681a3924862de188993c` |

最终含文档的 HEAD 已由 QA 目录中的 `SCREENSHOT_INDEX.md`、`FINAL_CODEX_V1_REPORT.md` 记录。交接时用 WSL 的 `git rev-parse HEAD`、`git status --short --branch` 核对。沿用本机项目登记、TASKS 和独占锁流程。

## 打开成品

在 Windows PowerShell 运行下列命令。脚本校验回环服务的项目标识，复用或启动本项目，然后在 Chrome 中打开官网和截图画廊。关机后也可用相同命令恢复。停止方式见 QA 中的 STOP_PREVIEW.md。

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "D:\AI-Agent-Workspace\Projects\YanYing-EEGLab-Merge\qa\codex-backend-visual-v1-20261119\Open-Preview.ps1"
```

## 本机复验

进入上表的 WSL 仓库后使用现有 Linux Node 和项目虚拟环境运行。启动脚本提供同源的已构建静态文件和本地只读 API，默认端口 4327。若修改前端，先重新构建再刷新。浏览器审查脚本向 QA 输出写证据，复跑请使用新的输出目录。

```bash
source .venv/bin/activate
npm run test:backend
npm run test:frontend
(cd frontend && node_modules/.bin/tsc --noEmit)
npm run build
python scripts/check_deployment.py
export QA_OUTPUT_DIR="$(mktemp -d)" QA_PREVIEW_PORT=4327
export CHROMIUM_PATH="$HOME/.cache/ms-playwright/chromium-1228/chrome-linux64/chrome"
python scripts/check_group_site.py
python scripts/check_adversarial_site.py
python scripts/check_original_people.py
```

## 受保护行为

- 路由、旧锚点、来源署名、导师职务、招生条件、成员分组以仓库现有数据为准。逐页入口与样式见 [视觉说明](CLAUDE_CODE_VISUAL_BRIEF.md)。
- 成果页读 /api/group/papers。研究者、版本、同步状态、ETag、查询筛选与手工审核均已有本地回归。严颖目录仅公开符合核验条件的关联，明确误收按研究者排除。旧目录与课题组目录各有来源策略。
- 审核决定、代表作、手工期刊信息、两条误收保护、管理鉴权、备份校验、COS/SCF 和发布配置均属于业务边界。视觉修改应保留这些模块及前端分页与回退契约。
- 成功态的两条是本地核验子集。服务异常时同一模块显示已有三篇静态代表作、状态与重试入口。注意核对研究者切换、假数据异常和空结果展示。
- 本轮后续仅限用户确认的前端设计、布局、组件、动效、无障碍和交互缺陷。本地验证后供用户复审。推送、发布、外部服务、正式数据恢复和后台同步均需另立任务。
