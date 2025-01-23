import csv
import json
import os

def ensure_directory(directory_path):
    """
    确保目录存在，不存在则创建。
    :param directory_path: 目录路径
    """
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
        print(f"目录已创建：{directory_path}")
    else:
        print(f"目录已存在：{directory_path}")

def extract_publications(csv_file, base_directory):
    """
    提取 publications.csv 中的 title 和 abstract 信息，并生成 JSON 数据。
    :param csv_file: publications.csv 文件路径
    :param base_directory: 程序运行时的当前工作目录
    :return: 生成的 JSON 数据
    """
    publications = []

    try:
        with open(csv_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)

            for row in reader:
                # 提取所需字段
                title = row.get("title", "").strip()
                abstract = row.get("abstract", "").strip()

                if not title or not abstract:
                    continue  # 跳过缺少必要信息的条目

                # 构造 PDF 文件路径
                sanitized_title = title.lower().replace(" ", "_").replace("/", "_")
                pdf_file_dir = os.path.join(base_directory, "knowledge_base", "pdf_paper", f"{sanitized_title}.pdf")

                # 添加到列表
                publications.append({
                    "title": title,
                    "abstract": abstract,
                    "pdf_file_dir": pdf_file_dir
                })

    except FileNotFoundError:
        print(f"文件 {csv_file} 未找到。")
    except KeyError as e:
        print(f"CSV 文件中缺少列：{e}")
    except Exception as e:
        print(f"处理文件时发生错误：{e}")

    return publications

def save_publications_to_json(publications, knowledge_base_path):
    """
    将提取的 publications 数据保存为 JSON 文件。
    :param publications: 提取的 publications 数据
    :param knowledge_base_path: knowledge_base 文件夹路径
    """
    # 确保 knowledge_base 和 pdf_paper 文件夹存在
    ensure_directory(knowledge_base_path)
    pdf_paper_path = os.path.join(knowledge_base_path, "pdf_paper")
    ensure_directory(pdf_paper_path)

    # 保存文件路径
    output_file = os.path.join(knowledge_base_path, "scientific_papers_base.json")

    try:
        with open(output_file, "w", encoding="utf-8") as file:
            json.dump(publications, file, indent=4, ensure_ascii=False)
        print(f"Publications 数据已保存为：{output_file}")
    except Exception as e:
        print(f"保存 JSON 文件时发生错误：{e}")

# 示例运行
if __name__ == "__main__":
    csv_path = "publications.csv"  # 替换为实际 publications.csv 文件路径
    base_dir = os.getcwd()  # 当前工作目录

    # 提取数据
    publications_data = extract_publications(csv_path, base_dir)

    if publications_data:
        # 确保 knowledge_base 文件夹路径
        knowledge_base_dir = os.path.join(base_dir, "knowledge_base")
        # 保存为 JSON 文件
        save_publications_to_json(publications_data, knowledge_base_dir)

        # 打印生成的 JSON 数据
        print("生成的 JSON 数据如下：")
        print(json.dumps(publications_data, indent=4, ensure_ascii=False))
    else:
        print("未提取到任何有效的 publications 数据。")
