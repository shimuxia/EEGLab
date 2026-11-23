// Verbatim content restored from the two source sites. See SOURCE_CONTENT_MATRIX.md.
// TEACHER = shimuxia/yan-ying-research-group (index.html, js/script.js SITE_DATA)
// LAB     = buerka/EEGLab upstream/main (frontend/src/pages/*)
// Do not paraphrase facts here; edit only to mirror an updated source.

/** TEACHER · RESEARCH_TAGLINES, same order as the seven directions. */
export const researchTaglines = [
  "看见系统异常。",
  "读懂脑电信号。",
  "预测电力与天气变化。",
  "看清舆论的走向。",
  "找到更优的解。",
  "让算法落到硬件系统。",
  "让机器自己行动。",
];

/** TEACHER · #research section head and closing note. */
export const researchIntro = {
  title: "七个方向，一条主线",
  desc: "以模式识别、机器学习与优化为核心，把智能方法落到复杂系统、脑机接口、预测与硬件等真实问题上。",
  note: "当前页面先展示课题组已有研究方向与代表性工作；后续将进一步补充课题组提出的新方法、模型与系统成果。",
};

/** TEACHER · about__bio paragraphs 2 and 3 (paragraph 1 is advisor.biography). */
export const advisorBioMore = [
  "研究方向涵盖模式识别、机器学习、深度学习与优化算法，应用场景聚焦复杂系统故障诊断与预测、脑机接口与脑电分析、具身智能与人机协同三大方向。在智能电网、智能建筑与故障诊断领域有十余年深厚积累，近年来将智能方法拓展至脑疾病辅助诊断、VR 晕动症评估、无人系统智能决策等交叉前沿。",
  "已发表论文 70 余篇，其中中科院 1 区论文 29 篇，以第一作者或通讯作者身份发表 SCI 论文 31 篇；获授权发明专利 16 项；以第一完成人获中国技协 2024 年职工技术创新成果二等奖（2025 年 2 月获奖）、2023 年度江苏省自动化学会科学技术奖三等奖（2024 年 2 月获奖）；有论文获 2023 年 IEEE PHM 最佳论文奖（Best Paper Award），另有论文入围 2015 年 IEEE CASE 最佳学生论文奖最终候选（Best Student Paper Award Finalist）；入选斯坦福大学/爱思唯尔全球前2%顶尖科学家榜单（2026年，单年度影响力）。担任多个国际期刊副编和二十余个 SCI 期刊审稿人。",
];

/** Figures taken from the paragraph above (no new numbers). */
export const advisorFigures = [
  { value: 70, suffix: "+", label: "已发表论文" },
  { value: 29, suffix: "", label: "中科院 1 区论文" },
  { value: 31, suffix: "", label: "第一 / 通讯作者 SCI" },
  { value: 16, suffix: "", label: "授权发明专利" },
];

/** TEACHER · about__facts. */
export const advisorFacts = [
  { label: "博士学位", value: "美国康涅狄格大学（University of Connecticut, 2018）" },
  { label: "学科", value: "电气工程及其自动化" },
  { label: "主要任职", value: "电气工程系副系主任 · 江苏省气象能源利用与控制工程技术研究中心副主任" },
];

/** TEACHER · admission__lead and admission__quote. */
export const admissionLead = "面向控制、数据与智能系统的交叉研究，招生信息按方向、规模、专业背景与学生特点分列如下。";
export const advisorQuote = {
  label: "导师寄语",
  text: "我不是那种“高冷”型导师，我是那种“论文写好了吗” + “别慌，我来帮你搞定”的暖心型导师。欢迎各种性格的小伙伴加入，内向的我帮你打开思路，外向的咱一起头脑风暴！我不喜欢“命令式”指导，更喜欢和学生像朋友一样讨论问题，一起成长。如果你想找一个能聊得来、讲得了段子、也带你发 Paper 的导师，那我可能正合你胃口！",
  cite: "严颖",
};

/** TEACHER · team.masters open entry and undergradGroups[4] closing entry. */
export const openPosition = { name: "招生中", stage: "5–7 人 / 年", note: "欢迎报考，详见招生信息" };
export const moreAlumni = { name: "更多同学", stage: "本科 · 已毕业", note: "浙大 / 东南 / 西电 / 南邮等，更多去向见个人主页" };

/** TEACHER · SITE_DATA.achievements[2]. */
export const projectPatentNote = {
  kind: "项目 / 专利",
  title: "高价值专利培育与产学研合作",
  meta: "省/市级大创、专利培育大赛多项获奖",
  source: "来源：个人主页",
};

/** LAB · index.astro hero + statement; research/index.astro intro. */
export const labSlogan = {
  short: "让思想驱动未来",
  line: "从脑电信号到运动控制，让思想驱动未来",
  en: "From EEG Signal to Motion Control — Let Thought Drive the Future",
  researchIntro: "围绕脑机接口核心技术，探索从信号采集到运动控制的完整链路，实现脑意图向机械动作的精准映射。",
};

/** LAB · index.astro statement stats (the "7 代表性奖项" figure conflicts with awards.toml and is omitted). */
export const labFigures = [
  { value: 16, suffix: "+", label: "授权专利" },
  { value: 5, suffix: "", label: "实验专题" },
];

/** LAB · team.astro join-block and contact.astro join section. */
export const labJoin = {
  text: "欢迎对脑机接口、EEG 信号分析、神经工程、嵌入式系统、机器人控制等方向感兴趣的研究生与本科生加入团队。课题组提供完善的实验设备、充足的科研经费与定期的国际学术交流机会。",
  detail: "课题组长期招收对脑机接口、EEG 信号分析、神经工程、嵌入式系统、机器人控制等方向感兴趣的研究生（学硕/专硕）与本科生。课题组依托南京信息工程大学自动化学院与金牛湖产教融合园区，拥有完善的实验平台与充足的科研经费，与多所国际知名高校保持密切合作关系。",
  requirements: [
    "自动化、电气工程、计算机科学、生物医学工程等相关专业背景",
    "具备扎实的数学基础与编程能力（Python / MATLAB）",
    "对神经工程与脑机接口领域有浓厚兴趣",
    "具有良好的英语阅读与写作能力",
  ],
};

/** TEACHER · contact card for the lab's own domain. */
export const labDomain = { href: "https://eeg.yanyinglab.cn/", label: "eeg.yanyinglab.cn" };
