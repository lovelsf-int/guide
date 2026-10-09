---
home: true
icon: "mdi:home-outline"
title: guide 复习与知识整理
description: Java、计算机基础、数据库、分布式、系统设计与 AI 应用开发的知识整理，结合原理、示例、源码阅读和自测进行复习。
heroImage: /logo.svg
heroText: guide
tagline: Java、计算机基础、数据库、系统设计与 AI 应用开发的知识整理和复习笔记
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
  - text: 专题复习
    link: /reading/
    type: default
footer: |-
  guide · 来源 <a href="https://github.com/Snailclimb/JavaGuide">Guide / JavaGuide contributors</a> · <a href="/guide/LICENSE.txt">Apache-2.0</a> | 主题: <a href="https://theme-hope.vuejs.press/" target="_blank">VuePress Theme Hope</a>
---

<!-- Modified for guide, 2026-10-09: add free lesson hub and describe the independently authored study supplements. -->

<!-- Modified for the guide mirror on 2026-10-05: title, attribution footer. Original article content preserved. -->
<!-- markdownlint-disable MD033 -->

## 核心入口

- **专题复习**：[专题复习目录](./reading/)：Redis 集群、Elasticsearch、Netty、Spring Boot、PriorityQueue、系统设计、设计模式、面试自测与实战教程。按原理、示例与自测组织复习。

- **后端面试主线**：[后端面试指南](./home.md)（⭐网站核心）：系统整理 Java 面试八股文和后端高频面试题，覆盖 Java 基础、集合、并发、JVM、Spring、MySQL、Redis、分布式、高并发、高可用和系统设计。
- **计算机基础**：[计算机基础面试指南](./cs-basics/)：系统梳理计算机网络、操作系统、数据结构与算法等后端面试底层基础，适合补齐基础短板。
- **AI 应用开发**：[AI 应用开发面试指南](./ai/)（⭐新增）：面向后端开发者梳理大模型基础、Prompt、Agent、RAG、MCP、LLM API 工程和 AI 系统设计等高频知识；如果想系统学习，可以配合 [AI 应用开发与 Agent 学习路线（2026 最新版）](./roadmap/java-to-ai-roadmap.md) 和 [后端转 AI Agent 学习建议（2026 最新版）](./roadmap/backend-to-ai-agent-roadmap.md)。
- **AI 编程实战**：[AI 编程实践指南](./ai-coding/)（⭐新增）：聚焦 Claude Code、Codex、AI IDE、CLI Agent、上下文管理和 AI 辅助开发工作流，帮助你把 AI 真正用进日常编码。
- **学习路线**：[学习路线合集（2026 最新版）](./roadmap/)：整理 Java 后端、AI 应用开发、AI Agent 和全栈开发等方向的系统学习建议。
- **专项练习**：
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
