---
author: guide 原创补充
title: Java 后端面试自测：28 题、参考答案与评分
description: 常见面试题自测：按面试提问方式整理Java后端高频问题，提供提示与重要程度标注，适合面试前自测、定位短板、针对性复习。
category: 面试准备
icon: "mdi:clipboard-check-outline"
head:
  - - meta
    - name: keywords
      content: 面试题自测,Java面试题,八股文自测,查缺补漏,面试复习,高频考点,Java后端面试,参考答案
---

> 通过 28 道题、参考答案和评分标准，检查 Java 后端知识的掌握程度。

## 自测方法与评分

每题先独立回答 60–90 秒，再展开参考答案。能背术语但不能解释机制不算掌握。每题 0–2 分，共 56 分：未回答或关键结论错误为 0 分；命中第一个得分点为 1 分；两个得分点都讲清楚为 2 分。这里的分数用于安排复习，不预测面试通过率。

| 分数 | 下一步 |
| --- | --- |
| 0–27 | 先补概念和最小例子，逐题完成指定阅读 |
| 28–41 | 重点追问失败窗口、并发边界和反例 |
| 42–50 | 练习项目化表达与有条件的取舍，避免绝对化结论 |
| 51–56 | 换具体场景继续追问，并用代码、执行计划或测试证明答案 |

可以记录 `题号 / 首次分数 / 错误原因 / 复习证据 / 三天后复测分数`。答错的问题优先复测，不必每次把所有题重新读一遍。

## 1. equals 和 hashCode 必须满足什么关系？

<details>
<summary>参考答案与得分点</summary>

逻辑相等的对象必须有相同的 hashCode；哈希相同不代表对象相等，容器还要进一步比较。重写 equals 时通常也要配套重写 hashCode。作为 HashMap 键参与相等和哈希计算的字段应保持稳定，否则放入后修改字段，查找可能落到不同桶而找不到原对象。

**得分点：** 说明相等与哈希的单向关系得 1 分；说明可变键问题并给出反例得 1 分。

[继续阅读](../java/basis/java-basic-questions-03.md)

</details>

## 2. 为什么通常推荐 String 作为键？StringBuilder 可以共享吗？

<details>
<summary>参考答案与得分点</summary>

String 内容不可变，适合作为稳定键，也易于安全共享；它的变量仍可重新赋值，不可变的是对象内容。StringBuilder 是可变缓冲区，通常用于单线程拼接，多个线程并发读写同一实例需要外部同步。大量拼接要结合循环与编译器处理方式分析，不能把任何加号都判为低效。

**得分点：** 区分引用可变和对象不可变得 1 分；正确说明 StringBuilder 共享边界得 1 分。

[继续阅读](../java/basis/java-basic-questions-02.md)

</details>

## 3. HashMap 怎样处理碰撞？为什么平均 O(1) 不是绝对保证？

<details>
<summary>参考答案与得分点</summary>

HashMap 先根据哈希定位桶，再比较键；碰撞时桶内需要额外查找，某些 JDK 实现会在满足容量等条件后把过长链表树化。均匀散列和适当装载因子使查询平均接近常数时间，但碰撞、扩容和键比较成本都会影响耗时。它不是并发容器，多个线程读写应选择同步方案或 ConcurrentHashMap。

**得分点：** 说明桶内比较与碰撞得 1 分；说明平均复杂度条件及并发边界得 1 分。

[继续阅读](../java/collection/hashmap-source-code.md)

</details>

## 4. ConcurrentHashMap 的 get 后 put 能保证整体原子吗？

<details>
<summary>参考答案与得分点</summary>

不能。每个方法的线程安全不等于多个方法组成的检查再写入是原子的。不存在时初始化可用 putIfAbsent 或 computeIfAbsent；计数等更新可用合适的原子方法。计算函数应简短，不做漫长外部 I/O，也不能假设单个键的原子操作能保证多个键之间的业务约束。

**得分点：** 指出复合操作竞态得 1 分；给出原子 API 并说明多键边界得 1 分。

[继续阅读](../java/collection/concurrent-hash-map-source-code.md)

</details>

## 5. volatile 为什么不能让 count++ 线程安全？

