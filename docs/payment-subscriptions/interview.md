---
title: 支付订阅项目 40 道面试题与参考回答
description: 海外游戏 SDK 订阅项目的完整回答、深度追问和易错点
status: reviewing
baseline: StoreKit 2 and App Store Server API V2 and Google subscriptionsv2
last_verified: 2026-10-14
level: P7/P8
source: 海外游戏 SDK 订阅项目面试手册与 Apple Google 官方资料
author: guide 原创补充
category: 支付订阅
tag:
  - Apple IAP
  - Google Play
  - 支付架构
date: 2026-10-14
---

题库按业务建模、Apple、Google、一致性、高并发、跨区容灾和故障复盘分组。先闭卷回答，再核对机制与失败边界。示范回答中的方案不自动代表个人已经落地；职责、容量与收益使用自己的证据。

需要先建立对象关系时，读 [表结构](./data-model.md)；对“后端如何知道用户有没有交易”不清楚时，先读 [恢复购买](./restore-purchases.md)。平台日千万级属于整体支付订单量，不能直接当订阅规模。

## 业务建模与项目表达

### 01 如何在两分钟内介绍海外游戏订阅项目

**参考回答**

这个项目面向海外游戏 SDK，支付平台接入 Apple、Google 等渠道，订阅模块负责首购、自动续费、权益与售后生命周期。我会先讲业务约束：渠道扣款异步发生，客户端可能离线，通知可能重复、延迟或丢失；平台还涉及日本和台湾跨区部署。设计重点是把业务订单、渠道交易、订阅关系和权益拆开，用交易唯一约束、本地事务加 Outbox、下游幂等和主动对账保障结果收敛。面试时再说明我实际负责的模块、一次具体故障以及可验证的改进结果。

**深度追问**

面试官问最难的点是什么。我会选择跨系统不确定结果：渠道已经扣款或 CP 已经发货，但平台没有收到确认。解决关键是保留 UNKNOWN 状态、用稳定业务键查询事实，再决定重试，而不是把超时直接判断为失败。平台日订单千万级属于整体支付规模，介绍订阅时要单列订阅交易量和续费峰值。

**易错点**

把整个支付平台的规模说成订阅模块规模，或只罗列中间件而不解释业务约束。

### 02 普通支付和订阅支付的核心区别是什么

**参考回答**

普通支付主要围绕一次交易的确认、发货和退款；自动续费订阅还需要管理持续关系、每期交易、续费偏好、账单失败及权益期限。商店自动续费时用户不一定打开 App，也没有新的客户端下单请求，因此后端必须能从渠道交易生成当期业务记录。一次性订单解决交易是否成立，订阅解决关系是否持续，权益解决用户此刻能否使用服务。三者状态不能合成一个 PAID 字段。

**深度追问**

