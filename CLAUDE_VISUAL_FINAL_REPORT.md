# Claude 视觉候选版 · 最终报告

> 状态：**Claude 视觉候选版 r3**，等待用户亲眼确认审美。只做了本地提交，没有 push、PR、merge、部署，也没有访问服务器、EdgeOne、备案或生产数据。

## r3（2026-11-24）

| 项 | 值 |
|---|---|
| 分支 | `feat/yanying-claude-art-direction-r3`（本文件所在提交即 HEAD） |
| 回退基线 | r2 `753402bfaef2a7dc56764bc6935fb24479c3e976`；第一版 `1e509fb`；V3 `89acaf4`（均未改动） |
| 本地预览 | http://127.0.0.1:4327/ |

**做了什么**：按 Claude 的审美重做视觉层（理由见 DESIGN_RATIONALE.md 的 r3 一节）。

- 自托管开源字体：思源黑体可变字体 4.6 MB，分 101 片，按页面需要加载；Inter 140 KB。
- 新色板：纸、墨、石板蓝、暖橙；实验室相关区块使用冷色调。
- 形态卡片化：圆角卡片、胶囊控件、轻阴影；减少线框。
- 首屏改为“七个方向，一条主线”动画索引，手机上为竖向时间轴。
- 导师位置修正（2026-11-25，按用户反馈）：撤掉首屏角落的小卡片，在首屏之后单独设“课题组负责人”一节，包含照片、姓名、职务、履历、研究兴趣与学术荣誉。
- 内页全部按同一套语言重排。

内容和逻辑未变：路由、测试契约、论文与后端逻辑都没有改动。

**本轮实际运行的检查**（证据在 `qa/claude-art-direction-20261122/r3/`；导师位置修正后又完整重跑了一遍，结果在 `r3/regression-advisor-3/`）：

- `npm run build`、`test:frontend`、`tsc`、`test:backend`、`check_deployment`、`check_group_site`、`check_original_people`、`check_adversarial_site`（含 axe WCAG 2.2 AA）全部通过，日志在 `r3/regression-final/`。
- 自查中发现并修正一处对比度问题：成果页侧栏计数原来用了透明度，已改为实色。
- 源站内容完整性 331/331，见 `r3/content-check.log`。
- 图片墙状态检查通过，见 `r3/wall-check.log`。

**证据**：

- `r3/GALLERY.html`：r2 与 r3 同视口对比，46 组。
- `r3/MOTION.html`：4 段实录。
- `r3/Open-Preview-r3.ps1`：一键打开以上页面。

**过程说明**：修正导师位置后第一次重跑回归时，有两项检查失败。原因是本地预览服务在电脑休眠后已经停止，不是代码问题。用原方式重启服务后，全部检查通过。

**未解决与待确认**：现有导师照片只有 248×298，如有高清正式照可替换。其余同 r2 一节（奖项日期冲突、实验室电话、未确认的统计数字、Safari/iOS 未实机验收）。另外，字体分片在首次访问时按需下载，下载完成前会短暂显示系统字体（`font-display: swap`）。

---

## r2（2026-11-23）

| 项 | 值 |
|---|---|
| 分支 | `feat/yanying-claude-art-direction-r2` @ `753402bfaef2a7dc56764bc6935fb24479c3e976` |
| 回退基线 | `feat/yanying-claude-art-direction` @ `1e509fbbbd693a22f06fe1dd75c519e0170dbeb5`（未改动）；V3 `89acaf4`（未改动） |
| 本地预览 | http://127.0.0.1:4327/ |

### 做了什么

1. **内容审计**：逐项比较老师站（本地只读副本 `bbec06e`）、实验室站（`upstream/main` `e3585f9`）和统一站，写入 [SOURCE_CONTENT_MATRIX.md](SOURCE_CONTENT_MATRIX.md)。
2. **补回缺失内容**（全部逐字取自源站，集中在 `frontend/src/data/source-extras.ts` 并注明出处）：七个方向短句标题、老师站七张差异化科学示意图、研究说明、履历第 2–3 段与学位/学科/任职、四个履历数字、导师寄语、招生导语、“招生中”名额卡、“更多同学”条目、项目/专利成果卡、实验室口号与导语、实验室研究生年级与兴趣（按姓名合并，不重复列人）、刘娜标签、实验室加入说明与 4 条申请要求、专题 subtitle、每个专题的 3 条方法标题、实验室图片墙（30 张）、首页“最新”论文标记、页脚 Faculty Profile / Google Scholar、实验室域名。
3. **视觉修订**（理由见 DESIGN_RATIONALE.md 的“r2 修订”一节）：柔和三层背景，取消整屏黑与整屏白；标题三档、统一间距；取消扫描线和重复波形；恢复差异化科学图形；人物区改为版心内白纸面；橙色只留给焦点。
4. **性能修正**：图片墙改用 400 px 派生缩略图（6.9 MB → 0.56 MB）。直接用原图时解码后约 394 MB，导致 Chromium 图片解码失败（`check_original_people.py` 首次因此失败，见 `r2/regression-1`）。

