## 用户最新且优先的视觉要求（2026-11-16）
居中标题/首屏四图/把视频移出首屏的方案已被用户明确否定，不作为当前方向。
当前恢复260bd51浅色版本的左右构图：左侧标题与介绍，右侧首屏视频。视频直接展示、静音自动循环，保留播放暂停与减少动效支持。
保留全站浅色、人物白底与自然照片、数据校验及对比度修复。后续必须基于用户认可的构图改进，不得再自行居中或隐藏首屏视频。

## 当前首页设计（2026-11-16，Apple式层级与视觉对抗）
用户要求真正审查视觉效果并学习优秀网站。已实际参考Apple、Linear、Stripe、Notion、MIT Media Lab，详细否定与改动见DESIGN_REVIEW.md。
当前首页：单一居中中文标题，英文退到辅助；删掉倾斜/轨道/假坐标/重复口号；4个原官网科研图形作方向入口；宣传视频移到BCI模块、默认暂停。正文和图像比例已修正。
代码：首页index.astro + home.css；group.css保留内页与共享研究浏览器；导航64px起步。浅色、自然人物照片及全部真实数据继续保留。
后续不要再把自动测试通过当作视觉验收，也不要恢复首屏自动宣传片与装饰仪表。

本轮浅色主题验证：13页构建/部署输入PASS；43项页面交互PASS；浅色初轮发现图库未选按钮和研究编号对比度不足，修正后128项对抗检查PASS（含全路由桌面/手机axe、极窄屏、200%文字、API/视频退化）。已查看首页、老师、团队的桌面和手机截图。原始照片/内容/后端/生产配置均未改；未push/PR/部署。

## 当前视觉方向：统一浅色（2026-11-16，用户最新反馈）
用户认可前端结构，但否定黑白区块交替，以及白底人物照片在深底上的高反差。当前方案已覆盖前面的深色方案：
- 全站暖白 #fafaf7、浅灰 #f2f3ed，人物区域纯白；深灰绿正文、克制深金细节。
- 首页/内页/导航/页脚同一浅色体系，视频画面内部保留深色，不再使用大块深色页面背景。
- 老师、学生、顾问照片恢复自然色彩；原始照片未编辑，蓝底原图也保持原貌。白底照片与人物区自然融合。
- 保留已认可的排版、七方向交互、视频、动效、论文安全逻辑。后续不要擅自退回黑白交替或深底衬白底证件照。

## 最终对抗审查结果（2026-11-16）
当前前端本地验收：43项页面交互、128项对抗场景、14项API边界测试及TypeScript检查全部PASS；13页构建和部署输入检查PASS。共修复渲染崩溃、危险链接输入、对比度、媒体错误时序、文字放大布局、焦点目标等实际问题。详细方法、命令和范围见VISUAL_REDESIGN_REPORT.md。
没有未修复的本轮已复现问题；不将此表述为所有设备和场景的绝对无缺陷。原真实数据迁移、真机/Safari和上线审批仍待独立阶段。最终SHA见工作区同名报告及git log。

## 2026-11-16 前端重做验收增量
用户否定第一版视觉后，已完成实质前端重做。首页不再使用通用卡片堆叠：深色实验视频首屏、七研究方向交互及原官网SVG、实验室大图、导师编辑版式、成果影像、学术荣誉、论文列表、错落团队照片和招生收尾。共享导航/页脚/内页/原论文React组件统一设计token。五研究详情新增现有真实研究图片，团队恢复顾问肖像。
本轮43项浏览器检查PASS（13路由×三宽度+原API合成场景+新增七方向/键盘/视频/减少动效/菜单Esc/滚动显现）；13页构建与部署输入检查PASS。后端无改动，本轮不引用旧后端PASS为新运行。
1440桌面/390手机/研究区/成果页截图已人工查看；修复手机轨道装饰溢出、研究SVG覆盖文案及成果荣誉组件未加载样式。窗口连接首轮超时，用户回来后重试成功，已在真实浏览器选中新版首页。
无push/PR/部署；后端、生产配置、种子、许可证、依赖lockfile未改。后续精修、真实备份迁移和上线审批边界继续有效。精确本地commit见工作区VISUAL_REDESIGN_REPORT.md。

# 统一官网本地整合验收报告
日期：2026-11-15（本地WSL，America/Los_Angeles）
状态：LOCAL_IMPLEMENTATION_VERIFIED；真实数据迁移、视觉精修及上线仍属后续阶段。

