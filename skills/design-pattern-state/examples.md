# State 案例

## 业务案例

订单在 Draft、Submitted、Paid、Cancelled 下对 pay/cancel/ship 行为不同。

## 适配判断

- 使用：对象有清楚生命周期，且不同状态下同一操作行为差异明显。
- 避免：状态很少且逻辑简单时 switch 更直观。
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
        // implement State variation for the business case
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
  // implement State variation for the business case
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
