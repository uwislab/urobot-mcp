# script6.py
from interpreter import interpreter

interpreter.offline = True
interpreter.llm.model = "ollama/llama3:8b"
interpreter.llm.api_base = "http://localhost:11434"

interpreter.chat("定位：一个能生成 C 语言程序的智能助手。"
                 "能力：可以根据用户提供的需求准确生成相应的 C 语言代码，并以文本格式保存。"
                 "知识储备：熟练掌握 C 语言的各种语法、数据结构、算法及标准库函数。"
                 "请根据以下需求生成 C 语言代码，："
                 "实现一个朴素贝叶斯算法，使用python调用os包将生成的C语言代码作为文本保存到本地,不需要C语言代码运行只需要保存到本地"
                 "保存位置C:\PlantUML\plantuml_graphviz_word2019_template_win64\sort.c")