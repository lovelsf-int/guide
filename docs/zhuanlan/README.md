---
title: 免费原创专题：面试、系统设计、RPC、源码与 RAG
description: guide 独立原创补充，连接免费面试训练、系统设计案例、源码阅读、RPC 与 RAG 工程教程，保留上游公开介绍。
category: 知识星球
sitemap:
  changefreq: weekly
  priority: 0.9
head:
  - - meta
    - name: keywords
      content: JavaGuide知识星球,Java面试指北,后端系统设计,手写RPC框架,Java源码阅读,Java实战项目,Java面试资料,知识星球专栏
author: guide 原创补充
---

## 免费原创专题与学习入口

> **guide 原创补充**：本镜像为下列五个公开专题补写了可直接阅读的独立教程，并保留原作者的公开介绍。补充内容不等于原付费专栏全文，也没有取得或还原其不可见章节。阅读正文无需加入外部社群。

先选一个能完成的小任务，再按失败点补知识。每个专题都包含完整示例、练习和验收条件；基础机制优先链接已有开源文章，避免同一知识在多页反复重写。

| 专题 | 直接学习的内容 | 完成后应留下什么 |
| --- | --- | --- |
| [面试准备与能力训练](./java-mian-shi-zhi-bei.md) | 诊断评分、线程池案例、项目证据、面经复盘与两周安排 | 自测记录、项目调用链、真实指标来源 |
| [系统设计与场景训练](./back-end-interview-high-frequency-system-design-and-scenario-questions.md) | 从导出任务练需求、容量、状态机、幂等和故障推演 | 数据模型、失败矩阵、容量假设 |
| [源码阅读实践](./source-code-reading.md) | Spring Boot 条件装配、Netty 消息边界、Dubbo 调用模型 | 版本固定的源码证据卡与实验 |
| [教学 RPC 设计](./handwritten-rpc-framework.md) | 协议、请求关联、超时清理、发现、SPI 与测试矩阵 | 一条正常调用与多条失败路径 |
| [AI 面试与 RAG 工程](./interview-guide.md) | 文档版本、授权检索、可靠任务、流式状态与离线评测 | 可追溯引用、权限测试、基线报告 |

## 先补直接影响阅读的空白

框架与数据方向可以直接阅读 [Spring Boot 面试](../system-design/framework/spring/springboot-knowledge-and-questions-summary.md)、[Spring Boot 源码](../system-design/framework/spring/springboot-source-code.md)、[Netty](../system-design/framework/netty.md)、[Redis 集群](../database/redis/redis-cluster.md)、[Elasticsearch](../database/elasticsearch/elasticsearch-questions-01.md)和[PriorityQueue 源码](../java/collection/priorityqueue-source-code.md)。训练方向有[自测](../interview-preparation/self-test-of-common-interview-questions.md)、[面经复盘](../interview-preparation/interview-experience.md)与[系统设计案例](../system-design/system-design-questions.md)。

已有完整开放正文的 [Kafka](../high-performance/message-queue/kafka-questions-01.md)、[分布式事务](../distributed-system/distributed-transaction.md)、[SQL 优化](../high-performance/sql-optimization.md)、[RAG 面试](../ai/interview-questions/rag-interview-questions.md)可以直接使用，不需要因为历史宣传曾将它们归入专栏而重复补写。

## 选择学习顺序

准备近期面试时，从面试训练开始，完成自测后选择最弱的一条技术链路。想补项目经验时，先完成 RPC 或 RAG 的最小可运行闭环，再回头读相应框架源码。想提高系统设计能力时，先独立写出不变量和失败表，再看案例，对比自己的遗漏。

每一轮学习只要求一个可检查成果：一段可以解释的代码、一份故障重现记录或一张有数字来源的容量估算表。未经执行的实验写为待验证；不把教学参数当作生产结果；不把模拟问答当作真实公司面经。这样的记录既能帮助复习，也能成为项目讨论时的依据。

## 使用本专题的验收方式

读完一个专题后合上页面，用自己的例子复述成功路径，再改变一个前提：请求重复、依赖超时、权限撤回、数据增长或进程重启。若只会重复原文结论，继续补对应的机制文章；若能说明约束、状态、代价与验证方法，就进入下一条链路。详细的上游内容定位与原作者介绍保留在各页最后，便于区分来源和理解原项目背景。


## 一次最小练习示例

选择“请求超时后服务端仍完成写入”这个问题，先画客户端、网络和服务端三条时间线，标出客户端放弃等待与数据库提交的先后关系。然后分别对只读查询和发券操作提出恢复方案：前者可以在预算内重查，后者需要幂等键与结果查询。最后到 RPC、系统设计或 RAG 专题中找到对应机制，补一个超时后响应晚到的实验。验收时检查实际副作用和资源清理，不能只看客户端是否收到超时异常。

