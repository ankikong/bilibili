from selenium import webdriver
import re

driver = webdriver.Chrome()
driver.get("https://member.bilibili.com/video/upload.html")
a = driver.find_element_by_id("bili-upload-btn")
sou = driver.page_source
idd = re.findall('(?<=rt_rt)[^"]*', sou)[0]
idd = "rt_rt" + idd
d = a.find_element_by_id(idd).find_element_by_name("file")
d.send_keys("file path")
# check finished
driver.find_element_by_class_name("upload-status-intro").get_attribute("innerHTML") == '上传完成'
# select first auto picture for cover
driver.find_element_by_class_name("select-ai-covers").click()
# select 转载
driver.find_elements_by_class_name("check-radio-v2-name")[0].click()
# add source url
driver.find_element_by_class_name("copyright-v2-source-input-wrp").find_element_by_class_name("input-box-v2-1-val").send_keys("https://www.youtube.com/watch?v=fzMi6yf1Roc")
# select the most used block
driver.find_element_by_class_name("type-list-v2-selector-wrp").find_element_by_class_name("item-main").click()
# add tags, end with \n
driver.find_element_by_id("content-tag-v2-container").find_element_by_class_name("input-box-v2-1-val").send_keys("youtube")
# add video describe
driver.find_element_by_class_name("content-desc-v2-container").find_element_by_class_name("text-area-box-v2-val").send_keys("test")
# finish
driver.find_element_by_class_name("submit-btn-group-add").click()
