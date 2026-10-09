---
author: guide 原创补充
title: 设计模式常见面试题：23 种模式与 Java 实例
description: 设计模式(Design pattern)代表了最佳的实践，通常被有经验的面向对象 的软件开发人员所采用。设计模式是软件开发人员在软件开发过程中面临 的一般问题的解决方案。这些解决方案是众多软件开发人员经过相当⻓的 一段时间的试验和错误总结出来的。
category: 系统设计
icon: "mdi:tools"
head:
  - - meta
    - name: keywords
      content: 设计模式,单例模式,工厂模式,代理模式,责任链模式,策略模式,观察者模式,面试题
---

> 本文由 **guide 项目原创补充**。内容包含 23 种经典设计模式的作用、适用场景与代价，以及 4 个可以独立保存运行的 Java 示例；原站公开介绍保留在文末。

## 设计模式首先解决什么问题

设计模式是对反复出现的协作问题的命名，不是必须凑齐的类图。先找变化点：创建什么对象、组合哪些能力、怎样协调多个对象。如果一个普通方法就能清楚表达需求，不需要为了“用了模式”而增加接口层。

依赖倒置要求高层策略依赖稳定契约；组合优于继承强调按需组合能力，减少对子类继承结构的依赖；开闭原则鼓励让经常变化的部分可以扩展，但不表示任何旧代码永远不能改。判断抽象是否值得做，要看它是否隔离了真实变化、能否独立测试，以及增加了多少理解成本。

## 23 种模式速查

### 创建型：控制对象的产生方式

| 模式 | 核心做法与适用场景 | 代价与边界 |
| --- | --- | --- |
| 单例 Singleton | 在约定作用域只保留一个实例，如一份进程级不可变配置；常用枚举或静态内部类实现 | 作用域通常受类加载器限制，不是分布式唯一；可变状态仍需并发控制，全局依赖不利于测试 |
| 工厂方法 Factory Method | 创建者定义创建接口，由子类决定具体产品；如不同报表工作流创建不同导出器 | 产品和创建者可能成对增长；只有简单分支时，普通工厂函数更易读 |
| 抽象工厂 Abstract Factory | 一次提供兼容的产品族，如同一供应商的支付、退款、查单适配器 | 加产品族较容易，加一种新产品会改动所有工厂；要保证族内契约一致 |
| 建造者 Builder | 分步骤收集参数并在 build 时校验，构造复杂不可变对象 | 必须明确必填字段和跨字段约束；链式 setter 不自动等于合理建造者 |
| 原型 Prototype | 从已有模板复制对象，减少重复初始化或保留初始配置 | 浅拷贝会共享内部可变对象；深拷贝要处理循环引用、资源句柄及复制成本 |

### 结构型：组合接口和对象

| 模式 | 核心做法与适用场景 | 代价与边界 |
| --- | --- | --- |
| 适配器 Adapter | 把旧系统接口转换为调用方需要的接口，如不同短信渠道统一成 send | 还须转换错误、单位和语义；仅改方法名不能解决契约差异 |
| 桥接 Bridge | 抽象维度和实现维度分开组合，如告警级别与发送渠道分别扩展 | 引入额外层；两个维度没有独立变化时可能过度设计 |
| 组合 Composite | 叶子和容器实现同一接口，如目录与文件统一计算大小 | 要禁止非法循环；不是所有叶子都适合暴露添加子节点方法 |
| 装饰器 Decorator | 保持同一接口，包裹对象并增加职责，如压缩、校验、计数 | 包装次序影响语义，层数过多难以追踪，资源关闭责任需明确 |
| 外观 Facade | 给复杂子系统提供较小的入口，如下单门面组织库存、订单、优惠券调用 | 外观不是数据库事务；跨系统一致性仍要单独解决，避免变成巨型类 |
| 享元 Flyweight | 共享大量相同且稳定的内部状态，把用户位置等外部状态由调用方传入 | 共享状态应不可变；缓存回收和身份相等语义需说明 |
| 代理 Proxy | 控制对真实对象的访问，如懒加载、权限检查、远程调用 | 代理不自动改变目标方法语义；远程代理有超时与部分失败，本地调用外观不能掩盖它 |

### 行为型：组织算法、状态和协作

