import sqlite3

# 连接到SQLite数据库（如果数据库不存在，则会被创建）
conn = sqlite3.connect('my_database.db')
c = conn.cursor()

# 创建一个表（如果表已经存在，则跳过此步骤）
c.execute('''CREATE TABLE IF NOT EXISTS shops (  
             id INTEGER PRIMARY KEY AUTOINCREMENT,  
             shop_name TEXT,  
             date TEXT,  
             -- 其他字段...  
             )''')

# 假设你有一个清洗后的数据列表
cleaned_data = [
    ('ShopA', '2023-10-23'),
    ('ShopB', '2023-10-22'),
    # ... 其他数据
]

# 插入数据
for shop_name, date_str in cleaned_data:
    c.execute("INSERT INTO shops (shop_name, date) VALUES (?, ?)", (shop_name, date_str))

# 提交更改并关闭连接
conn.commit()
conn.close()