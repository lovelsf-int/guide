---
title: 后端复习清单
author: guide 原创补充
description: Java 后端核心知识与场景练习的复习清单。
category: 面试准备
---

按“能解释、能举例、能验证”三个层次检查掌握程度。每次只选择一到两个模块复习。

## 核心知识

- [Java 基础](../java/basis/java-basic-questions-01.md)：对象、类型、异常与语言机制。
- [集合](../java/collection/java-collection-questions-01.md)：数据结构、复杂度与并发边界。
- [并发](../java/concurrent/java-concurrent-questions-01.md)：线程、锁、线程池与内存可见性。
- [JVM](../java/jvm/README.md)：内存、垃圾回收、类加载与排障。
- [MySQL](../database/mysql/mysql-questions-01.md)：索引、事务、锁与查询优化。
- [Redis](../database/redis/redis-questions-01.md)：数据结构、缓存、一致性与故障恢复。
- [Spring](../system-design/framework/spring/README.md)：容器、事务、自动配置与源码。

## 场景与验证

先独立完成[系统设计场景题](../system-design/system-design-questions.md)，再用[28 题自测](./self-test-of-common-interview-questions.md)定位遗漏。项目复盘记录实际需求、职责、关键决策、失败过程和验证结果。

## 复习记录模板

| 主题 | 当前能解释的内容 | 仍不清楚的问题 | 验证方式 | 下次复测 |
| --- | --- | --- | --- | --- |
| 例：缓存一致性 | 更新与失效的常见流程 | 并发回填的窗口 | 画时序图并构造并发例子 | 自定日期 |