<details>
<summary>参考答案与得分点</summary>

volatile 提供该变量读写的可见性和相应有序性约束，但 count++ 包含读取、加一、写回，多线程可能读到相同旧值后覆盖彼此。可以用 AtomicInteger 的原子更新或同一把锁保护复合操作。若不变量跨越多个字段，单个原子变量也未必足够，通常需要统一同步边界。

**得分点：** 区分可见性和原子性得 1 分；给出适合复合不变量的保护方式得 1 分。

[继续阅读](../java/concurrent/java-concurrent-questions-02.md)

</details>

## 6. synchronized 与 ReentrantLock 怎么选？

<details>
<summary>参考答案与得分点</summary>

两者都可实现互斥和可重入。synchronized 由语言结构负责释放锁；ReentrantLock 支持可中断获取、限时尝试及多个 Condition 等能力，但必须在正确的 try/finally 中释放。不要背诵某一种锁总更快；先看需要的语义，再在实际竞争、临界区长度和 JDK 环境下测量。

**得分点：** 说清自动释放与显式释放得 1 分；说出至少两个语义差异及适用场景得 1 分。

[继续阅读](../java/concurrent/reentrantlock.md)

</details>

## 7. 如何选择线程池大小和队列容量？

<details>
<summary>参考答案与得分点</summary>

先识别 CPU 密集还是等待外部 I/O，并估算吞吐与平均占用时间对应的并发需求，再受 CPU、数据库连接、下游限额和内存约束。队列要有界，容量反映可接受排队时延；任务进队前后都应考虑截止时间，超时任务继续执行可能造成浪费。观察活跃线程、队列等待、任务耗时、拒绝率和下游饱和度再调整。

**得分点：** 把线程数与下游约束关联得 1 分；给出有界队列、截止时间和监控指标得 1 分。

[继续阅读](../java/concurrent/java-thread-pool-best-practices.md)

</details>

## 8. Future.get、取消和异常处理有哪些容易遗漏的点？

<details>
<summary>参考答案与得分点</summary>

Future.get 会等待结果，带超时的 get 只限制调用方等待，不自动停止任务。cancel(true) 是请求中断，任务必须合作响应，不能保证外部请求或副作用被撤回。submit 捕获的任务异常通常通过 Future 暴露，因此不能提交后永久忽略结果；中断异常应按调用契约传播或恢复中断标记。

**得分点：** 说明等待超时与任务停止的区别得 1 分；说明异常与中断处理得 1 分。

[继续阅读](../java/concurrent/java-thread-pool-summary.md)

</details>

## 9. ThreadLocal 为什么会发生数据串用或内存滞留？

<details>
<summary>参考答案与得分点</summary>

线程池会复用线程，ThreadLocal 中的旧请求值若未清理，下一请求可能读到它。ThreadLocalMap 的键是弱引用不代表值立刻消失，长寿命线程可能继续持有值。请求范围数据应在 finally 中 remove；异步任务要显式传递上下文，不能假定普通 ThreadLocal 会自动跨线程。

**得分点：** 解释线程复用和 finally 清理得 1 分；说明值滞留或异步传播边界得 1 分。

[继续阅读](../java/concurrent/threadlocal.md)

</details>

## 10. JVM 怎样判断对象可回收？内存泄漏一定是对象不可达吗？

<details>
<summary>参考答案与得分点</summary>

可达性分析从 GC Roots 沿引用关系遍历，仍可达的对象通常不能回收；具体还需区分强弱引用等语义。Java 内存泄漏常见形式是业务已不用的对象仍被缓存、监听器或线程持有，因此它们对 GC 仍可达。对象互相引用本身不会必然泄漏，只要整个环不再从 Roots 可达。

**得分点：** 正确说明可达性与环得 1 分；用缓存或监听器解释业务泄漏得 1 分。

[继续阅读](../java/jvm/jvm-garbage-collection.md)

</details>

## 11. 接口突然变慢，如何区分 CPU、锁和 I/O 问题？

<details>
<summary>参考答案与得分点</summary>