## 位置与版本
- Windows：D:/AI-Agent-Workspace/Projects/YanYing-EEGLab-Merge/repo
- WSL：/mnt/d/AI-Agent-Workspace/Projects/YanYing-EEGLab-Merge/repo
- 分支：feat/unify-yanying-group-site
- origin：https://github.com/shimuxia/EEGLab.git，已核对fork parent=buerka/EEGLab
- upstream：https://github.com/buerka/EEGLab.git；两者push URL均DISABLED。
- EEGLab源版本：e3585f90fabec82f22cf4452e014b7769012a1f7
- 私有官网源版本：bbec06eba92ee19a004b7909c2eb3ecdb2cc07bf
- 最终本地commit：本文件所在交付提交，以 git rev-parse HEAD 查询；提交后工作区根目录同名报告记录精确SHA，避免提交哈希自引用。
- Author/Committer：He Qihan <heqihan6@gmail.com>；仅单次命令配置，未改全局身份。
- 是否推送：NO；是否创建PR：NO；是否merge：NO；是否部署：NO。只创建了授权Fork。

## 实现
单一Astro应用，共13个路由：课题组首页、关于、七方向总览、团队、成果、招生、联系；BCI实验室总览；保留diagnosis/arm/drone/hand/glove五详情。
导师/成员/研究/荣誉/招生共享数据；深色hero、暖金信号动效、导师照片、手机折叠菜单、备案展示；实验室图库、奖项、研究内容和所有原资源保留。原首页视频在BCI模块，有播放控件。原官网只迁移67项变更清单中的必要内容及图片，不迁移其Git历史、后端或内部资料。
新增统一论文只读适配：严颖confirmed限制、两篇误收独立基线、人工exclude优先、研究者隔离、分页前排除及完整关联计数。前端超时/结构检查/错误重试及三篇静态代表论文回退。不改生产同步、种子和审核数据。

## 实际验证
|检查|本次结果|
|---|---|
|WSL环境|Linux；git2.43.0；Node24.14.0；process.platform=linux；npm11.9.0；Python3.12.3|
|npm --prefix frontend ci|PASS，严格使用原lockfile；lockfile未修改|
|项目Python依赖|独立.venv安装backend/requirements-dev及cloud-functions/requirements|
|npm run test:backend|38项PASS（含原30项及新增8项）|
|原官网test_restore_exclusions.py|10项PASS，仅临时/合成数据库；原仓库无修改|
|npm run build|13页PASS；最后格式整理后重新构建PASS|
|python scripts/check_deployment.py|PASS，必需路由、25MB资源门禁、Python3.10语法及公开目录隔离|
|本地Chromium Playwright|40项PASS：13路由×1440/768/390及API成功/失败筛选|
|图片和内部链接|构建HTML引用与浏览器图片解码、404检查PASS|
|移动交互|菜单展开、导航跳转、aria-expanded、无横向溢出PASS|
|论文API|临时数据库TestClient与内存COS端点PASS；研究者/搜索/空结果、503回退及重试入口PASS|
|排除安全|confirmed误收仍排除；共著其他研究者保留；review/excluded/OpenAlex-only隐藏；644项总数超过500分页仍正确|
|人工字段|原有同步保留字段测试及新增只读前后对比PASS|
|恢复门禁预检|缺失规则/accept别名冲突拒绝、无隐式写入PASS；不是生产恢复验收|
|视频|本地Chromium通用MP4：1280×720，readyState=4；未穷尽所有编码/真机|
|视觉观察|已查看桌面长截图及390px首页截图；无明显标题遮挡；待Claude精修|
|公开构建扫描|常见token模式、密钥名称、内部路径与禁止服务器地址无命中|
|Git检查|diff --check PASS；LICENSE未改，生产配置未改，参考仓库clean；缓存/DB/output不纳入commit|

命令在WSL执行。测试日志、截图和合成运行产物保存在repo/output/，Git忽略且不提交。浏览器依赖Playwright1.65.2为本地QA安装，使用既有Linux Chromium；无生产请求，外网资源被测试拦截。
没有执行云端Python3.10解释器、真实COS、真实Scholar/API Key、真实备份或生产域名验收，不把语法检查/本地成功等同生产成功。

## 发现、修复及限制
- WSL直连GitHub/npm超时；临时命令代理使用已有127.0.0.1:7890后成功。未修改系统代理、FlClash/TUN或其他环境。
- 首轮390px检测失败：旧页脚学校Logo横排溢出；已改手机尺寸及换行，三宽度重跑通过。
- 测试脚本曾因滚动隐藏导航Logo超时；改为图片解码检查后完整重跑通过。
- 旧奖项数据存在2025年3月冲突；修为2024成果/2025年2月，江苏省奖分别标注2023年度与2024年2月。2015入围与2026单年度已保护。
- 本轮默认关闭原统计；独立批准后才能启用，未增加遥测。
- 原全屏滚动/打字动画未机械迁移；统一站为常规文档滚动与轻量SVG动效，支持减少动效偏好。
- 学生当前身份、照片继续由老师审核；未按相似姓名/照片合并。顾问及临床伙伴保留协作角色。
- 真实Scholar-only同步及人工审核迁移尚未执行。只读策略能安全隐藏未确认记录，因此旧种子不能被当作完整统一论文库；无后端时显示静态回退。
- 独立恢复预检不替代原官网完整启动门禁，正式迁移前必须核查完整备份、全部审核记录、冻结写入者并演练；本轮没有操作生产数据库。
- Safari、真实iOS/Android、全部视频编码及跨网络情况尚未验收。
- 域名、301/旧子域名、备案归属和云端切换需要用户及朋友独立确认；不触碰/quiz/。

