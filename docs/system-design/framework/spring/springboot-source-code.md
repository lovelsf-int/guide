---
title: Spring Boot 启动与自动配置源码解读
description: Spring Boot核心源码深度解读，涵盖启动流程、自动配置机制、条件注解及SpringApplication源码分析。
category: 框架
tag:
  - Spring
head:
  - - meta
    - name: keywords
      content: Spring Boot源码,启动流程,自动配置源码,SpringApplication,Bean加载,条件注解,源码解读
author: guide 原创补充
date: 2026-10-09
---

::: tip 阅读说明
源码入口固定到 Spring Boot 3.5.0 与 Spring Framework 6.2.7，用于学习常规 JVM 启动流程；AOT 和 Native Image 还有额外路径。
:::

## 一分钟讲清启动过程

**SpringApplication 组织应用启动，ApplicationContext 完成容器刷新，自动配置参与 Bean 定义的发现与注册。** 它们不是三个互不相关的黑盒：启动器先准备环境和上下文，刷新过程中解析配置并创建对象，随后执行启动任务，最后发布就绪信号。

```text
main 调用 SpringApplication.run
  → 准备启动上下文与监听器
  → 准备 Environment
  → 创建并准备 ApplicationContext
  → refresh：解析配置、注册定义、创建 Bean、启动生命周期组件
  → 发布 started 阶段事件
  → 执行 ApplicationRunner / CommandLineRunner
  → 发布 ready 阶段事件
```

面试里应先给出主线，再选一个真实问题向下展开。例如“自定义客户端为什么没创建”对应自动配置和条件；“端口已出现，但流量仍不应进入”对应生命周期与就绪状态。只按顺序背方法名，无法解释这些现象。

## 从 SpringApplication.run 开始，但不要一路盲目单步

