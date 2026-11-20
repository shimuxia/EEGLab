# 严颖课题组统一官网 · Windows 本地 V3 交接

Windows 仓库为 `D:/AI-Agent-Workspace/Projects/YanYing-EEGLab-Merge/repo`，WSL 对应 `/mnt/d/AI-Agent-Workspace/Projects/YanYing-EEGLab-Merge/repo`。本地分支为 `feat/yanying-visual-v3-motion-first`，V2 回看基点为 `453f26dbebba0f2815f7256e275ea84bf2b6c20a`。V3 完整提交见同级工作区 `qa/visual-v3-motion-first/FINAL_VISUAL_V3_REPORT.md` 和截图索引。交接时使用 `git rev-parse HEAD` 核对。

## Windows 预览

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "D:/AI-Agent-Workspace/Projects/YanYing-EEGLab-Merge/qa/visual-v3-motion-first/Open-Preview.ps1"
```

启动器核对项目标识和 V3 首页，打开三个 Chrome 标签。第一个为回环官网；第二个提供 69 组同状态 V2/V3 浏览器截图，点击可打开原图；第三个提供五段 Windows Chrome 实录，可跳到交互发生的时间点。证据保存在本机同级 QA 目录。

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

V3 使用原有履历、成员、招生、联系和媒体素材。后续 Windows Claude Code 若收到用户授权，仅精修前端版式、色彩、交互与媒体呈现。实际启动和账号选择由用户决定。V1、V2 的视觉已被用户否定，V3 的最终审美评议待用户查看。见 [视觉交接](CLAUDE_CODE_VISUAL_BRIEF.md)。

## V3 专项复验

在上述 WSL 仓库根目录执行 `bash ../qa/visual-v3-motion-first/final_regression.sh` 运行浏览器与工程回归，执行 `bash ../qa/visual-v3-motion-first/final_motion_run.sh` 以 Windows Chrome 重录五段实况并在本机验证解码。运行前确认回环预览已指向待测版本。复跑会替换同名 QA 证据，需保留历史证据时先复制 QA 目录。
