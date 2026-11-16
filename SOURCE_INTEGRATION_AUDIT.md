# 源码及内容核对（2026-11-15，本地）
源版本：
- buerka/EEGLab e3585f90fabec82f22cf4452e014b7769012a1f7
- shimuxia/yan-ying-research-group bbec06eba92ee19a004b7909c2eb3ecdb2cc07bf（私有，只迁移必要公开页面内容）
- fork shimuxia/EEGLab，parent=buerka/EEGLab；许可证和署名保持原样。

## 功能与映射
旧官网单页的 about/research/team/achievements/papers/admission/contact 分区分别映射 /about、/research、/team、/achievements、/achievements#papers、/join、/contact；首页保留旧锚点入口。
EEGLab 的 /、/research、/team、/achievements、/contact 统一为课题组主体。五个研究详情 diagnosis/arm/drone/hand/glove 原样保留；新增 brain-computer-interface 作为实验室总览，无 iframe 或第二首页。
Astro 静态页面与 React 论文组件继续使用 frontend/；图片、压缩视频、gallery.toml、awards.toml 保留。原首页视频移入实验室总览。
原官网是深色黑银、暖金点缀、SVG 科研图形及进入视口动画；整合保留深色 hero、导师介绍、大留白和克制动画，不加载旧全局 CSS。
人员：group-content.json 来源旧官网 SITE_DATA；lab-team.json 来源 EEGLab team.astro。独立来源分区，已确认同一导师使用共享介绍；不推断其他同名身份。招生卡和“更多同学”不作为人员。
研究方向：旧官网七方向完整保留；实验室五方向另作 BCI 子模块。
荣誉：以用户明确核对及旧 index.html 为依据；2024年度中国技协二等奖于2025-02颁奖；2023年度江苏省自动化学会三等奖于2024-02颁奖；2023 PHM获奖；2015 CASE入围；2026前2%仅单年度。
联系：以旧官网公开邮箱和 N505 为主；实验室金牛湖园区为实验地点。不扩散旧实验室手机号码。
备案：保留旧官网真实备案文字及工信部链接，部署归属待独立审批。
静态资料：仅复制 SITE_DATA 引用的公开成员照片，不复制私有后端/历史/数据库/内部文档。未确认动态计数、占位项目不迁移。

## 论文平台比较与决策
|维度|原官网|EEGLab|整合|
|---|---|---|---|
|模型|SQLite九表，研究者关联与人工覆盖|相近共享Python模型|继承EEGLab单后端|
|作者标识|ying-yan / lkDrRmoAAAAJ / A5101638873 / ORCID 0000-0002-3609-0496|相同|明确身份一致|
|来源|Scholar唯一发现源|OpenAlex + Scholar|统一只读端点对严颖仅公开confirmed|
|去重|Scholar ID/DOI/规范标题+年份和证据|OpenAlex ID/DOI及Scholar匹配|不拼库，不改同步|
|审核|accept/exclude版本化；人工字段独立|审核种子、paper_overrides|读取已有审核，排除优先，人工字段不写|
|排除|两篇独立基线，恢复前检查|原规则集未含该基线|独立代码基线+研究者级输出过滤|
|API|论文、研究者、版本、状态|同类API + analytics|新增/group只读适配，原接口保留|
|调度|单一Scholar scheduler|SCF每日03:30|本轮均不启动、不修改|
|回退|失败保留快照，前端三篇代表论文|旧COS快照、前端错误重试|保留前端重试与静态代表论文|
|持久化|本地SQLite，外置运行目录|COS快照+临时SQLite|仅临时合成数据验收|
恢复门禁代码与测试已审阅：缺失/冲突规则不得静默补齐；输出须在分页及统计之前排除；共享论文只移除严颖关联，不误伤其他研究者。新只读策略不宣称完成生产恢复或Scholar-only同步迁移。
正式迁移前仍须一致性完整数据库备份、全部人工审核、冻结写入者、身份/规则映射审查及独立上线授权；不以种子或公开API导出代替备份。

## 已读入口与验证基础
EEGLab AGENTS、README、docs/handoff、publications-platform、tencent-makers、frontend/README、backend/README、todo、edgeone、package/astro配置及CI；旧官网AGENTS、README、index、CSS、script、paper-sync README/restore_guard/研究者与审核模型、排除门禁及测试结构。
原有Python unittest、Astro构建和部署输入检查作为基础；补充合成数据安全回归、全部路由/资源/桌面手机检查。历史PASS不作为本次结果。
