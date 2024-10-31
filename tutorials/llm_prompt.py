from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain_community.llms.ollama import Ollama
import time
import json

def get_completion_ollama(prompt, llm=Ollama(base_url="http://localhost:11434", model="qwen2.5:7b")):
    """Get completion from Ollama model.
    
    Args:
        prompt: Input text prompt
        llm: Ollama model instance
        
    Returns:
        Generated completion text
    """
    res = llm.invoke(prompt)
    print(f'prompt -> {prompt}\ncompletion -> {res}')
    return res

# Example prompts and responses
def process_product_description(fact_sheet_chair):
    """Generate product description from technical specifications."""
    prompt = f"""
    您的任务是帮助营销团队基于技术说明书创建一个产品的零售网站描述。

    根据```标记的技术说明书中提供的信息，编写一个产品描述。

    该描述面向家具零售商，因此应具有技术性质，并侧重于产品的材料构造。

    在描述末尾，包括技术规格中每个7个字符的产品ID。

    在描述之后，包括一个表格，提供产品的尺寸。表格应该有两列。
    第一列包括尺寸的名称。第二列只包括英寸的测量值。

    给表格命名为"产品尺寸"。

    将所有内容格式化为可用于网站的HTML格式。将描述放在<div>元素中。

    技术规格：```{fact_sheet_chair}```
    """
    response = get_completion_ollama(prompt)
    print(response)
    
    from IPython.display import display, HTML
    display(HTML(response))

def analyze_sentiment(text):
    """Analyze sentiment and extract information from review text."""
    prompts = [
        f"以下用三个反引号分隔的产品评论的情感是什么？\n用一个单词回答：「正面」或「负面」。\n评论文本: ```{text}```",
        f"识别以下评论的作者表达的情感。包含不超过五个项目。将答案格式化为以逗号分隔的单词列表。\n评论文本: ```{text}```",
        f"以下评论的作者是否表达了愤怒？评论用三个反引号分隔。给出是或否的答案。\n评论文本: ```{text}```"
    ]
    
    for prompt in prompts:
        get_completion_ollama(prompt)

def extract_info(text):
    """Extract structured information from review text."""
    prompts = [
        f"""从评论文本中识别以下项目：
        - 评论者购买的物品
        - 制造该物品的公司
        
        评论文本用三个反引号分隔。将你的响应格式化为以 "物品" 和 "品牌" 为键的 JSON 对象。
        如果信息不存在，请使用 "未知" 作为值。
        让你的回应尽可能简短。
        
        评论文本: ```{text}```""",
        
        f"""从评论文本中识别以下项目：
        - 情绪（正面或负面）
        - 审稿人是否表达了愤怒？（是或否）
        - 评论者购买的物品
        - 制造该物品的公司
        
        评论用三个反引号分隔。将你的响应格式化为 JSON 对象，
        以 "情感倾向"、"是否生气"、"物品类型" 和 "品牌" 作为键。
        如果信息不存在，请使用 "未知" 作为值。
        让你的回应尽可能简短。
        将 "是否生气" 值格式化为布尔值。
        
        评论文本: ```{text}```"""
    ]
    
    for prompt in prompts:
        get_completion_ollama(prompt)

def analyze_topics(story):
    """Analyze topics in a given text."""
    prompts = [
        f"""确定以下给定文本中讨论的五个主题。
        每个主题用1-2个词概括。
        请输出一个可解析的Python列表，每个元素是一个字符串，展示了一个主题。
        给定文本: ```{story}```""",
        
        f"""判断主题列表中的每一项是否是给定文本中的一个话题，
        以列表的形式给出答案，每个元素是一个Json对象，键为对应主题，值为对应的 0 或 1。
        主题列表：美国航空航天局、当地政府、工程、员工满意度、联邦政府
        给定文本: ```{story}```"""
    ]
    
    for prompt in prompts:
        get_completion_ollama(prompt)

def translate_text():
    """Demonstrate various translation capabilities."""
    prompts = [
        """将以下中文翻译成西班牙语:\n```您好，我想订购一个搅拌机。```""",
        """请告诉我以下文本是什么语种: \n```Combien coûte le lampadaire?```""",
        """请将以下文本分别翻译成中文、英文、法语和西班牙语: \n```I want to order a basketball.```""",
        """请将以下文本翻译成中文，分别展示成正式与非正式两种语气: \n```Would you like to order a pillow?```"""
    ]
    
    for prompt in prompts:
        get_completion_ollama(prompt)

def universal_translator(messages):
    """Universal translator for multiple languages."""
    for issue in messages:
        time.sleep(3)  # Reduced from 20s to 3s for better UX while still preventing rate limits
        lang_prompt = f"告诉我以下文本是什么语种，直接输出语种，如法语，无需输出标点符号: ```{issue}```"
        lang = get_completion_ollama(lang_prompt)
        print(f"原始消息 ({lang}): {issue}\n")
        
        trans_prompt = f"""
        将以下消息分别翻译成英文和中文，并写成
        中文翻译：xxx
        英文翻译：yyy
        的格式：
        ```{issue}```
        """
        response = get_completion_ollama(trans_prompt)
        print(f"{response}\n{'='*41}")

def format_conversion(data):
    """Convert between different data formats."""
    prompt = f"""
    将以下Python字典从JSON转换为HTML表格，保留表格标题和列名：{data}
    """
    get_completion_ollama(prompt)
    prompt = f"""
    将以下Python字典从HTML表格转换为JSON格式：{data}
    """
    get_completion_ollama(prompt)

def spelling_grammar_check():
    """Demonstrate spelling and grammar checking capabilities."""
    prompts = [
        """请检查以下文本的拼写和语法错误，给出修改建议：
        ```我昨天去商场买东西。店里人很多，我花了2个小是才买完。```""",
        
        """请纠正以下英文文本中的拼写和语法错误：
        ```I goes to the store yesterday and buyed some food.```""",
        
        """分析下面这段话的语法结构，指出主谓宾：
        ```小明在图书馆认真地学习数学。```"""
    ]
    
    for i in range(len(prompts)):
        time.sleep(3)  # Reduced from 20s to 3s
        prompt = f"""请校对并更正以下文本，注意纠正文本保持原始语种，无需输出原始文本。
        如果您没有发现任何错误，请说"未发现错误"。
        
        例如：
        输入：I are happy.
        输出：I am happy.
        ```{prompts[i]}```"""
        response = get_completion_ollama(prompt)
        print(i, response)

if __name__ == "__main__":
    spelling_grammar_check()
