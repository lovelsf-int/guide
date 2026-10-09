---
title: AI 面试与 RAG 项目工程实践
description: RAG 工程实践，覆盖文档版本、异步任务、授权检索、引用、结构化评分、SSE 状态和离线评测。
category: 技术专题
star: 5
head:
  - - meta
    - name: keywords
      content: Spring AI实战,Spring AI项目,Spring Boot AI,RAG知识库,AI面试平台,大模型实战项目,Agent实战项目,大模型项目,Agent项目,AI应用开发实战,Spring Boot 4,AI模拟面试,RAG实战,Java AI项目,大模型落地项目,AI简历项目,Spring AI 2.0
author: guide 原创补充
---

## 把 RAG 面试项目做成可解释的工程闭环

> 梳理 AI 面试与 RAG 项目的文档处理、授权检索、引用和评测流程。以下表结构、流程与指标均为教学示例。

一个可用于面试讨论的 AI 项目，除了“能问答”，还应解释文档如何进入系统、谁有权检索、答案依据在哪里、任务失败如何恢复，以及改动后效果是否变好。先把这些问题连接起来，再决定使用哪个模型和框架，可以避免项目只剩一层聊天接口。

## 用一条最小业务链限定范围

教学版本只需要四个能力：用户上传一份自己的文档；系统解析并建立可查询的索引；用户在指定知识库中提问并看到引用；系统从授权材料生成一道面试题，按预先确定的评分维度给出练习反馈。语音、复杂 Agent 和多模型自动路由可以后加。

