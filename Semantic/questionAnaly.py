# 导入HanLP模块
from pyhanlp import *

# 加载命名实体识别模型
NER_MODEL = JClass('com.hankcs.hanlp.model.perceptron.PerceptronLexicalAnalyzer')(
    "data/model/perceptron/pku199801/cws.bin",
    "data/model/perceptron/pku199801/pos.bin",
    "data/model/perceptron/pku199801/ner.bin"
)

# 加载依存句法分析模型
DEP_MODEL = JClass('com.hankcs.hanlp.dependency.nnparser.NeuralNetworkDependencyParser')()

# 输入待处理文本
text = "李克强总理今天来我家了，我感到非常荣幸"

# 命名实体识别
ner_results = NER_MODEL.analyze(text)
for term in ner_results.iterator():
    if str(term.nature) in ['nr', 'nt', 'ns']:
        print(f"{term.word} : {term.nature}")

# 依存句法分析
dep_results = DEP_MODEL.parse(text)
for word in dep_results.iterator():
    print(f"{word.LEMMA} --({word.DEPREL})--> {word.HEAD.LEMMA}")