如果用户关掉续费，权益是否立刻失效。通常只是下一期不再扣款，本期仍按有效期限提供服务；退款撤销、到期、暂停生效则需要单独处理。取消标志和当前权益要分别存储，才能解释“已取消但仍可用”。具体以渠道当前状态和商品类型为准。[S5](https://developer.apple.com/help/app-store-connect/manage-subscriptions/enable-billing-grace-period-for-auto-renewable-subscriptions)[S8](https://developer.apple.com/app-store/subscriptions/)

**易错点**

把取消续费等同于退款，或认为自动续费必须由平台定时调用扣款。

### 03 你会怎样拆分订单 交易 订阅和权益模型

**参考回答**

订单保存业务购买意图和归属；交易保存渠道实际发生的事实，每期续费独立记账；订阅保存渠道关系、当前计划、续费偏好和归属账户；权益保存可访问能力与生效区间。通知 Inbox 留存原始事件，Outbox 保存待投递动作，发货流水记录 CP 执行结果。交易事实尽量追加，订阅和权益是由事实计算出的投影，这样能重放、纠错和审计。

**深度追问**

一个用户在 iOS 和 Android 都有会员怎么办。我会让权益聚合多个来源 grant，而不是覆盖一个 expiresAt。业务需要明确是并集、取最高等级还是可叠加。撤销某一渠道 grant 后重新计算聚合权益，另一条有效订阅不会被误关。金币礼包等可消费权益另记账，不能直接用会员到期时间代表。

**易错点**

一个 subscription 表同时承担交易账本、用户归属、会员状态和发货结果。

### 04 为什么每期续费要生成新的业务订单或账单

**参考回答**

每期续费是一个新的交易事实，需要独立追踪交易金额、币种、渠道标识、退款和发货。平台从验真的渠道交易生成续费订单或账单记录，并关联已有订阅关系；首购业务订单保留作为购买意图，不能反复修改它代表每一期。模型中允许一笔账单关联多个商品明细；存在零金额试用或计划调整时，也应留痕，不要只用金额大于零判断有效订阅。

**深度追问**

通知重试一百次，会不会生成一百个续费订单。不会依靠“先查再插”保证，而是用渠道交易事实键建立数据库唯一约束，重复插入返回已有记录。Google 的 purchaseToken 用于购买关系，正常续费不能只按 token 去重后全部跳过；每期账务要另识别交易或周期明细。[S6](https://developers.google.com/android-publisher/api-ref/rest/v3/purchases.subscriptionsv2)[S7](https://developer.android.com/google/play/billing/security)

**易错点**

把一个 purchaseToken 当作所有续费交易的唯一键，导致只处理首期。

### 05 订阅状态机是不是只能单向前进

**参考回答**

交易事实可以通过受约束的转换确认支付、退款和撤销；退款也是新的事实，不应把已支付订单重置为未支付。订阅状态天然允许恢复，例如扣款失败进入宽限期，再恢复 ACTIVE，也可能暂停后重新启用。我会把“交易事实不可随意回写”与“订阅状态可合法恢复”分开。每次状态更新保存来源、版本、有效时间和转换原因，不用枚举数字大小判断新旧。

**深度追问**

如何处理旧到期事件晚于恢复事件到达。到达顺序不代表业务顺序。按照渠道事实重新核实关系，结合被影响的交易或计划、事件时间和本地并发版本计算投影。到期定时任务携带预期版本和期限，执行时重新比较，不能让旧任务关掉已经续费的会员。[S5](https://developer.apple.com/help/app-store-connect/manage-subscriptions/enable-billing-grace-period-for-auto-renewable-subscriptions)[S8](https://developer.apple.com/app-store/subscriptions/)

**易错点**

把所有状态编号排序，然后用“只允许数字变大”保证正确性。

### 06 时间 金额和商品配置如何设计

**参考回答**

业务统一存 UTC 时间，显示时转用户时区，渠道时间保留原始精度和来源。权益使用半开区间 startAt ≤ now < endAt；月度续费按商店返回的期限更新，不能统一加三十天。金额使用整数最小货币单位或带精度的十进制，显式保存币种和单位，不能用 double，也不能默认所有币种都有两位小数。业务商品映射到 app、渠道商品、计划及权益配置，历史账单保留当时配置版本。

**深度追问**

渠道返回当前价格能否用于历史对账。不能直接替代历史成交价，因为试用、优惠、调价、税费和汇率都可能不同。对账应使用当笔交易或财务报表的价格口径。配置更新也不能把过去订单的权益规则悄悄改掉；需要版本化，必要时执行可审计迁移。[S6](https://developers.google.com/android-publisher/api-ref/rest/v3/purchases.subscriptionsv2)

**易错点**

expiresAt 加三十天，或把 Google recurringPrice 当作含税历史实付金额。

## Apple 订阅链路

### 07 Apple IAP 的业务订单到底在哪里生成

**参考回答**

业务 orderId 由我们的后端生成，用于记录用户、游戏、角色、商品和购买意图；Apple 的 transactionId 由 App Store 在交易发生后生成。典型首购流程是 SDK 请求后端创建购买意图，后端返回 orderId、商品和账户关联信息，客户端调用 StoreKit，再把签名交易提交后端验真。商店交易与业务订单是两个命名空间，Apple 不会天然知道任意业务 orderId。[S1](https://developer.apple.com/videos/play/wwdc2025/249/)[S2](https://developer.apple.com/documentation/storekit/product/purchaseoption/appaccounttoken%28_:%29)

**深度追问**

如果用户没有客户端预订单就发生购买呢。系统要支持渠道先发生的事实，例如续费或商店外购买。先持久化已验真交易，用已有账户与订阅绑定关联；无法确认归属的交易进入待认领队列，不能随便绑给第一个上传 transactionId 的用户。认领完成后再生成或关联业务账单。

**易错点**

说 Apple 直接帮业务创建 orderId，或强制所有续费必须存在客户端预订单。

### 08 后端如何知道 Apple 交易对应哪个业务 orderId

**参考回答**

首购由客户端带上 orderId 和 signedTransactionInfo，后端验签后校验账户关联、应用、环境、商品和订单归属，再用 transactionId 原子绑定。appAccountToken 是账户关联 UUID，不应当作每笔订单唯一编号；同一用户并发购买时还需校验购买意图。后端通过 transactionId 唯一约束防止同一交易绑定多个订单，用户身份取自登录态，不能相信客户端传入 userId。[S1](https://developer.apple.com/videos/play/wwdc2025/249/)[S2](https://developer.apple.com/documentation/storekit/product/purchaseoption/appaccounttoken%28_:%29)[S3](https://github.com/apple/app-store-server-library-java)

**深度追问**

通知先到但客户端没有上报 orderId 怎么办。先完成验真和交易事实落库，根据 appAccountToken 或已绑定的 originalTransactionId 定位账户，创建待关联交易。多个候选预订单存在时不要猜；可以生成渠道触发账单，之后通过绑定流程关联购买意图。归属可确认不代表首购意图可唯一确定。

**易错点**

只凭相同 productId 匹配订单，或把 appAccountToken 等同于 orderId。

### 09 transactionId originalTransactionId 和 appAccountToken 各负责什么

**参考回答**

transactionId 标识一笔渠道交易，可用于交易事实幂等；originalTransactionId 用于关联自动续费订阅的交易链；appAccountToken 是开发者设置的 UUID，用于关联业务账户。通常维持稳定账户 token，续费时使用已绑定的订阅关系识别账户并生成当期账单。三者分别解决交易、关系和账户问题，业务 orderId 仍由平台维护。[S1](https://developer.apple.com/videos/play/wwdc2025/249/)[S2](https://developer.apple.com/documentation/storekit/product/purchaseoption/appaccounttoken%28_:%29)

**深度追问**

appAccountToken 一定存在吗。不一定，历史交易、未设置 token 或家庭共享等场景需要其他经验证的绑定路径。不能把 originalTransactionId 当作全球业务 userId，也不能在收到新的 token 后无条件改归属。账户迁移须检查既有绑定、登录身份和权益冲突并留审计。更新 token 的服务器接口也不替代归属授权。[S1](https://developer.apple.com/videos/play/wwdc2025/249/)

**易错点**

把 originalTransactionId 当每期交易号，导致续费全部被判重复。

### 10 Apple 回调和客户端交易怎样验真

**参考回答**

Apple V2 通知携带 JWS signedPayload。解码只能读取内容，必须验证签名与证书信任链，并检查 bundleId、environment 等应用边界；生产环境按官方库要求配置 appAppleId 和可信根证书。优先使用官方 App Store Server Library 的 SignedDataVerifier，按需要验证通知与嵌套交易或续费信息。验真后仍校验商品、账户归属、撤销信息和有效区间。[S3](https://github.com/apple/app-store-server-library-java)[S4](https://developer.apple.com/documentation/appstoreservernotifications/signedpayload)

**深度追问**

只验证外层通知够不够。客户端上传的交易是独立入口，需要单独验签；内部服务传递解码事实时需要可信身份和防篡改边界。外层通知验证和嵌套对象处理遵循库的接口契约，不手工假设每个字段都可靠。验签失败不发权益，暂时无法完成校验的请求持久化或返回可重试结果。

**易错点**

Base64 解码后直接相信 payload，或把 Sandbox 交易写入生产权益。

### 11 用户离线时 Apple 自动续费如何处理

**参考回答**

自动续费由商店按订阅规则触发，后端无需也不能代替 StoreKit 去重复下单。收到 DID_RENEW 等通知后验真并记录当期 transactionId，按 originalTransactionId 找订阅与账户，生成本期账单并更新权益。客户端上报、商店通知和主动查询都汇入同一事实处理入口，防止重复开通。通知缺失时使用 App Store Server API 查询订阅状态、交易历史和通知历史做补偿。[S1](https://developer.apple.com/videos/play/wwdc2025/249/)[S8](https://developer.apple.com/app-store/subscriptions/)[S9](https://developer.apple.com/documentation/appstoreserverapi/get-all-subscription-statuses)[S10](https://developer.apple.com/documentation/appstoreserverapi/get-transaction-history)

**深度追问**

补偿查询到当前有效，能否认定所有中间账单都齐了。不能，当前状态只能恢复当前权益；历史交易或财务账务要另外补齐。同步权限与恢复账本是不同目标。补偿有时间窗口、分页游标、失败重试和完成水位，避免“接口查询成功”被当作整条订阅链已经完整。

**易错点**

依赖用户下次打开 App 才续费发货，或仅凭当前 expiresDate 生成全部历史收入。

### 12 Apple 取消续费 退款和宽限期怎样影响权益

**参考回答**

续费偏好变化通常影响下一期，当前有效权益按已确认期限保留。启用 Billing Grace Period 后，账单失败进入符合配置的宽限状态时继续提供对应权益；宽限期结束仍未恢复则收回该来源访问。退款、撤销和家庭共享权限变化按受影响交易或关系处理，重新聚合其他来源权益。Apple 的 billing retry 与 grace period 是不同概念，不能把所有扣款重试都当成可访问状态。[S5](https://developer.apple.com/help/app-store-connect/manage-subscriptions/enable-billing-grace-period-for-auto-renewable-subscriptions)[S8](https://developer.apple.com/app-store/subscriptions/)

**深度追问**

退款一笔旧周期，是否把现在会员全部关掉。不应只看到 REFUND 就修改全局会员。先确认受影响交易、撤销时间、当前关系状态以及是否还有其他有效 grant，再计算访问。对于已消耗的礼包，走独立退款补偿和风控规则，不能只调整会员到期时间。

**易错点**

“关续费立即封会员”“重试期永远有权益”或“任一退款删除用户全部权益”。

## Google Play 订阅链路

### 13 Google purchaseToken 和 orderId 应该怎么使用

**参考回答**

purchaseToken 是购买关系的重要验证与关联标识，服务端用它调用 purchases.subscriptionsv2.get。正常续费可能继续使用相同 token，所以 token 适合防止购买关系重复认领，不适合让所有续费只执行一次。每期财务交易保留渠道订单信息；新模型关注 lineItems 中的 latestSuccessfulOrderId。商品、line item 和周期事实共同参与账单识别，缺少订单号时仍可更新经确认的当前权益。[S6](https://developers.google.com/android-publisher/api-ref/rest/v3/purchases.subscriptionsv2)[S7](https://developer.android.com/google/play/billing/security)

**深度追问**

为什么不直接用 Google orderId 做全部去重。并非所有购买都有 orderId，账户归属与购买验证仍依赖 token。渠道账单去重、通知去重、权益动作去重各自不同。交易号缺失时不能凭空编造收入记录，应保存购买事实和待补齐账务状态，之后通过交易接口或财务对账确认。[S7](https://developer.android.com/google/play/billing/security)

**易错点**

所有记录仅以 orderId 为主键，或相同 purchaseToken 的续费直接返回已处理。

### 14 收到 RTDN 后能否立即按事件类型改会员

**参考回答**

RTDN 是状态变化通知，不包含完成业务判断所需的全部购买信息。接收后验证 Pub/Sub 投递身份和应用范围，持久化 messageId 与原始数据，再用 token 查询 purchases.subscriptionsv2.get。以渠道当前状态和 lineItems 计算权益，并保存通知事实。不能把 RTDN 的事件名称直接映射成“加一个月”，因为到达时关系可能已再次变化。[S6](https://developers.google.com/android-publisher/api-ref/rest/v3/purchases.subscriptionsv2)[S11](https://developer.android.com/google/play/billing/rtdn-reference)

**深度追问**

查渠道 API 超时后是否应对 Pub/Sub ACK。若通知已可靠落库，ACK 表示接收责任已转移，本地任务会重试查询；若连持久化都失败，应按照投递协议让上游重试。业务处理完成与消息已接收分开观察，Inbox 中有 pending、retry、processed 状态，另设积压年龄告警。

**易错点**

收到 SUBSCRIPTION_RENEWED 就直接 expiresAt 加一个月。

### 15 Google acknowledge 和自动续费确认有什么区别

**参考回答**

新订阅购买在验真、资格确认并授予权益后需要及时 acknowledge；普通自动续费不需要每期重复确认。新购买不能漏确认，否则可能自动退款撤销。通常新自动续费购买有三天确认期限，PENDING 购买从转为 PURCHASED 后计算；预付费短周期等商品需遵循各自期限。设计独立确认任务，保留 acknowledgementState、截止时间和重试结果。[S7](https://developer.android.com/google/play/billing/security)[S12](https://developer.android.com/google/play/billing/integrate)[S13](https://developer.android.com/google/play/billing/subscriptions)

**深度追问**

权益已入库但 acknowledge 超时怎么办。保留已授予的权益事实，查询确认状态或幂等重试确认，不盲目重复发放。临近期限提高任务优先级和告警等级；后续若渠道退款撤销，再执行对应撤销补偿。对接 CP 的发货若持续失败，必须有期限内的异常决策流程，不能无限等待。

**易错点**

把 acknowledge 当作扣款动作，或对每期续费都要求新的 acknowledge。

### 16 Google 升降级时如何处理 linkedPurchaseToken

**参考回答**

升级、降级或某些重新订阅会创建新 token，linkedPurchaseToken 提供与旧购买关系的关联。先验真新购买，核对旧关系归属，再把新旧 token 纳入同一业务订阅关系或关系谱系。具体生效时间按 replacement mode 与返回的 item 信息处理。旧 grant 被替换时必须避免同时给两个账户发权益；延迟替换场景则保留到生效时点，不能无条件立刻清空旧权益。[S6](https://developers.google.com/android-publisher/api-ref/rest/v3/purchases.subscriptionsv2)[S7](https://developer.android.com/google/play/billing/security)[S13](https://developer.android.com/google/play/billing/subscriptions)

**深度追问**

所有重新购买都有 linkedPurchaseToken 吗。不保证，过期后的商店外重新订阅可能走新购买，并有其他归属上下文。不要把旧 token 存成唯一链根且强制缺字段就失败。建立 token 别名与谱系表，使用可信 external account identifiers 或规定的认领流程恢复归属，并及时完成新购买确认。[S6](https://developers.google.com/android-publisher/api-ref/rest/v3/purchases.subscriptionsv2)

**易错点**

认为 Google token 永不改变，或新 token 到达后允许另一个用户抢占订阅。

### 17 Google 宽限期 account hold 和暂停有什么区别

**参考回答**

宽限期通常继续提供订阅权益；进入 account hold 后停止该购买来源的访问，恢复付款后再开启。主动取消普通自动续费通常保留到当前有效期限；暂停在其生效区间停止访问，暂停安排和当前已付区间要区分。实现时保留原始 subscriptionState、计划类型和 lineItems，再映射平台权益状态，不把所有非 ACTIVE 状态都当作无权限。[S6](https://developers.google.com/android-publisher/api-ref/rest/v3/purchases.subscriptionsv2)[S13](https://developer.android.com/google/play/billing/subscriptions)

**深度追问**

为什么 expiresAt 没到却不一定有权益。撤销、暂停以及被替换的来源可能使时间判断失效；反过来宽限期也可能需要扩展可访问区间。访问判断要由状态、有效区间、来源有效性共同计算。当前状态查询决定投影，定时任务只是触发检查的手段，不能替代渠道事实。

**易错点**

只判断 expiresAt，忽略 revoked、hold、暂停和多个 line item。

### 18 Google PENDING 购买和重装恢复如何处理

**参考回答**

PENDING 表示交易尚未完成，不能先发永久权益，也不能按成功购买确认。等客户端或 RTDN 提示完成后，由后端查询并验真再授予权益。重装或换设备时客户端查询已有购买，把 token 上传后端；后端验证关系是否仍有效以及归属是否匹配，恢复权益投影。恢复购买是恢复已有事实，不应自动新增一笔付费收入或重复发首购礼包。[S7](https://developer.android.com/google/play/billing/security)[S12](https://developer.android.com/google/play/billing/integrate)

**深度追问**

恢复时登录了另一业务账号怎么办。商店账户与游戏业务账户并非同一个身份域。已有绑定先检查，冲突进入明确的迁移或申诉流程；不能“谁上传 token 就属于谁”。如果允许迁移，要核验双边身份、旧权益处理与冷却规则，保持购买关系唯一有效归属。

**易错点**

把 PENDING 当成功，或恢复购买就重新计收入和首购奖励。

## 幂等与事务一致性

### 19 回调幂等是不是加一个 Redis 锁就够了

**参考回答**

锁只能减少并发冲突，数据库唯一约束才是最终持久化边界。我会分层处理：通知层用 notificationUUID 或 Pub/Sub messageId 去重；交易层用渠道应用环境范围内的交易事实键；发货层用 fulfillmentKey；账户绑定层限制购买关系有效归属。Redis 可做快速重复过滤，但失效后仍必须安全。唯一键冲突后读取已有处理结果，不能直接认为下游已经执行完成。

**深度追问**

消费者拿到锁，执行一半宕机怎么办。锁过期后后继任务能继续读取 Inbox、交易账本与发货流水，根据实际阶段恢复。处理状态包含重试次数、nextRetryAt、执行租约和结果未知标志。只写“已处理”标记再执行，会丢动作；只执行后写标记，则必须靠下游幂等防止重复。

**易错点**

“有分布式锁，所以不需要唯一索引和发货流水”。

### 20 数据库更新成功但 Kafka 消息没发出怎么办

**参考回答**

把交易入账、订阅投影更新和待发动作写入同一个本地事务，Outbox 记录与业务记录一起提交。发布任务通过轮询或 CDC 投递 Kafka，成功后记录投递状态。发送成功但更新状态失败会重复投递，因此消费端仍做业务幂等。Outbox 解决业务写入与发送意图的原子性，不自动提供端到端 exactly once。

**深度追问**

为什么不在事务提交后回调里直接发消息。提交后到发消息之间仍有进程崩溃窗口。可持久化的发送意图才能被其他实例恢复。若权益服务独立部署，支付库只写已确认交易与权益命令；权益服务在自身事务内写 Inbox 和权益，不能声称跨两个数据库属于同一个本地事务。

**易错点**

认为 @Transactional 能覆盖数据库、Kafka、HTTP 发货的完整链路。

### 21 CP 已发货但响应超时 后端如何避免重复发货

**参考回答**

每个发货动作使用稳定 fulfillmentKey，并要求 CP 将幂等记录与实际资产变更放在同一个事务。平台超时后标记 UNKNOWN，用该键查询 CP 执行结果；确认已成功则补写本地成功，确认未执行才重试。如果 CP 支持用同一键重试并返回历史结果，也可直接按协议安全重试。禁止每次重试生成新的业务键。

**深度追问**

CP 不提供幂等和查询怎么办。仅靠平台本地唯一表无法覆盖“CP 已执行但平台不知道”的窗口，不能承诺绝不重复。应协商改造 CP 协议；过渡期保留未知态、停止盲目自动补发，用 CP 流水和人工核验决策。可逆权益支持版本覆盖，但金币等非幂等增量动作必须有业务事务保护。

**易错点**

本地发货表唯一就宣称任意第三方系统都绝不会重复发货。

### 22 回调乱序怎样避免权益回滚

**参考回答**

原始事件追加保存，当前投影按渠道有效事实计算；按订阅键串行化可以降低冲突，但不能修复源头乱序。我会把可访问权益与周期奖励分开：权益设置到渠道确认的有效区间，周期奖励按独立周期动作键一次发放。退款可缩短或撤销区间，所以“总是取最大 expiresAt”也不正确。更新时使用乐观锁或事务行锁，并保留旧事件处理记录。

**深度追问**

两个查询并发，旧响应晚到怎么办。渠道响应未必有统一递增业务版本。按关系使用执行租约序列，提交时要求仍持有当前序列和本地版本；失效响应丢弃或重查。局部串行化并发查询与更新，也可降低窗口。signedDate、eventTime 或收到通知的时间都不能被随意当成覆盖全部语义的全局版本。

**易错点**

认为 Kafka 同分区能解决商店通知乱序，或所有退款也只取 max expiresAt。

### 23 为什么收到回调应该先落库再返回成功

**参考回答**

成功响应表示平台已经可靠接管这条消息，而不是全部业务已经完成。先完成来源校验、必要验真和可靠持久化，再按渠道投递协议返回成功；后续验真补充、查状态、发货和确认由可恢复任务执行。若队列作为接收边界，需要确认可靠写入并有明确保留与恢复策略。数据库落库失败时不能返回成功把重试机会丢掉。

**深度追问**

重复通知还要返回失败吗。已持久化且可以恢复处理的重复通知通常返回协议成功，避免上游持续重试。永久非法请求按接口约定拒绝并记录；可重试校验或存储故障区分处理。重要指标是从接收到权益落地的延迟与未完成消息年龄，不能只看 HTTP 成功率。

**易错点**

回调先返回 200，再用未持久化的线程异步处理。

### 24 主动补偿 对账和死信如何配合

**参考回答**

通知驱动提供实时性，主动补偿覆盖漏消息与未知态，对账验证交易和账务最终结果。近期临界到期、确认待完成、发货 UNKNOWN 等记录优先查询；历史账单按渠道流水和报表补齐。重试使用指数退避与抖动，区分限流、暂时错误和永久错误；死信保留原始输入、失败原因和重放键。人工修复通过同一事实入口，不直接随意改会员表。

**深度追问**

补偿会不会把渠道 API 打满。使用分层时间窗、游标扫描、查询配额和每订阅合并任务。优先级由风险与截止时间决定，热路径与历史回补隔离。补偿记录完成水位，查询失败保留未完成状态；商店 API 查询窗口与财务报表延迟都要考虑，不能假设历史可无限查询。

**易错点**

所有异常无限重试，或死信只有日志没有责任人和可审计重放入口。

## 高并发与服务设计

### 25 你会按照什么原则拆分订阅服务

**参考回答**

按业务不变量和变更边界拆分：渠道适配负责验真与原始事实标准化，订单交易负责记账，订阅负责关系和计划，权益负责可访问能力，履约负责 CP 协议，对账负责修复与财务核对。初期可以模块化单体，让同库事实与投影使用本地事务；独立拆服务后必须显式承担消息延迟和补偿成本。不会为了服务数量把一次原子更新拆成多个远程调用。

**深度追问**

怎样证明拆分有收益。比较发布独立性、团队责任、故障隔离、扩缩容差异与数据所有权。例如渠道查询被限流时，已有权益查询仍应可用；CP 故障只堆积履约任务，不阻塞渠道通知接收。拆分收益要超过分布式一致性和运维复杂度，否则保留模块边界即可。

**易错点**

每个数据库表拆一个微服务，导致主链路同步调用过多。

### 26 多渠道接口怎样抽象 又保留渠道差异

**参考回答**

用适配器加策略注册统一验证入口，但能力分开声明：verifyPurchase、querySubscription、acknowledge、fetchHistory 等操作各有契约。内部标准事实包含 channel、app、environment、relationKey、transactionKey、lineItems、有效期、归属、退款信息和原始引用。渠道差异通过 capability 和扩展对象表达，不能为了统一强制 Apple、Google 都实现同样的扣款接口。

**深度追问**

新增第三个渠道怎样做到少改核心。先验证通用模型能表达关系、交易和权益语义，再实现适配器映射与契约测试。未知枚举保留原值并进入待核验，避免默认为成功。跨渠道编排只消费标准事实，渠道原始数据仍保留，便于审计和未来字段迁移。

**易错点**

大段 switch 分散全项目，或统一 pay 方法掩盖自动续费由商店触发的事实。

### 27 订单和权益接口怎样设计才可靠

**参考回答**

创建购买意图由服务端确定用户、商品、金额口径和目标角色，客户端提供 idempotencyKey；同一键相同请求返回同一结果，不同请求拒绝冲突。确认交易接口提交 orderId 与渠道证明，身份从登录态读取。查询接口返回交易状态、权益版本、生效期限和处理中原因。外部动作采用任务状态查询，超时不代表失败；错误码区分非法、可重试、未知结果和归属冲突。

**深度追问**

为什么权益查询不每次直接查 Apple。渠道配额与网络延迟会让游戏入口依赖外部服务。读取本地已确认权益投影，必要时触发受控刷新；高风险临界状态可执行强校验。客户端只展示购买结果，受保护资源仍由后端根据权益判断，不能靠 SDK 本地 PAID 标志授权。

**易错点**

客户端传任意 userId、金额和商品就创建可信订单。

### 28 续费峰值怎么做容量评估和削峰

**参考回答**

先区分首购、续费、通知重复、状态查询、CP 发货和权益读取。日量只能算平均值，例如每日一千万笔约为 116 笔每秒，并不等于峰值；还要结合新游首发、活动和账单聚集时段。容量按峰值到达率、耗时、重复放大与下游配额估算。通知可靠接收后异步处理，渠道查询与履约分别限流，线程和连接池按下游承载能力设置。

**深度追问**

堆积怎样估恢复时间。若处理能力 μ 大于持续到达率 λ，积压 B 的理想清空时间约为 B ÷ (μ − λ)，还需留重试与尾延迟余量。压测同时检查数据库写放大、消息年龄、P99、确认截止风险和故障恢复，而不是只报告接口吞吐。单实例约 200 QPS 的历史口径需要测量环境与失败率才能外推。

**易错点**

用日订单除全天当设计峰值，或队列无限堆积却没有完成时间目标。

### 29 数据库分片和跨分片唯一性怎样解决

**参考回答**

交易与订阅按稳定归属键路由，避免用户、订阅、账单在每次续费时换分片。channel transaction 或 token 查询可用索引映射定位 owner shard。分片内唯一索引只保护本片；跨分片认领需要唯一登记服务、确定性交易键路由，或先固定交易归属再挂接业务订单。冷热账单与当前关系分开存储，历史分页使用稳定排序键和游标。

**深度追问**

登记成功但目标账单写入失败怎么办。登记记录有 RESERVED、COMMITTED 等状态和可恢复任务，不能永远占用又没有账单。后续请求读取登记归属并继续补写，同一个交易不重新选其他分片。登记服务的单主或一致性约束也必须明确；仅把表拆分之后仍宣称全局唯一是不成立的。

**易错点**

认为所有分片各有唯一索引，就能保证全平台交易号只入账一次。

### 30 Redis 缓存和 Java 虚拟线程怎么用

**参考回答**

权益投影存数据库，Redis 按业务身份缓存版本与期限。事务后通过可靠事件失效或更新缓存，更新使用版本条件防止旧消息覆盖新值；TTL 不跨越可确认的到期边界，撤销传播延迟要有明确上限。Java 虚拟线程适合等待渠道和 CP 网络请求，但不能放大数据库连接或渠道配额；使用信号量、超时预算和独立并发舱控制每类下游。

**深度追问**

缓存删除与并发旧读竞争怎么办。失效事件携带版本，写回缓存要求不低于撤销水位，水位保留足够覆盖旧请求；或直接采用版本覆盖更新。普通 Cache Aside 加 TTL 只能提供有界陈旧，不能保证立即撤销。虚拟线程能提高等待并发，但数据库池仍可能成为瓶颈；锁固定 carrier 的行为还需按 JDK 版本分析。

**易错点**

把 Redis 当权益唯一真相，或认为虚拟线程无需限流即可解决高并发。

## 双活 容灾与生产治理

### 31 日本和台湾双活如何保证同一订阅不会双写

**参考回答**

站点双活可以同时服务不同归属的用户，但同一订阅关系需要明确唯一写入归属。我会按 tenant 或 subscription owner 路由本地主写，异地备份；状态变更、认领和发货命令遵循同一归属。跨区故障切换先阻止旧主继续写，再提升新主和切路由。DNS 或负载均衡切换只改变入口，不能单独解决旧实例与后台任务继续执行的问题。

**深度追问**

分区期间两边都能服务是否更好。读取可以按陈旧预算服务，新增写入与发货需要满足唯一 owner 条件。无法证实旧主已隔离时，优先暂停高风险增量发货，而不是允许两边各自成功。所谓双活必须说明是不同实体分别主写，还是同一实体多主；后者的冲突代价远高于普通路由切换。

**易错点**

“两边库都有唯一索引，所以网络分区也不可能重复”。

### 32 fencing epoch 怎样真正挡住旧主

**参考回答**

epoch 是写入任期标识，由可信控制平面分配，任务和写请求携带任期。存储写入、Outbox 消费、履约入口等真正产生副作用的边界校验当前 owner 与 epoch，旧任期拒绝执行。仅在业务代码里先查 Redis epoch 再写库存在竞争窗口，需要把校验与写入原子关联，或先通过基础设施隔离旧库写权限及旧实例出口。

**深度追问**

CP 不支持 epoch，旧主已经有 HTTP 请求在途怎么办。fencing 不能撤回已飞出的请求。CP 必须使用跨区相同 fulfillmentKey 做幂等，或切换时等待在途排空并核验未知结果。检查和发送也非一个跨系统事务；因此任期隔离与终点幂等互补，不能只靠入口增加 epoch 就承诺没有重复副作用。

**易错点**

把 epoch 写到日志里，却不让数据库或 CP 在执行边界检查。

### 33 日本提交成功 发货成功 但数据没复制到台湾怎么办

**参考回答**

这个场景意味着异步复制存在非零 RPO，新主可能不知道已经发生的支付处理和 CP 副作用。切换后不能看到“台湾没有记录”就补发。先从渠道验真恢复交易，再用同一 fulfillmentKey 查询 CP；确认成功后补账，结果未知时暂停自动发货并核验。渠道可以恢复扣款事实，但不能凭扣款证明恢复 CP 是否已发货这个事实。

**深度追问**

能否做到 RPO 为零。关键交易若使用同步跨区提交或一致性存储，可降低提交记录丢失窗口，但增加写延迟并在分区时影响可用性；外部 CP 的结果仍需幂等与查询。面试要明确复制确认点、持久化副本和外部执行协议，不能用“多副本”笼统保证所有副作用零丢失。

**易错点**

只查新主数据库不存在，就认为渠道与 CP 都没有执行。

### 34 灾备切换和回切的流程是什么

**参考回答**

切换先确认影响范围和数据水位，冻结高风险动作，隔离旧主及旧任务，获取新任期；然后恢复待处理 Inbox、Outbox 与未知发货，开放新主写入并切路由，最后用对账和抽样验证业务结果。回切先追平数据并核对冲突、未知动作和归属映射，再按受控切换执行。切换状态与路由配置版本化，避免两个操作员各自启动不同流程。

**深度追问**

自动故障切换为什么容易出问题。健康检查只能判断服务可达，不能证明旧主停止写入。自动化必须具备可信任期、隔离能力和副作用幂等；无法满足时设置人工判断步骤。演练记录 RTO 从业务不可用到恢复的时间，RPO 按实际丢失提交记录衡量，并另外记录重复与未知履约数量。

**易错点**

只说“改 DNS 即可”，或回切前不核查旧主独有交易。

### 35 订阅平台应该监控哪些技术和业务指标

**参考回答**

技术指标看通知接收成功率、验真失败、渠道查询 P95/P99、限流、Inbox 与 Outbox 最老消息年龄、发货 UNKNOWN 数及确认待完成风险。业务指标看首购成功、续费成功、权益落地时延、重复发货、扣款但无权益、退款后权益未撤销，以及不同渠道与地区的偏差。支付成功率要说明分母和观察窗口，不能把用户取消与系统失败混为一类。

**深度追问**

为什么不能只看 MQ lag。大量通知被快速消费却全部卡在 CP 发货，lag 很低但用户仍拿不到权益。需要分阶段待办数量与最老年龄，关联 orderId、relationKey、transactionId、fulfillmentKey 和 traceId。指标不以原始 userId 或交易号做标签，避免高基数；详细定位放审计日志与业务检索。

**易错点**

HTTP 200 和消费者无积压就判定业务正常。

### 36 退款 风控和账户归属怎样治理

**参考回答**

后端不信任客户端购买证明之外的业务归属声明，校验应用、环境、商品、账户映射以及既有 token 或订阅链绑定。原始凭证加密保留、日志脱敏，商店密钥在服务端管理并支持轮换。退款或拒付记录独立事实与受影响 grant；金币回收、负余额或限制行为需要明确产品规则，技术上通过账本补偿，不能删除历史充值记录。[S7](https://developer.android.com/google/play/billing/security)

**深度追问**

账号合并或转区能否直接改 userId。不能只改一张表。需要迁移购买关系、权益 grant、角色映射、未完成发货和索引定位，保留原账户审计，并防止两边同时授予权益。商店账户身份与游戏账号不同，证明交易合法仍不足以证明当前登录用户拥有这笔交易。

**易错点**

把 transactionId 或 token 当登录凭证，允许任意用户认领。

## 场景题与面试复盘

### 37 用户扣款成功但没有会员 你怎么排查

**参考回答**

先固定用户、app、环境、商品、角色与渠道交易标识，从商店查询确认扣款和当前权益状态。沿交易绑定、Inbox、订阅投影、Outbox、CP 发货与缓存逐段检查，区分没有接收到事实、归属错误、权益处理失败和读到旧缓存。若 CP 响应未知，先查结果。修复用相同交易键重新执行可恢复流程，并记录补偿来源，不能直接加一个月绕过账本。

**深度追问**

面试官追问你先做什么。我会先确认渠道事实与目标身份，再看分阶段未完成记录；避免根据客户端成功截图立即补发。若是系统性事故，先限制错误路径和扩大人工核验，再跑按风险优先的补偿任务。最后通过同交易多入口重放、查询权益和 CP 流水证明没有重复。

**易错点**

先改会员表救火，却没有保留交易、归属和补偿原因。

### 38 旧到期通知晚到 导致新续费会员被关闭 怎么修复

**参考回答**

止血时先阻断旧到期消息直接覆盖投影的路径，保留原始事件；查询渠道当前关系和最近交易，以验真事实恢复有效 grant。排查是否按通知到达时间覆盖、是否存在旧查询晚写入、旧定时任务缺少版本条件或退款逻辑扩大范围。修复采用订阅级并发控制、事实重算、版本条件更新及可重放审计，不仅增加一个时间戳比较。

**深度追问**

如何验证修复有效。构造续费成功后旧 EXPIRED 晚到、两个查询反序完成、退款后旧 RENEW 重放、旧定时任务到期等序列。断言最终投影符合当前渠道事实，周期奖励次数仍为一；模拟消费者在本地提交前后崩溃，证明重放可收敛。结果检查包括权益正确性与账单完整性。

**易错点**

只测试重复同一通知，不测试不同语义事件的反序到达。

### 39 你如何讲清一次实际故障的价值和反思

**参考回答**

我会按背景、目标、判断、行动、结果、反思讲述。背景交代渠道、峰值窗口和用户影响；目标说明先恢复哪些用户及可接受风险；判断用交易事实和链路证据排除错误假设；行动解释为何采用幂等补偿或切换隔离；结果用时间窗口内的成功率、权益时延、未知动作和工单变化证明；反思给出复现方式与机制改进。所有数字必须来自事故记录或压测。

**深度追问**

面试官问这是你做的还是团队做的。我会明确我的职责、亲自做的决策、依赖哪些同事及落地范围。若实际系统没有某机制，我先讲现网方案和局限，再说后续改进，避免把参考架构当已完成经历。P8 深度还要解释成本、组织边界和是否可复用于其他渠道。

**易错点**

虚构“零故障”“百分之百成功”，或把团队所有成果都说成个人贡献。

### 40 怎样证明系统真的可靠而不是只会画架构图

**参考回答**

验证应覆盖三条不变量：同一渠道购买关系不能被两个账户同时拥有，同一履约动作不能重复增加资产，最终权益由已验证且未撤销的有效事实计算。测试覆盖重复、乱序、消息丢失、过期任务、API 超时、确认失败、事务前后崩溃、跨区复制延迟与旧主在途请求。压测还要验证下游配额、P99、消息最老年龄和积压恢复时间；生产通过对账与事故演练持续证明。

**深度追问**

端到端 exactly once 能承诺吗。只在明确的事务边界和执行协议内谈一次业务效果。跨商店、平台和 CP 使用至少一次投递、持久化事实、终点幂等和查询补偿；第三方不支持这些能力时，标明 UNKNOWN 与人工核验边界。可靠性结论必须附验证范围、失败模型和剩余窗口。

**易错点**

用 Kafka exactly once 或 Redis 锁替代所有外部副作用的正确性证明。

## 官方资料索引

### S1 Apple WWDC25 服务端购买 API 与交易标识

[Apple WWDC25 服务端购买 API 与交易标识](https://developer.apple.com/videos/play/wwdc2025/249/)

### S2 StoreKit appAccountToken 购买选项

[StoreKit appAccountToken 购买选项](https://developer.apple.com/documentation/storekit/product/purchaseoption/appaccounttoken%28_:%29)

### S3 Apple 官方 Java 服务端库及验签示例

[Apple 官方 Java 服务端库及验签示例](https://github.com/apple/app-store-server-library-java)

### S4 Apple V2 signedPayload 与 JWS 格式

[Apple V2 signedPayload 与 JWS 格式](https://developer.apple.com/documentation/appstoreservernotifications/signedpayload)

### S5 Apple Billing Grace Period 配置

[Apple Billing Grace Period 配置](https://developer.apple.com/help/app-store-connect/manage-subscriptions/enable-billing-grace-period-for-auto-renewable-subscriptions)

### S6 Google SubscriptionPurchaseV2 字段参考

[Google SubscriptionPurchaseV2 字段参考](https://developers.google.com/android-publisher/api-ref/rest/v3/purchases.subscriptionsv2)

### S7 Google Play 购买验真与防滥用

[Google Play 购买验真与防滥用](https://developer.android.com/google/play/billing/security)

### S8 Apple 自动续费订阅与状态查询说明

[Apple 自动续费订阅与状态查询说明](https://developer.apple.com/app-store/subscriptions/)

### S9 Apple 查询全部订阅状态

[Apple 查询全部订阅状态](https://developer.apple.com/documentation/appstoreserverapi/get-all-subscription-statuses)

### S10 Apple 交易历史与通知历史恢复

[Apple 交易历史与通知历史恢复](https://developer.apple.com/documentation/appstoreserverapi/get-transaction-history)

### S11 Google RTDN 通知参考

[Google RTDN 通知参考](https://developer.android.com/google/play/billing/rtdn-reference)

### S12 Google Billing 购买处理与确认

[Google Billing 购买处理与确认](https://developer.android.com/google/play/billing/integrate)

### S13 Google 订阅生命周期与计划替换

[Google 订阅生命周期与计划替换](https://developer.android.com/google/play/billing/subscriptions)

Google 完整状态转换另见 [Subscription lifecycle](https://developer.android.com/google/play/billing/lifecycle/subscriptions)，Apple 漏通知回补另见 [Get Notification History](https://developer.apple.com/documentation/appstoreserverapi/get-notification-history)。
