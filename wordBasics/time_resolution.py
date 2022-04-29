
import os
from pyltp import SentenceSplitter
from pyltp import Postagger, Segmentor
import jieba
import jieba.posseg as pseg
import jiagu

import re
import datetime
import sxtwl


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


class TimeResolution:

    def __init__(self):        # 模型路径
        # 初始化模块
        self.lunar = sxtwl.Lunar()
        self.segmentor = Segmentor()
        self.postagger = Postagger()
        self.stopwords = {}.fromkeys([line.rstrip() for line in open(os.path.join(r'D:\Courses\FYP\AIPlatform_flask\dictionary','TimeStopWords.txt'), 'r',encoding='utf-8')])


    # 提取全部时间词
    def time_word_extract(self, words_list,postags_list):
        # 输出全部时间词
        time_word = []
        cutresult = []
        nt_num = [i for i, x in enumerate(postags_list) if x == 'nt']
        print(nt_num)
        for i in nt_num:
            cutresult.append(words_list[i])
        for obj in cutresult:
            if obj not in self.stopwords:
                time_word.append(obj)
        # 包含大写汉字的日期列表
        original_time_word=time_word

        for date_word in time_word :
            # 判断年
            if re.search(r"[零|一|二|三|四|五|六|七|八|九]{4}年", date_word):
                temp_date_word_position=time_word.index(date_word )
                final_year=''
                for i in date_word :
                    if i=='零':
                        final_year+='0'
                    elif i=='一':
                        final_year+='1'
                    elif i == '二':
                        final_year += '2'
                    elif i=='三':
                        final_year+='3'
                    elif i=='四':
                        final_year+='4'
                    elif i=='五':
                        final_year+='5'
                    elif i=='六':
                        final_year+='6'
                    elif i=='七':
                        final_year+='7'
                    elif i=='八':
                        final_year+='8'
                    elif i=='九':
                        final_year+='9'
                    elif i=='年':
                        final_year +='年'
                time_word[temp_date_word_position]=final_year
            # 判断月：一月到十月
            if re.search(r"[三|四|五|六|七|八|九]{1}月", date_word):
                temp_date_word_position=time_word.index(date_word )
                final_month_1=''
                for i in date_word :
                    if i=='三':
                        final_month_1+='3'
                    elif i=='四':
                        final_month_1+='4'
                    elif i=='五':
                        final_month_1+='5'
                    elif i=='六':
                        final_month_1+='6'
                    elif i=='七':
                        final_month_1+='7'
                    elif i=='八':
                        final_month_1+='8'
                    elif i=='九':
                        final_month_1+='9'
                    elif i=='月':
                        final_month_1 +='月'
                time_word[temp_date_word_position]=final_month_1
            if date_word =='一月':
                temp_date_word_position=time_word.index(date_word)
                time_word[temp_date_word_position]='1月'
            if date_word =='一月份':
                temp_date_word_position=time_word.index(date_word)
                time_word[temp_date_word_position]='1月份'
            if date_word =='二月':
                temp_date_word_position=time_word.index(date_word)
                time_word[temp_date_word_position]='2月'
            if date_word =='二月份':
                temp_date_word_position=time_word.index(date_word)
                time_word[temp_date_word_position]='2月份'
            if date_word =='十月':
                temp_date_word_position=time_word.index(date_word)
                time_word[temp_date_word_position]='10月'
            if date_word =='十月份':
                temp_date_word_position=time_word.index(date_word)
                time_word[temp_date_word_position]='10月份'
            if date_word =='十一月':
                temp_date_word_position=time_word.index(date_word)
                time_word[temp_date_word_position]='11月'
            if date_word =='十一月份':
                temp_date_word_position=time_word.index(date_word)
                time_word[temp_date_word_position]='11月份'
            if date_word =='十二月':
                temp_date_word_position=time_word.index(date_word)
                time_word[temp_date_word_position]='12月'
            if date_word =='十二月份':
                temp_date_word_position=time_word.index(date_word)
                time_word[temp_date_word_position]='12月份'

        # 汉字转换成数字后的日期
        temp_final_time=time_word

        return original_time_word, temp_final_time,nt_num, words_list

    # 提取准确时间词
    def date_extract(self, time_word):
        dic_year = {}
        dic_mon = {}
        dic_day = {}
        final_date = " "
        for i in range(len(time_word)):
            if re.search(r"\d{4}年", time_word[i]):
                dic_year[i] = time_word[i]
        for j in range(len(time_word)):
            if re.search(r"\d{1,2}月", time_word[j]) or re.search(r"\d{1,2}月份", time_word[j]):
                if time_word[j][-1] == '份':
                    dic_mon[j] = time_word[j][0:-1]
                else:
                    dic_mon[j] = time_word[j]

        for k in range(len(time_word)):
            if re.search(r"\d{1,2}日", time_word[k]) or re.search(r"\d{1,2}号", time_word[k]):
                dic_day[k] = time_word[k]
        if dic_year and dic_mon and dic_day:
            final_date = list(dic_year.values())[0] + list(dic_mon.values())[0] + list(dic_day.values())[0]
        elif dic_year and dic_mon:
            final_date = list(dic_year.values())[0] + list(dic_mon.values())[0]
        elif dic_mon and dic_day:
            final_date = list(dic_mon.values())[0] + list(dic_day.values())[0]
        elif dic_year:
            final_date = list(dic_year.values())[0]
        elif dic_mon:
            final_date = list(dic_mon.values())[0]
        elif dic_day:
            final_date = list(dic_day.values())[0]
        return final_date

    # 计算之前或之后日期
    def day_l_a(self, timeword, today, num):
        if re.search('年', today) and re.search('月', today) and re.search('日', today):
            loc_year = today.index('年')
            loc_mon = today.index('月')
            loc_day = today.index('日')
            day_l = datetime.datetime(int(today[0:loc_year]), int(today[loc_year+1:loc_mon]), int(today[loc_mon+1:loc_day])) + datetime.timedelta(days=num)
            time1 = str(day_l.strftime('%Y%m%d'))
            yesterday = time1[0:4] + '年' + time1[4:6] + '月' + time1[6:] + '日'
        elif re.search('月', today) and re.search('日', today):
            loc_mon = today.index('月')
            loc_day = today.index('日')
            time = datetime.datetime(2018, int(today[0:loc_mon]), int(today[loc_mon + 1:loc_day])) + datetime.timedelta(days=num)
            time1 = str(time.strftime('%Y%m%d'))
            yesterday = time1[4:6] + '月' + time1[6:] + '日'
        else:
            yesterday = timeword

        return yesterday

    # 计算之前或之后月份
    def month_l_a(self, timeword, today, num):
        if (re.search('年', today) and re.search('月', today) and re.search('日', today)) or (re.search('年', today) and re.search('月', today)):
            month_l = int(today[(today.index('年') + 1):(today.index('月') )])
            if month_l + num > 12:
                month = str(int(today[0:today.index('年')]) + 1) + '年' + str((month_l + num) % 12) + timeword[(timeword.index('月')):]
            elif month_l + num < 1:
                month = str(int(today[0:today.index('年')]) - 1) + '年' + str((month_l + num +12)) + timeword[(timeword.index('月')):]
            else:
                month = today[0:(today.index('年') + 1)] + str((month_l + num)) + timeword[(timeword.index('月')):]
        elif (re.search('月', today) and re.search('日', today)) or re.search('月', today):
            month_l = int(today[0:(today.index('月'))])
            if month_l + num > 12:
                month = str((month_l + num) % 12) + timeword[(timeword.index('月')):]
            elif month_l + num < 1:
                month = str((month_l + num + 12)) + timeword[(timeword.index('月')):]
            else:
                month = str((month_l + num)) + timeword[(timeword.index('月')):]
        else:
            month = timeword
        return month

    # 计算之前之后年份
    def year_l_a(self, timeword, today, num):
        if re.search('年', today):
            year = str(int(today[0:4]) + num) + timeword[timeword.index('年'):]
        else:
            year = timeword
        return year

    # 指代消除
    def date_resolution(self, final_date, nt_num, word_list):
        festival_solar = {
            "元旦": "1.1",
            "情人节": "2.14",
            "妇女节": "3.8",
            "植树节": "3.12",
            "消费者权益日": "3.15",
            "愚人节": "4.1",
            "清明节": "4.5",
            "清明": "4.5",
            "世界卫生日": "4.7",
            "世界地球日": "4.22",
            "劳动节": "5.1",
            "青年节": "5.4",
            "世界无烟日": "5.31",
            "无烟日": "5.31",
            "国际儿童节": "6.1",
            "儿童节": "6.1",
            "世界环境保护日": "6.5",
            "建党节": "7.1",
            "建军节": "8.1",
            "教师节": "9.10",
            "国庆": "10.1",
            "国庆节": "10.1",
            "平安夜": "12.24",
            "圣诞节": "12.25"
        }
        festival_lunar = {
            "春节": "1.1",
            "元宵节": "1.15",
            "元宵": "1.15",
            "龙抬头": "2.2",
            "春龙节": "2.2",
            "端午节": "5.5",
            "端午": "5.5",
            "七夕": "7.7",
            "中元节": "7.15",
            "中元": "7.15",
            "中秋节": "8.15",
            "中秋": "8.15",
            "重阳节": "9.9",
            "重阳": "9.9",
            "腊八节": "12.8",
            "腊八": "12.8",
            "小年": "12.23",
            "除夕": "12.30"
        }
        for i in nt_num:
            if word_list[i] in festival_solar.keys():
                if re.search('年', final_date):
                    festival = self.lunar.getDayBySolar(int(final_date[0:(final_date.index('年'))]),
                                                        int(festival_solar[word_list[i]].split(".")[0]),
                                                        int(festival_solar[word_list[i]].split(".")[-1]))
                    word_list[i] = str(festival.y) + '年' + str(festival.m) + '月' + str(festival.d) + '日'
                else:
                    word_list[i] = word_list[i]
            elif word_list[i] in festival_lunar.keys():
                if re.search('年', final_date):
                    festival = self.lunar.getDayByLunar(int(final_date[0:(final_date.index('年'))]),
                                                        int(festival_solar[word_list[i]].split(".")[0]),
                                                        int(festival_solar[word_list[i]].split(".")[-1]))
                    word_list[i] = str(festival.y) + '年' + str(festival.m) + '月' + str(festival.d) + '日'
                else:
                    word_list[i] = word_list[i]
            elif word_list[i] in {"今天", "今日", "本日"} and re.search('日', final_date):
                word_list[i] = self.day_l_a(word_list[i], final_date, 0)
            elif word_list[i] in {"昨天", "昨日"} and re.search('日', final_date):
                word_list[i] = self.day_l_a(word_list[i], final_date, -1)
            elif word_list[i] in {"前天", "前日"} and re.search('日', final_date):
                word_list[i] = self.day_l_a(word_list[i], final_date, -2)
            elif word_list[i] in {"大前天", "大前日"} and re.search('日', final_date):
                word_list[i] = self.day_l_a(word_list[i], final_date, -3)
            elif word_list[i] in {"明天", "明日"} and re.search('日', final_date):
                word_list[i] = self.day_l_a(word_list[i], final_date, 1)
            elif word_list[i] in {"后天", "后日"} and re.search('日', final_date):
                word_list[i] = self.day_l_a(word_list[i], final_date, 2)
            elif word_list[i] in {"大后天", "大后日"} and re.search('日', final_date):
                word_list[i] = self.day_l_a(word_list[i], final_date, 3)
            elif word_list[i] in {"本月", "本月初", "本月底", "本月中"} and re.search('月', final_date):
                word_list[i] = self.month_l_a(word_list[i], final_date, 0)
            elif word_list[i] in {"上月", "上月初", "上月底", "上月中"} and re.search('月', final_date):
                word_list[i] = self.month_l_a(word_list[i], final_date, -1)
            elif word_list[i] in {"上上月", "上上月初", "上上月底", "上上月中"} and re.search('月', final_date):
                word_list[i] = self.month_l_a(word_list[i], final_date, -2)
            elif word_list[i] in {"下月", "下月初", "下月底", "下月中"} and re.search('月', final_date):
                word_list[i] = self.month_l_a(word_list[i], final_date, 1)
            elif word_list[i] in {"下下月", "下下月初", "下下月底", "下下月中"} and re.search('月', final_date):
                word_list[i] = self.month_l_a(word_list[i], final_date, 2)
            elif word_list[i] in {"今年", "今年初", "今年底", "今年中"} and re.search('年', final_date):
                word_list[i] = self.year_l_a(word_list[i], final_date, 0)
            elif word_list[i] in {"去年", "去年初", "去年底", "去年中"} and re.search('年', final_date):
                word_list[i] = self.year_l_a(word_list[i], final_date, -1)
            elif word_list[i] in {"前年", "前年初", "前年底", "前年中"} and re.search('年', final_date):
                word_list[i] = self.year_l_a(word_list[i], final_date, -2)
            elif word_list[i] in {"明年", "明年初", "明年底", "明年中"} and re.search('年', final_date):
                word_list[i] = self.year_l_a(word_list[i], final_date, 1)
            elif word_list[i] in {"后年", "后年初", "后年底", "后年中"} and re.search('年', final_date):
                word_list[i] = self.year_l_a(word_list[i], final_date, 2)
            elif re.search('月', word_list[i]) and re.search('年', final_date) and word_list[i-1][-1] != '年':
                day_result = final_date[:4] + '年' + word_list[i]
                word_list[i] = day_result
        final_resolution = ''.join(word_list)
        # fp.write(final_resolution)
        return final_resolution

    def timeReApi(self, text, words_list,postags_list):
        # text = "2018年我国宽带网络全面提速，去年，我国国家人口、企业法人、自然资源等基础数据库建成，71个部门、32个地方全面接入国家电子政务外网和国家数据共享交换平台，数据共享交换总量累计超过394亿条次"
        print('原文本内容为：',text )
        original_time_word, time_word,nt, words_list = self.time_word_extract(words_list,postags_list)
        print('第一步：time_word_extract结果：' )
        print('①：original_time_word',original_time_word )
        print('②：time_word', time_word)
        print('③：nt', nt)
        print('④：words_list', words_list)
        time = self.date_extract(time_word)
        print('第二步：date_extract结果：',time)
        result = self.date_resolution(time, nt, words_list)
        print('第三步：date_resolution结果：',result )
        # 释放模型
        # TR.release_model()
        # return {"time_word":original_time_word,"before_rep":text,"after_rep":result}

        return original_time_word ,text ,result




if __name__ == '__main__':
    # text='今天，天气晴朗，姚明在体育场门口吃红苹果。'
    # text = input('请输入测试文本：')
    text='2018年五月1日，我国宽带网络全面提速，去年，我国国家人口、企业法人、自然资源等基础数据库建成，71个部门、32个地方全面接入国家电子政务外网和国家数据共享交换平台，截止到国庆节，数据共享交换总量累计超过394亿条次'
    print('分句结果：', sentence_splitter(text))
    words, tags, word_postag_list = seg_pos(text)
    print('分词结果：', words)
    print('词性标注结果：', word_postag_list)
    TR = TimeResolution()
    original_time_word, text, result = TR.timeReApi(text, words,tags)
    print(200 * '*')
    print('时间名称消解后的文本为：', result)
