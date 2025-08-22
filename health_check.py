#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
健康检查脚本
"""

import requests
import sys
import time

def health_check():
    """健康检查"""
    try:
        # 等待服务启动
        time.sleep(5)
        
        # 检查服务是否响应
        response = requests.get("http://localhost:8080/docs", timeout=10)
        
        if response.status_code == 200:
            print("✅ 服务健康检查通过")
            return True
        else:
            print(f"❌ 服务响应异常，状态码: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到服务")
        return False
    except requests.exceptions.Timeout:
        print("❌ 服务响应超时")
        return False
    except Exception as e:
        print(f"❌ 健康检查失败: {e}")
        return False

if __name__ == "__main__":
    success = health_check()
    sys.exit(0 if success else 1)
