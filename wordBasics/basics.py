
import os
from pyltp import SentenceSplitter
from pyltp import Postagger, Segmentor
import jieba.posseg as pseg
import jiagu




# 分句
def sentence_splitter(text):
    sents = SentenceSplitter.split(text)
    sents_list = list(sents)
    return sents_list


def seg_pos(text, method=2):
    word_tag_list = []
    postags_list = []
    words_list = []
    if method==1:  # jieba
        results = pseg.cut(text)
        for r in results:
            words_list.append(r.word)
            postags_list.append(r.flag)
            word_tag_list.append(r.word + '/' + r.flag)
        print(type(postags_list))

    if method==2:  # LTP
        segmentorltp = Segmentor()  # 实例化分词模块
        segmentorltp.load('D:\LTP\ltp_data_v3.4.0\cws.model')  # 加载分词库
        words_notlist = segmentorltp.segment(text)
        words_list=list(words_notlist)
        print(words_list)
        segmentorltp.release()
        postagger = Postagger()
        postagger.load('D:\LTP\ltp_data_v3.4.0/pos.model')
        postags = postagger.postag(words_list)
        for word, postag in zip(words_list, postags):
            word_tag_list.append(word + '/' + postag)
            # print(word + '/' + postag)
        postags_list = list(postags)
        postagger.release()

    if method==3:  # jiagu
        words_list = jiagu.seg(text)  # 分词
        postags_list = jiagu.pos(words_list)  # 词性标注
        for word, postag in zip(words_list, postags_list):
            word_tag_list.append(word + '/' + postag)
    return words_list, postags_list, word_tag_list





if __name__ == '__main__':
    text='今天，天气晴朗，姚明在体育场门口吃红苹果。'
    # text = input('请输入测试文本：')
    print('分句结果：', sentence_splitter(text))
    words, tags, word_postag_list = seg_pos(text)
    print('分词结果：', words)
    print('词性标注结果：', word_postag_list)
