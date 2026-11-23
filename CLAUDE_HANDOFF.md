# 严颖课题组统一官网 · 本地交接

Windows 仓库 `D:/AI-Agent-Workspace/Projects/YanYing-EEGLab-Merge/repo`，WSL 对应 `/mnt/d/AI-Agent-Workspace/Projects/YanYing-EEGLab-Merge/repo`。开发、Git、构建和测试都在 WSL 中进行。交接时用 `git rev-parse HEAD` 核对。

## 当前：Claude 视觉候选版 r2（2026-11-23）

- 分支 `feat/yanying-claude-art-direction-r2`，基于上一版 `feat/yanying-claude-art-direction` @ `1e509fb`（保留为回退基线），后者基于 V3 `89acaf446a5205169643be81fda5dd67e67bc073`。
- r2 补回了源站内容，并修订了色彩、背景层级、标题比例和研究图形。逐项核对见 [SOURCE_CONTENT_MATRIX.md](SOURCE_CONTENT_MATRIX.md)。
- 状态：**待用户审美确认的候选版**，只做了本地提交，没有 push、PR、merge 或部署。
- 设计依据见 [DESIGN_RATIONALE.md](DESIGN_RATIONALE.md)，修改清单与证据路径见 [CLAUDE_VISUAL_FINAL_REPORT.md](CLAUDE_VISUAL_FINAL_REPORT.md)。
- QA 证据（截图对比、动效实录、回归日志）都在仓库外的 `../qa/claude-art-direction-20261122/`，r2 的证据在其中的 `r2/` 子目录，不进 Git。

### 样式结构（`frontend/src/styles/`，按加载顺序）

| 文件 | 内容 |
|---|---|
| `global.css` | 设计 token（颜色、字体、字阶、标题三档、间距、时长、缓动）、reset、基础排版、按钮 `.btn`、链接 `.link`、小标 `.kicker` |
| `theme.css` | 共享组件：区块标题、`.band-mist` / `.sheet` 背景层、研究科学图形 `.research-glyph`、研究选项卡、荣誉列表、页头、人像卡、分段筛选、状态块 |
| `group.css` | 首页构图 |
| `pages.css` | 内页构图（研究、实验室、专题详情、团队、关于、招生、联系、成果、404） |
| `edition.css` | 动效（入场、描线、扫描线、滚动显现、跨页过渡），全部受 `prefers-reduced-motion` 约束 |

主要 token（r2）：`--canvas #f2f3ef`（页面底色）、`--bg #fff`（内容纸面）、`--bg-surface #e8ebe6`（雾灰带）、`--bg-dark #20272b`（只用于视频画框）、`--text #1c2125`、`--text-2 #4a5157`、`--text-3 #5d6469`、`--graph #5f7f87` / `--graph-dim #a8b8bb`（科学图形线条）、`--graph-text #46646c`（青色文字）、`--accent #b33c0b`（文字橙）、`--signal #e0601a`（图形焦点橙）；标题三档 `--fs-h1/h2/h3`，间距 `--space-section`、`--space-head`。字体只用系统栈：Windows 为 Segoe UI Variable + 微软雅黑，macOS 为 PingFang SC，Linux 为 Noto Sans CJK，没有打包任何字体文件。

### 新增与重写的组件

- `components/ResearchGlyph.astro`：老师站的 7 张研究方向示意图（数据在 `src/data/research-visuals.json`），首页研究焦点、选项卡（`ResearchArtwork`）、研究页共用。
- `src/data/source-extras.ts`：r2 从两个源站逐字补回的内容（方向短句、研究说明、履历第 2–3 段与学位信息、导师寄语、招生导语、“招生中”与“更多同学”条目、项目/专利卡、实验室口号与导语、实验室加入说明与申请要求、实验室域名），每段都注明出处。
- `scripts/make_wall_thumbs.py`：首页图片墙缩略图生成（输出到 `frontend/public/images/achievements/wall/`，需要 Pillow）。
- `src/lib/signals.ts` + `components/SignalTrace.astro`：现在只用于 404 页的脑电波形。
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
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "D:/AI-Agent-Workspace/Projects/YanYing-EEGLab-Merge/qa/claude-art-direction-20261122/r2/Open-Preview-r2.ps1"
```

### 检查命令

```bash
# WSL，仓库根目录；需要 4327 指向当前构建
bash ../qa/claude-art-direction-20261122/regression.sh r2/regression-final
# 源站内容完整性（331 项）：
python -I ../qa/claude-art-direction-20261122/r2/check_content.py
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
- 两处奖项日期在两个源站之间不一致，实验室电话是否公开也未定，都在 SOURCE_CONTENT_MATRIX.md 中标为待确认，等老师决定。
- Safari / iOS 真机没有验收。

## 回退到上一版或 V3

```bash
git switch feat/yanying-claude-art-direction     # 1e509fb，r2 之前的 Claude 版
```


```bash
git switch feat/yanying-visual-v3-motion-first   # 89acaf4，未改动
```

V3 的交接内容、启动器和证据保持原样：`../qa/visual-v3-motion-first/`（`FINAL_VISUAL_V3_REPORT.md`、`Open-Preview.ps1`、`final_regression.sh`）。V3 的视觉说明见 [CLAUDE_CODE_VISUAL_BRIEF.md](CLAUDE_CODE_VISUAL_BRIEF.md)（历史文档）。
