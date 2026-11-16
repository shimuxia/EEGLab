## 当前首页设计（2026-11-16，Apple式层级与视觉对抗）
用户要求真正审查视觉效果并学习优秀网站。已实际参考Apple、Linear、Stripe、Notion、MIT Media Lab，详细否定与改动见DESIGN_REVIEW.md。
当前首页：单一居中中文标题，英文退到辅助；删掉倾斜/轨道/假坐标/重复口号；4个原官网科研图形作方向入口；宣传视频移到BCI模块、默认暂停。正文和图像比例已修正。
代码：首页index.astro + home.css；group.css保留内页与共享研究浏览器；导航64px起步。浅色、自然人物照片及全部真实数据继续保留。
后续不要再把自动测试通过当作视觉验收，也不要恢复首屏自动宣传片与装饰仪表。

## 当前视觉方向：统一浅色（2026-11-16，用户最新反馈）
用户认可前端结构，但否定黑白区块交替，以及白底人物照片在深底上的高反差。当前方案已覆盖前面的深色方案：
- 全站暖白 #fafaf7、浅灰 #f2f3ed，人物区域纯白；深灰绿正文、克制深金细节。
- 首页/内页/导航/页脚同一浅色体系，视频画面内部保留深色，不再使用大块深色页面背景。
- 老师、学生、顾问照片恢复自然色彩；原始照片未编辑，蓝底原图也保持原貌。白底照片与人物区自然融合。
- 保留已认可的排版、七方向交互、视频、动效、论文安全逻辑。后续不要擅自退回黑白交替或深底衬白底证件照。

本轮最终结果：43页面交互+128对抗+14数据契约测试PASS；TypeScript/13页构建/部署检查PASS。已在真实浏览器打开，后续请从当前视觉成品继续，具体方法见VISUAL_REDESIGN_REPORT.md。

## 对抗审查补充（2026-11-16）
新增 lib/publication-contract.ts 和14项Node边界测试；npm run test:frontend。
新增 scripts/check_adversarial_site.py：axe-core4.14.0（只安装到忽略output）、五档屏宽、200%文字、畸形/注入API、超时/恢复、视频断流、无JavaScript阅读。
已复现并修复嵌套null渲染崩溃、两种背景的文字对比度、失效视频初始化时序、放大文字布局与焦点目标。详细方法和命令见VISUAL_REDESIGN_REPORT.md。所有源数据和后端审核策略不变。

# 2026-11-16 前端重做增量
用户否定上一版前端，本轮已直接实现视觉重做，不再把基础视觉设计留作待办。
首页采用深墨绿黑/暖金的课题组身份与实验室视频组合；浅灰绿七方向交互区复用原官网7套SVG；实验室大图、导师编辑版式、成果影像、荣誉、代表论文、错落成员照片及招生收尾。
新增 HomeResearch.astro（ARIA tabs及键盘切换）、ResearchArtwork.astro、research-visuals.json、theme.css；设计token统一在global.css，theme.css负责共享交互基础；Layout加载单一共享主题，group.css管理首页/内页布局。Nav含手机菜单/Escape/当前页状态。视频支持播放暂停、减少动效和离屏暂停；滚动显现渐进增强。
团队顾问照片与五个研究详情实图恢复；React论文组件仅换样式token，未改后端、过滤和审核逻辑。
设计色：#101310底、#d3bc8d强调、#e8e9df研究区、#cbd0be招生区；字体补充本机已有文泉驿黑体，避免Linux中文回退成不协调字体。无外部字体/新框架/生图/新增跟踪请求。
保留原图像与视频的真实性，不新增论文数量或奖项级别。新版实际测试见工作区VISUAL_REDESIGN_REPORT.md及忽略output/visual-*日志。
下一步应基于实际页面微调视觉；不要退回上一版通用卡片首页。禁止push/PR/部署边界继续有效。

# Claude Code 接手：严颖课题组统一官网
本轮目标是可运行的单一课题组官网；脑机实验室为研究方向与平台，不再保留独立首页。下一轮重点为统一视觉、排版层次、动效与手机体验，不改变学术事实或论文安全逻辑。

## 接手及权限
- WSL 家目录：/mnt/d/AI-Agent-Workspace/Projects/YanYing-EEGLab-Merge
- Git 工程：该目录下 repo/；只读原官网：../reference/original/
- 分支：feat/unify-yanying-group-site
- 最终提交：执行 git log -1 --format=%H；精确 SHA 另见 ../FINAL_INTEGRATION_REPORT.md（报告在提交后生成，避免自引用）。
- Fork：shimuxia/EEGLab，parent=buerka/EEGLab；upstream 和 origin push URL 均为 DISABLED。
- 先按熔炉上下文门禁读取当前任务与锁；本次 Codex 释放锁后 Claude 才能接手。
- 禁止 push、PR、merge、部署；禁止修改任何生产服务器、DNS、证书、备案、COS/SCF/EdgeOne、生产定时器和部署凭据。不得把私有参考仓库整体复制或发布。
- LICENSE 和原作者版权保留。不要安装/登录另一套 Codex；本轮没有安装 Claude Code。

## 路由与组件
13页：/、/about、/research、/team、/achievements、/join、/contact、/research/brain-computer-interface，以及 /research/diagnosis、arm、drone、hand、glove。
首页兼容 #about/#research/#team/#achievements/#papers/#admission/#contact；具体七方向锚点保留在研究卡片。旧 /index.html 由静态入口自然支持。
GroupLayout → 原 Layout + Nav + main + Footer；共享模块 Advisor、GroupResearch、GroupMembers、GroupHonors、Admission。
成果页保留 PublicationsExplorer + PublicationCount + GalleryFilter；研究详情继续使用 RelatedPublications。
首页七方向和团队页均使用 data/group.ts；不要另建第二份人员名单。