先根据延迟分位、错误率、流量和发布变更定位时间范围，再看 CPU、线程栈、连接池与下游耗时。CPU 高看热点方法、GC 和重试；CPU 不高但等待多，查锁、数据库、网络和队列。线程快照要多次采样，单次 BLOCKED 或 WAITING 不能直接证明根因。先保留证据，验证一个假设后再变更。

**得分点：** 给出指标到调用链的定位顺序得 1 分；区分等待类型并提出验证动作得 1 分。

[继续阅读](../java/jvm/jdk-monitoring-and-troubleshooting-tools.md)

</details>

## 12. TCP 可靠为什么业务请求还会重复？

<details>
<summary>参考答案与得分点</summary>

TCP 保障连接内字节流的有序传输，不承诺业务操作恰好一次。服务端可能已提交订单，但响应在断线中丢失，客户端重试会发起新的应用请求。业务需要幂等键、唯一约束和结果查询；读取超时也不能直接解释为服务端没执行。

**得分点：** 说明传输语义与业务语义的边界得 1 分；给出提交成功但响应丢失的恢复方案得 1 分。

[继续阅读](../high-availability/idempotency.md)

</details>

## 13. HTTP 缓存里 ETag 与 Cache-Control 分别负责什么？

<details>
<summary>参考答案与得分点</summary>

Cache-Control 描述缓存策略和新鲜度；ETag 是资源表示的验证标识，客户端可通过 If-None-Match 做条件请求。缓存仍新鲜时可能无需访问源站，过期后可验证并得到 304。私有数据要正确设置缓存作用域和 Vary 等规则，不能因为用了 HTTPS 就认为共享缓存不会泄露用户数据。

**得分点：** 区分新鲜度与协商验证得 1 分；说明个性化响应缓存边界得 1 分。

[继续阅读](../cs-basics/network/http-status-codes.md)

</details>

## 14. 联合索引 (a,b,c) 如何帮助查询？哪些说法太绝对？

<details>
<summary>参考答案与得分点</summary>

联合索引按键的顺序组织，常见情况下以前导列等值约束再利用后续列更有效；能否用于过滤、排序或覆盖，还取决于查询、范围条件、优化器和版本。范围条件之后的列未必完全无用，仍可能参与索引条件下推或覆盖。先用 EXPLAIN 看所用键与估算行数，再在可控环境用 EXPLAIN ANALYZE 对比实际行数和耗时；后者会执行语句，也要观察回表成本。

**得分点：** 说明前导列顺序与查询目标得 1 分；避免范围后全失效等绝对化并给出验证方法得 1 分。

[继续阅读](../database/mysql/mysql-index.md)

</details>

## 15. InnoDB 的 RR 与 RC 快照读取有什么区别？

<details>
<summary>参考答案与得分点</summary>

普通一致性读在 RC 下每次读取建立新快照；RR 下通常沿用事务内第一次一致性读建立的快照。锁定读和写操作要读取、锁定相应当前记录，不能简单当作同一历史快照。RR 中范围锁定查询可能使用 next-key 锁防止范围内插入，具体取决于索引和访问条件。

**得分点：** 区分快照建立时机得 1 分；区分普通读、锁定读和索引范围得 1 分。

[继续阅读](../database/mysql/transaction-isolation-level.md)

</details>

## 16. 数据库死锁如何避免和恢复？

<details>
<summary>参考答案与得分点</summary>

死锁是事务形成循环等待。通过固定访问顺序、缩短事务、建立合适索引和减少锁范围来降低概率，但不能承诺彻底消除。数据库选择受害事务回滚后，应用应在明确事务边界重新执行，并采用有限重试和退避；外部副作用不能在事务重试中重复触发。

**得分点：** 解释循环等待与降低手段得 1 分；说明完整事务重试和副作用保护得 1 分。

[继续阅读](../database/mysql/innodb-implementation-of-mvcc.md)

</details>

## 17. 更新数据库后，缓存如何保持一致？

<details>
<summary>参考答案与得分点</summary>

常见 Cache Aside 是写数据库后删除缓存，读取未命中再查库并回填；它通常提供有限窗口的最终一致性。删除失败要有可靠重试或变更事件，并发旧读回填也需要结合版本、失效事件或可接受的 TTL 处理。强一致业务不能只靠延时双删，可能需要绕过缓存读取事实库或更严格的版本协议。

