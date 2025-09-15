#!/usr/bin/env python3
"""
MCP PostgreSQL 测试脚本
演示如何使用 MCP Store 中的 PostgreSQL 服务
"""

import psycopg2
import json
from datetime import datetime

# 数据库连接配置
DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'ai_db',
    'user': 'test',
    'password': 'test'
}

def test_connection():
    """测试数据库连接"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # 获取数据库版本
        cursor.execute("SELECT version();")
        version = cursor.fetchone()[0]
        print(f"✅ 数据库连接成功!")
        print(f"📊 PostgreSQL 版本: {version}")
        
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"❌ 数据库连接失败: {e}")
        return False

def query_users():
    """查询用户数据"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM mcp_test_users ORDER BY id;")
        users = cursor.fetchall()
        
        print("\n👥 用户数据:")
        print("ID | 姓名 | 邮箱 | 创建时间")
        print("-" * 50)
        for user in users:
            print(f"{user[0]:2} | {user[1]:4} | {user[2]:20} | {user[3]}")
        
        cursor.close()
        conn.close()
        return users
    except Exception as e:
        print(f"❌ 查询失败: {e}")
        return []

def add_user(name, email):
    """添加新用户"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        cursor.execute(
            "INSERT INTO mcp_test_users (name, email) VALUES (%s, %s) RETURNING id;",
            (name, email)
        )
        user_id = cursor.fetchone()[0]
        conn.commit()
        
        print(f"✅ 用户添加成功! ID: {user_id}")
        
        cursor.close()
        conn.close()
        return user_id
    except Exception as e:
        print(f"❌ 添加用户失败: {e}")
        return None

def get_table_info():
    """获取表结构信息"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT column_name, data_type, is_nullable, column_default
            FROM information_schema.columns 
            WHERE table_name = 'mcp_test_users'
            ORDER BY ordinal_position;
        """)
        columns = cursor.fetchall()
        
        print("\n📋 表结构 (mcp_test_users):")
        print("字段名 | 数据类型 | 可空 | 默认值")
        print("-" * 60)
        for col in columns:
            nullable = "是" if col[2] == "YES" else "否"
            default = col[3] if col[3] else "无"
            print(f"{col[0]:15} | {col[1]:15} | {nullable:4} | {default}")
        
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"❌ 获取表信息失败: {e}")

def main():
    """主函数"""
    print("🔍 MCP PostgreSQL 服务测试")
    print("=" * 40)
    
    # 测试连接
    if not test_connection():
        return
    
    # 获取表结构
    get_table_info()
    
    # 查询现有用户
    query_users()
    
    # 添加新用户
    print(f"\n➕ 添加新用户...")
    add_user("赵六", "zhaoliu@example.com")
    
    # 再次查询用户
    print(f"\n🔄 更新后的用户列表:")
    query_users()
    
    print(f"\n✨ 测试完成! 时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()
