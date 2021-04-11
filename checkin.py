import sys
import time
import requests
import datetime
import traceback
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def pushWechat(desp, sckey):    #微信推送函数，默认只推送 签到失败 的状态，如果要推送其他状态，请在文件最后输出的部分添加 'pushWechat(desp, sckey)'
    send_url='https://sc.ftqq.com/' + sckey + '.send'
    params = {
        'text': '签到失败: '+ (datetime.datetime.utcnow() + datetime.timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S'),
        'desp': desp
    }
    requests.post(send_url,params=params)

def Checkin(desp, sckey):
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    browser = webdriver.Chrome('/usr/bin/chromedriver',options=chrome_options)
    try:
        try:
            browser.get('https://xmuxg.xmu.edu.cn/app/214')
            browser.find_element_by_xpath('//*[@id="loginLayout"]/div[3]/div[2]/div/button[2]').click()
        except:
            print('\n\n\n|||出错信息如下：|||\n\n\n')
            traceback.print_exc()
            pushWechat(desp, sckey)
            return 404
        time.sleep(10)
        browser.find_element_by_xpath('//*[@id="username"]').send_keys(input())
        browser.find_element_by_xpath('//*[@id="password"]').send_keys(input())
        time.sleep(5)
        browser.find_element_by_xpath('//*[@id="casLoginForm"]/p[4]').click()
        time.sleep(5)
        browser.get('https://xmuxg.xmu.edu.cn/app/214')
        time.sleep(10)
        browser.find_element_by_xpath('//*[@id="mainM"]/div/div/div/div[1]/div[1]/div[2]')
        browser.find_element_by_xpath('//*[@id="mainM"]/div/div/div/div[1]/div[2]/div/div[3]/div[2]').click()
        time.sleep(2)
        browser.find_element_by_xpath('/html/body').click()
        browser.find_element_by_xpath('/html/body/div[1]').click()
        browser.find_element_by_xpath('//*[@id="mainM"]/div').click()
        browser.find_element_by_xpath('//*[@id="mainM"]/div/div').click()
        browser.find_element_by_xpath('//*[@id="mainM"]/div/div/div/div[2]').click()
        browser.find_element_by_class_name('preview-container').click()
        browser.find_element_by_xpath('//*[@id="pdfDomContent"]').click()
        browser.find_element_by_xpath('//*[@id="pdfDom"]').click()
        time.sleep(5)
        b1 = browser.find_element_by_xpath('//*[@id="select_1582538939790"]/div')
        if b1.text.find('是 Yes') != -1:
            return 2
        else:
            b1.click()
            browser.find_element_by_xpath('/html/body/div[8]/ul/div/div[3]').click()
            browser.find_element_by_xpath('/html/body/div[1]/div/div/div/div/div[2]/div[1]/div/div/div/span/span').click()
            a1 = browser.switch_to.alert  # 通过switch_to.alert切换到alert
            time.sleep(1)
            a1.accept()  # alert“确认”
            time.sleep(1)
            browser.quit()
            return 1

    except Exception as e:
        print('\n\n\n|||出错信息如下：|||\n\n\n')
        traceback.print_exc()
        pushWechat(desp, sckey)
        browser.quit()
        return -1

desp = [':', '-', ' ']
sckey = input()
status = Checkin(desp, sckey)
if status == 1:
    print('\n\n\n|||签到成功|||\n\n\n')
elif status == 2:
    print('\n\n\n|||您今日已经签到过一次，请勿重复签到|||\n\n\n')
elif status == -1:
    print('\n\n\n|||签到失败，请检查网络或者账号设置|||\n\n\n')
elif status == 404:
    print('\n\n\n|||连接签到网站出错，等等再试|||\n\n\n')

sys.exit(0)
exit()