**得分点：** 说明基础流程得 1 分；指出删除失败和旧值回填竞态得 1 分。

[继续阅读](../database/redis/3-commonly-used-cache-read-and-write-strategies.md)

</details>

## 18. 缓存穿透、击穿、雪崩分别是什么？

<details>
<summary>参考答案与得分点</summary>

穿透是持续请求不存在的数据；击穿通常指热点键失效时大量请求同时回源；雪崩是大批键失效或缓存服务故障引起广泛回源。分别可用参数校验与空值缓存、热点互斥重建或逻辑过期、过期时间打散及回源限流。任何方案都要说明旧数据容忍度和缓存不可用时的降级行为。

**得分点：** 准确区分三者得 1 分；给出匹配方案并说明正确性代价得 1 分。

[继续阅读](../database/redis/redis-questions-02.md)

</details>

## 19. Redis 分布式锁加了过期时间就安全吗？

<details>
<summary>参考答案与得分点</summary>

过期避免锁永久遗留，但持锁线程暂停超过 TTL 后，另一线程可能获得锁，旧线程恢复后仍继续写。用随机持有者令牌并原子校验删除，可避免误删新锁；续租也不能完全解决旧执行者问题。对严格资源写入需资源端接受单调 fencing token 或使用数据库条件更新保护，且要说明故障与复制模型。

**得分点：** 说明锁过期后的并发执行风险得 1 分；区分持有者令牌与 fencing token 得 1 分。

[继续阅读](../distributed-system/distributed-lock.md)

</details>

## 20. Redis 的 RDB、AOF 和副本能保证什么？

<details>
<summary>参考答案与得分点</summary>

RDB 是时间点快照；AOF 记录写操作，丢失窗口与刷盘策略、实现和故障有关。副本通常异步追赶，主从切换仍可能丢失已向客户端确认但未复制的写入。备份、持久化和高可用分别解决不同问题，不能因为有三台机器就宣称绝对不丢数据。

**得分点：** 区分快照与写日志得 1 分；说明异步复制和备份边界得 1 分。

[继续阅读](../database/redis/redis-persistence.md)

</details>

## 21. 消息队列怎样处理重复、丢失和顺序？

<details>
<summary>参考答案与得分点</summary>

生产者确认、持久化与复制、消费者处理后确认各负责一段链路；消费者提交业务后确认前崩溃会造成重投，所以用业务唯一键或收件表去重。顺序通常限制在某个分区或业务键，多个消费者并发和重试会改变完成顺序。声称 exactly-once 时必须说明范围，队列事务不自动包含任意外部数据库或支付接口。

**得分点：** 说出提交后确认前的重复窗口得 1 分；说明幂等和顺序的范围得 1 分。

[继续阅读](../high-performance/message-queue/message-queue.md)

</details>

## 22. Spring 的 @Transactional 为什么可能不生效？

<details>
<summary>参考答案与得分点</summary>

常用代理式事务在调用经过代理时建立事务，同对象内自调用通常绕过代理。事务管理器、方法可代理性、异常传播和 rollbackFor 配置都会影响效果；默认回滚规则不能概括为所有异常。新线程不自动继承原事务，异步调用和数据库连接各有边界。排查时检查实际调用路径、事务日志及回滚后的数据库事实。

**得分点：** 解释代理与自调用得 1 分；说明异常或异步边界并给出核验方法得 1 分。

[继续阅读](../system-design/framework/spring/spring-transaction.md)

</details>

## 23. IoC 和 AOP 分别解决什么问题？

<details>
<summary>参考答案与得分点</summary>

IoC 把对象创建和依赖装配交给容器，通过明确接口减少业务对象自行查找依赖；AOP 将事务、监控等横切逻辑织入调用过程。它们不会自动修复循环依赖或不清楚的领域边界。构造器注入让必需依赖显式可见，测试可直接替换依赖；理解代理类型和执行顺序有助于解释 AOP 失效。

**得分点：** 说清创建装配与横切逻辑的区别得 1 分；结合依赖注入或代理边界给例子得 1 分。

[继续阅读](../system-design/framework/spring/ioc-and-aop.md)

