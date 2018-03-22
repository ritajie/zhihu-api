import json
import requests
import re


def Header():
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'cookie': '_zap=a4939fc7-dd22-4432-b06d-1e17a5c53b54; _xsrf=925ea14f778acf5c7f5dbc51f905e019; d_c0="AODsZnXnNQ2PTl4-WJdPK-4G0039_Dwcqr0=|1519735744"; __DAYU_PP=RZaeQjbIbFYIiJFIAbEY72586ad54818; q_c1=55e1a61e9cc3489ca465a91aaba9be3e|1521427697000|1518745782000; capsion_ticket="2|1:0|10:1521448841|14:capsion_ticket|44:ZWNkMzM5NzU4NTQwNDI2ODhjNWFkNTBlNDBkZDZkODQ=|5fbe99f7ec2695647c9ed8bc156b568f8c86e83b29ed887fd94e8a66a339b993"; z_c0="2|1:0|10:1521449166|4:z_c0|92:Mi4xMzJEbEFRQUFBQUFBNE94bWRlYzFEU1lBQUFCZ0FsVk56c2FjV3dBS1pYZjQ1dWpNRHlFaTF2ZzlnOV9pbEc3Z293|b3d9026659951a00c2b3e38b54e2e2906b12fd3da71b2b061bd2083870145803"; __utma=155987696.810355594.1521544514.1521544514.1521544514.1; __utmz=155987696.1521544514.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)',
        'pragma': 'no-cache',
        'referer': 'https://www.zhihu.com/people/wu-yu-0427/following',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
    }
    return headers


def information(hername):
    "路小鹿的第一个原创api本体"
    url = 'https://www.zhihu.com/people/' + hername + '/activities'
    headers = Header()
    res = requests.get(url, headers=headers)
    jsonstr = re.findall(
        'data-state="({.*})" ', res.text)[0].replace('&quot', '"').replace(';', '')
    thejson = json.loads(jsonstr)
    return thejson.get('entities').get('users').get(hername)


def parser(thejson):
    "从json中提取各个信息"
    if type(thejson) == str:
        thejson = json.loads(thejson)
    name = thejson.get('name')
    urlToken = thejson.get('urlToken')
    avatarUrl = thejson.get('avatarUrl')
    gender = thejson.get('gender')
    description = thejson.get('description')
    # 居住地
    locations = []
    for eachlocation in thejson.get('locations'):
        locations.append(eachlocation.get('name'))
    # 公司职位
    employments = []
    for eachemploy in thejson.get('employments'):
        company = ""
        job = ""
        if eachemploy.get('company'):
            company = eachemploy.get('company').get('name')
        if eachemploy.get('job'):
            job = eachemploy.get('job').get('name')
        employments.append(company + '_' + job)
    # 职业领域
    business = ""
    if thejson.get('business'):
        business = thejson.get('business').get('name')
        # for eachbusiness in thejson.get('business').get('name'):
        # business.append(eachbusiness.get('name'))
    # 学校
    educations = []
    for eachedu in thejson.get('educations'):
        majar = ""
        school = ""
        if eachedu.get('major'):
            majar = eachedu.get('major').get('name')
        if eachedu.get('school'):
            school = eachedu.get('school').get('name')
        educations.append(majar + '_' + school)
    headline = thejson.get('headline')
    followerCount = thejson.get('followerCount')

    return name, urlToken, avatarUrl, gender, description, locations, employments, business, educations, headline, followerCount


def makeJsonstrBetter():
    "原声的json是放在html里的 格式混乱"
    file = open('2000个json(单引号原始版).txt', 'r')
    newfile = open('2017个json', 'w')
    for eachline in file:
        # 更正一些有毛病的字符：False True加上引号 ...
        eachline = eachline.replace('"', '___').replace("'", '"').replace(
            '\\xa0', '\\\\xa0').replace('False', '\"False\"').replace('True', '\"True\"')
        newfile.write(eachline)

    file.close()
    newfile.close()


if __name__ == '__main__':
file = open('2017个json', 'r')
newfile = open('完整的表.xls', 'w')
newfile.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t\n" % ('name', 'gender', 'followerCount', 'description', 'locations', 'employments', 'business', 'educations', 'headline', 'urlToken','avatarUrl'))
for line in file:
    arr = line.split('\t')
    name, urlToken, avatarUrl, gender, description, locations, employments, business, educations, headline, followerCount = parser(arr[2])

    newfile.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t\n" % (name, gender, followerCount, description, locations, employments, business, educations, headline, urlToken, avatarUrl))
file.close()
newfile.close()
print('gone!')
