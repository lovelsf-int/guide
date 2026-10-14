import { arraySidebar } from "vuepress-theme-hope";

export const paymentSubscriptions = arraySidebar([
  { text: "专题入口与项目口径", link: "/payment-subscriptions/" },
  {
    text: "数据模型与恢复购买",
    children: [
      { text: "表结构与流水关系", link: "data-model" },
      { text: "恢复购买与交易查询", link: "restore-purchases" },
    ],
  },
  {
    text: "生产可靠性",
    children: [
      { text: "生命周期与事务一致性", link: "lifecycle-consistency" },
      { text: "补偿与跨区可靠性", link: "reliability" },
    ],
  },
  { text: "40 道面试题与参考回答", link: "interview" },
]);
