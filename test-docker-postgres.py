#!/usr/bin/env python3
"""
Docker PostgreSQL MCP 测试脚本
验证 MCP 工具可以访问 Docker 中的 PostgreSQL 数据库
"""

import psycopg2
import json
from datetime import datetime

# Docker PostgreSQL 连接配置
DOCKER_DB_CONFIG = {
    'host': 'localhost',
    'port': 5433,  # Docker 容器映射的端口
    'database': 'mcpdb',
    'user': 'mcpuser',
    'password': 'mcppassword'
}

def test_docker_connection():
    """测试 Docker PostgreSQL 连接"""
    try:
        conn = psycopg2.connect(**DOCKER_DB_CONFIG)
        cursor = conn.cursor()
        
        # 获取数据库版本
        cursor.execute("SELECT version();")
        version = cursor.fetchone()[0]
        print(f"✅ Docker PostgreSQL 连接成功!")
        print(f"📊 版本: {version}")
        
        # 获取容器信息
        cursor.execute("SELECT current_database(), current_user, inet_server_addr(), inet_server_port();")
        db_info = cursor.fetchone()
        print(f"📋 数据库: {db_info[0]}")
        print(f"👤 用户: {db_info[1]}")
        print(f"🌐 服务器: {db_info[2] or 'localhost'}:{db_info[3] or 5432}")
        
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"❌ Docker PostgreSQL 连接失败: {e}")
        return False

def query_docker_users():
    """查询 Docker 数据库中的用户数据"""
    try:
        conn = psycopg2.connect(**DOCKER_DB_CONFIG)
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM docker_test_users ORDER BY id;")
        users = cursor.fetchall()
        
        print("\n👥 Docker 数据库用户数据:")
        print("ID | 姓名        | 邮箱                 | 创建时间")
        print("-" * 60)
        for user in users:
            print(f"{user[0]:2} | {user[1]:11} | {user[2]:20} | {user[3]}")
        
        cursor.close()
        conn.close()
        return users
    except Exception as e:
        print(f"❌ 查询失败: {e}")
        return []

def add_docker_user(name, email):
    """向 Docker 数据库添加新用户"""
    try:
        conn = psycopg2.connect(**DOCKER_DB_CONFIG)
        cursor = conn.cursor()
        
        cursor.execute(
            "INSERT INTO docker_test_users (name, email) VALUES (%s, %s) RETURNING id;",
            (name, email)
        )
        user_id = cursor.fetchone()[0]
        conn.commit()
        
        print(f"✅ Docker 数据库用户添加成功! ID: {user_id}")
        
        cursor.close()
        conn.close()
        return user_id
    except Exception as e:
        print(f"❌ 添加用户失败: {e}")
        return None

def get_docker_table_info():
    """获取 Docker 数据库表结构信息"""
    try:
        conn = psycopg2.connect(**DOCKER_DB_CONFIG)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT column_name, data_type, is_nullable, column_default
            FROM information_schema.columns 
            WHERE table_name = 'docker_test_users'
            ORDER BY ordinal_position;
        """)
        columns = cursor.fetchall()
        
        print("\n📋 Docker 数据库表结构 (docker_test_users):")
        print("字段名          | 数据类型        | 可空 | 默认值")
        print("-" * 65)
        for col in columns:
            nullable = "是" if col[2] == "YES" else "否"
            default = col[3] if col[3] else "无"
            print(f"{col[0]:15} | {col[1]:15} | {nullable:4} | {default}")
        
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"❌ 获取表信息失败: {e}")

def compare_environments():
    """对比本地和 Docker 环境"""
    print("\n🔄 环境对比:")
    print("=" * 50)
    print("本地 PostgreSQL:")
    print("  - 版本: 17.6 (Homebrew)")
    print("  - 端口: 5432")
    print("  - 数据库: ai_db")
    print("  - 用户: test/test")
    print()
    print("Docker PostgreSQL:")
    print("  - 版本: 17.6 (Alpine Linux)")
    print("  - 端口: 5433 (映射到容器的 5432)")
    print("  - 数据库: mcpdb")
    print("  - 用户: mcpuser/mcppassword")
    print("  - 容器: mcp-postgres")

def main():
    """主函数"""
    print("🐳 Docker PostgreSQL MCP 服务测试")
    print("=" * 45)
    
    # 测试连接
    if not test_docker_connection():
        return
    
    # 环境对比
    compare_environments()
    
    # 获取表结构
    get_docker_table_info()
    
    # 查询现有用户
    query_docker_users()
    
    # 添加新用户
    print(f"\n➕ 向 Docker 数据库添加新用户...")
    add_docker_user("Docker新用户", "newdocker@example.com")
    
    # 再次查询用户
    print(f"\n🔄 更新后的 Docker 用户列表:")
    query_docker_users()
    
    print(f"\n✨ Docker PostgreSQL 测试完成!")
    print(f"⚙️  MCP 配置已更新为连接 Docker 数据库")
    print(f"🕐 时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()
