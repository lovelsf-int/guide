import { navbar } from "vuepress-theme-hope";

export default navbar([
  { text: "后端开发", icon: "mdi:language-java", link: "/home.md" },
  { text: "计算机基础", icon: "mdi:desktop-classic", link: "/cs-basics/" },
  { text: "AI应用开发", icon: "mdi:robot-outline", link: "/ai/" },
  { text: "AI编程", icon: "mdi:code-tags", link: "/ai-coding/" },
  {
    text: "学习导航",
    icon: "mdi:book-open-page-variant-outline",
    children: [
      {
        text: "专题复习",
        icon: "mdi:book-open-page-variant-outline",
        link: "/reading/",
      },
      { text: "学习路线", icon: "mdi:map-outline", link: "/roadmap/" },
      { text: "开源项目", icon: "mdi:github", link: "/open-source-project/" },
      {
        text: "技术书籍",
        icon: "mdi:book-open-page-variant-outline",
        link: "/books/",
      },
      {
        text: "工程实践与经验",
        icon: "mdi:code-tags",
        link: "/high-quality-technical-articles/",
      },
    ],
  },
  {
    text: "复习工具",
    icon: "mdi:information-outline",
    children: [
      {
        text: "使用指南",
        icon: "mdi:account-edit-outline",
        link: "/javaguide/use-suggestion.md",
      },
      {
        text: "复习清单",
        icon: "mdi:file-pdf-box",
        link: "/interview-preparation/pdf-interview-javaguide.md",
      },
      {
        text: "面试自测",
        icon: "mdi:file-pdf-box",
        link: "/interview-preparation/self-test-of-common-interview-questions.md",
      },
      {
        text: "来源与许可",
        icon: "mdi:information-outline",
        link: "/about-the-author/",
      },
    ],
  },
]);
