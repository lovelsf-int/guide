---
title: 海外游戏 SDK 支付订阅专题
description: Apple 与 Google 订阅的账户归属、表结构、恢复购买、一致性及项目面试
status: reviewing
baseline: StoreKit 2 and App Store Server API V2 and Google subscriptionsv2
last_verified: 2026-10-14
level: P7/P8
source: 本人项目讨论、支付订阅面试手册与 Apple Google 官方文档
author: guide 原创补充
category: 支付订阅
tag:
  - Apple IAP
  - Google Play
  - 支付架构
date: 2026-10-14
---

面向海外游戏聚合 SDK 的 Apple／Google 订阅场景，主线是：一笔商店交易如何归属到业务用户，如何落成业务订单，如何形成可恢复的订阅与权益，以及通知重复、丢失和跨区故障时怎样收敛。

最重要的模型边界是 **业务订单、渠道交易、订阅关系、权益来源分别保存**。商店不认识平台的任意 `userId`；恢复购买依赖已保存的渠道标识，或客户端找回并经服务端验证的购买凭证。有效交易证明与业务账户归属仍要分别核验。

## 按问题阅读

| 当前问题 | 主读页面 | 读完应能解释 |
|---|---|---|
| 这些对象到底是什么关系 | [表结构与流水关系](./data-model.md) | 一个用户、多条订阅、每期交易和业务订单怎样关联 |
| 怎么知道用户有没有交易 | [恢复购买与交易查询](./restore-purchases.md) | 有本地绑定、无本地绑定、跨账户认领三个分支 |
| 自动续费和取消怎么处理 | [生命周期与事务一致性](./lifecycle-consistency.md) | 商店扣款、平台记账、权益与履约的分工 |
| 漏通知、乱序、双活怎么兜底 | [补偿与跨区可靠性](./reliability.md) | 幂等、UNKNOWN、查询水位和副作用恢复 |
| 怎样讲项目和应对追问 | [40 道面试题与参考回答](./interview.md) | 结论、机制、项目条件和失败边界 |

先读表结构与恢复购买，再进入一致性和故障场景。题库用于闭卷自测，不必把同一知识点重复通读。

## 项目范围与容量口径

| 项目口径 | 已提供的信息 | 面试时的边界 |
|---|---|---|
| 业务场景 | 海外游戏 SDK，接入 Apple、Google 等支付渠道 | 订阅模块覆盖首购、自动续费、权益与售后 |
| 支付平台总订单量 | 日千万级 | 这是整个支付平台口径，不是订阅日订单量 |
| 单实例接口能力 | 创建／回调约 200 QPS | 补充机器配置、接口拆分、P99、错误率与测试窗口后再外推 |
| 查询规模 | 查询总量超过万级 QPS | 明确哪些是订单查单、权益读取和渠道主动查询 |
| 跨区背景 | 日本与台湾部署及容灾 | 同一订阅的主写归属、切换机制和演练指标要据现网说明 |
| 尚需补充 | 订阅独立日量、续费峰值、渠道配额、实际 RTO／RPO | 不用整体支付量或教学参数替代 |

下文 SQL、状态名和失败处理是实现参考；具体已落地范围、个人职责及改进结果，以自己的系统与验证记录为准。

## 两分钟项目表达

这个项目面向海外游戏 SDK。支付平台对接 Apple、Google 等渠道，订阅模块负责首购、自动续费、权益和售后。难点在于商店扣款是异步的，用户可能离线，通知可能重复、延迟或丢失，平台还需要处理日本和台湾之间的故障切换。

我会把购买意图、渠道交易、订阅关系和权益分开：每期交易使用渠道事实键入账，订阅关系绑定业务账户，权益根据已验证事实计算。客户端上报、渠道通知与主动补偿汇入同一处理入口，通过唯一约束、本地事务、Outbox 和下游幂等保证恢复时不重复发放。结果未知时先查询，不把超时直接当失败。

最后补上自己真正负责的模块、一个具体失败窗口和可验证结果。讲容量时，明确日千万级属于整个支付平台，订阅续费量和峰值另列。

## 商店订阅与通用协议代扣的区别

Apple／Google 自动续费由商店触发扣款。平台负责接收和查询事实、生成本期账单、发放权益及补偿，不通过自己的到期扫描任务再次向商店发起自动续费扣款。

原有 [DDD 订阅案例](https://lovelsf-int.github.io/backend-ai-interview-handbook-zh-cn/finance-payment-ddd/subscription-case/01-bounded-contexts.html) 保留领域划分与聚合建模；[续费调度](https://lovelsf-int.github.io/backend-ai-interview-handbook-zh-cn/finance-payment-ddd/subscription-case/07-renewal-scheduling.html) 中的“调用协议扣款”适用于平台持有相应代扣能力的渠道。不要把这条调用链直接套到 StoreKit／Play Billing 自动续费。

## 关联资料

- [支付与 DDD 基础](https://lovelsf-int.github.io/backend-ai-interview-handbook-zh-cn/finance-payment-ddd/)：聚合、账务、Outbox 和支付不变量。
- [海外游戏支付项目](https://lovelsf-int.github.io/backend-ai-interview-handbook-zh-cn/system-design/overseas-payment.html)：更广的支付接入与项目背景。
- [全球订阅与跨区容灾](https://lovelsf-int.github.io/backend-ai-interview-handbook-zh-cn/system-design/global-subscription.html)：跨区部署与故障切换的扩展设计。
- [本站专题复习目录](../reading/)：按知识点、项目与自测组织复习。
- [项目案例与证据卡](https://lovelsf-int.github.io/backend-ai-interview-handbook-zh-cn/guide/projects.html)：个人职责、业务约束与证据卡。
