import 'dart:async';
import 'dart:convert';
import 'dart:io';

class CacheManager {
  final Map<String, dynamic> _memoryCache = {};
  final String _cacheDirectory;

  CacheManager({String? cacheDirectory})
      : _cacheDirectory = cacheDirectory ?? 'cache';

  /// 获取缓存
  Future<dynamic> get(String key) async {
    // 1. 先查内存缓存
    if (_memoryCache.containsKey(key)) {
      final cacheData = _memoryCache[key];
      if (cacheData['expiry'] == null ||
          DateTime.now().millisecondsSinceEpoch < cacheData['expiry']) {
        return cacheData['value'];
      } else {
        _memoryCache.remove(key);
      }
    }

    // 2. 查磁盘缓存
    final file = File('$_cacheDirectory/$key.json');
    if (await file.exists()) {
      try {
        final content = await file.readAsString();
        final data = jsonDecode(content);
        if (data['expiry'] == null ||
            DateTime.now().millisecondsSinceEpoch < data['expiry']) {
          // 同步到内存
          _memoryCache[key] = data;
          return data['value'];
        } else {
          await file.delete();
        }
      } catch (e) {
        // 文件损坏，删除
        await file.delete();
      }
    }

    return null;
  }

  /// 设置缓存
  Future<void> set(String key, dynamic value, {Duration? ttl}) async {
    final expiry = ttl != null
        ? DateTime.now().millisecondsSinceEpoch + ttl.inMilliseconds
        : null;

    final cacheData = {
      'value': value,
      'expiry': expiry,
      'timestamp': DateTime.now().millisecondsSinceEpoch,
    };

    // 1. 存入内存
    _memoryCache[key] = cacheData;

    // 2. 存入磁盘
    final file = File('$_cacheDirectory/$key.json');
    await file.create(recursive: true);
    await file.writeAsString(jsonEncode(cacheData));
  }

  /// 删除缓存
  Future<void> delete(String key) async {
    _memoryCache.remove(key);
    final file = File('$_cacheDirectory/$key.json');
    if (await file.exists()) {
      await file.delete();
    }
  }

  /// 清除所有缓存
  Future<void> clear() async {
    _memoryCache.clear();
    final directory = Directory(_cacheDirectory);
    if (await directory.exists()) {
      await directory.delete(recursive: true);
    }
  }
}