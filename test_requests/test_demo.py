from pprint import pprint

import requests
from requests import Session, Response

proxies = {
    #代理
    'http':'http://127.0.0.1:8888',
    'https':'https://127.0.0.1:8888'
}

url_get = 'https://home.testing-studio.com/get'

def test_requests():
    #r = requests.get('https://home.testing-studio.com/categories.json')
    # print(r.content)  #返回的内容，为原生的，完全是二进制
    # print(r.text)     #utf8 gbk 自动解码

    #print(r.request) #请求方法
    # print(r.headers) #resoponse的header
    # print(r)
    # pprint(r)
    # print(r.status_code)
    # print(r.json())

    #print(r.text)

    # 可以请求任何方法，可以写出http协议里面没有的内容
    r1 = requests.request('xxx','https://home.testing-studio.com/categories.json')



# get请求
def test_get():
    # 请注意请求的链接地址，不是域名噢
    # get使用params
    r = requests.get('https://httpbin.testing-studio.com/get', params={
        "a": 1,
        "b": 2,
        "c": "ccc"

    })

    assert r.status_code == 200
    print(r.json())


# post请求 form表单
def test_post():
    # 请注意请求的链接地址，不是域名噢
    # post使用data
    r = requests.post('https://httpbin.testing-studio.com/post',
                      data={
        "a": 1,
        "b": 2,
        "c": "ccc"

    },
                      # 新增post传递query参数
                      params={
                          "a": 'query',
                          "b": 2,
                          "c": "333"

                      },

                      #使用proxies,网站会检查是否使用代理，第一种是信任证书，第二种关闭掉ssl校验
                      proxies = proxies,
                      verify = False #关闭掉ssl校验
                      )

    assert r.status_code == 200
    print(r.json())


# 文件上传
def test_upload():
    # 注意传文件时，要保证文件有内容，这样打印print(r.json())时就可以发现file里面的内容
    r = requests.post(
        'https://httpbin.testing-studio.com/post',
        #文件只是打开了，所以拿不到文件名
        #打印文件信息时，只要'files':{'file':''}解析到file内容就是正确的,文件有内容,文件内容会在里面进行展示
        files={'file': open('__init__.py', 'rb')},
        headers={'Content-Type': 'application/plain','h':'head demo'},
        #使用的是cookies,不是cookie，不然会报错
        cookies={'name':'zhangkai'},

        proxies = proxies,
        verify = False
    )
    assert r.status_code == 200
    assert r.json()["headers"]['H'] == 'head demo'



def test_session():
    s = Session()
    #session里面加一次，到时候访问所有页面都会带有
    s.proxies=proxies
    s.verify = False
    s.get(url_get)

def test_hook():
    #给r添加一个类型为Response,由于会报错，所以后面把指定类型删除了
    def modify_response(r,*args,**kwargs):
        r.content = "ok hook success"
        r.demo="demo content"
        return r #返回使修改生效


    # 请注意请求的链接地址，不是域名噢
    # get使用params
    r = requests.get('https://httpbin.testing-studio.com/get', params={
        "a": 1,
        "b": 2,
        "c": "ccc"

    },
        hooks = {"response":[modify_response]} #不要加括号，只给一个方法名称modify_response)
 )
