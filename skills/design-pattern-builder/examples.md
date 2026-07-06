# Builder 案例

## 业务案例

创建 OrderSearchQuery，需要状态、时间区间、分页、排序、权限过滤和默认值。

## 适配判断

- 使用：构造参数多、默认值多、校验复杂，或同一构造过程需要生成不同表示。
- 避免：简单 DTO 或只有两三个参数时不要引入。
- 变化轴：把会变化的部分隔离，让调用方依赖稳定角色。

## 最佳实现步骤

1. 用业务语言命名角色，避免 ConcreteXxx 这类示例化命名。
2. 定义稳定接口或协议，让调用方只依赖稳定能力。
3. 把具体变体放在组合根、工厂、注册表或配置层选择。
4. 为新增变体写一条替换测试，证明调用方不用改。
5. 为失败路径和边界条件写测试。

## Java 风格示例

~~~java
interface StableRole {
    Result execute(Request request);
}

final class ConcreteVariation implements StableRole {
    public Result execute(Request request) {
        // implement Builder variation for the business case
        return Result.ok();
    }
}

final class ClientService {
    private final StableRole role;

    ClientService(StableRole role) {
        this.role = role;
    }

    Result handle(Request request) {
        return role.execute(request);
    }
}
~~~

## TypeScript 风格示例

~~~ts
type StableRole = (request: Request) => Result;

const concreteVariation: StableRole = (request) => {
  // implement Builder variation for the business case
  return { ok: true };
};

export function handle(request: Request, role: StableRole): Result {
  return role(request);
}
~~~

## 测试案例

- 新增一个变体，调用方代码不需要修改。
- 传入非法输入时，错误语义清楚且可断言。
- 组合或创建顺序不依赖隐藏全局状态。

## 代码审查清单

- 模式是否绑定真实变化轴？
- 角色命名是否来自业务语义？
- 是否能用更简单的函数、组合或语言机制替代？
- 目标语言实现是否惯用？