## 上游公开介绍（原文保留）

> 以下为 JavaGuide 原作者在开源仓库中公开的介绍与宣传材料，保留原文及来源归属。文中项目版本、数量、服务与效果描述属于上游介绍，不作为本镜像原创补充的验证结果。


这份 **星球专属优质专栏** 汇总 JavaGuide 知识星球里的系统学习资料，覆盖 Java 面试、系统设计与场景题、手写 RPC、源码阅读和实战项目。

如果你正在准备 Java 后端面试，建议先看 [《Java 面试指北》](./java-mian-shi-zhi-bei.md) 和 [《后端面试高频系统设计&场景题》](./back-end-interview-high-frequency-system-design-and-scenario-questions.md)；如果你想补项目和源码能力，可以继续看 [AI 智能面试辅助平台 + RAG 知识库](./interview-guide.md)、[《手写 RPC 框架》](./handwritten-rpc-framework.md) 和 [《Java 必读源码系列》](./source-code-reading.md)。

## 适合谁看

- 正在准备 Java 后端校招、社招、中大厂面试的同学。
- 想用系统资料替代碎片化搜索，提高复习效率的读者。
- 需要补齐系统设计、场景题、项目实战和源码阅读能力的后端开发者。
- 希望在 JavaGuide 开源内容之外获得更完整学习路线和资料支持的读者。

## 学习重点

- Java 面试复习要同时覆盖基础知识、项目经验、系统设计、场景题和表达方式。
- 系统设计与场景题重点看问题拆解、容量估算、核心链路、数据一致性和可用性设计。
- 手写 RPC 适合把网络通信、序列化、注册中心、动态代理和服务治理串起来。
- 源码阅读要带着问题看，重点理解框架设计思路和可迁移的工程经验。
- 实战项目要能跑起来、讲清楚、改得动，才真正能转化为面试竞争力。

## 建议阅读顺序

1. [《Java 面试指北》](./java-mian-shi-zhi-bei.md)：先建立 Java 后端面试复习主线。
2. [《后端面试高频系统设计&场景题》](./back-end-interview-high-frequency-system-design-and-scenario-questions.md)：补齐短链、秒杀、海量数据去重、第三方授权登录等高频场景。
3. [AI 智能面试辅助平台 + RAG 知识库](./interview-guide.md)：用完整实战项目补简历亮点和工程经验。
4. [《手写 RPC 框架》](./handwritten-rpc-framework.md)：通过从零实现 RPC 框架理解分布式服务调用。
5. [《Java 必读源码系列》](./source-code-reading.md)：在有基础后阅读 Dubbo、Netty、Spring Boot 等框架源码。

## 核心文章

### 面试资料

- [《Java 面试指北》](./java-mian-shi-zhi-bei.md)：与 JavaGuide 开源版内容互补，面向 Java 后端面试系统复习。
- [《后端面试高频系统设计&场景题》](./back-end-interview-high-frequency-system-design-and-scenario-questions.md)：覆盖短链系统、秒杀系统、海量数据去重、第三方授权登录等高频问题。
- [《Java 必读源码系列》](./source-code-reading.md)：整理 Dubbo 2.6.x、Netty 4.x、Spring Boot 2.1 等框架和中间件源码阅读资料。

### 实战项目

- [AI 智能面试辅助平台 + RAG 知识库](./interview-guide.md)：基于 Spring Boot 4.0、Java 21、Spring AI 2.0 开发，适合作为学习和简历项目。
- [《手写 RPC 框架》](./handwritten-rpc-framework.md)：从零开始基于 Netty、Kryo、ZooKeeper 实现一个简易 RPC 框架。

## 高频问题

- Java 后端面试复习应该先看开源内容，还是先看星球专栏？
- 系统设计题应该怎么拆解，如何避免只背固定答案？
- 手写 RPC 框架适合什么基础的读者学习？
- 源码阅读应该从 Dubbo、Netty、Spring Boot 哪个开始？
- 实战项目写进简历时，如何讲清楚技术难点和个人贡献？
- 星球内容如何和 JavaGuide、项目实战、面试题一起使用？

## 相关专题

- [Java 知识体系](../java/)
- [面试准备](../interview-preparation/)
- [系统设计](../system-design/)
- [分布式系统知识体系](../distributed-system/)
- [Java 开源项目精选](../open-source-project/)
- [高质量技术文章](../high-quality-technical-articles/)

<!-- @include: @planet2.snippet.md -->
