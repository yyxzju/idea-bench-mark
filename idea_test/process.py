import json
import csv

# 输入文件名和输出CSV文件名
input_json = 'ideas_summary20241226_221643.json'
output_csv = 'jieda.csv'
# input_json = 'ideas_summary20241226_214844.json'
# output_csv = 'qifa.csv'

# 读取 JSON 文件
with open(input_json, 'r', encoding='utf-8') as f:
    data = json.load(f)

# 打开输出CSV文件，准备写入
with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    
    # 写入表头
    
    # 遍历每个条目，合并 idea_description 和 experiment_plan
    for entry in data:
        # 获取 idea_description 和 experiment_plan 并进行合并
        idea_description = entry.get('idea_description', '').replace('\n', ' ').replace('\r', '')
        experiment_plan = entry.get('experiment_plan', '').replace('\n', ' ').replace('\r', '')
        
        # 合并这两个字段，确保它们之间有适当的分隔符（比如换行符或者分号）
        combined = f"idea {idea_description} 执行步骤 {experiment_plan}"
        
        # 写入合并后的内容
        writer.writerow([combined])

print(f"CSV 文件已生成: {output_csv}")
