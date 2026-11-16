import content from "./group-content.json";
import lab from "./lab-team.json";

export interface Member {
  name: string;
  stage: string;
  note?: string;
  photo?: string;
  photoAlt?: string;
}
export interface Direction {
  no: string;
  id: string;
  title: string;
  en: string;
  desc: string;
  tags: string[];
}
export const directions: Direction[] = content.research;
export const members: Member[] = content.team.masters;
export const studentGroups = content.team.undergradGroups;
export const admission = content.admission;
export const representativePapers = content.papers;
export const labTeam = lab;
export const advisor = {
  name: "严颖",
  nameEn: "Ying Yan",
  photo: content.team.advisor.photo,
  role: content.team.advisor.stage,
  affiliation: "南京信息工程大学自动化学院",
  biography:
    "南京信息工程大学自动化学院副教授、硕士生导师，电气工程系副系主任，江苏省气象能源利用与控制工程技术研究中心副主任。博士毕业于美国康涅狄格大学，师从 IEEE Life Fellow Peter B. Luh 教授。",
  interests: content.aboutTags,
  email: "ying.yan@nuist.edu.cn",
  homepage: "https://faculty.nuist.edu.cn/yanying/zh_CN/index/110297/list/",
  scholar: "https://scholar.google.com/citations?user=lkDrRmoAAAAJ&hl=zh-CN",
  office: "学科楼 3 号楼 N505",
};
export const honors = [
  {
    year: "2026",
    title: "斯坦福大学 / 爱思唯尔全球前2%顶尖科学家",
    detail: "2026年单年度影响力榜单",
  },
  {
    year: "2025.02",
    title: "中国技协2024年职工技术创新成果二等奖",
    detail: "严颖为第一完成人；2025年2月获奖",
  },
  {
    year: "2024.02",
    title: "2023年度江苏省自动化学会科学技术奖三等奖",
    detail: "严颖为第一完成人；2024年2月获奖",
  },
  {
    year: "2023",
    title: "IEEE PHM Best Paper Award",
    detail: "最佳论文奖（获奖）",
  },
  {
    year: "2015",
    title: "IEEE CASE Best Student Paper Award Finalist",
    detail: "最佳学生论文奖最终候选（入围）",
  },
];