### 本轮实际运行的检查

| 检查 | 结果 | 证据 |
|---|---|---|
| `npm run build` | 通过（14 页） | — |
| `npm run test:frontend` | 通过 | `r2/regression-final/frontend.log` |
| `tsc --noEmit` | 通过 | `r2/regression-final/typescript.log` |
| `npm run test:backend` | 通过 | `r2/regression-final/backend.log` |
| `check_deployment.py` | 通过 | `r2/regression-final/deployment.log` |
| `check_group_site.py` | 通过 | `r2/regression-final/group.log` |
| `check_original_people.py` | 通过 | `r2/regression-final/people.log` |
| `check_adversarial_site.py`（含 axe WCAG 2.2 AA） | 通过 | `r2/regression-final/adversarial.log` |
| 源站内容完整性 `r2/check_content.py` | 331/331 项在构建产物中找到 | `r2/content-check.log` |
| 图片墙状态 `r2/check_wall.cjs`（离屏 / 视口内 / 悬停 / 按钮 / 减少动效） | 通过 | `r2/wall-check.log` |

过程中发现并修正的问题：青色小字对比度不足（axe 报告，已换成 `--graph-text`）；选项卡图形压到文字上（已限制高度）；图片解码超预算（已改缩略图）；实验室口号断行；期刊论文计数延迟显示“—”。

### 证据（`D:/AI-Agent-Workspace/Projects/YanYing-EEGLab-Merge/qa/claude-art-direction-20261122/r2/`）

- `GALLERY.html`：当前版（1e509fb）与 r2 同视口对比 46 组（9 个路由 × 1440/390 首屏与整页，首页 1920/768/360，成果页 503 回退）。
- `MOTION.html`：4 段 Windows Chrome 真实实录（CDP 截屏流）及关键帧。
- `Open-Preview-r2.ps1`：一键打开官网、画廊、实录。
- `iter1`–`iter3`：迭代截图。

### 未解决 / 待确认

- 奖项日期冲突两处、实验室电话是否公开、老师站“19+ 竞赛获奖”（源码注明待确认）、实验室站“7 项代表性奖项”与 25 条奖项不一致：均未展示，等老师确认。
- 实验室站的全屏分段滚动、右侧圆点导航和打字机效果没有恢复（理由见内容矩阵第 11 节）。
- 本地论文目录只有 2 篇核验种子；生产 105 篇没有在本地验证。Safari / iOS 没有实机验收。

---

## 上一轮（2026-11-22）

### 版本

| 项 | 值 |
|---|---|
| 分支 | `feat/yanying-claude-art-direction` |
| 基线（V3，未改动） | `feat/yanying-visual-v3-motion-first` @ `89acaf446a5205169643be81fda5dd67e67bc073` |
| 设计与代码提交 | `71b2a3f8a7ad37cd9d27bbb3ef08a6217f5cf265` |
| 报告提交 | `1e509fbbbd693a22f06fe1dd75c519e0170dbeb5` |
| 本地预览 | http://127.0.0.1:4327/ （仅回环地址；V3 冻结对照版 http://127.0.0.1:4328/） |

### 修改的文件

只涉及 `frontend/` 和文档，后端、论文 API、数据库、同步程序、鉴权、CI 配置都没有改动。

- 新增：`frontend/src/lib/signals.ts`、`frontend/src/components/SignalTrace.astro`、`frontend/src/styles/pages.css`、`DESIGN_RATIONALE.md`、本报告。
- 重写样式：`frontend/src/styles/global.css`（token 与基础层）、`theme.css`（组件）、`group.css`（首页）、`edition.css`（动效）。
- 页面：`index`、`about`、`team`、`join`、`contact`、`404`、`achievements`、`research/index`、`research/brain-computer-interface`、`research/[slug]`。
- 组件：`Nav`、`Footer`、`SectionHeader`、`HomeResearch`、`ResearchArtwork`、`GroupResearch`、`GroupHonors`、`GroupMembers`、`Advisor`、`Admission`、`DevicePlate`；`PublicationsExplorer`、`RelatedPublications`、`GalleryFilter` 只改样式字符串。
- 布局：`Layout.astro`（样式顺序、统一的显现脚本、首帧前同步设置 `js-reveal`）、`GroupLayout.astro`。
- `frontend/public/favicon.svg` 改为新标识。
- 文档：`CLAUDE_HANDOFF.md`（重写）、`README.md`、`frontend/README.md`、`CLAUDE_CODE_VISUAL_BRIEF.md`（标为历史文档）。
- `frontend/src/data/research-visuals.json` 已不再被引用。按“不删文件”的约定保留，后续可由维护者决定是否删除。