定义清晰的数据流：上传 → 文件校验 → 对象保存 → 文档版本登记 → 异步解析与分块 → 向量化 → 发布索引版本 → 检索 → 生成与引用检查。原始文档与生成内容分开保存，避免模型输出反过来成为未经审核的知识证据。框架接口可以复用 [Spring AI 的 RAG 能力](https://docs.spring.io/spring-ai/reference/api/retrieval-augmented-generation.html)，但访问权限与业务状态仍由应用负责。

## 数据模型：身份、版本和来源不能缺席

```text
knowledge_base(id, tenant_id, owner_id, acl_version)
document(id, kb_id, object_key, content_hash, current_version, status)
document_version(id, document_id, parser_version, embedding_model, dimension)
chunk(id, document_version_id, ordinal, page_no, text, embedding)
ingest_job(id, document_version_id, state, attempt, lease_until, error_code)
conversation(id, tenant_id, user_id, kb_id)
answer(id, conversation_id, status, model_id, prompt_version, citations)
question(id, source_version, rubric_version, content, reference_points)
```

同一文件的内容哈希可以帮助去重，但不能跨租户直接泄露“这个文件已被别人上传”。文档版本记录解析器、分块策略与向量模型标识，才能解释两次结果为什么不同。维度相同也不代表不同模型的向量可以混用；更换模型应建立新索引版本，完成回归后再切换查询入口。

引用至少携带文档版本、片段 ID 和页码或标题位置。生成结束时重新核对引用 ID 来自本次授权检索集合，不能接受模型凭空生成的来源。显示引用和下载源文件也要重新鉴权，不能因为提问时有权限就永远有效。

## 文档处理：让失败能够被重试

上传入口检查大小、允许类型和实际内容特征，再交给隔离的解析过程；压缩包、损坏文件与复杂嵌套都可能消耗大量资源，解析应有时间和资源预算。清洗应保留标题、页码、表格上下文，过度删除标点或换行会破坏证据。

以下保留 Apache Tika 的最小文本提取调用；示例背景版本为 2.9.2，`inputStream` 由调用方提供，依赖与接口应按实际项目版本核对。这段代码只展示解析入口，完整处理仍需满足上面的文件检查与资源预算。

```java
Tika tika = new Tika();
String content = tika.parseToString(inputStream);
```

分块先按语义结构，再在超长段落中按模型 Token 预算切分；保留有限重叠用于跨边界检索。不要把“每 500 个字符”当作所有语言和文档都适用的常数。对表格可以保存列名和行范围，让独立检索的片段仍可解释。

异步任务以文档版本为单位幂等执行。消费者领取任务时增加执行代次，发布结果时按代次条件更新，防止旧消费者恢复后覆盖新结果。分块、向量写入与索引发布分为准备和发布两步；全部必要片段准备好后才切换可见版本。失败任务记录可读错误码，重试不会产生同一版本的重复片段。相关机制见[文档处理](../ai/rag/rag-document-processing.md)、[知识更新](../ai/rag/rag-knowledge-update.md)与[Redis Stream](../database/redis/redis-stream-mq.md)。

## 检索权限：过滤条件必须来自服务端身份

请求里的 `tenant_id` 和知识库 ID 不是权限证明。服务端先根据登录身份得到可访问范围，再构造检索条件；检索出的文本在进入模型、日志和返回值前再次校验范围。缓存键也要包含租户、知识库、权限版本、索引版本和模型相关信息，避免一个用户命中另一个用户的回答。

下面是简化的 SQL 形态，参数均由受信任的服务端代码绑定。示例只表达版本与知识库范围，真实系统仍需实现用户 ACL 检查或数据库行级安全。

```sql
SELECT c.id, c.text, c.page_no
FROM chunk c
JOIN document_version v ON v.id = c.document_version_id
JOIN document d ON d.id = v.document_id
JOIN knowledge_base k ON k.id = d.kb_id
WHERE k.tenant_id = :authenticated_tenant
  AND k.id = :authorized_kb
  AND v.id = d.current_version
  AND d.status = 'READY'
ORDER BY c.embedding <=> :query_vector
LIMIT :candidate_count;
```

近似向量索引与过滤结合时，可能出现有权限的返回结果不足。pgvector 官方说明了近似索引扫描后过滤以及迭代扫描等机制；应在自己的数据分布上检查召回数量和执行计划，必要时评估分区、索引参数或精确检索，不能为补足 Top K 而放宽授权范围。参见 [pgvector 检索与过滤说明](https://github.com/pgvector/pgvector)。

## 生成和面试评分：把不确定性写进契约

生成 Prompt 分清系统规则、用户问题和检索资料，资料只提供事实，不能改变工具权限或身份。清洗可减少一部分干扰，但不能保证抵御全部 Prompt 注入；关键权限检查必须在模型之外执行。没有足够证据时，明确返回无法从当前资料确认，并允许用户切换到标明性质的一般性解释。

面试题生成保存考点、参考要点、评分维度和来源版本。评分要求模型输出结构化结果后，再用程序校验分数范围、必填字段与引用合法性；解析失败只允许有预算的重试或降级，不能悄悄返回空报告。反馈用于学习，不应把一次模型评分包装成客观招聘结论。可复用[结构化输出](../ai/llm-basis/structured-output-function-calling.md)、[Prompt 工程](../ai/agent/prompt-engineering.md)与[LLM 安全](../ai/system-design/llm-security.md)。

下面沿用 Spring AI 2.0.0 背景下的 `BeanOutputConverter` 调用片段。假定 `chatClient`、提示词和业务 DTO 已定义；它展示格式提示与对象转换，转换之后仍需执行上述业务校验。实际依赖版本与接口需单独核对，片段不是完整可运行工程。

```java
var converter = new BeanOutputConverter<>(ResumeAnalysisDTO.class);
String result = chatClient.prompt()
    .system(systemPrompt)
    .user(userPrompt + converter.getFormat())
    .call()
    .content();
return converter.convert(result);
```

## 流式输出：连接结束不是业务完成

用独立的 `answer_id` 表示一次回答，状态区分 `GENERATING`、`COMPLETED`、`FAILED`、`CANCELLED`。流中发送带序号的事件，例如开始、文本增量、引用、结束与错误；最终状态持久化后再通知客户端完成。浏览器断开时，后端需要按产品规则决定停止生成还是继续保存，不能只捕获一个网络异常便认为任务已取消。

SSE 的事件 ID 和 `Last-Event-ID` 可用于重连游标，事件以空行分隔；这来自 [WHATWG SSE 规范](https://html.spec.whatwg.org/multipage/server-sent-events.html)。但可恢复性仍需应用保存事件或最终结果：没有历史记录，重连头不会自动恢复丢失的文本。教学版本可以只保留最终结果，重连时返回当前状态并在结束后拉取完整内容，清楚说明不提供逐 Token 历史重放。

流式验收至少包含慢客户端、重复连接、中途断线和服务重启。对输出队列设置上限，避免慢客户端积压全部 Token；同时设置空闲超时与心跳策略，并在实际反向代理配置下验证首包和刷新行为。更多传输选择见[Web 实时消息推送](../system-design/web-real-time-message-push.md)。

## 用一个小评测集决定下一步优化

建立 30 条教学查询：10 条单片段可回答、5 条跨片段、5 条无答案、5 条版本冲突、5 条无权限。每条记录允许的证据片段、预期边界和禁止出现的材料。先固定模型、分块和 Top K，运行基线；再一次只改变一个参数，比较正确性、引用准确性、延迟和成本。真实内容和密钥不进入可公开报告。

例如，有答案的 20 条问题中，16 条的前 5 个候选包含至少一条目标证据，那么本例的 Hit@5 为 80%；它不是回答准确率，也不等于所有相关片段的 Recall@5。若还要衡量证据覆盖，必须为每题标注全部相关片段，再计算召回。无权限和无答案查询单独统计，不能让它们被平均分掩盖。

**完成标准**：原文删除或权限撤销后不能继续在缓存答案中泄露；两次重试不会产生重复文档版本；每条答案引用可回到授权原文；断线与模型失败都有明确终态；优化结果有固定数据集的前后对比。先完成这些证据，再扩展语音面试、多模型路由与 Agent 功能。可进一步阅读[RAG 优化](../ai/rag/rag-optimization.md)、[AI 可观测性](../ai/system-design/ai-observability.md)和[RAG 面试问题](../ai/interview-questions/rag-interview-questions.md)。
