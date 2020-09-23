import time
from selenium import webdriver
from pyquery import PyQuery as pq


def openurl(url):
    browser = webdriver.Chrome()
    browser.get(url)
    html = browser.page_source
    data = str(pq(html))
    print(data)
    time.sleep(3)

    urls = browser.find_elements_by_xpath('//div[@class="pic"]/a')
    print(urls)
    #把点击链接全部append到一个list
    click_urls = []
    for url in urls:
        if 'https://movie.douban.com/subject/' in url.get_attribute('href'):
            click_urls.append(url.get_attribute('href'))
    print(click_urls)
    for i in range(len(click_urls)):
        link = click_urls[i]
        browser.get(link)
        time.sleep(1)
        #获取所有的窗口句柄
        handles = browser.window_handles
        #原主窗口
        index_handle = browser.current_window_handle
        #因为即使点击新的链接，浏览器还是定位在原窗口，需要加判断
        for handle in handles:
            if handle != index_handle:
                browser.switch_to.window(handle)
            else :
                continue
        try:
            name = browser.find_element_by_xpath('//h1/span').text
            #跳转之后页面的编剧信息
            director = browser.find_element_by_xpath('//div[@id="info"]/span[2]/span[@class="attrs"]').text
            with open('file.txt','a+',encoding='utf-8')as f:
                f.write(name)
                f.write(director+'\n')
        except Exception:
            print("not exist")
            continue


if __name__ == '__main__':
     for offset in range(0,250,25):
         time.sleep(1)
         url = 'https://movie.douban.com/top250?start={}'.format(offset)+'&filter'
         openurl(url)