| 模式 | 核心做法与适用场景 | 代价与边界 |
| --- | --- | --- |
| 责任链 Chain of Responsibility | 多个处理节点按顺序决定处理、拒绝或传给下一个，如请求校验链 | 终止条件与顺序必须明确；漏掉 next 或重复调用会丢请求或重复处理 |
| 命令 Command | 把操作封装为带参数的对象，支持排队、日志或撤销 | 撤销需要旧状态或补偿动作；外部副作用并非都有真正逆操作 |
| 解释器 Interpreter | 用语法树解释一个受限语言，如简单业务表达式 | 复杂语法效率和可维护性差；输入不可信时需要资源与能力限制 |
| 迭代器 Iterator | 隐藏集合内部结构，按约定遍历元素 | 必须定义并发修改时的行为；快照、一致视图和弱一致不是同一保证 |
| 中介者 Mediator | 多个对象通过中介协调，如界面组件联动或流程编排 | 减少网状依赖，却可能把复杂性集中到一个“大中介” |
| 备忘录 Memento | 捕获并恢复对象状态，如编辑器撤销快照 | 快照有空间成本，恢复后外部世界可能已变化；不能当跨系统事务回滚 |
| 观察者 Observer | 主题发布状态变化，已订阅对象接收通知 | 需确定同步/异步、异常隔离、顺序和退订；普通内存通知不保证持久交付 |
| 状态 State | 不同状态对象封装不同允许行为，如订单待支付、已支付、已关闭 | 状态迁移要集中约束；多线程/多进程一致性仍依靠原子状态更新 |
| 策略 Strategy | 相同目标用不同可替换算法，如运费、计价或排序规则 | 调用方或配置需要选择策略；算法输入输出契约应一致 |
| 模板方法 Template Method | 父类固定流程骨架，子类实现少数步骤，如导入流程中的解析步骤 | 继承耦合较强；子类不能随意破坏固定步骤和异常处理 |
| 访问者 Visitor | 对稳定对象结构增加新操作，如 AST 的类型检查与格式化 | 加新操作方便，加新节点会修改多个访问者，需评估哪一维更常变 |

## 1. 策略：把计价规则与调用流程分开

下面用“分”保存金额，普通用户原价，会员按九折向下取整，满减券减 500 分且不为负数。舍入是明确的示例规则；实际支付需按合同约定确定。

将代码保存为 `StrategyDemo.java`，可用 JDK 17 或以上版本运行。

```java
import java.util.Map;

public class StrategyDemo {
    interface PriceStrategy {
        long price(long originalCents);
    }

    static final Map<String, PriceStrategy> STRATEGIES = Map.of(
        "normal", cents -> cents,
        "member", cents -> Math.multiplyExact(cents, 9) / 10,
        "coupon", cents -> Math.max(0, cents - 500)
    );

    static long calculate(String type, long cents) {
        if (cents < 0) throw new IllegalArgumentException("negative amount");
        PriceStrategy strategy = STRATEGIES.get(type);
        if (strategy == null) throw new IllegalArgumentException("unknown strategy");
        return strategy.price(cents);
    }

    public static void main(String[] args) {
        if (calculate("normal", 1000) != 1000) throw new AssertionError();
        if (calculate("member", 1000) != 900) throw new AssertionError();
        if (calculate("coupon", 300) != 0) throw new AssertionError();
        System.out.println("strategy: OK");
    }
}
```

**为什么用策略：** 计算流程不需要知道每条规则内部怎么做，新增稳定规则可以单独实现并测试。策略选择仍可能需要一个分支或映射，不必为了“消灭所有 if”再引入复杂注册体系。对于无状态的单方法算法，Lambda 已能表达策略，JDK 的 [Function](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/function/Function.html)就是可组合函数接口。

**验证与代价：** 覆盖零值、负值、未知策略、舍入与溢出。示例中的 `multiplyExact` 对过大金额拒绝计算，避免静默溢出。策略若保存可变请求数据，共享实例会产生线程安全问题；无状态策略更容易复用。

## 2. 工厂方法：让子类选择产品

工厂方法的重点是“创建操作可由子类改变”，不是方法名叫 `create`。这里父类固定验证及导出过程，具体创建者选择文本导出器或 HTML 导出器。