## 本地预览与交接
本轮已启动仅绑定127.0.0.1:4327的Astro preview；访问 http://127.0.0.1:4327 。
停止后从repo启动：
ASTRO_TELEMETRY_DISABLED=1 npm --prefix frontend run dev -- --host 127.0.0.1 --port 4327
静态预览无后端时论文回退为预期；不要运行生产同步来填充数据。

Claude入口：repo/CLAUDE_HANDOFF.md；PR草稿：repo/PR_DRAFT.md。
来源比较：SOURCE_INTEGRATION_AUDIT.md；素材清单与哈希：ASSET_SOURCE_MAP.md。
Claude下一步统一视觉、优化信息层次/动效/手机，保留共享数据、学术事实及论文安全策略；接手前按熔炉任务/锁流程取得新锁。

## 实际修改文件
- "frontend/public/group/assets/members/\345\256\227\347\246\271\350\203\204.jpg"
- "frontend/public/group/assets/members/\345\274\240\344\271\220\344\271\220.jpg"
- "frontend/public/group/assets/members/\346\234\261\345\256\266\347\220\246.jpg"
- "frontend/public/group/assets/members/\346\262\210\345\237\271\346\266\265.jpg"
- "frontend/public/group/assets/members/\347\216\213\345\256\207\346\243\256.jpg"
- "frontend/public/group/assets/members/\350\213\227\344\272\211\345\205\211.jpg"
- "frontend/public/group/assets/members/\351\231\206\346\200\235\350\257\255.jpg"
- "frontend/public/group/assets/members/\351\231\210\345\210\230\346\230\245.jpg"
- ASSET_SOURCE_MAP.md
- CLAUDE_HANDOFF.md
- PR_DRAFT.md
- README.md
- SOURCE_INTEGRATION_AUDIT.md
- backend/README.md
- backend/app/cloud_api.py
- backend/app/group_policy.py
- backend/app/main.py
- backend/app/repository.py
- backend/tests/test_group_policy.py
- docs/handoff.md
- frontend/.env.example
- frontend/README.md
- frontend/public/group/assets/team/cai-haoyang.webp
- frontend/public/group/assets/team/du-wenjie.webp
- frontend/public/group/assets/team/fan-huixi.webp
- frontend/public/group/assets/team/gu-qihang.webp
- frontend/public/group/assets/team/he-qihan.webp
- frontend/public/group/assets/team/he-yuhan.webp
- frontend/public/group/assets/team/huangfu-chenmeng.webp
- frontend/public/group/assets/team/liu-guanting.webp
- frontend/public/group/assets/team/lv-jiongrui.webp
- frontend/public/group/assets/team/sun-dingyi.webp
- frontend/public/group/assets/team/sun-jianqiang.webp
- frontend/public/group/assets/team/sun-xihan.webp
- frontend/public/group/assets/team/tang-yun.webp
- frontend/public/group/assets/team/zhang-jinhao.webp
- frontend/public/group/assets/team/zhang-yukun.webp
- frontend/public/group/assets/yan-ying-portrait.png
- frontend/src/components/Admission.astro
- frontend/src/components/Advisor.astro
- frontend/src/components/Footer.astro
- frontend/src/components/GroupHonors.astro
- frontend/src/components/GroupMembers.astro
- frontend/src/components/GroupResearch.astro
- frontend/src/components/Nav.astro
- frontend/src/components/PublicationsExplorer.tsx
- frontend/src/data/awards.toml
- frontend/src/data/group-content.json
- frontend/src/data/group.ts
- frontend/src/data/lab-team.json
- frontend/src/layouts/GroupLayout.astro
- frontend/src/layouts/Layout.astro
- frontend/src/lib/publications.ts
- frontend/src/pages/about.astro
- frontend/src/pages/achievements.astro
- frontend/src/pages/contact.astro
- frontend/src/pages/index.astro
- frontend/src/pages/join.astro
- frontend/src/pages/research/[slug].astro
- frontend/src/pages/research/brain-computer-interface.astro
- frontend/src/pages/research/index.astro
- frontend/src/pages/team.astro
- frontend/src/styles/group.css
- scripts/check_deployment.py
- scripts/check_group_site.py
- scripts/requirements-qa.txt
- todo.md
- FINAL_INTEGRATION_REPORT.md
