# Aggregation View Patterns

## Dashboard Summary

面向运营或管理者的状态总览。字段通常来自多个 Domain，常见指标包括数量、金额、比率、异常数、趋势。优先明确刷新周期、`generatedAt` 和权限。

## List Item Summary

面向扫描和比较的列表项。字段应少而稳定，支持筛选、排序、分页。不要为了列表字段污染 Aggregate。

## Detail Page Composition

面向单个业务对象的详情页，可组合订单、用户、支付、物流、售后等来源。详情页模型不等于写侧 Aggregate。

## Report Row

面向报表导出或分析。通常允许 scheduled freshness，适合 materialized view、read table 或 analytics table。

## Search Result Document

面向搜索命中和排序。字段可冗余，必须说明索引来源、刷新方式和重建策略。

## Admin Operation View

面向后台操作人员。除展示字段外，还要显式声明可操作状态、权限字段、审计字段和 stale data 行为。
