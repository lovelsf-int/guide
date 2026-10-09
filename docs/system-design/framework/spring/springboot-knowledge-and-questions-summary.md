---
title: Spring Boot 常见面试题与排障实战
description: SpringBoot核心面试题详解，涵盖自动配置原理、Starter机制、配置文件加载及Actuator监控等核心知识。
category: 框架
tag:
  - Spring
head:
  - - meta
    - name: keywords
      content: Spring Boot面试题,SpringBoot原理,自动配置,Starter,配置文件,Actuator,SpringBoot常见问题
author: guide 原创补充
date: 2026-10-09
---

::: tip 阅读说明
本文由 guide 镜像独立原创补充，不是原站付费正文。以 Spring Boot 3.5、Java 17 及以上的常规 JVM 应用为基线，避免把不同大版本的注册方式、包名和默认配置混在一起。原站公开介绍保留在文末。
:::

## 面试先回答 Spring Boot 帮我们做了什么

**Spring Boot 在 Spring 容器之上提供自动配置、依赖组织、应用启动和运维集成。** Spring 负责对象管理、依赖注入、事务和 AOP 等基础能力，Boot 根据依赖与配置提供常见场景的默认组合。它减少重复配置，但仍需要开发者理解默认值的条件、覆盖方式和生命周期。

