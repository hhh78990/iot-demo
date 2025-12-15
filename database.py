
import sqlite3
import json

conn = sqlite3.connect('sensor_data.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS sensor_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    device_id TEXT NOT NULL,
    sensor_type TEXT NOT NULL,
    value REAL NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
''')

cursor.execute("SELECT COUNT(*) FROM sensor_history")
if cursor.fetchone()[0] == 0:
    sample_data = [
        ('device_001', 'temperature', 25.3),
        ('device_001', 'temperature', 26.1),
        ('device_001', 'humidity', 65.2),
        ('device_002', 'temperature', 24.8),
        ('device_002', 'pressure', 1013.2),
    ]
    
    for data in sample_data:
        cursor.execute(
            "INSERT INTO sensor_history (device_id, sensor_type, value) VALUES (?, ?, ?)",
            data
        )
    print("✅ 已插入示例数据")

print("\n=== 查询结果：所有传感器数据 ===")
cursor.execute("SELECT * FROM sensor_history ORDER BY timestamp DESC")
all_data = cursor.fetchall()

for row in all_data:
    print(f"ID: {row[0]}, 设备: {row[1]}, 类型: {row[2]}, 值: {row[3]}, 时间: {row[4]}")

# 4. 导出为JSON文件（供HTML使用）
print("\n=== 导出数据为JSON ===")
data_for_json = []
for row in all_data:
    data_for_json.append({
        'id': row[0],
        'device_id': row[1],
        'sensor_type': row[2],
        'value': row[3],
        'timestamp': row[4]
    })

with open('sensor_data.json', 'w', encoding='utf-8') as f:
    json.dump(data_for_json, f, ensure_ascii=False, indent=2)
print("✅ 数据已导出到 sensor_data.json")

# 关闭连接
conn.commit()
conn.close()
print("\n✅ 数据库操作完成！")