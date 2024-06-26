import requests
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.middleware.csrf import get_token
from page.models import *
from page.views import platforms
import threading
from platformReddit.post import Post


class ServerView:
    def UpdateSetting(request):
        setting = Setting.objects.all().first()
        setting.theme = request.POST.get('theme')
        setting.redditSize = request.POST.get('reddit')
        setting.youtubeSize = request.POST.get('youtube')
        setting.everytimeSize = request.POST.get('everytime')
        setting.save()
        return redirect(request.META.get('HTTP_REFERER', '/home'))
    def Disconnect(request):
        cookies = {'csrftoken': get_token(request)}
        headers = {
                'Content-Type': 'application/json',
                'csrfmiddlewaretoken': get_token(request),  # 'X-CSRFToken': 'token
                'X-CSRFToken': get_token(request)
        }
        for platform in platforms():
            url = f'http://127.0.0.1:8000/{platform}/disconnect/'
            requests.post(url, cookies=cookies, headers=headers)
        return redirect('http://127.0.0.1:8000/accounts', cookies=cookies, headers=headers)

    def GetContent(request):
        thread = []
        def sendRequest(url, cookies, headers):
            requests.post(url, cookies=cookies, headers=headers)
            print(f"Successfully requested content from {url}")

        ContentDB.objects.all().delete()
        FileDB.objects.all().delete()
        cookies = { 'csrftoken': get_token(request) }
        headers = { 'Content-Type': 'application/json','csrfmiddlewaretoken': get_token(request),'X-CSRFToken': get_token(request) }
        for account in AccountDB.objects.all():
            if (account.connected == False):
                continue
            url = f'http://127.0.0.1:8000/{account.platform}/get-content/'
            t = threading.Thread(target=sendRequest, args=(url, cookies, headers))
            t.start()
            thread.append(t)
        for t in thread:
            t.join()
        return redirect('http://127.0.0.1:8000/home/', cookies=cookies)
        
    def Post(request):
        if request.method == "POST":
            file = None
            if 'File' in request.FILES:
                file = request.FILES['File']              
            data = {
                "title": request.POST.get("title"),
                "text": request.POST.get("text"),
            }
  
            headers = {
                'Content-Type': 'application/json',
                'csrfmiddlewaretoken': get_token(request),  # 'X-CSRFToken': 'token
                'X-CSRFToken': get_token(request)
            }
            base_url = "http://localhost:8000"  # 기본 URL 설정

            for platform in platforms():
                if request.POST.get(platform):
              
                    url = f'{base_url}/{platform}/post/'
                    try:
                        
                        cookies = {
                            'csrftoken': get_token(request),
                        }
                    
                        response = requests.post(url, json=data,headers=headers, cookies=cookies)
                        if response.status_code:
                    
                            if platform == 'Reddit':
                                print("Reddit")
                                success = Post(data['title'], text=data['text'], image=file)
                            elif platform == "Youtube":
                                print("Youtube")
                            print(f"Successfully posted to {platform}")
                        else:
                            print(f"Failed to post to {platform}: {response.status_code} {response.text}")
                    except requests.exceptions.RequestException as e:
                        print(f"Request to {platform} failed: {e}")
            
            return redirect('http://127.0.0.1:8000/create')
        return redirect(request.META.get('HTTP_REFERER', '/home'))
    def ClearContent(request):
        ContentDB.objects.all().delete()
        FileDB.objects.all().delete()
        headers = {
            'Content-Type': 'application/json',
            'csrfmiddlewaretoken': get_token(request),  # 'X-CSRFToken': 'token
            'X-CSRFToken': get_token(request)
        }
        cookies = {
            'csrftoken': get_token(request)
        }
        redirect('http://127.0.0.1:8000/server/get-content/', cookies=cookies, headers=headers)
        return redirect(request.META.get('HTTP_REFERER', '/home'))