自动配置可以概括为“发现候选配置 → 判断条件 → 注册 Bean 定义 → 容器创建对象”。类路径存在某个库，不代表相关配置一定生效；属性、应用类型、现有 Bean 与排除列表都可能改变结果。Boot 允许通过自己的 Bean 或显式排除来调整默认行为，但具体是否退让要看该自动配置的条件。[自动配置官方说明](https://docs.spring.io/spring-boot/reference/using/auto-configuration.html)

## Starter 和自动配置不是同一件事

Starter 主要是方便引入一组兼容依赖的入口，自动配置类才描述满足什么条件时创建哪些 Bean。一个团队 SDK 可以拆成普通 Java 客户端、自动配置模块和 Starter：客户端不依赖 Spring；自动配置把属性转换成客户端对象；Starter 聚合依赖，降低接入成本。

在 Boot 3.5 中，自定义自动配置通常使用 `@AutoConfiguration`，并在 `META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports` 中登记全限定类名。一行一个类。不能照搬旧文章，把 Boot 3.x 自动配置候选注册仍然全部解释成 `spring.factories`；其他扩展点仍可能使用该文件，所以也不能反过来说它已经完全无用。[创建自动配置](https://docs.spring.io/spring-boot/3.5/reference/features/developing-auto-configuration.html)

常见条件包括 `@ConditionalOnClass`、`@ConditionalOnMissingBean` 和 `@ConditionalOnProperty`。前者检查类是否存在，中间者为使用方提供覆盖默认对象的机会，后者控制功能开关。条件判断依赖可见的上下文与解析阶段，自动配置顺序也不能直接等同于 Bean 实例创建顺序。

## 配置为什么没有按预期生效

把配置拆成三个问题：配置从哪里加载、同名值如何覆盖、最终如何绑定到对象。`application.yml` 只是一种来源；环境变量、系统属性、命令行参数、外部文件和 profile 配置都可能参与。排查时应沿来源链确认最终值，而不是不断修改包内文件。

在常规默认配置下，`--server.port=9090` 命令行参数会覆盖文件中的端口配置。profile 决定启用哪些配置，但不能把“生产 profile 已开启”当成密钥、连接地址与监控权限都正确的证明。敏感值应由受控的部署配置提供，日志与排障输出只展示必要信息。[外部配置的来源与优先级](https://docs.spring.io/spring-boot/3.5/reference/features/external-config.html)

一组相关配置优先使用 `@ConfigurationProperties` 表达，便于类型绑定、验证和统一测试。少量单值注入可以使用 `@Value`，但几十个散落的占位符会增加发现拼写错误与默认值不一致的难度。

## 实战：用类型化配置构建一个小服务

下面示例放在已使用 Spring Boot 3.5 的应用中。它只依赖 Boot 核心与 Spring Context，代码可放入一个 `DemoApplication.java` 文件，包名按项目修改。

```java
package example.demo;

import java.time.Duration;
import org.springframework.boot.ApplicationRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.boot.context.properties.EnableConfigurationProperties;
import org.springframework.context.annotation.Bean;

@SpringBootApplication
@EnableConfigurationProperties(DemoApplication.GreetingProperties.class)
public class DemoApplication {
    public static void main(String[] args) {
        SpringApplication.run(DemoApplication.class, args);
    }

    @ConfigurationProperties("guide.greeting")
    public record GreetingProperties(String prefix, Duration timeout) {
        public GreetingProperties {
            if (prefix == null || prefix.isBlank()) {
                throw new IllegalArgumentException("prefix must not be blank");
            }
            if (timeout == null || timeout.isNegative() || timeout.isZero()) {
                throw new IllegalArgumentException("timeout must be positive");
            }
        }
    }

    record GreetingService(GreetingProperties properties) {
        String greet(String name) {
            return properties.prefix() + ", " + name;
        }
    }

    @Bean
    GreetingService greetingService(GreetingProperties properties) {
        return new GreetingService(properties);
    }

    @Bean
    ApplicationRunner demo(GreetingService service) {
        return args -> System.out.println(service.greet("面试学习者"));
    }
}
```

对应 `application.yml`：

```yaml
guide:
  greeting:
    prefix: 你好
    timeout: 2s
```

预期启动后输出“你好, 面试学习者”。加入参数 `--guide.greeting.prefix=欢迎` 后输出应变化。将 timeout 改为负值则应启动失败，而不是让错误配置悄悄进入业务流程。示例 timeout 用于展示类型绑定与校验；实际网络调用必须把它传给客户端才会真正限制调用时间。

这个练习能区分“文件里写了值”“属性对象拿到了值”“业务真正使用了值”三个层次。生产系统常见问题恰恰是第三层：配置看似正确，却没有连到实际客户端或线程池。

## Bean、依赖注入与线程安全

构造器注入可以明确一个对象创建时必须具备的依赖，并方便在普通单元测试中直接实例化。把主应用类放在合理的根包中，有助于组件扫描覆盖业务代码；遇到“找不到 Bean”，应检查包边界、条件、扫描范围与配置类是否被导入。

默认 singleton 表示一个容器里该 Bean 定义通常只有一个共享实例，并不自动保证对象内部状态线程安全。控制器若把当前用户 ID 写到实例字段，多个请求可能相互覆盖。请求相关状态应作为局部变量、参数或经过明确生命周期设计的对象处理。[Spring Bean 作用域](https://docs.spring.io/spring-framework/reference/core/beans/factory-scopes.html)

循环依赖也不应靠“到处加懒加载”掩盖。先判断两个服务是否承担了相互缠绕的职责，能否提取共同依赖或使用事件解耦。若使用懒代理，需要理解它只是延迟解析，并没有修复业务架构中不清晰的依赖方向。

## 事务问题为什么不能归咎于 Boot 注解少写了

在常见代理事务模式下，调用要经过代理才能被事务拦截。同一对象内部直接调用自己的 `@Transactional` 方法，通常不会经过该代理。解决方式可以是把事务边界放在外部服务入口，或拆分到另一个清晰的服务中；不要把注解位置当成事务一定存在的证明。

还要检查异常是否被捕获吞掉、所用事务管理器是否对应目标资源、传播行为是否符合预期，以及异常的回滚规则。数据库事务不会自动回滚已经发送成功的外部 HTTP 请求。订单与通知的一致性更适合用 outbox、补偿或明确的异步交付设计。[声明式事务与代理语义](https://docs.spring.io/spring-framework/reference/data-access/transaction/declarative/annotations.html)

## Actuator 与测试应证明什么

Actuator 可以提供健康、指标、条件报告和配置排查入口。端点存在、允许访问以及通过 HTTP 暴露是不同配置层面。不要为了排查把所有管理端点公开到互联网；配置详情、线程栈和内存转储应有明确的访问边界。[Actuator 端点与暴露规则](https://docs.spring.io/spring-boot/3.5/reference/actuator/endpoints.html)

一个进程健康并不意味着它能承接流量。启动期间需要关键资源预热时，应把“进程存活”和“业务就绪”区分开；依赖短暂故障如何影响 readiness 也要结合流量与恢复机制设计，避免把所有实例同时摘除。

测试可以分层：普通单元测试验证业务计算；配置或切片测试验证绑定、条件和 Web 映射；`@SpringBootTest` 验证组合后的应用上下文。使用模拟 HTTP 环境的测试通过，并不能证明真实端口、反向代理和数据库部署都正确。对关键业务仍需有真实依赖下的集成验证。[Spring Boot 测试指南](https://docs.spring.io/spring-boot/3.5/reference/testing/spring-boot-applications.html)

## 自测与参考答案

1. **引入数据库 Starter 后启动报错，是否说明自动配置坏了？** 先看条件报告和根异常。可能是自动配置成功决定创建数据源，但连接地址、驱动或凭证不满足要求。
2. **自己声明 Bean 后默认 Bean 一定消失吗？** 不一定，要看相应自动配置是否使用缺失 Bean 条件，以及它按什么类型或名称匹配。
3. **默认单例控制器能保存当前请求的用户信息吗？** 不适合放入共享字段，会产生跨请求竞态；使用参数、局部变量或设计清楚的请求作用域。
4. **`@SpringBootTest` 通过能证明线上 API 正常吗？** 只能证明它实际覆盖的条件。模拟环境没有验证真实网络链路，外部依赖被替身替代时也没有验证真实服务行为。

## 原站公开介绍

以下保留原始公开页面的介绍、链接与署名语境，其中“我的”指原作者；上方新增正文由 guide 独立编写。

**Spring Boot** 相关的面试题为我的[知识星球](https://javaguide.cn/about-the-author/zhishixingqiu-two-years.html)（点击链接即可查看详细介绍以及加入方法）专属内容，已经整理到了[《Java 面试指北》](https://javaguide.cn/zhuanlan/java-mian-shi-zhi-bei.html)中。

很多 Spring Boot 重要的新特性都已经同步到了这篇文章中，质量很高，保证内容与时俱进！

![SpringBoot 面试题](https://oss.javaguide.cn/javamianshizhibei/springboot-questions.png)

<!-- @include: @planet.snippet.md -->

<!-- @include: @article-footer.snippet.md -->
