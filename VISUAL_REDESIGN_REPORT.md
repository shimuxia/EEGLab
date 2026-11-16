本轮浅色主题验证：13页构建/部署输入PASS；43项页面交互PASS；浅色初轮发现图库未选按钮和研究编号对比度不足，修正后128项对抗检查PASS（含全路由桌面/手机axe、极窄屏、200%文字、API/视频退化）。已查看首页、老师、团队的桌面和手机截图。原始照片/内容/后端/生产配置均未改；未push/PR/部署。

## 当前视觉方向：统一浅色（2026-11-16，用户最新反馈）
用户认可前端结构，但否定黑白区块交替，以及白底人物照片在深底上的高反差。当前方案已覆盖前面的深色方案：
- 全站暖白 #fafaf7、浅灰 #f2f3ed，人物区域纯白；深灰绿正文、克制深金细节。
- 首页/内页/导航/页脚同一浅色体系，视频画面内部保留深色，不再使用大块深色页面背景。
- 老师、学生、顾问照片恢复自然色彩；原始照片未编辑，蓝底原图也保持原貌。白底照片与人物区自然融合。
- 保留已认可的排版、七方向交互、视频、动效、论文安全逻辑。后续不要擅自退回黑白交替或深底衬白底证件照。

# 前端重做与对抗审查交接
2026-11-16；仅本地功能分支。精确交付SHA由提交后的工作区同名报告记录，仓库内以 git rev-parse HEAD 查询。

## 前端实际改动
- 以课题组为主角的深色首屏：中文组名、英文标识、实验室视频、科研信号和轨道细节；有视频控制及减少动效处理。
- 从原官网选择性复用七套科研SVG，建立七方向ARIA tabs；支持点击、方向键、Home/End与手机横向选择。
- 实验室真实现场大图和五专题入口；导师编辑版式；非等高成果影像；荣誉时间线；论文行列表；错落成员照片；招生收尾。
- global.css单一设计token；theme.css共享交互/动效基础；group.css管理首页和内页版式。原论文组件、导航、页脚和成果图库统一主题。
- 五个研究详情恢复现有研究实图；团队恢复顾问肖像。内容身份及后台数据逻辑不变。
- 没有生造图片或论文数量，没有引入新框架、外部字体或跟踪请求。原视频和图片继续作为真实素材。

## 对抗方法与已修问题
主动构造失败而非只测正常路径：
1. 嵌套null研究者导致React读取slug崩溃：已复现；新增纯数据契约解析，拒绝无效嵌套对象、错误集合/计数、危险URL，前端安全退化。
2. 研究浅色区/图库/论文徽章残留低对比度：用axe逐节点检测后修正；邮箱正文链接加下划线。
3. 视频在脚本加载前失败时漏接error：检查NETWORK_NO_SOURCE，保留海报，给出状态并禁用失效控制。
4. 390px轨道装饰溢出、SVG挤入说明文字：局部裁切装饰并明确图形尺寸，加入图文边界断言。
5. 200%文字放大导致页脚溢出、首屏高度挤压、跳转链接露出：页脚允许换行，移除首屏高度上限，导航随文字增长，隐藏链接改为基于自身高度位移；CTA允许换行。
6. 完善main焦点目标、菜单Esc关闭及标签键盘导航；修正首页重复标题。
7. 后端失败及无效JSON不得向访客输出错误详情；超时中止与缓存拒绝清理保留恢复重试能力。

## 复现命令
全部在WSL工程repo目录执行：
```bash
npm run test:frontend
(cd frontend && node_modules/.bin/tsc --noEmit --target ES2022 --module ESNext --moduleResolution bundler --jsx react-jsx --skipLibCheck --types astro/client src/lib/*.ts src/components/*.tsx)
ASTRO_TELEMETRY_DISABLED=1 npm run build
.venv/bin/python scripts/check_deployment.py
CHROMIUM_PATH=/home/shimuxia/.cache/ms-playwright/chromium-1228/chrome-linux64/chrome .venv/bin/python scripts/check_group_site.py
# 仅本地QA工具，output受Git忽略；不改变项目生产依赖：
npm install --prefix output/accessibility --no-save axe-core@4.14.0
CHROMIUM_PATH=/home/shimuxia/.cache/ms-playwright/chromium-1228/chrome-linux64/chrome .venv/bin/python scripts/check_adversarial_site.py
```
页面预览需已运行于127.0.0.1:4327，所有浏览器测试阻断外部请求，API为合成数据。Playwright安装命令见原交接。

## 最终实测结果
- npm run test:frontend：14项PASS。
- React与数据模块TypeScript检查：PASS，无诊断输出。
- npm run build：13页PASS；check_deployment.py：PASS。
- check_group_site.py：43项PASS（完整页面/交互）。
- check_adversarial_site.py：128项PASS；含27个axe场景（26个路由宽度组合+1个合成API成功态）、65个五档屏宽场景、26个200%文字放大场景，以及异常API/注入/媒体/超时/恢复/无JS。
- 对抗集最后重跑已加入：放大后首屏不挤压后续内容、隐藏跳转链接不露出、主要CTA不被裁切。
- 已看桌面/手机/研究区/成果页及文字放大前后截图；公开构建敏感模式/内部路径扫描PASS；git diff --check PASS。
- 本轮失败均有复现与修复后验证；不把历史PASS替代本次结果。

## 验证范围与边界
- 基础页面集：13路由×1440/768/390；导航、图片/链接、图库、论文筛选、七方向/键盘、视频及动效。
- 对抗集：26个桌面/手机axe场景；65个五档屏宽路由场景；26个200%文字放大场景；异常/注入/恢复/媒体退化。
- API边界14项Node测试；React与数据模块TypeScript检查；13页构建和部署输入检查。
- 结果、截图和失败基线保存在忽略的output，不把这些临时文件提交到仓库。
- 不将自动axe无违规等同人工屏幕阅读器认证；尚未运行Safari/真实iOS/Android。不同网络和真实生产数据迁移继续单独审核。
- 原后端无修改，本轮不把旧后端测试当作新执行结果。LICENSE、生产配置、种子、审核数据和lockfile未改。
- 未push、未创建PR、未merge、未部署。用户回来后浏览器已成功连接并打开本地首页。

## 后续接手
代码在 /mnt/d/AI-Agent-Workspace/Projects/YanYing-EEGLab-Merge/repo ，分支 feat/unify-yanying-group-site。
先读 CLAUDE_HANDOFF.md 及当前熔炉任务锁；在已经落地的视觉版本上精修，不回退成上一版通用信息卡片。