</details>

## 24. 库存最后一件，两个请求同时到来怎样保证不超卖？

<details>
<summary>参考答案与得分点</summary>

在事实库用带 available > 0 条件的原子扣减，检查影响行数，并在同一事务里创建订单；用户重复下单再用唯一业务键保护。缓存预扣可以缓冲流量，但其确认、释放和恢复都要有状态机。分布式锁不是唯一办法，也不能替代最终存储约束。

**得分点：** 给出条件更新与事务边界得 1 分；解释幂等和预扣恢复得 1 分。

[继续阅读](../system-design/system-design-questions.md)

</details>

## 25. OAuth、OIDC 和 JWT 是什么关系？

<details>
<summary>参考答案与得分点</summary>

OAuth 2.0 主要解决授权，OpenID Connect 在其上提供身份层，JWT 是一种令牌表示格式。拿到一个 JWT 不等于它可信，必须验证签名、允许算法、issuer、audience、时效及协议要求。访问令牌与 ID Token 用途不同，不能随意互换；第三方登录还要防回调伪造和账号错误绑定。

**得分点：** 区分三个概念得 1 分；列出验证与令牌用途边界得 1 分。

[继续阅读](../system-design/security/basis-of-authority-certification.md)

</details>

## 26. Top K 与去重为什么要先确认精确性？

<details>
<summary>参考答案与得分点</summary>

精确去重不能仅依赖有假阳性的 Bloom Filter；先根据键值域和内存预算选择位图、哈希分区或外部排序。最大 K 个数可以用小顶堆，频次 Top K 需要先按键聚合。分布式随机分片各取频次 Top K 后直接合并可能漏掉全局第一，因此必须说明聚合方式。

**得分点：** 给出 Bloom Filter 边界得 1 分；区分值 Top K、频次 Top K 与分布式聚合得 1 分。

[继续阅读](../system-design/system-design-questions.md)

</details>

## 27. 微服务拆分依据是什么？怎样避免分布式单体？

<details>
<summary>参考答案与得分点</summary>

按业务能力、数据所有权和团队变化边界拆分，而不是一个表一个服务。服务之间建立稳定契约，避免到处跨库写和同步长链调用；将必须一起强一致变更的数据尽量放在合理事务边界内。拆分增加网络失败、观测和发布成本，规模较小时模块化单体可能更合适。

**得分点：** 围绕业务和数据所有权回答得 1 分；说明事务、调用链和运维成本得 1 分。

[继续阅读](../distributed-system/microservices-interview-questions.md)

</details>

## 28. 怎样证明项目优化有效，而不是只是加了 Redis 或线程池？

<details>
<summary>参考答案与得分点</summary>

描述优化前的瓶颈证据、工作负载、指标口径、改动和同条件对比。报告 P95/P99、错误率、资源消耗与吞吐，不只给平均耗时；区分本地压测、预发布和真实生产观察。保留原方案及回滚条件，说明副作用、样本量和未验证范围。未做过的改造可以讲设计推演，不能写成个人生产成果。

**得分点：** 有基线与同条件测量得 1 分；有权衡、回滚和真实证据边界得 1 分。

[继续阅读](./backend-project-interview-guide.md)

</details>

## 一轮追问练习

把第 7、17、21、24 题串成同一个下单系统：线程池队列满怎么办，缓存与订单状态冲突谁为准，消息重投会不会重复扣库存，超时响应又该怎样重试。每个答案都应指出事实存储、原子边界和恢复动作。如果这三个要素在追问中互相矛盾，就回到设计修正。

## 版本与核验资料

以上回答以现代 Java 和常见 InnoDB/Spring 用法为背景，具体实现细节应与项目版本对应。ConcurrentHashMap 的单键并发保证可核对 [JDK 21 API](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/concurrent/ConcurrentHashMap.html)；任务提交、执行与 Future.get 的内存可见性关系见 [ExecutorService API](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/concurrent/ExecutorService.html)；RR/RC 的一致性读和锁定读行为见 [MySQL 8.4 官方说明](https://dev.mysql.com/doc/refman/8.4/en/innodb-transaction-isolation-levels.html)。这些来源用于核对机制与版本差异。
