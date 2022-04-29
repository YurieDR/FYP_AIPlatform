# coding=utf-8
# LTP相关
import os
from pyltp import SentenceSplitter
from pyltp import Postagger
from pyltp import Parser
from pyltp import SementicRoleLabeller
import jieba


# 分句
def sentence_splitter(text):
    sents = SentenceSplitter.split(text)
    sents_list = list(sents)
    return sents_list


# 分词
def segmentor(text):
    # jieba.load_userdict('dictionary/information_safety')
    words = jieba.lcut(text)
    return words


# 词性标注
def posttagger(words):
    word_tag_list = []
    posttagger = Postagger()
    posttagger.load('D:\LTP\ltp_data_v3.4.0/pos.model')
    postags = posttagger.postag(words)
    for word, postag in zip(words, postags):
        word_tag_list.append(word + '/' + postag)
        print(word + '/' + postag)
    postags_list = list(postags)
    posttagger.release()
    return postags_list, word_tag_list


# 句法分析
def parser(words, postags):
    result_temp = []
    par = Parser()
    par.load('D:\LTP\ltp_data_v3.4.0/parser.model')
    partags = par.parse(words, postags)
    # print("\t".join("%d:%s" % (partag.head, partag.relation) for partag in partags))
    rely_id = [arc.head for arc in partags]  # 提取依存父节点id
    relation = [arc.relation for arc in partags]  # 提取依存关系
    heads = ['Root' if id == 0 else words[id - 1] for id in rely_id]  # 匹配依存父节点词语
    for i in range(len(words)):
        print(relation[i] + '(' + words[i] + ', ' + heads[i] + ')')
        result_temp.append(relation[i] + '(' + words[i] + ', ' + heads[i] + ')')
    par.release()
    return partags, result_temp


# 语义角色标注
def srl(words, postags):
    labeller = SementicRoleLabeller()
    labeller.load('D:\LTP\ltp_data_v3.4.0/pisrl_win.model')
    arcs = parser(words, postags)
    roles = labeller.label(words, postags, arcs)
    for role in roles:
        print(role.index, "".join(
            ["%s:(%d,%d)" % (arg.name, arg.range.start, arg.range.end) for arg in role.arguments]))

    labeller.release()
    return roles


if __name__ == '__main__':
    text='今天，天气晴朗，姚明在体育场门口吃红苹果。'
    # text = input('请输入测试文本：')
    print('分句结果：', sentence_splitter(text))
    print('分词结果：', segmentor(text))
    words = segmentor(text)
    tags, word_postag_list = posttagger(words)
    print('词性标注结果：', word_postag_list)
    arcs, temp=parser(words, tags)
    print('句法分析结果：', parser(words, tags))

    srl_model_path = os.path.join(os.path.dirname(__file__), 'D:\LTP\ltp_data_v3.4.0/pisrl_win.model')  # 语义角色标注模型目录路径

    labeller = SementicRoleLabeller()  # 初始化实例
    labeller.load(srl_model_path)  # 加载模型
    roles = labeller.label(words, tags, arcs)  # 语义角色标注
    print(roles)  # type: object

    # 打印结果
    for role in roles:
        print(words[role.index], end=' ')
        print(role.index,
              "".join(["%s:(%d,%d) " % (arg.name, arg.range.start, arg.range.end) for arg in role.arguments]))

    # 释放模型

    labeller.release()