先在 `SpringApplication#run(String... args)` 设置断点，观察 `prepareEnvironment`、`createApplicationContext`、`prepareContext` 和 `refreshContext` 的边界。构造阶段会根据类路径推断应用类型，并准备一些初始化器与监听器；run 阶段再组织真正启动。静态便捷方法只是常见入口，不意味着构造与运行是同一阶段。[SpringApplication 3.5.0 源码](https://raw.githubusercontent.com/spring-projects/spring-boot/v3.5.0/spring-boot-project/spring-boot/src/main/java/org/springframework/boot/SpringApplication.java)

每次进入一个阶段，只回答三件事：输入是什么、修改了什么状态、后续哪一步依赖这个结果。比如准备环境阶段输出的是属性来源与 profile 等信息，不是已经创建好的全部业务 Bean；准备上下文阶段把环境、初始化器和源配置组织进去，也不等于所有单例都已实例化。

可以为调试准备三个观察值：最终生效的某个非敏感属性、当前 Bean 定义数量、某个目标 Bean 是否已经创建。不要在断点处随意执行 `getBean()` 作为纯查看动作，因为它可能触发实例化，从而改变原本要观察的执行路径。

## Environment 如何影响后面的配置

环境准备阶段处理属性来源、命令行参数和环境相关扩展。此时就要确定一些启动选择，所以把所有配置都归因于 `@Value` 是错误的：`@Value` 属于后续对象注入的常见方式，而 Boot 在创建很多对象之前已经需要读取配置。

把下面练习应用到已有 Boot 3.5 工程：文件里设置 `guide.demo.mode=file`，启动时传入 `--guide.demo.mode=cli`。在环境准备后的断点查看该属性，预期结果为 `cli`。随后在业务 Bean 中读取它，结果应保持一致。如果不一致，要查是否读取了不同配置对象、命名不一致或存在应用自定义逻辑。

profile 和配置文件位置也在较早阶段生效。因此某些路径参数放在过晚才加载的属性来源里，无法倒过来决定已经完成的配置加载过程。排障时先确定来源链，再判断绑定对象，而不是看到空值就增加一个兜底常量。[外部配置生命周期与优先级](https://docs.spring.io/spring-boot/3.5/reference/features/external-config.html)

## refresh 内部最值得读的几个阶段

`AbstractApplicationContext#refresh()` 是容器生命周期的主干。先准备 BeanFactory，再执行工厂后处理器，注册 Bean 后处理器，完成事件与其他基础设施准备，最后初始化剩余非懒加载单例并完成刷新。[Spring Framework 6.2.7 容器刷新源码](https://raw.githubusercontent.com/spring-projects/spring-framework/v6.2.7/spring-context/src/main/java/org/springframework/context/support/AbstractApplicationContext.java)

| 阶段               | 要观察的内容                            | 常见误解                           |
| ------------------ | --------------------------------------- | ---------------------------------- |
| 工厂后处理         | Bean 定义如何补充或修改，配置类如何解析 | 注册定义等于对象已经创建           |
| Bean 后处理器注册  | 创建对象时有哪些拦截与扩展逻辑          | 后处理器只负责打印日志             |
| 非懒加载单例初始化 | 依赖解析、实例化、初始化回调与代理形成  | 所有 Bean 都在启动时创建           |
| 完成刷新           | 生命周期组件与事件通知                  | 容器刷新结束就等于所有业务预热完成 |

BeanDefinition 可以理解为“如何创建对象的说明”，Bean 实例才是最终对象。理解这层区分后，就更容易看懂为什么条件判断可能基于定义，为什么某些扩展需要较早注册，以及为什么懒加载能把错误延迟到首次访问。

工厂后处理器和对象后处理器也不要混淆。前者主要处理定义与工厂层面，后者参与对象创建的阶段。过早在工厂处理阶段获取业务 Bean，可能导致对象没有经历预期的完整后处理链，造成代理或初始化行为与想象不同。

## 自动配置候选从哪里来

在 Boot 3.5.0，`AutoConfigurationImportSelector` 是重要阅读入口。先查看 `getAutoConfigurationEntry`：读取候选、去重、处理排除并过滤，形成导入结果。再看 `getCandidateConfigurations`，它通过 `ImportCandidates` 加载自动配置候选。不要把候选名单中出现某个类，等同于这个类的全部 Bean 都已经创建。[自动配置选择器 3.5.0 源码](https://raw.githubusercontent.com/spring-projects/spring-boot/v3.5.0/spring-boot-project/spring-boot-autoconfigure/src/main/java/org/springframework/boot/autoconfigure/AutoConfigurationImportSelector.java)

自定义自动配置在 `META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports` 中列出类名。配置类、方法上仍可能有条件；有些条件在解析或注册过程中继续判断。要回答“为什么没生效”，应找候选是否发现、是否排除、类路径是否存在、属性是否满足、已有 Bean 是否使默认配置退让。

建议优先使用条件报告，而不是直接在框架里改返回值。`--debug` 可辅助输出条件评估信息；对大型应用，先按目标自动配置名缩小范围。框架条件是结果，真正的修复经常发生在应用依赖、属性或用户配置里。

## 实战：写一个能退让的自动配置

以下是一个独立教学自动配置类，放在 SDK 的自动配置模块中。它不访问外部系统，便于专注观察条件与创建行为。

```java
package example.guide.autoconfigure;

import org.springframework.boot.autoconfigure.AutoConfiguration;
import org.springframework.boot.autoconfigure.condition.ConditionalOnMissingBean;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.context.annotation.Bean;

@AutoConfiguration
@ConditionalOnProperty(
        prefix = "guide.greeting", name = "enabled",
        havingValue = "true", matchIfMissing = true)
public class GreetingAutoConfiguration {
    public record GreetingClient(String prefix) {
        public String greet(String name) {
            return prefix + ", " + name;
        }
    }

    @Bean
    @ConditionalOnMissingBean(GreetingClient.class)
    public GreetingClient greetingClient() {
        return new GreetingClient("你好");
    }
}
```

在模块资源目录创建登记文件，内容为：

```text
example.guide.autoconfigure.GreetingAutoConfiguration
```

文件完整路径是 `src/main/resources/META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports`。发布后还要确认它确实进入 JAR，不能只看 IDE 里存在文件。使用方引入该模块后，应该在没有自定义客户端且开关允许时获得默认客户端。

至少验证三个情况：没有设置开关时创建一个默认客户端；设置 `guide.greeting.enabled=false` 时不创建；使用方提供同类型 Bean 时保留用户 Bean 且不再创建默认 Bean。这些结果体现自动配置的可预测性。[自定义自动配置与测试建议](https://docs.spring.io/spring-boot/3.5/reference/features/developing-auto-configuration.html)

测试自动配置时可用 `ApplicationContextRunner` 构建小上下文，注入属性并断言 Bean 的数量和内容。还需在真实消费工程里验证 JAR 登记文件能被发现，因为测试中直接指定配置类会跳过候选发现步骤。这样才能区分“类逻辑正确”和“打包接入正确”。

## Started、Runner 与 Ready 的区别

容器刷新完成后，Boot 会进入 started 阶段，然后调用 `ApplicationRunner` 与 `CommandLineRunner`，最后进入 ready 阶段。两类 runner 的参数形式不同：前者使用解析后的 `ApplicationArguments`，后者使用原始字符串参数。[官方应用事件与 Runner 说明](https://docs.spring.io/spring-boot/3.5/reference/features/spring-application.html)

如果 runner 要进行同步的关键预热，它会影响就绪时机；如果 runner 只是发起异步任务后立即返回，Boot 不会自动知道该任务何时真正完成。此时要自己设计 readiness 与失败传播，不能把日志出现“启动成功”理解成后台异步加载已经完成。

同样，Web 服务端的初始化和端口状态属于 Web 上下文及生命周期过程，不应简化成“所有代码执行到 run 的最后一行后才可能监听”。流量调度需要使用合适的就绪信号，避免启动边界上的请求访问尚未准备好的业务资源。

## 常见失败与定位方法

出现创建 Bean 失败时，从最内层原因开始判断：是类缺失、配置无法绑定、依赖歧义、连接失败，还是初始化逻辑异常。最外层的 `BeanCreationException` 只是传播包装，不能据此判断一定是容器实现出错。

启动慢也应分段测量。大量扫描、昂贵初始化、外部连接与 runner 都可能占时间。使用启动指标、记录单项耗时或缩小上下文，比盲目启用懒加载更可靠。懒加载可以降低启动工作量，但会把首次请求延迟与部分配置错误转移到运行阶段，需要结合验收目标选择。

关闭时应让已注册的资源通过容器生命周期释放，线程池、连接池和监听器都有明确所有者。异常启动需要清理已创建资源，不能只处理正常退出。调试时若端口一直被占用，应先确认旧进程或自建线程是否真正结束。

## 自测与参考答案

1. **自动配置候选名单里有客户端配置，但容器没有客户端，先查哪里？** 查排除、类与方法条件、已有 Bean 和条件报告；发现候选只是流程前半段。
2. **为什么测试直接导入配置能通过，打成 SDK 后却不生效？** 测试绕过了自动发现，登记文件路径、内容、打包或依赖引入可能有问题。
3. **Runner 启动异步线程后返回，Ready 是否等待它？** 默认不会。异步业务的完成和错误需要单独纳入就绪与恢复机制。
4. **Bean 定义有 100 个，是否证明已创建 100 个对象？** 不证明。定义与实例分离，懒加载、作用域和 FactoryBean 等机制都会影响实际对象创建。
