# Security Architecture

> Mobile App 认证与安全架构

## 概述

本文档描述移动应用的认证和安全机制实现。

## 认证流程

### JWT Token 认证

```dart
// lib/services/auth/auth_service.dart
class AuthService {
  Future<TokenPair> login(String email, String password);
  Future<void> logout();
  Future<TokenPair> refreshToken(String refreshToken);
}
```

### Token 存储

- AccessToken: 内存中，自动刷新
- RefreshToken: 安全存储 (flutter_secure_storage)

## 安全措施

1. **传输层**: TLS 1.3 强制加密
2. **证书锁定**: SSL Pinning 防止 MITM
3. **代码混淆**: ProGuard/R8 混淆
4. **Root检测**: 检测 Root/越狱设备

## 相关代码

| 功能 | 文件路径 |
|------|----------|
| 认证服务 | `mobile/src/services/auth/auth_service.dart` |
| Token管理 | `mobile/src/services/auth/token_manager.dart` |
| 安全中间件 | `mobile/src/middleware/auth_middleware.dart` |
| 登录页面 | `mobile/src/screens/auth/login_screen.dart` |
| 注册页面 | `mobile/src/screens/auth/register_screen.dart` |

## 参考资料

- [OWASP Mobile Security](https://owasp.org/www-project-mobile-security/)
- [JWT Best Practices](https://auth0.com/blog/jwt-authentication-best-practices/)
