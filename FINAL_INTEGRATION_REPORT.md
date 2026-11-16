# 统一官网本地验收报告
2026-11-16；本次为用户指定的“只学新城前端效果”独立分支实验。状态：LOCAL_FUSION_VERIFIED，视觉待用户审阅。本地验证不等于生产验收。

## 位置、版本与权限
- Windows：D:/AI-Agent-Workspace/Projects/YanYing-EEGLab-Merge/repo
- WSL：/mnt/d/AI-Agent-Workspace/Projects/YanYing-EEGLab-Merge/repo
- 当前分支：feat/yanying-xincheng-visual-fusion
- 原功能分支：feat/unify-yanying-group-site；恢复基线01ee1066a898c1fd1f96549c77fa9fc1f913974e已提交保留。
- origin：shimuxia/EEGLab，fork parent=buerka/EEGLab；upstream：buerka/EEGLab；两个push URL保持DISABLED。
- EEGLab工程来源：e3585f90fabec82f22cf4452e014b7769012a1f7。
- 原私有官网内容来源：bbec06eba92ee19a004b7909c2eb3ecdb2cc07bf。
- 新城仅为本地视觉参考，不成为工程/内容来源；准确历史快照哈希与取舍见 FUSION_REVIEW.md。
- 最终本地commit：本报告所在提交，以 git rev-parse HEAD 查询；提交后 ../FINAL_INTEGRATION_REPORT.md 记录精确SHA，避免自引用。
- 本地Git身份：He Qihan <heqihan6@gmail.com>，仅单次commit配置。
- 是否推送：NO；是否创建PR：NO；是否merge：NO；是否部署：NO。
- 本轮没有访问生产服务器、COS、SCF或修改DNS、证书、备案、部署任务；没有安装Claude Code。

## 已实现的统一工程
单一Astro前端、React论文/图库交互、原EEGLab Python架构；共享导师/团队/研究/荣誉内容数据，不运行第二生产论文后端。
13路由正常构建：/、/about、/research、/team、/achievements、/join、/contact、/research/brain-computer-interface、/research/diagnosis、/research/arm、/research/drone、/research/hand、/research/glove。
首页原锚点与原实验室研究详情、媒体和论文入口继续有效。备案保留展示，不代表域名切换获批。
原私有官网只迁移已审阅公开内容和素材白名单，未复制完整源码、Git历史或数据库；许可证不变。
既有只读/api/group/papers、研究者筛选、人工审核优先、误收排除和静态回退保留；本轮未改其实现、种子或同步任务。

## 本轮实际展示层改动
- 暖白背景、石墨文字与香槟金细节，人物区纯白；沿用单一共享token。
- 保留左文右视频；视频平直16:9完整画幅，说明放到框外，避免与内置字幕重叠。保留静音自动循环、暂停和失败回退。
- 按钮扫光、箭头微移、细线展开、标题/影像进入及名单错峰；原生IntersectionObserver，零新依赖。
- 无JS/无Observer默认可读；实时减少动效会清除待进入状态；键盘焦点不会落入透明段落。
- 导师/学生/顾问原照不改文件，不加深色滤镜；手机提前堆叠首屏，保持视频可见。

## 当前真实测试结果
所有命令在WSL运行。Node24.14.0、Python3.12.3；3.10仅做部署语法检查，未用3.10解释器执行。
- npm run test:backend：38项PASS，使用本项目.venv。
- npm run test:frontend：14项PASS。
- 前端现有TypeScript库与React组件tsc --noEmit：PASS。
- npm run build：13页PASS。
- python scripts/check_deployment.py：PASS，路由/打包输入/生产私密运行文件隔离检查。
- scripts/check_group_site.py：43项PASS，13路由三宽度、资源、导航、研究tabs、键盘、视频和模拟API。
- scripts/check_adversarial_site.py：128项PASS，axe 27状态、65宽度场景、26文字放大场景以及异常API/XSS、超时重试、视频失败、无JS等。
- scripts/check_visual_fusion.py：11项PASS，8种宽度（320/390/605/774/800/805/1024/1440）、视频时间推进/比例/说明分离、错峰/焦点/实时减少动效/无Observer。
- git diff --check：PASS；相对恢复基线的backend、data、lib、public资源、LICENSE、edgeone.json、.github无改动。
失败及修复过程见 FUSION_REVIEW.md；没有把旧报告PASS当作本轮运行。测试项存在场景重叠，不相加为独立功能数量。
本地证据：忽略目录 output/fusion/ 与 output/fusion-*.log；不提交截图、缓存或QA产物。

## 实际浏览器检查
实看新城黑金/动效两个历史版本首页与滚动段，动效版手机390px。
实看本地融合版桌面、手机390px菜单、首屏播放和导师白底原照；另查看已等待图片解码的团队与导师截图。
确认没有明显首屏重叠、横向溢出、字幕被说明遮挡；自动检查不能保证所有审美偏好，当前视觉待用户审阅。真实Safari/iOS及物理手机未测。

## 本轮修改文件
- frontend/src/components/Nav.astro
- frontend/src/components/SiteMotion.astro（新增）
- frontend/src/layouts/Layout.astro
- frontend/src/pages/index.astro
- frontend/src/styles/global.css
- frontend/src/styles/group.css
- frontend/src/styles/theme.css
- scripts/check_group_site.py
- scripts/check_visual_fusion.py（新增）
- FUSION_REVIEW.md（新增）
- CLAUDE_HANDOFF.md
- PR_DRAFT.md
- VISUAL_REDESIGN_REPORT.md
- FINAL_INTEGRATION_REPORT.md

## 本地预览与交接
已运行的构建预览：http://127.0.0.1:4327/ 。
开发命令：ASTRO_TELEMETRY_DISABLED=1 npm --prefix frontend run dev -- --host 127.0.0.1 --port 4327；已有预览占用时复用或停止本任务自己的服务，不终止其他程序。
Claude从 CLAUDE_HANDOFF.md 接手，先读本项目/Furnace当前任务与范围锁，再在本分支按用户反馈精修展示层。PR_DRAFT.md仅本地草稿。
未完成：用户审阅本实验视觉、Claude后续精修、老师确认人员当前状态/素材与事实、真实生产审核记录迁移、Safari/iOS验证、域名/部署独立审批。生产迁移没有授权，不执行。
