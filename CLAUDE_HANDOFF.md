# 当前基准：恢复原版，只修人物区域
用户已明确：“就是我说那个背景和照片不搭配的那版”，对应405f7a9。当前分支 feat/yanying-original-people-fix。
首页index.astro、Nav.astro与405f7a9字节一致；原深色首屏、左文右倾斜视频、轨道/波形及原动效恢复。仅人物区增加白底/深色文字，照片恢复自然色，不编辑原图。不要再把全站刷成浅色、居中标题或隐藏视频。
新城融合分支 feat/yanying-xincheng-visual-fusion 已被用户否定，完整保留供历史追溯，不作为当前设计方向。本分支不加载SiteMotion实验控制器；恢复原动效实现。
后端/数据/API客户端/素材/生产配置不变；正式上线与真实数据迁移仍需独立授权。

# Claude Code 接手：严颖课题组统一官网
本轮目标是可运行的单一课题组官网；脑机实验室为研究方向与平台，不再保留独立首页。后续以用户确认的左右视频首屏为基础局部精修，不改变学术事实或论文安全逻辑。

## 接手及权限
- WSL 家目录：/mnt/d/AI-Agent-Workspace/Projects/YanYing-EEGLab-Merge
- Git 工程：该目录下 repo/；只读原官网：../reference/original/
- 当前分支：feat/yanying-original-people-fix；feat/unify-yanying-group-site与feat/yanying-xincheng-visual-fusion均保留。
- 最终提交：执行 git log -1 --format=%H；精确 SHA 另见 ../FINAL_INTEGRATION_REPORT.md（报告在提交后生成，避免自引用）。
- Fork：shimuxia/EEGLab，parent=buerka/EEGLab；upstream 和 origin push URL 均为 DISABLED。
- 先按熔炉上下文门禁读取当前任务与锁；本次 Codex 释放锁后 Claude 才能接手。
- 禁止 push、PR、merge、部署；禁止修改任何生产服务器、DNS、证书、备案、COS/SCF/EdgeOne、生产定时器和部署凭据。不得把私有参考仓库整体复制或发布。
- LICENSE 和原作者版权保留。不要安装/登录另一套 Codex；本轮没有安装 Claude Code。

## 路由与组件
13页：/、/about、/research、/team、/achievements、/join、/contact、/research/brain-computer-interface，以及 /research/diagnosis、arm、drone、hand、glove。
首页兼容 #about/#research/#team/#achievements/#papers/#admission/#contact；具体七方向锚点保留在研究卡片。旧 /index.html 由静态入口自然支持。
GroupLayout → Layout（global.css/theme.css及原滚动显现）+ Nav + main + Footer；共享模块 Advisor、GroupResearch、GroupMembers、GroupHonors、Admission。
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
global.css恢复405f7a9的深色/香槟金token；group.css保留原布局，仅在.people-surface、.home-advisor、.home-team覆盖白底、深色文字及深金链接，原照片无滤镜。about导师区及team人物区明确标记people-surface。不新增全站浅色主题。
首页/导航保持原版；prefers-reduced-motion与无JS可读行为沿用原实现。不要移植被否定的新城效果试验。
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
npm run test:frontend
npm run build
python scripts/check_deployment.py
python -m pip install -r scripts/requirements-qa.txt
# 另开终端：npm --prefix frontend run preview -- --host 127.0.0.1 --port 4327
CHROMIUM_PATH=/home/shimuxia/.cache/ms-playwright/chromium-1228/chrome-linux64/chrome python scripts/check_group_site.py
CHROMIUM_PATH=/home/shimuxia/.cache/ms-playwright/chromium-1228/chrome-linux64/chrome python scripts/check_original_people.py
CHROMIUM_PATH=/home/shimuxia/.cache/ms-playwright/chromium-1228/chrome-linux64/chrome python scripts/check_adversarial_site.py
git diff --check
```
QA脚本只访问本地，拦截合成API，阻断外站请求；截图和日志在忽略的output，不提交临时QA资料。浏览器位置是当前机器已有缓存，其他环境可用CHROMIUM_PATH或安装项目级Playwright浏览器。
实际测试和失败修复记录见 ../FINAL_INTEGRATION_REPORT.md，不引用旧报告当新PASS。

## 视觉精修与已知边界
后续以用户指定原版为基准，仅作明确的局部修正；人物白底与自然色已处理。不得借精修再次改换整体视觉、首屏构图或动效系统。
人员当前状态与照片继续由老师确认；不凭肖像或同名推断。未迁移私有在线数据库和历史人工审核。
真实设备Safari/iOS、媒体全部编码播放与线上跨网络均未验收；本轮仅本地Chromium。外部域名/备案归属及301重定向需要单独确认；/quiz/属于其他项目，绝不覆盖。

## 学术事实不可回退
- 2024年中国技协成果二等奖，2025年2月获奖，严颖第一完成人。
- 2023年度江苏省自动化学会科技奖三等奖，2024年2月获奖，严颖第一完成人。
- 2023 IEEE PHM Best Paper Award 为获奖。
- 2015 IEEE CASE Best Student Paper Award Finalist 为入围。
- 2026前2%榜单仅“2026年单年度影响力”。
