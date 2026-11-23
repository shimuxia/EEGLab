# Claude 视觉候选版 · 最终报告（2026-11-22）

> 状态：**Claude 视觉候选版**，等待用户亲眼确认审美。只做了本地提交，没有 push、PR、merge、部署，也没有访问任何生产系统。

## 版本

| 项 | 值 |
|---|---|
| 分支 | `feat/yanying-claude-art-direction` |
| 基线（V3，未改动） | `feat/yanying-visual-v3-motion-first` @ `89acaf446a5205169643be81fda5dd67e67bc073` |
| 设计与代码提交 | `71b2a3f8a7ad37cd9d27bbb3ef08a6217f5cf265` |
| 报告提交 | 本文件所在提交，即本分支 HEAD，用 `git rev-parse HEAD` 查看 |
| 本地预览 | http://127.0.0.1:4327/ （仅回环地址；V3 冻结对照版 http://127.0.0.1:4328/） |

## 修改的文件

只涉及 `frontend/` 和文档，后端、论文 API、数据库、同步程序、鉴权、CI 配置都没有改动。

- 新增：`frontend/src/lib/signals.ts`、`frontend/src/components/SignalTrace.astro`、`frontend/src/styles/pages.css`、`DESIGN_RATIONALE.md`、本报告。
- 重写样式：`frontend/src/styles/global.css`（token 与基础层）、`theme.css`（组件）、`group.css`（首页）、`edition.css`（动效）。
- 页面：`index`、`about`、`team`、`join`、`contact`、`404`、`achievements`、`research/index`、`research/brain-computer-interface`、`research/[slug]`。
- 组件：`Nav`、`Footer`、`SectionHeader`、`HomeResearch`、`ResearchArtwork`、`GroupResearch`、`GroupHonors`、`GroupMembers`、`Advisor`、`Admission`、`DevicePlate`；`PublicationsExplorer`、`RelatedPublications`、`GalleryFilter` 只改样式字符串。
- 布局：`Layout.astro`（样式顺序、统一的显现脚本、首帧前同步设置 `js-reveal`）、`GroupLayout.astro`。
- `frontend/public/favicon.svg` 改为新标识。
- 文档：`CLAUDE_HANDOFF.md`（重写）、`README.md`、`frontend/README.md`、`CLAUDE_CODE_VISUAL_BRIEF.md`（标为历史文档）。
- `frontend/src/data/research-visuals.json` 已不再被引用。按“不删文件”的约定保留，后续可由维护者决定是否删除。

## 本轮实际运行的测试（WSL，最终构建）

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

## 浏览器验收证据（Windows Chrome）

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

## 自查中发现并修正的问题

- 首屏标题遮罩把粗体汉字的上下沿裁掉 → 加大遮罩内边距。
- “金牛湖脑机实验室”在 5/12 栏中断成三行 → 改为对半分栏。
- 影像区第一张图被拉伸成不同比例 → 三张统一 4:3。
- 成员证件照饱和的蓝底在大尺寸下太抢眼 → 人像卡缩小一档。
- 联系页小标被段落规则放大 → 修正选择器。
- **只在实录里才看得到**：波形描线因 `non-scaling-stroke` 与 `pathLength` 冲突被截短；扫描线在启动前停在左边可见 → 描线改为 `clip-path` 擦出，扫描线透明度写进关键帧。

## 未解决与需要注意

- 审美没有经过用户确认。下一步：用户看过本地预览后反馈，再交给 Codex 做工程验收，之后才谈向朋友提交 PR。
- 本地论文目录只有 2 篇经核验的种子条目，生产 105 篇完整导入没有在本地验证。页面不使用任何静态论文数量。
- 跨页过渡只在 Chromium 内核浏览器中生效；Safari/iOS 没有实机验收。
- 截图和实录都由 Windows Chrome 无头模式产生。字体与用户桌面 Chrome 一致（Segoe UI Variable + 微软雅黑），但窗口外观（滚动条等）可能略有不同。
- WSL 中没有 Git 身份。本次提交用 `git -c` 临时传入 `Claude Code <claude-code@localhost>`（与先前 `Codex <codex@localhost>` 的做法一致），没有写入任何 Git 配置。
