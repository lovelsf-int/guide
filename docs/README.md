---
home: true
icon: "mdi:home-outline"
title: guide（JavaGuide 独立学习镜像）
description: JavaGuide 是 GitHub 156K+ Star 的 Java 面试与后端知识体系指南，免费开源，系统覆盖 Java、计算机基础、数据库、分布式、高并发、高可用、系统设计与 AI 应用开发，适合校招、社招、跳槽和后端能力体系化复习。
heroImage: /logo.svg
heroText: guide
tagline: 基于 JavaGuide 的独立学习镜像，覆盖 Java、计算机基础、数据库、分布式、高并发、系统设计与 AI 应用开发
sitemap:
  changefreq: weekly
  priority: 0.9
head:
  - - meta
    - name: keywords
      content: JavaGuide,Java面试,Java面试指南,Java八股文,后端面试,后端开发,数据库面试,MySQL面试,Redis面试,分布式,高并发,高性能,高可用,系统设计,消息队列,缓存,计算机网络,Linux,AI面试,AI应用开发,Agent,RAG,MCP,LLM,AI编程
  - - meta
    - property: og:image
      content: https://javaguide.cn/logo.png
actions:
  - text: 开始阅读
    link: /home.md
    type: primary
  - text: 免费完整讲解
    link: /reading/
    type: default
footer: |-
  guide · JavaGuide 独立学习镜像 · 原作者 <a href="https://github.com/Snailclimb/JavaGuide">Guide / JavaGuide contributors</a> · <a href="/guide/LICENSE.txt">Apache-2.0</a> | 主题: <a href="https://theme-hope.vuejs.press/" target="_blank">VuePress Theme Hope</a>
---

<!-- Modified for guide, 2026-10-09: add free lesson hub and describe the independently authored study supplements. -->

<!-- Modified for the guide mirror on 2026-10-05: title, attribution footer. Original article content preserved. -->
<!-- markdownlint-disable MD033 -->

## 核心入口

- **免费完整讲解**：[专题补全目录](./reading/)：Redis 集群、Elasticsearch、Netty、Spring Boot、PriorityQueue、系统设计、设计模式、面试自测与实战教程。开源正文直接显示，新增内容均标明原创补充。

- **后端面试主线**：[后端面试指南](./home.md)（⭐网站核心）：系统整理 Java 面试八股文和后端高频面试题，覆盖 Java 基础、集合、并发、JVM、Spring、MySQL、Redis、分布式、高并发、高可用和系统设计。
- **计算机基础**：[计算机基础面试指南](./cs-basics/)：系统梳理计算机网络、操作系统、数据结构与算法等后端面试底层基础，适合补齐基础短板。
- **AI 应用开发**：[AI 应用开发面试指南](./ai/)（⭐新增）：面向后端开发者梳理大模型基础、Prompt、Agent、RAG、MCP、LLM API 工程和 AI 系统设计等高频知识；如果想系统学习，可以配合 [AI 应用开发与 Agent 学习路线（2026 最新版）](./roadmap/java-to-ai-roadmap.md) 和 [后端转 AI Agent 学习建议（2026 最新版）](./roadmap/backend-to-ai-agent-roadmap.md)。
- **AI 编程实战**：[AI 编程实践指南](./ai-coding/)（⭐新增）：聚焦 Claude Code、Codex、AI IDE、CLI Agent、上下文管理和 AI 辅助开发工作流，帮助你把 AI 真正用进日常编码。
- **学习路线**：[学习路线合集（2026 最新版）](./roadmap/)：整理 Java 后端、AI 应用开发、AI Agent 和全栈开发等方向的系统学习建议。
- **原创免费教程**：
  - [Java 后端系统复习](./zhuanlan/java-mian-shi-zhi-bei.md)：从基础、项目表达、场景题到自测，建立可执行的复习路径。
  - [系统设计与场景题练习](./zhuanlan/back-end-interview-high-frequency-system-design-and-scenario-questions.md)：用完整案例练习需求、不变量、失败处理与验证，并衔接 26 道场景题。
  - [AI 面试平台与 RAG](./zhuanlan/interview-guide.md)：讲解数据模型、权限过滤、检索、结构化回答和评测，适合作为独立练习项目的实现指南。

## 精选文章

