from django.shortcuts import render
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from page.models import ContentDB, FileDB
from .utils import sleep, quit_driver_forcefully
from .account import Account
from django.db.models import Count, Max
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

MAX_POSTS = 10
default_user_icon = "https://cf-fpi.everytime.kr/0.png"

class Content(Account):
    def __init__(self, request):
        super().__init__(request)
 
    
    #DB에 값만 저장
   
    def free_field(self):
        if self.driver is None:
            self.driver = Account.initialize_driver()
            self.driver = self.login()
           
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'logged'))
            )
            sleep()
            
            free_field_box = self.driver.find_element(By.XPATH, "//*[@id=\"submenu\"]/div/div[2]/ul/li[1]/a")
            free_field_box.click()

            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//*[@id=\"writeArticleButton\"]"))
            )
            sleep()
            
            for i in range(MAX_POSTS, 0, -1):
                post = self.driver.find_element(By.XPATH, f'//*[@id="container"]/div[5]/article[{i}]/a')
                info = self.driver.find_element(By.XPATH, f'//*[@id="container"]/div[5]/article[{i}]/a/div/div')
                
            
                post_title = post.find_element(By.CLASS_NAME, 'medium').text
                post_text = post.find_element(By.XPATH, f"//*[@id=\"container\"]/div[5]/article[{i}]/a/div/p").text
                
                
                post_user = info.find_element(By.XPATH, f"//*[@id=\"container\"]/div[5]/article[{i}]/a/div/div/h3").text
                
                try:
                    post_vote = info.find_element(By.CLASS_NAME, "vote").text

                except:
                    post_vote = 0

                image_url = 0

                try:
                    image_list = []
                    #이미지 uid 이용해서 contentDB's image_url, FileDB's uid uid 값 주고 FileDB url 에 이미지 url 저장
                    post_image = post.find_element(By.CLASS_NAME, f"attachthumbnail").get_attribute("style")
                    image_list.append(post_image.split("\"")[1])
                    
                    
                    
                    latest = FileDB.objects.aggregate(max_uid=Max('uid'))['max_uid']
                    if latest is None:
                        latest = 0  # 최신 값이 없으면 0으로 초기화
                    image = None
                    if image_list:
                        for i, image in enumerate(image_list, start=1):
                            image_url = latest + 1

                            # # 이미지가 존재하는지 확인
                            # if not FileDB.objects.filter(url=image).exists():
                            #     # 이미지가 존재하지 않는 경우에만 저장
                            FileDB.objects.create(
                                uid=image_url,
                                url=image,
                            ).save()

                except NoSuchElementException:
                    image_url = 0
                ContentDB.objects.create(
                    platform = "Everytime",
                    userID = post_user,
                    text = post_title+"|||" + post_text,
                    image_url = image_url,
                    userIcon = default_user_icon,
                    vote = post_vote,
                ).save()       
                
        except Exception as e:
            return False
        finally:
            return True
            