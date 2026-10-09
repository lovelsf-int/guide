---
title: 免费完整讲解：专题补全目录
author: guide 原创补充
description: 直接阅读 Redis 集群、Elasticsearch、Netty、Spring Boot、系统设计、面试自测与实战教程，附代码示例、故障分析和自测答案。
category: 学习指南
---

本目录集中列出原来只有付费介绍、外链或简略提纲的学习入口。**本站新增讲解全部可直接阅读**；原有开源文章完整显示。新增正文是 guide 的原创补充，原站商业课程介绍在文末保留，便于区分来源。

## 技术原理与源码

| 主题 | 这次可以学到什么 |
| --- | --- |
| [Redis 集群](../database/redis/redis-cluster.md) | 复制、Sentinel、槽迁移、故障切换、写入丢失边界与订单缓存实例 |
| [Elasticsearch](../database/elasticsearch/elasticsearch-questions-01.md) | 倒排索引、分片副本、查询与过滤、深分页、写入与搜索一致性 |
| [Netty](../system-design/framework/netty.md) | EventLoop、Pipeline、拆包、ByteBuf 引用计数、超时与背压 |
| [Spring Boot 面试题](../system-design/framework/spring/springboot-knowledge-and-questions-summary.md) | 自动配置、配置覆盖、Bean 与测试、启动排障 |
| [Spring Boot 源码](../system-design/framework/spring/springboot-source-code.md) | 从启动入口追到配置导入、容器刷新和条件判断 |
| [PriorityQueue 源码](../java/collection/priorityqueue-source-code.md) | 堆的上浮下沉、复杂度、比较器陷阱与 Top K |
| [设计模式](../system-design/design-pattern.md) | 模式之间的区别、适用约束和代码示例 |

## 场景题与面试训练

- [系统设计完整场景题](../system-design/system-design-questions.md)：先确定业务不变量，再讲数据模型、失败重试、容量和验证。
- [带答案的面试自测](../interview-preparation/self-test-of-common-interview-questions.md)：先自己回答，再按关键点打分和回看知识点。
- [模拟面试与复盘](../interview-preparation/interview-experience.md)：明确标注为训练情境，练习追问、取舍与项目证据表达。
- [Java 后端系统复习](../zhuanlan/java-mian-shi-zhi-bei.md)：把准备、技术题、项目、自测和工作经验连成学习路径。
- [系统设计练习方法](../zhuanlan/back-end-interview-high-frequency-system-design-and-scenario-questions.md)：把一道场景题练成可解释、可验证的方案。

## 实战教程

- [手写 RPC](../zhuanlan/handwritten-rpc-framework.md)：协议、调用关联、服务发现、超时、重试及异常处理。
- [AI 面试平台与 RAG](../zhuanlan/interview-guide.md)：数据流、权限过滤、检索、结构化回答、评测与故障处理。
- [源码阅读方法](../zhuanlan/source-code-reading.md)：带问题追调用链，记录版本，用最小实验验证判断。

## 原先缺失的小节

- [Maven 传递依赖](../tools/maven/maven-core-concepts.md#传递依赖性)：scope、optional、版本调解与依赖树排错。
- [MySQL 日志](../database/mysql/mysql-questions-01.md)：redo、undo、binlog 的职责和恢复边界。
- [SQL 优化](../high-performance/sql-optimization.md)：执行计划、索引、分页和测量方法。
- [数据库压力测试边界](../database/mysql/mysql-high-performance-optimization-specification-recommendations.md#禁止在线上做数据库压力测试)：测试环境、指标、停止条件与演练要求。

## 怎样检查自己真的掌握了

拿一项知识，用自己的话写出：它解决什么问题、什么情况下不适用、失败后会发生什么、如何验证。代码示例先在隔离练习环境运行，再主动制造一个失败场景。本站的示例与训练情境不会被当成真实生产运行或真实面试经历。
