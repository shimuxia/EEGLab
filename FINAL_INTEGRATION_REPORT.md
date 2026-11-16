# 统一官网当前本地验收报告
2026-11-16；当前状态LOCAL_ORIGINAL_PEOPLE_VERIFIED，视觉待用户审阅。

## 当前版本与位置
- Windows：D:/AI-Agent-Workspace/Projects/YanYing-EEGLab-Merge/repo
- WSL：/mnt/d/AI-Agent-Workspace/Projects/YanYing-EEGLab-Merge/repo
- 当前分支：feat/yanying-original-people-fix。
- 用户明确指定基准：“我说那个背景和照片不搭配的那版”，对应405f7a9c7278ad43bc232bd5730c213de9011bcf。
- feat/unify-yanying-group-site及feat/yanying-xincheng-visual-fusion均保留，未重写或合并。
- EEGLab源版本e3585f90fabec82f22cf4452e014b7769012a1f7；原官网源版本bbec06eba92ee19a004b7909c2eb3ecdb2cc07bf。
- origin=shimuxia/EEGLab（fork parent=buerka/EEGLab）；upstream=buerka/EEGLab；两者push URL仍为DISABLED。
- 最终本地commit：本报告所在提交，git rev-parse HEAD查询；工作区根目录同名报告在提交后记录精确SHA，避免自引用。
- Git身份He Qihan <heqihan6@gmail.com>，仅单次命令配置。
- 是否push：NO；是否创建PR：NO；是否merge：NO；是否部署：NO。

## 本轮完成
首页index.astro、导航Nav.astro恢复到405f7a9字节一致版本。原深色首屏、左文右倾斜视频、轨道/波形及原动效全部恢复。
只修复人物与背景搭配：首页导师/团队区域为白底；about导师区、team人物区增加people-surface局部浅色变量；文字/链接对比度适配；导师、学生、顾问照片取消滤镜且原文件不变。
移除本分支未使用的SiteMotion实验控制器和仅针对被否定试验的专项脚本；对应实验仍完整保存在原分支。
保留API客户端校验及后续无障碍修复；深色界面补回适合深底的成功标签色。论文后端、共享内容数据、素材、LICENSE、依赖、CI/部署配置均未改。

## 统一功能保留
单一Astro+React前端，原EEGLab Python架构；13路由：/、/about、/research、/team、/achievements、/join、/contact、/research/brain-computer-interface、/research/diagnosis、/research/arm、/research/drone、/research/hand、/research/glove。
共享导师/研究/人员/荣誉数据；原五研究详情及媒体、七方向交互、成果/图库/论文筛选、招生和备案展示保留。
/api/group/papers只读兼容层、研究者限定排除、人工审核优先、API失败静态回退仍有效。本轮未操作同步任务或生产数据。

## 本轮真实验证
全部在WSL运行，Linux Node24.14.0/Python3.12.3；Python3.10仅做部署语法兼容检查。
- npm run build：13页PASS。
- npm run test:backend（本项目.venv）：38项PASS。
- npm run test:frontend：14项PASS。
- python scripts/check_deployment.py：PASS。
- scripts/check_group_site.py：43项PASS，资源/链接、13路由三宽度、导航、研究tabs、视频和模拟API。
- scripts/check_adversarial_site.py：128项PASS，axe、窄屏、200%文字、API恶意/异常响应、视频失败、超时/重试和无JS。退出时出现一次Playwright pending路由任务清理警告，exit0，断言全部通过；不是浏览器页面脚本错误。
- scripts/check_original_people.py：7项PASS及首页/导航原版字节对照；1440/390下首页、about、team白底/照片解码/自然色/无溢出，普通动效下视频时间实际推进。
- git diff --check：PASS；受保护数据/后端/素材/配置对照无改动。
截图/日志在忽略目录output/original-people/及output/original-people-*.log，QA产物不提交。各项存在覆盖重叠，不相加为独立功能数。
Chrome实看恢复后的深色首屏及白底导师区域；查看桌面/手机人物截图。实际首页视频在普通动效下可见且播放。用户审美、真实iOS/Safari及生产未验收。

## 本轮修改文件
- CLAUDE_HANDOFF.md
- FINAL_INTEGRATION_REPORT.md
- FUSION_REVIEW.md
- PR_DRAFT.md
- README.md
- VISUAL_REDESIGN_REPORT.md
- frontend/src/components/Footer.astro
- frontend/src/components/Nav.astro
- frontend/src/components/SiteMotion.astro
- frontend/src/layouts/Layout.astro
- frontend/src/pages/about.astro
- frontend/src/pages/index.astro
- frontend/src/pages/team.astro
- frontend/src/styles/global.css
- frontend/src/styles/group.css
- frontend/src/styles/theme.css
- scripts/check_group_site.py
- scripts/check_original_people.py
- scripts/check_visual_fusion.py

## 预览与后续
预览：http://127.0.0.1:4327/ ，浏览器已展示当前版。
本地开发：ASTRO_TELEMETRY_DISABLED=1 npm --prefix frontend run dev -- --host 127.0.0.1 --port 4327；占用时复用当前预览，不终止他人服务。
Claude入口CLAUDE_HANDOFF.md；先核对Furnace任务/锁，以用户指定原版作局部修正，不再自行换设计方向。
未完成：用户实际审阅、老师复核人物当前状态/学术资料、真实生产审核数据迁移、Safari/iOS和正式域名/部署独立审批。
未访问生产服务器、COS/SCF，未改DNS、备案、证书、EdgeOne或定时器，未安装Claude Code。
