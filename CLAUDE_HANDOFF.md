# 严颖课题组统一官网 · 本地交接

Windows 仓库 `D:/AI-Agent-Workspace/Projects/YanYing-EEGLab-Merge/repo`，WSL 对应 `/mnt/d/AI-Agent-Workspace/Projects/YanYing-EEGLab-Merge/repo`。开发、Git、构建和测试都在 WSL 中进行。交接时用 `git rev-parse HEAD` 核对。

## 当前：Claude 视觉候选版（2026-11-22）

- 分支 `feat/yanying-claude-art-direction`，基于 V3 `89acaf446a5205169643be81fda5dd67e67bc073`。
- 状态：**待用户审美确认的候选版**，只做了本地提交，没有 push、PR、merge 或部署。
- 设计依据见 [DESIGN_RATIONALE.md](DESIGN_RATIONALE.md)，修改清单与证据路径见 [CLAUDE_VISUAL_FINAL_REPORT.md](CLAUDE_VISUAL_FINAL_REPORT.md)。
- QA 证据（截图对比、动效实录、回归日志）都在仓库外的 `../qa/claude-art-direction-20261122/`，不进 Git。

### 样式结构（`frontend/src/styles/`，按加载顺序）

| 文件 | 内容 |
|---|---|
| `global.css` | 设计 token（颜色、字体、字阶、间距、时长、缓动）、reset、基础排版、按钮 `.btn`、链接 `.link`、小标 `.kicker` |
| `theme.css` | 共享组件：区块标题、标签列表、信号波形、研究选项卡、荣誉列表、页头、人像卡、分段筛选、状态块 |
| `group.css` | 首页构图 |
| `pages.css` | 内页构图（研究、实验室、专题详情、团队、关于、招生、联系、成果、404） |
| `edition.css` | 动效（入场、描线、扫描线、滚动显现、跨页过渡），全部受 `prefers-reduced-motion` 约束 |

主要 token：`--bg #fff`、`--bg-surface #f3f3f0`、`--bg-dark #141618`、`--text #16181b`、`--text-2 #45494f`、`--text-3 #6a6f76`、`--accent #c2410c`（文字橙）、`--signal #e8590c`（图形橙）、`--signal-on-dark #ff7a2f`。字体只用系统栈：Windows 为 Segoe UI Variable + 微软雅黑，macOS 为 PingFang SC，Linux 为 Noto Sans CJK，没有打包任何字体文件。

### 新增与重写的组件

- `src/lib/signals.ts` + `components/SignalTrace.astro`：七个方向的确定性波形，首页索引、选项卡图版（`ResearchArtwork`）、研究页和 404 共用。
- `SectionHeader.astro`：所有内页共用的页头（小标 / 标题 / 英文副标 / 本页目录）。
- 重写：`Nav`、`Footer`、`GroupHonors`、`GroupMembers`、`GroupResearch`、`Advisor`、`Admission`、`DevicePlate`；`PublicationsExplorer`、`RelatedPublications`、`GalleryFilter` **只改样式字符串，逻辑未动**。
- `achievements.astro` 和 `research/[slug].astro` 改用统一的 `GroupLayout`（原来各自拼装 Layout、Nav 和自带的 `<main>`）。

### 保持不变的契约

13 个正式路由加 404；7 个 `role=tab` 与 `#research-panel-N`；`[data-hero-video]` / `[data-video-toggle]` / `[data-video-status]` 与“播放/暂停实验视频”按钮名；`.home-hero-copy` / `.hero-bottom` / `.hero-actions`；人物区白底且照片不加滤镜；`.gf-chip`、`.pr-title`、`.stats-row .stat-num`；`#nav-toggle` / `#nav-links`。论文 API、排除规则、后端、数据文件都没有改动。

### 预览

```bash
# WSL，仓库根目录
npm run build
# 4327 由 ../qa/codex-backend-visual-v1-20261119/preview.py 提供，直接服务 frontend/dist，重建即生效。
# 若服务已停：
.venv/bin/python ../qa/codex-backend-visual-v1-20261119/preview.py start 4327
# V3 冻结对照版（可选，端口 4328）：
nohup .venv/bin/python ../qa/claude-art-direction-20261122/v3_preview.py 4328 >/dev/null 2>&1 &
```

Windows 一键打开（新版官网、对比画廊、动效实录）：

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "D:/AI-Agent-Workspace/Projects/YanYing-EEGLab-Merge/qa/claude-art-direction-20261122/Open-Preview.ps1"
```

### 检查命令

```bash
# WSL，仓库根目录；需要 4327 指向当前构建
bash ../qa/claude-art-direction-20261122/regression.sh regression-final
#   test:frontend、tsc、test:backend、check_deployment、check_group_site、
#   check_original_people、check_adversarial_site
# Windows：同状态截图与动效实录（Windows Chrome 无头）
node ../qa/claude-art-direction-20261122/capture.cjs http://127.0.0.1:4327 compare/claude
node ../qa/claude-art-direction-20261122/motion.cjs  http://127.0.0.1:4327 motion
# WSL：编码实录
python3 -I ../qa/claude-art-direction-20261122/encode.py ../qa/claude-art-direction-20261122/motion
```

### 已知限制

- 本地论文目录只有 2 篇经 DOI 核验的种子条目，生产 105 篇的完整导入没有在本地验证。
- 跨页过渡依赖 Chromium 的 cross-document View Transition；Safari 和 Firefox 会直接跳转，功能不受影响。
- 成员证件照的底色（蓝/白）来自原图，按既有约定不加滤镜，所以团队页仍有色块差异。
- Safari / iOS 真机没有验收。

## 回退到 V3

```bash
git switch feat/yanying-visual-v3-motion-first   # 89acaf4，未改动
```

V3 的交接内容、启动器和证据保持原样：`../qa/visual-v3-motion-first/`（`FINAL_VISUAL_V3_REPORT.md`、`Open-Preview.ps1`、`final_regression.sh`）。V3 的视觉说明见 [CLAUDE_CODE_VISUAL_BRIEF.md](CLAUDE_CODE_VISUAL_BRIEF.md)（历史文档）。
