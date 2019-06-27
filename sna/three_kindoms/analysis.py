#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys


def read_basic_data(src_file):
    with open(src_file, 'rt') as file:
        data = file.read()
    return data


if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf8')
    print(unicode('宋江', 'utf-8'))
    novel_data = read_basic_data('./data/shuihuzhuan.csv')
    novel_data = novel_data.replace('\n', '')
    novel_set = novel_data.split(' ')
    novel_set = [k for k in novel_set if k != '']
    songjiang_set = [k for k in novel_set if unicode('宋江', 'utf-8') in k]

    print(novel_set[0].encode('utf-8'))
    # print songjiang_set
    # heros = pd.read_excel('水浒人物.xlsx')
    #
    # heros['出场段落'] = 0
    # heros.sort_values('出场段落', ascending=False, inplace=True)
    # attr = heros['姓名'][0:10]
    # v1 = heros['出场段落'][0:10]
    # bar = Bar("水泊梁山年收入TOP10")
    # bar.add("年收入（万）", attr, v1, is_stack=True, is_label_show=True)
    # bar.render('水泊梁山年收入TOP10.html')
    #
    # net_df = pd.DataFrame(columns=['Source', 'Target', 'Weight', 'Source_Ratio', 'Target_Ratio'])
    # for i in range(0, 107):
    #     for j in range(i + 1, 108):
    #         this_weight = len([k for k in novel_set if heros['使用名'][i] in k and heros['使用名'][j] in k])
    #         net_df = net_df.append({'Source': heros['姓名'][i], 'Target': heros['姓名'][j], 'Weight': this_weight,
    #                                 'Source_Ratio': this_weight / heros['出场段落'][i],
    #                                 'Target_Ratio': this_weight / heros['出场段落'][j]}, ignore_index=True)
    #         print(str(i) + ':' + str(j))
