'''

所有的接口需使用HTTPS协议、JSON数据格式、UTF8编码。
'''
import json

import requests


class TestWeWork:
    token_url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken'
    corpid = 'ww90f0c479861a01d9'                           #公司corpid
    secret = 'k4M6z7gKERLbZHL6JwCFujqQU9RzCTJSdyzc0lmei0Y'  #应用管理-测试开发11期secret
    secret_groupchat = 'C0ue_JECOL4zaTK0OD0c3VrZviJypYqU3G773nX44b8' #客户联系-客户secret
    access_token = None
    chatid = None


    @classmethod     #装饰器，代表是一个类，cls只是一个泛指
    def setup_class(cls):
        #获取token
        r = requests.get(cls.token_url,
                         params={'corpid': cls.corpid,
                                 'corpsecret': cls.secret_groupchat
                                 }
                         )
        #print(r.json())
        cls.access_token = r.json()['access_token']
        print(cls.access_token)


        #获取chatid
        payload = {
            'offset': 0,  # 0代表的第一页
            'limit': 100
        }
        '''
         post请求，1.如果是data，数据是以form表单进行发送，如果给词典是form数据，如果不给词典，给文本，那就表示文本以二进制发送出去。
         2.如果是json，会先把词典转换成Json结构，再通过data请求体结构发送出去
        '''
        r = requests.post('https://qyapi.weixin.qq.com/cgi-bin/externalcontact/groupchat/list',
                          # params= 指的是query，通过获取客户群列表api可以查看
                          params={
                              'access_token': cls.access_token,
                          },
                          json=payload
                          )

        assert r.json()['errcode'] == 0
        print(r.json())
        cls.chatid = r.json()['group_chat_list'][0]['chat_id']

    def test_get_token(self):
        r = requests.get(self.token_url,
                         params={'corpid': self.corpid,
                                 'corpsecret': self.secret
                                 }
                         )
        print(r.json())
        access_token = r.json()['access_token']
        print(access_token)

    def test_get_token_exist(self):
        assert self.access_token is not None
        print(self.access_token)


    #获取企业微信列表

    #封装的核心：把不变的东西剥离出来，变化的东西留下来进行维护
    def test_groupchat_get(self):
        payload = {
            'offset': 0,  #0代表的第一页
            'limit': 100
        }
        '''
         post请求，1.如果是data，数据是以form表单进行发送，如果给词典是form数据，如果不给词典，给文本，那就表示文本以二进制发送出去。
         2.如果是json，会先把词典转换成Json结构，再通过data请求体结构发送出去
        '''
        r = requests.post('https://qyapi.weixin.qq.com/cgi-bin/externalcontact/groupchat/list',
                         #params= 指的是query，通过获取客户群列表api可以查看
                         params={
                             'access_token':self.access_token,
                         },
                          json=payload
                          )

        assert r.json()['errcode'] == 0
        print(r.json())
        #self.chatid = r.json()['group_chat_list'][0]['chat_id']
        #print(self.chatid)



    def test_groupchat_detail(self):
        r = requests.post('https://qyapi.weixin.qq.com/cgi-bin/externalcontact/groupchat/get',
                          params = {'access_token':self.access_token},
                          json = {'chat_id':self.chatid}
                          )
        assert r.json()['errcode'] == 0
        #print(r.json())
        print(json.dumps(r.json(), indent=2)) #将json数据打印时格式化进行展示
        assert len(r.json()['group_chat']['member_list']) > 0