```java
public class FactoryMethodDemo {
    interface Exporter {
        String export(String text);
    }

    static abstract class ExportJob {
        protected abstract Exporter createExporter();

        final String run(String text) {
            if (text == null) throw new IllegalArgumentException("text required");
            return createExporter().export(text);
        }
    }

    static class TextJob extends ExportJob {
        protected Exporter createExporter() {
            return text -> text;
        }
    }

    static class HtmlJob extends ExportJob {
        protected Exporter createExporter() {
            return text -> "<p>" + text.replace("&", "&amp;")
                .replace("<", "&lt;").replace(">", "&gt;") + "</p>";
        }
    }

    public static void main(String[] args) {
        if (!new TextJob().run("guide").equals("guide")) throw new AssertionError();
        if (!new HtmlJob().run("<guide>").equals("<p>&lt;guide&gt;</p>")) {
            throw new AssertionError();
        }
        System.out.println("factory method: OK");
    }
}
```

保存为 `FactoryMethodDemo.java`。例子的 HTML 转义仅针对元素文本，不用于属性、URL 或脚本上下文。实际导出需明确编码及资源释放契约。

**与其他工厂的区别：** 简单工厂是在一个函数中选择产品；工厂方法把选择交给子类；抽象工厂提供一组相关产品。示例也含固定流程的模板方法 `run`，一个设计可以同时体现多个模式。若只需要创建对象、不需要扩展工作流，注入 `Supplier<Exporter>` 可能比增加两层继承更简单。JDK [ServiceLoader](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/ServiceLoader.html)提供运行时服务发现能力，但服务发现与工厂模式不是同一个概念。

## 3. 装饰器：在同一接口上叠加行为

下面把“前缀”和“大写”作为可组合装饰。外层装饰调用内层，再处理结果，所以调整包装顺序会改变输出。

```java
import java.util.Locale;
import java.util.Objects;

public class DecoratorDemo {
    interface TextSource {
        String read();
    }

    static class PlainText implements TextSource {
        private final String value;
        PlainText(String value) { this.value = Objects.requireNonNull(value); }
        public String read() { return value; }
    }

    static class Prefix implements TextSource {
        private final TextSource next;
        private final String prefix;
        Prefix(TextSource next, String prefix) {
            this.next = Objects.requireNonNull(next);
            this.prefix = Objects.requireNonNull(prefix);
        }
        public String read() { return prefix + next.read(); }
    }

    static class UpperCase implements TextSource {
        private final TextSource next;
        UpperCase(TextSource next) { this.next = Objects.requireNonNull(next); }
        public String read() { return next.read().toUpperCase(Locale.ROOT); }
    }

    public static void main(String[] args) {
        TextSource first = new UpperCase(new Prefix(new PlainText("guide"), "id:"));
        TextSource second = new Prefix(new UpperCase(new PlainText("guide")), "id:");
        if (!first.read().equals("ID:GUIDE")) throw new AssertionError();
        if (!second.read().equals("id:GUIDE")) throw new AssertionError();
        System.out.println("decorator: OK");
    }
}
```

保存为 `DecoratorDemo.java`。在真实 I/O 场景，`FilterInputStream` 包裹另一个流并扩展功能，是理解包装协作的直接例子。[JDK 文档](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/io/FilterInputStream.html)

**与代理、适配器的区别：** 装饰器增强职责；代理控制访问；适配器改变接口。它们都可能持有一个委托对象，区分依据是意图。压缩再加密与加密再压缩不同，缓存代理放在权限检查外侧也可能暴露数据，所以组合次序需要显式测试。

## 4. 观察者：发布事件并隔离订阅者

下面是同步、进程内的事件通知，使用写时复制列表让通知过程遍历稳定快照。每个订阅者失败会被收集，其他订阅者仍能执行；调用者负责处理错误。它不具备消息队列的持久化和重试保证。

```java
import java.util.ArrayList;
import java.util.List;
import java.util.Objects;
import java.util.concurrent.CopyOnWriteArrayList;
import java.util.function.Consumer;

public class ObserverDemo {
    static class Events {
        private final CopyOnWriteArrayList<Consumer<String>> listeners =
            new CopyOnWriteArrayList<>();

        Runnable subscribe(Consumer<String> listener) {
            Consumer<String> checked = Objects.requireNonNull(listener);
            listeners.add(checked);
            return () -> listeners.remove(checked);
        }

        List<RuntimeException> publish(String event) {
            List<RuntimeException> errors = new ArrayList<>();
            for (Consumer<String> listener : listeners) {
                try {
                    listener.accept(event);
                } catch (RuntimeException error) {
                    errors.add(error);
                }
            }
            return errors;
        }
    }

    public static void main(String[] args) {
        Events events = new Events();
        List<String> received = new ArrayList<>();
        Runnable unsubscribe = events.subscribe(received::add);
        events.subscribe(event -> { throw new IllegalStateException("demo failure"); });
        if (events.publish("created").size() != 1) throw new AssertionError();
        unsubscribe.run();
        events.publish("closed");
        if (!received.equals(List.of("created"))) throw new AssertionError();
        System.out.println("observer: OK");
    }
}
```

