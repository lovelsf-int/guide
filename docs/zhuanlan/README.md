---
title: 学习专题：面试、系统设计、RPC、源码与 RAG
description: 按主题整理面试训练、系统设计案例、源码阅读、RPC 与 RAG 工程实践。
category: 技术专题
sitemap:
  changefreq: weekly
  priority: 0.9
head:
  - - meta
    - name: keywords
      content: Java面试,后端系统设计,手写RPC框架,Java源码阅读,Java实战项目,RAG,技术专题
author: guide 原创补充
---

## 专题与学习入口

> 按面试准备、系统设计、RPC、源码阅读和 RAG 五个专题整理知识、示例与练习。

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

相关知识可继续阅读 [Kafka](../high-performance/message-queue/kafka-questions-01.md)、[分布式事务](../distributed-system/distributed-transaction.md)、[SQL 优化](../high-performance/sql-optimization.md)和 [RAG 面试](../ai/interview-questions/rag-interview-questions.md)。

## 选择学习顺序

准备近期面试时，从面试训练开始，完成自测后选择最弱的一条技术链路。想补项目经验时，先完成 RPC 或 RAG 的最小可运行闭环，再回头读相应框架源码。想提高系统设计能力时，先独立写出不变量和失败表，再看案例，对比自己的遗漏。

每一轮学习只要求一个可检查成果：一段可以解释的代码、一份故障重现记录或一张有数字来源的容量估算表。未经执行的实验写为待验证；不把教学参数当作生产结果；不把模拟问答当作真实公司面经。这样的记录既能帮助复习，也能成为项目讨论时的依据。

## 使用本专题的验收方式

读完一个专题后合上页面，用自己的例子复述成功路径，再改变一个前提：请求重复、依赖超时、权限撤回、数据增长或进程重启。若只会重复原文结论，继续补对应的机制文章；若能说明约束、状态、代价与验证方法，就进入下一条链路。


## 一次最小练习示例

选择“请求超时后服务端仍完成写入”这个问题，先画客户端、网络和服务端三条时间线，标出客户端放弃等待与数据库提交的先后关系。然后分别对只读查询和发券操作提出恢复方案：前者可以在预算内重查，后者需要幂等键与结果查询。最后到 RPC、系统设计或 RAG 专题中找到对应机制，补一个超时后响应晚到的实验。验收时检查实际副作用和资源清理，不能只看客户端是否收到超时异常。