### 测试（WSL，最终构建）

日志：`../qa/claude-art-direction-20261122/regression-final/`

| 检查 | 结果 |
|---|---|
| `npm run build`（13 个正式页面 + 404，共 14 页） | 通过 |
| `npm run test:frontend`（论文契约） | 17/17 通过 |
| `tsc --noEmit` | 退出码 0 |
| `npm run test:backend` | 50 项测试 OK |
| `scripts/check_deployment.py` | 通过 |
| `scripts/check_group_site.py`（1440/390/768 全路由、选项卡键盘、视频控制、菜单、API 503 回退、合成 API 筛选与搜索） | 43 项通过 |
| `scripts/check_original_people.py`（人物区白底无滤镜、首屏与影片构图、影片入视口真实播放） | 7 项通过 |
| `scripts/check_adversarial_site.py`（axe WCAG 2.2 AA @1440/390、320–1920 无溢出、文字放大 200%、超长混排标题、恶意或损坏 API、视频失败、API 挂起、重试恢复、禁用 JS） | 130 项通过 |

本轮没有运行 V3 专属的 QA 脚本（`../qa/visual-v3-motion-first/check_*.py`），因为它们针对的是 V3 的封面轮播等已经移除的结构。

### 浏览器验收证据（Windows Chrome）

都在 `D:/AI-Agent-Workspace/Projects/YanYing-EEGLab-Merge/qa/claude-art-direction-20261122/`：

- `GALLERY.html`：46 组 V3 与新版对比。同一截图脚本 `capture.cjs`、同一 Windows Chrome、同一路由、同一视口、同一本地种子 API。覆盖 9 个路由的 1440/390 首屏和整页、首页 1920/768/360、成果页论文服务 503 回退。原图在 `compare/`。
- `MOTION.html`：4 段真实实录（CDP screencast 抓帧，按真实时间轴编码为 webm，见 `motion/encode.json`）：
  1. `01-hero-entrance`：首屏入场、描线、扫描线、导联悬停。7.4 秒，385 帧互不相同。
  2. `02-home-scroll-research`：滚动叙事、选项卡重绘、影片入视口播放、用户暂停后保持暂停、研究页目录高亮。
  3. `03-team-achievements-interaction`：成员筛选、论文搜索、图录筛选。
  4. `04-mobile-menu-touch`：390 宽触控菜单、跳转、横向选项卡、设备图横滑。
- `concepts/`：首页概念 A 与 B 的对比截图（B 已放弃，原因见 DESIGN_RATIONALE.md）。
- `iter/`：迭代过程截图（r1 → r2）。
- `Open-Preview.ps1`：一键在 Chrome 打开官网、画廊和实录。

### 自查中发现并修正的问题

- 首屏标题遮罩把粗体汉字的上下沿裁掉 → 加大遮罩内边距。
- “金牛湖脑机实验室”在 5/12 栏中断成三行 → 改为对半分栏。
- 影像区第一张图被拉伸成不同比例 → 三张统一 4:3。
- 成员证件照饱和的蓝底在大尺寸下太抢眼 → 人像卡缩小一档。
- 联系页小标被段落规则放大 → 修正选择器。
- **只在实录里才看得到**：波形描线因 `non-scaling-stroke` 与 `pathLength` 冲突被截短；扫描线在启动前停在左边可见 → 描线改为 `clip-path` 擦出，扫描线透明度写进关键帧。

### 未解决与需要注意

- 审美没有经过用户确认。下一步：用户看过本地预览后反馈，再交给 Codex 做工程验收，之后才谈向朋友提交 PR。
- 本地论文目录只有 2 篇经核验的种子条目，生产 105 篇完整导入没有在本地验证。页面不使用任何静态论文数量。
- 跨页过渡只在 Chromium 内核浏览器中生效；Safari/iOS 没有实机验收。
- 截图和实录都由 Windows Chrome 无头模式产生。字体与用户桌面 Chrome 一致（Segoe UI Variable + 微软雅黑），但窗口外观（滚动条等）可能略有不同。
- WSL 中没有 Git 身份。本次提交用 `git -c` 临时传入 `Claude Code <claude-code@localhost>`（与先前 `Codex <codex@localhost>` 的做法一致），没有写入任何 Git 配置。
