import requests
import json
import re
from tqdm import tqdm
import radar


def get_content():
    content = ("你是一个人工智能助手，你将帮助开发人员生成可靠的指令对进行评估，指令内容要求如下：\n"
               "1.你将扮演一个经验丰富的查案人员，你的工作是针对不同的案件提出不同的历史案件信息查询，从而帮助你破案；\n"
               "2.指令内容应该尽可能多样化，指令所问的内容应该是多样化的，可以对所有案件相关信息进行询问；\n"
               "3.指令可以是问句、陈述句或者其他合适的形式；\n"
               "4.指令的内容应该是真实、复杂、富有挑战性的，涉及到各种复杂的SQL操作，例如：2020年发生在公园的性侵案件中，受害人是14周岁以下女性的，身高最高的嫌疑人的姓名；\n"
               "5.你应该尽可能将指令的内容翻译成对应的SQL语句，表结构如下：\n"
               "CREATE TABLE IF NOT EXISTS CASES(\n"
               "AJBH VARCHAR(20) NOT NULL COMMENT '案件编号，案件的唯一编号',\n"
               "AJMC VARCHAR(20) NOT NULL COMMENT '案件名称',\n"
               "AJLX VARCHAR(20) NOT NULL COMMENT '案件类型，[性侵案件，抢劫案件，偷盗案件]',\n"
               "AJMS VARCHAR(100) NOT NULL COMMENT '案件描述，对案件现场的描述',\n"
               "AJDD_S VARCHAR(100) NOT NULL COMMENT '案件地点-城市，案件发生地点所在的城市，[上海市]',\n"
               "AJDD_Q VARCHAR(100) NOT NULL COMMENT '案件地点-区县，案件发生地点所在的区县，[黄浦区，徐汇区，长宁区，静安区，普陀区，虹口区，杨浦区，闵行区，宝山区，嘉定区，浦东新区，金山区，松江区，青浦区，奉贤区，崇明区]',\n"
               "AJDD VARCHAR(100) NOT NULL COMMENT '案件地点，案件发生的详细地点',\n"
               "AJSJ DATETIME NOT NULL COMMENT '案件时间，案件发生的时间',\n"
               "XYRXM VARCHAR(20) NOT NULL COMMENT '嫌疑人姓名',\n"
               "XYRSFZH VARCHAR(50) NOT NULL COMMENT '嫌疑人身份证号',\n"
               "XYRXB VARCHAR(20) NOT NULL COMMENT '嫌疑人性别，[男，女]',\n"
               "XYRNL INT(4) NOT NULL COMMENT '嫌疑人年龄（岁）',\n"
               "XYRSG INT(4) NOT NULL COMMENT '嫌疑人身高（cm）',\n"
               "XYRTZ INT(4) NOT NULL COMMENT '嫌疑人体重（kg）',\n"
               "XYRWM VARCHAR(100) NOT NULL COMMENT '嫌疑人外貌，嫌疑人的外貌描述',\n"
               "BHRXM VARCHAR(20) NOT NULL COMMENT '被害人姓名',\n"
               "BHRSFZH VARCHAR(50) NOT NULL COMMENT '被害人身份证号',\n"
               "BHRXB VARCHAR(20) NOT NULL COMMENT '被害人性别，[男，女]',\n"
               "BHRNL INT(4) NOT NULL COMMENT '被害人年龄（岁）',\n"
               "BHRSG INT(4) NOT NULL COMMENT '被害人身高（cm）',\n"
               "BHRTZ INT(4) NOT NULL COMMENT '被害人体重（kg）',\n"
               "BHRWM VARCHAR(100) NOT NULL COMMENT '被害人外貌，被害人的外貌描述',\n"
               "PRIMARY KEY(AJBH)\n"
               ")ENGINE=INNODB DEFAULT CHARSET=utf8;\n"
               "6.请给出10条符合JSON格式的指令对，格式：\n"
               "{\n"
               "\t\"instruction\": \"\";\n"
               "\t\"output\": \"\"\n"
                "}\n")
    return content


def get_payload():
    payload = {
        "model": "gpt-3.5-turbo-0613",
        "messages": [
            {
                "role": "user",
                "content": get_content()
            }
        ],
        "stream": False
    }
    return payload


def main():
    proxy = '127.0.0.1:7890'

    proxies = {
        'http': 'http://' + proxy,
        'https': 'https://' + proxy
    }
    url = r'https://cfwus02.opapi.win/v1/chat/completions'
    headers = {
        'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
        'Content-Type': 'application/json',
        'Authorization': 'Bearer sk-BOATTlUU478801532161T3BLbkFJA37E314ccd1949efa37d'
    }
    sql_data = list()
    with tqdm(range(50), desc='Crawling') as tq:
        for bar in tq:
            try:
                response = requests.post(url=url, headers=headers, data=json.dumps(get_payload()))
                data = json.loads(response.text)
                result = data['choices'][0]['message']['content']
                r = re.findall('{(.*?)}', result, re.DOTALL)
                for i in r:
                    origin = json.loads('{'+i+'}')
                    sql_data.append(origin)
            except Exception as e:
                print(e)
                pass
    with open('./finetune_data.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(sql_data, ensure_ascii=False, indent=1))


if __name__ == '__main__':
    main()