保存为 `ObserverDemo.java`。示例 `main` 单线程运行；若多个线程同时发布，订阅者自己仍需线程安全。退订可能与已经开始的快照遍历并发，因此不承诺取消已经进入本次通知的调用。写时复制适合订阅变更少、通知多的场景，频繁订阅会增加复制成本。[CopyOnWriteArrayList 文档](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/concurrent/CopyOnWriteArrayList.html)

**工程边界：** 订单事务提交后才应发布“订单已创建”；如果消息必须可靠送达，应保存事务内 Outbox，再由消费者幂等处理。直接在事务里异步发通知可能出现事务回滚但通知已发，换成观察者模式并不会自动修复这一点。

## 几组最容易混淆的面试问题

### 策略与状态有什么区别

策略通常由外部根据需求选择一种算法，多个策略共同实现同一个目标；状态对象由当前状态决定允许行为，并伴随状态迁移。例如普通/会员运费是策略，订单待支付/已支付/已关闭是状态。策略一般不负责把上下文转到下一种策略，状态模式通常需要明确转移关系。

### 模板方法与策略如何选择

共同流程稳定、步骤只有少数差异时，模板方法可固定顺序和必要校验；算法组合经常变化或需要运行时切换时，策略更灵活。继承会把子类和父类实现绑定，组合则需要注入与管理策略实例。优先选择能表达当前变化且容易测试的一种，而不是把两者叠满。

### 单例为何不等于线程安全

安全地创建唯一对象，只保证实例发布和数量；对象里的 `ArrayList`、计数器和复合业务操作不会因此自动同步。静态内部类通过类初始化机制延迟创建，枚举方式实现简洁；需要每租户独立实例、测试替身或生命周期管理时，依赖注入容器往往更适合。容器单例也有自己的作用域，不能保证多实例服务只有一个执行者。

### 责任链与装饰器都层层调用，有什么差别

责任链表达请求沿处理序列流转，节点可以中断或移交；装饰器表达一个对象同时拥有多层能力，通常保持接口并调用被包裹对象。HTTP 过滤链中可以同时出现两种意图。解释时给出“谁决定继续、返回值如何组合、失败由谁处理”，比只背类图更有用。

### 命令撤销为什么不等于数据库回滚

本地未提交事务可以回滚；发送短信、第三方扣款等外部效果通常不能原地撤回。命令模式可以记录意图并安排补偿，例如退款，但退款本身又可能失败，需要新的状态和幂等键。备忘录同样只能恢复其负责的状态，不能让外部世界恢复到过去。

## 用一张检查表评估自己的设计

| 检查点 | 可验证的证据 |
| --- | --- |
| 抽象隔离了真实变化吗 | 新增一种业务规则时，核心流程无需复制或散落修改 |
| 接口契约一致吗 | 输入、返回、异常、幂等和资源释放对所有实现都成立 |
| 能测试失败路径吗 | 可注入失败实现，验证异常、超时和恢复行为 |
| 生命周期清楚吗 | 订阅能退订，流能关闭，共享状态有并发策略 |
| 成本值得吗 | 类和跳转层数没有超过变化带来的维护收益 |

结合框架阅读可继续看 [Spring 中的设计模式](./framework/spring/spring-design-patterns-summary.md)。四个示例仅演示模式的协作方式；支付、鉴权或消息系统的生产保证仍需完整的领域约束和故障验证。

---

## 原站公开介绍

以下为迁移时的公开资料入口；前文为 guide 项目独立补充的在线教程。

**设计模式** 相关的面试题已经整理到了 PDF 手册中，你可以在我的公众号“**JavaGuide**”后台回复“**PDF**” 获取。

![JavaGuide 官方公众号](https://oss.javaguide.cn/github/javaguide/gongzhonghaoxuanchuan.png)

**《设计模式》PDF 电子书内容概览**：

![《设计模式》PDF文档概览](https://oss.javaguide.cn/github/javaguide/system-design/design-pattern-pdf.png)

<!-- @include: @article-footer.snippet.md -->
