import requests
import json
import time
import os
import re

# ====== 配置区域 ======
DEEPSEEK_API_KEY = "your_deepseek_api_key"  # 替换为你的 DeepSeek API 密钥
DEEPSEEK_ENDPOINT = "https://api.deepseek.com/v1/chat/completions"
MODEL = "deepseek-chat"  # 或 deepseek-coder

# 示例问题列表（你也可以从文件读取）
questions = [
    "我在用 ClickHouse 查询一个分区表，发现有的查询特别慢，怀疑没走到分区裁剪，能不能帮我分析下原因？",
    "Flink 里的窗口函数怎么处理迟到数据？watermark 怎么设置？",
    "StarRocks 的 bitmap_union_count 和 count(distinct) 哪个效率更高？",
    "数据仓库里维度表更新频率很低，是否适合建成宽表？",
]

# 系统 Prompt（强制结构化输出）
SYSTEM_PROMPT = """
你是一个专业的数据仓库问答助手，具备逻辑推理、结构化分析和联网搜索能力。
请按照以下步骤处理用户的问题，并根据需要结合外部搜索信息（系统会提前提供搜索摘要）。

=== 输入说明 ===
用户输入的问题可能已经附带了一个“search_info”字段，里面包含了系统通过搜索引擎查询到的摘要。请合理引用该信息以增强你的回答。

=== 分析步骤 ===
1. summary：复述用户输入
2. problem：明确的技术问题或场景
3. intent：用户真正的目的
4. intent_class：分类（只能为以下之一）：
   - 知识查询
   - 使用咨询
   - 故障排查
   - 性能优化
   - 方案设计
   - 数据验证
   - 其他（请注明）
5. suggestion：给出下一步建议（如需要）

=== 输出格式 ===
请严格使用以下 JSON 格式输出：

{
  "summary": "...",
  "problem": "...",
  "intent": "...",
  "intent_class": "...",
  "suggestion": "...",
  "references": ["..."]  // 可选，列出引用到的搜索摘要关键词或链接
}
"""

# ====== 核心函数 ======
def analyze_question(question):
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": question}
        ],
        "temperature": 0.3
    }

    response = requests.post(DEEPSEEK_ENDPOINT, headers=headers, json=payload)
    response.raise_for_status()
    result = response.json()
    content = result["choices"][0]["message"]["content"]

    try:
        json_str = re.search(r"\{[\s\S]+\}", content).group(0)
        parsed = json.loads(json_str)
        return parsed, content
    except Exception as e:
        print("⚠️ JSON 解析失败，原始内容如下：\n", content)
        raise e

def main():
    results = []
    for i, q in enumerate(questions):
        print(f"\n=== 问题 {i+1} ===")
        print(f"输入：{q}")
        try:
            parsed, full_text = analyze_question(q)
            parsed["question"] = q
            parsed["full_output"] = full_text
            print(f"✅ 分类识别：{parsed.get('intent_class', '未知')}")
            results.append(parsed)
            time.sleep(1.5)
        except Exception as e:
            print(f"❌ 处理失败：{e}")

    # 可选：保存结果为 JSON 文件
    # Create output directory if it doesn't exist
    output_dir = os.path.join(os.path.dirname(__file__), "output")
    os.makedirs(output_dir, exist_ok=True)
    
    # Save results to output directory
    output_file = os.path.join(output_dir, "deepseek_analysis_results.json")
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
        print("\n✅ 全部问题处理完毕，结果保存在 deepseek_structured_analysis.json")

if __name__ == "__main__":
    main()