## 数据与来源
- data/group.ts：类型、导师、荣誉、共享导出。
- group-content.json：旧官网已审阅公开内容（方向、研究生、分组本科生、招生、三篇静态代表论文）。
- lab-team.json：实验室原成员和顾问；只按实验室协作角色展示，禁止将临床伙伴或顾问自动归类为课题组学生。
- 原研究 research.ts、awards.toml、gallery.toml 和原 public/images、public/videos 保留。
- 原官网照片仅迁移引用白名单到 public/group；完整哈希见 ASSET_SOURCE_MAP.md。
- 人员可能有多个角色；同名不是合并证据。硕士当前身份采用原官网标注，不新增学历或方向。lab-team 中历史研究生字段为来源保留，不重复推断身份。
- SOURCE_INTEGRATION_AUDIT.md 记录来源版本、功能/路由、数据规则比较和冲突处理。
- 不能把占位统计或运行时论文数写成固定宣传数据。

## 论文后端
单一 EEGLab Python 工程，新增 GET /api/group/papers；查询参数同 /api/papers：researcher（支持多个）、tag、field、year、representative、q、limit、offset。
main.py 和 cloud_api.py 共用 repository 的 group_policy 分支；原接口和生产同步不改。前端默认 /api/group。旧本地环境若指定 /api 必须改正。
group_policy.py：严颖仅 confirmed 可见；两篇误收独立代码基线；按研究者执行 exclude 优先；先过滤关联再统计和分页；共著论文仍可对其他研究者显示。read-only 读取不改人工覆盖字段。
validate_recovery_rules 是离线备份预检函数，不是生产启动门禁替代品。真实Scholar-only同步、审核规则迁移和完整数据库恢复尚未执行；正式迁移必须另审。
默认无后端时显示三篇静态代表论文和重试，不编造实时数量；请求8秒超时，拒绝明显无效API结构，不输出服务端错误详情。

## 设计与媒体
沿用 global.css 的蓝色/白色设计系统及原布局；group.css 是限定 group-* 的增量样式，不加载旧CSS reset。
保留旧官网深色hero、黑银色阶、暖金信号线、导师肖像、留白及适度SVG动效；prefers-reduced-motion 下停止动效。
导航1100px以下折叠，aria-expanded/controls；页脚手机Logo可换行。
BCI总览使用 /videos/promo-hero-v1.mp4（通用版本，带controls、muted、playsinline）；其余编码和poster、成果视频仍保留。实验室成果媒体完整清单见 frontend/public/images/achievements/README.md。
统计原代码保留但默认关闭；没有本次批准不打开 PUBLIC_ENABLE_ANALYTICS。
备案文字来自旧站苏ICP备2026027101号-2，仅保留显示，不代表批准域名/备案切换。

## WSL 本地运行
从 repo/ 执行，Node Linux 24.14.0、Python3.12.3 为本轮实际环境；CI原22.21.1/Python3.10配置保留，云端3.10语法由部署检查覆盖，本轮未执行3.10解释器。
依赖已安装；如需重装：
```bash
npm --prefix frontend ci
python3 -m venv .venv
.venv/bin/python -m pip install -r backend/requirements-dev.txt -r cloud-functions/requirements.txt
ASTRO_TELEMETRY_DISABLED=1 npm --prefix frontend run dev -- --host 127.0.0.1 --port 4327
```
访问 http://127.0.0.1:4327 。已有本地预览若占4327，复用或先停止自己的服务；不要终止其他程序。无API时回退是预期行为。
如网络直连失败，本轮验证现有 http://127.0.0.1:7890 可用；只临时给命令设置 http_proxy/https_proxy，不改系统代理。
不要运行 sync、scheduler、Docker Compose 或连接真实COS来预览。

## 测试
```bash
export PATH="$PWD/.venv/bin:$PATH" ASTRO_TELEMETRY_DISABLED=1
npm run test:backend
npm run build
python scripts/check_deployment.py
python -m pip install -r scripts/requirements-qa.txt
# 另开终端：npm --prefix frontend run preview -- --host 127.0.0.1 --port 4327
CHROMIUM_PATH=/home/shimuxia/.cache/ms-playwright/chromium-1228/chrome-linux64/chrome python scripts/check_group_site.py
git diff --check
```
QA脚本只访问本地，拦截合成API，阻断外站请求；截图和日志在忽略的output，不提交临时QA资料。浏览器位置是当前机器已有缓存，其他环境可用CHROMIUM_PATH或安装项目级Playwright浏览器。
实际测试和失败修复记录见 ../FINAL_INTEGRATION_REPORT.md，不引用旧报告当新PASS。

## 视觉精修与已知边界
优化首页卡片节奏、研究图形、团队照片裁切、亮暗段衔接和手机阅读层次；保留所有业务组件及筛选行为。旧全屏滚动/打字器不机械移植，现用普通文档滚动及轻量信号动画；可在可访问性前提下优化。
人员当前状态与照片继续由老师确认；不凭肖像或同名推断。未迁移私有在线数据库和历史人工审核。
真实设备Safari/iOS、媒体全部编码播放与线上跨网络均未验收；本轮仅本地Chromium。外部域名/备案归属及301重定向需要单独确认；/quiz/属于其他项目，绝不覆盖。

## 学术事实不可回退
- 2024年中国技协成果二等奖，2025年2月获奖，严颖第一完成人。
- 2023年度江苏省自动化学会科技奖三等奖，2024年2月获奖，严颖第一完成人。
- 2023 IEEE PHM Best Paper Award 为获奖。
- 2015 IEEE CASE Best Student Paper Award Finalist 为入围。
- 2026前2%榜单仅“2026年单年度影响力”。
