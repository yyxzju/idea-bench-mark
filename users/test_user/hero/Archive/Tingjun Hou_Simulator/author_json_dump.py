import csv
import json
import os

def extract_author_info(csv_file):
    """
    提取 author.csv 中的指定信息。
    :param csv_file: author.csv 文件路径
    :return: 包含处理后信息的列表
    """
    extracted_data = []

    try:
        with open(csv_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)

            for row in reader:
                # 提取并处理指定字段
                name = f"{row['name']}_Simulator"  # 添加“_Simulator”
                title = row['title']
                interests = row['interests']
                citedby = int(row['citedby']) if row['citedby'].isdigit() else 0  # 转为数字

                # 将处理后的数据存储到列表
                extracted_data.append({
                    "name": name,
                    "title": title,
                    "focus_area": interests,
                    "citations": citedby
                })

    except FileNotFoundError:
        print(f"文件 {csv_file} 未找到。")
    except KeyError as e:
        print(f"CSV 文件中缺少列：{e}")
    except Exception as e:
        print(f"处理文件时发生错误：{e}")

    return extracted_data

def extract_coauthor_info(csv_file):
    """
    提取 coauthors.csv 中的名字信息。
    :param csv_file: coauthors.csv 文件路径
    :return: 包含提取名字的列表
    """
    coauthors = []

    try:
        with open(csv_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)

            for row in reader:
                # 提取名字
                coauthors.append(row['name'])

    except FileNotFoundError:
        print(f"文件 {csv_file} 未找到。")
    except KeyError as e:
        print(f"CSV 文件中缺少列：{e}")
    except Exception as e:
        print(f"处理文件时发生错误：{e}")

    return coauthors

def generate_author_prompt(author_info, coauthors):
    """
    根据作者和合作者信息生成动态 prompt。
    
    :param author_info: 包含作者信息的字典，例如：
        {
            "name": "张三_Simulator",
            "title": "教授",
            "focus_area": "人工智能",
            "citations": 1200
        }
    :param coauthors: 包含合作者名字的列表，例如 ["李四", "王五"]
    :return: 动态生成的 prompt 字符串
    """
    # 作者的基础信息
    name = author_info.get("name", "未知")
    title = author_info.get("title", "未知")
    focus_area = author_info.get("focus_area", "未知")
    citations = author_info.get("citations", 0)

    # 合作者信息
    collaborators = ", ".join(coauthors) if coauthors else "暂无合作者"

    # 构造动态 prompt
    prompt = (
        f"You are {name}, a renowned {title} specializing in {focus_area}. "
        f"You have been cited {citations} times in academic works. "
        f"Your collaborators include: {collaborators}. Provide expert analysis and recommendations."
    )

    return prompt
def update_hero_json(author_csv, coauthor_csv, base_directory):
    """
    更新 JSON 模板文件，生成符合需求的 JSON 数据。
    :param author_csv: author.csv 文件路径
    :param coauthor_csv: coauthors.csv 文件路径
    :param base_directory: 程序运行时的当前工作目录
    :return: 生成的 JSON 数据
    """
    # 提取作者信息
    author_data = extract_author_info(author_csv)

    if not author_data:
        print("未找到作者信息，无法更新 JSON 文件。")
        return None

    # 假设只处理第一个作者
    author = author_data[0]

    # 提取合作作者信息
    collaborators = extract_coauthor_info(coauthor_csv)

    # 生成动态 prompt
    prompt = generate_author_prompt(author, collaborators)

    # 获取绝对路径
    knowledge_base_directory = os.path.abspath(os.path.join(base_directory, "knowledge_base"))
    memory_base_directory = os.path.abspath(os.path.join(base_directory, "memory_base"))

    # 生成 JSON 数据
    hero_json = {
        "name": author["name"],
        "title": author["title"],
        "description": f"You are {author['name']} providing expert analysis and scientific recommendations.",  # 使用动态生成的 prompt
        "focus_area": author["focus_area"],
        "citations": author["citations"],
        "collaborators": collaborators,
        "prompt": prompt,  
        "knowledge_base_directory": knowledge_base_directory,
        "memory_base_directory": memory_base_directory
    }

    # 保存 JSON 文件
    file_name = f"{author['name']}.json"
    file_path = os.path.join(base_directory, file_name)

    try:
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(hero_json, file, indent=4, ensure_ascii=False)
        print(f"JSON 文件已保存为：{file_path}")
    except Exception as e:
        print(f"保存 JSON 文件时发生错误：{e}")

    return hero_json

# 示例运行
if __name__ == "__main__":
    author_csv_path = "author.csv"  # 替换为实际 author.csv 文件路径
    coauthor_csv_path = "coauthors.csv"  # 替换为实际 coauthors.csv 文件路径
    base_dir = os.getcwd()  # 当前工作目录

    hero_data = update_hero_json(author_csv_path, coauthor_csv_path, base_dir)

    if hero_data:
        print("生成的 JSON 数据如下：")
        print(json.dumps(hero_data, indent=4, ensure_ascii=False))
