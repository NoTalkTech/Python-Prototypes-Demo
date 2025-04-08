import requests
import json
import time

# 替换为你的 DeepSeek API Key
DEEPSEEK_API_KEY = "sk-"
DEEPSEEK_ENDPOINT = "https://api.deepseek.com/v1/chat/completions"

# 中文 Prompt 设定（适配数据仓库问答助手）
SYSTEM_PROMPT = """
你是一个专业的数据仓库问答助手，具备逻辑推理和多步思考能力。
在接收到用户输入后，请按照以下步骤思考与处理：

1. 理解用户输入：简要复述，确保你真正理解了用户想表达的内容。
2. 识别问题或请求：明确用户遇到的核心问题或需求点。
3. 推断用户意图：深入思考用户的真实目的。
4. 对用户意图进行分类：
   - 💡 知识查询
   - ⚙️ 使用咨询
   - 🛠 故障排查
   - 📈 性能优化
   - 🧱 方案设计
   - 🧪 数据验证
   - ❓其他（请注明）
5. （可选）下一步建议。

请按步骤逐条思考，并展示你的推理过程。
"""

# 示例问题列表
questions = [
    "我在用 ClickHouse 查询一个分区表，发现有的查询特别慢，怀疑没走到分区裁剪，能不能帮我分析下原因？",
    "Flink 里的窗口函数怎么处理迟到数据？watermark 怎么设置？",
    "StarRocks 的 bitmap_union_count 和 count(distinct) 哪个效率更高？",
]

def analyze_question(question):
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "deepseek-chat",  # 或 deepseek-coder
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": question}
        ],
        "temperature": 0.3
    }

    response = requests.post(DEEPSEEK_ENDPOINT, headers=headers, json=payload)
    response.raise_for_status()
    result = response.json()
    return result["choices"][0]["message"]["content"]

def main():
    results = []
    for i, q in enumerate(questions):
        print(f"\n--- 问题 {i+1} ---")
        print(f"输入问题：{q}")
        try:
            answer = analyze_question(q)
            print("分析结果：")
            print(answer)
            results.append({
                "question": q,
                "analysis": answer
            })
            time.sleep(1.5)  # 加一点延迟避免触发速率限制
        except Exception as e:
            print(f"处理失败：{e}")

    # 可选：保存结果为 JSON 文件
    with open("deepseek_analysis_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()