- **后端面试路径**：[Java 后端面试通关计划](./interview-preparation/backend-interview-plan.md)、[Java 学习路线（2026 最新版）](./interview-preparation/java-roadmap.md)、[Java 后端面试重点总结](./interview-preparation/key-points-of-interview.md)。不知道从哪里开始复习时，优先看这一组。
- **Java 与数据库高频题**：[Java 基础](./java/basis/java-basic-questions-01.md)、[Java 集合](./java/collection/java-collection-questions-01.md)、[Java 并发](./java/concurrent/java-concurrent-questions-01.md)、[JVM](./java/jvm/README.md)、[MySQL](./database/mysql/mysql-questions-01.md)、[Redis](./database/redis/redis-questions-01.md)。适合集中刷语言、运行时和数据存储相关的核心问题。
- **架构与中间件高频题**：[分布式](./distributed-system/distributed-system-interview-questions.md)、[微服务](./distributed-system/microservices-interview-questions.md)、[消息队列](./high-performance/message-queue/message-queue-interview-questions.md)、[高性能](./high-performance/high-performance-system-interview-questions.md)、[高可用](./high-availability/high-availability-system-interview-questions.md)、[系统设计](./system-design/system-design-questions.md)。适合准备社招、中高级岗位和项目场景追问。
- **计算机基础补强**：[计算机网络](./cs-basics/network/other-network-questions.md)、[操作系统](./cs-basics/operating-system/operating-system-basic-questions-01.md)、[进程和线程](./cs-basics/operating-system/process-and-thread.md)、[数据结构与算法](./cs-basics/algorithms/)。适合补齐校招、社招和大厂面试都绕不开的基础能力。
- **AI 应用开发进阶**：[AI 应用开发与 Agent 学习路线（2026 最新版）](./roadmap/java-to-ai-roadmap.md)、[后端转 AI Agent 学习建议（2026 最新版）](./roadmap/backend-to-ai-agent-roadmap.md)、[AI 应用开发知识体系](./ai/)、[LLM API 工程实践](./ai/llm-basis/llm-api-engineering.md)、[RAG 基础概念](./ai/rag/rag-basis.md)、[AI 应用系统设计](./ai/system-design/ai-application-architecture.md)。适合后端开发者先明确学习路径，再从模型调用走向可上线的 AI 应用。
- **AI 编程效率提升**：[AI 编程实战指南](./ai-coding/)、[Claude Code 使用指南](./ai-coding/practices/claudecode-tips.md)、[Codex 使用指南](./ai-coding/practices/codex-best-practices.md)、[AI IDE 选型与实践](./ai-coding/practices/ai-ide.md)。适合把 AI 编程工具真正接入日常开发、重构和排障流程。

## 关于 JavaGuide

JavaGuide 是一份面向 Java 和后端开发者的开源知识库，已在 GitHub 获得 **156K+ Star**。项目从 Java 面试复习出发，逐步扩展为覆盖后端核心技术、工程实践和 AI 应用开发的系统化学习指南。

JavaGuide 自 2018 年开源以来持续维护，累计提交 **6200+** commit ，共有 **640+** 多位贡献者共同参与维护和完善。

![JavaGuide 目前的 Star、Fork、Issue 和 PR 情况](https://oss.javaguide.cn/github/javaguide/intro/javaguide-star-issue-pr.png)

网站内容覆盖：

- **后端面试**：Java 基础、集合、并发、JVM、MySQL、Redis、分布式、系统设计等核心知识。
- **AI 应用开发**：大模型（LLM）基础、Agent 智能体、RAG 检索增强生成、MCP 协议等前沿技术。

真心希望能够把这个项目做好，真正能够帮助到有需要的朋友！

如果觉得 JavaGuide 的内容对你有帮助的话，还请点个免费的 Star（绝不强制点 Star，觉得内容不错有收获再点赞就好），这是对我最大的鼓励，感谢各位一路同行，共勉！传送门：[GitHub](https://github.com/Snailclimb/JavaGuide) | [Gitee](https://gitee.com/SnailClimb/JavaGuide)。

- [项目介绍](./javaguide/intro.md)（JavaGuide 的诞生）
- [贡献指南](./javaguide/contribution-guideline.md)（期待你的贡献，奖励丰富）
- [常见问题](./javaguide/faq.md)（统一回复大家的一些疑问）

## PDF 版本 & 微信联系

- 如果你更喜欢 **PDF**（比如通勤/离线阅读/打印学习），扫描下方二维码，后台回复“**PDF**”即可获取最新版（持续更新，详细介绍见：**[2026 最新后端面试 PDF 资料](./interview-preparation/pdf-interview-javaguide.md)**）。
- 如果你想加我的微信，可以扫描下方二维码，后台回复“**微信**”。我会在朋友圈分享一些优质技术内容、学习资料和项目更新。

<img src="https://oss.javaguide.cn/github/javaguide/gongzhonghao-javaguide.png" alt="JavaGuide 公众号" style="zoom: 43%; display: block; margin: 0 auto;" />
