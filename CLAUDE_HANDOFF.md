# 严颖课题组统一官网 · Windows 本地 V2 交接

Windows 仓库为 `D:\AI-Agent-Workspace\Projects\YanYing-EEGLab-Merge\repo`。WSL 仓库为 `/mnt/d/AI-Agent-Workspace/Projects/YanYing-EEGLab-Merge/repo`。本地分支 `feat/yanying-visual-v2-best-of-both`，基点为已完成后端收口的 V1 `4c4aa21d7904a88a849ea69168eff0c378c33469`。本轮最终完整 SHA 由同级 QA 目录的截图索引和最终报告记录，接手前用 `git rev-parse HEAD` 核对。

## 本机打开

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "D:\AI-Agent-Workspace\Projects\YanYing-EEGLab-Merge\qa\visual-v2-best-of-both-20261119\Open-Preview.ps1"
```

脚本复用本项目已有回环启动器，验证首页具有 V2 研究图版，然后打开 Chrome 和 V1/V2 对照画廊。默认端口 4327；端口占用时核对脚本实际输出。关机后可重新执行。工作区内的 `qa/visual-v2-best-of-both-20261119` 保存选型、两份原站渲染、截图原图、全部日志及 `FINAL_VISUAL_V2_REPORT.md`。在画廊点击左右原图可检查小屏、全页和异常状态。

## 开发与检查

在既有 WSL 仓库根目录使用现有依赖。测试浏览器通过项目 QA 开发依赖、缓存的 Chromium 和 axe 运行。先构建，待构建完成后再对预览开始浏览器验收，避免静态目录重建期间产生无效的 404。

```bash
git status --short --branch
source .venv/bin/activate
npm run test:frontend
npm run test:backend
(cd frontend && node_modules/.bin/tsc --noEmit)
npm run build
python scripts/check_deployment.py
export QA_OUTPUT_DIR="$(mktemp -d)" QA_PREVIEW_PORT=4327
export CHROMIUM_PATH="$HOME/.cache/ms-playwright/chromium-1228/chrome-linux64/chrome"
python scripts/check_group_site.py
python scripts/check_adversarial_site.py
python scripts/check_original_people.py
```

## 内容边界

站点保留 13 个正式路由、404、七个方向和五个脑机专题。成果页读 /api/group/papers；两篇历史误收的排除以研究者为范围，保留其他研究者的有效关联。本机预览以两个经接受 DOI 匹配的种子条目为正常态，全量未知。目录为空或失联时展示标明来源的三篇原有代表作。禁止通过静态数字替代目录、改变论文 API、放宽归属或覆盖人工审核。

V2 沿用已有学术履历、成员状态、招生、联系、图像和署名。后续视觉工作可调整 Astro 布局、样式、键盘交互及媒体呈现。完整设计意图见 [视觉交接](CLAUDE_CODE_VISUAL_BRIEF.md)。本轮没有用户对 V2 的审美认可记录。下一轮须以用户看片反馈为准，由一位执行者持锁操作；本次没有启动 Claude Code。线上配置、云环境、生产数据和发布另属授权范围。
