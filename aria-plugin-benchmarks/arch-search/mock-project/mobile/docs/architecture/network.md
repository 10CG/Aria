# Network Architecture

> Mobile App 网络通信架构

## 概述

本文档描述应用的网络层设计和 API 调用策略。

## 技术选型

- **HTTP Client**: Dio
- **API 定义**: Retrofit (代码生成)
- **序列化**: json_serializable

## 网络层架构

```
┌─────────────────────────────────────────────┐
│              API Service                    │
│         (Retrofit Interface)                │
├─────────────────────────────────────────────┤
│            Interceptors                     │
│   (Auth, Logging, Retry, Cache)             │
├─────────────────────────────────────────────┤
│               Dio Client                    │
│         (HTTP Connection)                   │
└─────────────────────────────────────────────┘
```

## API Service 示例

```dart
@RestApi(baseUrl: '/api/v1')
abstract class TaskApiService {
  factory TaskApiService(Dio dio) = _TaskApiService;

  @GET('/tasks')
  Future<List<Task>> getTasks();

  @POST('/tasks')
  Future<Task> createTask(@Body() CreateTaskRequest request);

  @GET('/tasks/{id}')
  Future<Task> getTask(@Path('id') String id);
}
```

## 拦截器配置

### 认证拦截器

```dart
class AuthInterceptor extends Interceptor {
  @override
  void onRequest(RequestOptions options, RequestInterceptorHandler handler) {
    final token = getAccessToken();
    if (token != null) {
      options.headers['Authorization'] = 'Bearer $token';
    }
    handler.next(options);
  }
}
```

### 重试拦截器

```dart
class RetryInterceptor extends Interceptor {
  final int maxRetries = 3;
  // 自动重试失败的请求
}
```

## 相关代码

| 功能 | 文件路径 |
|------|----------|
| API 服务 | `mobile/src/services/api/` |
| 拦截器 | `mobile/src/services/api/interceptors/` |
| 网络配置 | `mobile/src/config/network_config.dart` |
| 错误处理 | `mobile/src/services/api/error_handler.dart` |

## API 契约

API 定义位于 `shared/contracts/openapi/`

## 错误处理策略

1. 网络错误: 自动重试 (指数退避)
2. 401 错误: Token 刷新后重试
3. 服务器错误: 显示用户友好提示
4. 业务错误: 根据错误码处理
