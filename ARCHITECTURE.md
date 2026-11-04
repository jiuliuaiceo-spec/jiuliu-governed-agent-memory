# Governed Agent Memory：架构与功能介绍

## 定位

Governed Agent Memory 是一个面向多 Agent 系统的记忆与知识治理层。它不替代模型、任务系统或企业知识库，而是在它们之间提供可追溯的上下文绑定、权限边界、候选经验治理和运行证据。

## 架构

```text
Agent
  │
  ▼
Governed Connector
  ├─ Identity / scope checks
  ├─ Context binding
  ├─ Hindsight adapter (memory)
  ├─ Read-only RAG adapter (knowledge)
  ├─ Candidate governance (self-growth)
  └─ Audit evidence
```

## 一次受治理运行

```text
register → recall → cognition → planning → execution
        → retain candidate → supervision → publish/consolidate
        → readback/effect observation
```

每次运行必须携带 `task_id`、`event_id`、`conversation_id`、`connector_run_id`。缺字段直接拒绝，防止跨任务、跨对话和重试串线。

## 记忆与知识

记忆适配器负责工作记忆和长期经验；RAG 适配器默认只读并返回来源。两者接口分离，知识库写入需要显式治理流程，不能由普通检索调用绕过。

## 自成长

候选状态为 `created → pending_review → source_verified → approved → published → observed → rolled_back`。`created` 不等于 `approved`，未经审核的候选不能发布为正式知识或规则。

## 降级与审计

记忆服务不可用时返回 `memory_unavailable` 和 `degraded=true`，调用方必须决定是否暂停、转人工或继续无记忆模式。策略或最高目标哈希变化会生成审计事件。

## 生产使用边界

本项目是通用治理内核和适配器协议，不包含任何组织的身份、密钥、企业文档、生产地址或业务规则。生产部署前应增加真实身份提供商、审计存储、密钥管理、数据保留和独立安全评审。
