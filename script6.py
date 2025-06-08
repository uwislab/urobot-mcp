# script6.py
from interpreter import interpreter

interpreter.offline = True
interpreter.llm.model = "ollama/llama3:8B"

interpreter.llm.api_base = "http://localhost:11434"

interpreter.chat("你是一个能生成 PlantUML 代码的智能助手。"
                 "能力：能够根据输入的描述准确生成 PlantUML 代码，并以文本文件形式提供。"
                 "知识储备：精通 PlantUML 语法及各类图形绘制规则。"
                 "请根据以下描述生成 PlantUML 代码，"
                 "以文本形式输出保存成 ：(包含学生、教师、课程、班级、选课记录、成绩、考勤等七个对象的学生管理系统)的PlantUML代码，"
                 "保存位置C:\PlantUML\plantuml_graphviz_word2019_template_win64\estuml.txt"
                 "1.只调用os的python包，2.将PlantUML代码在python代码中作为文本写入txt文件")