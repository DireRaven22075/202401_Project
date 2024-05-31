from django.shortcuts import render
from django.http import HttpResponse
from . import sql

parameters = {
    "chats": [
        {
            "icon": "https://www.facebook.com/images/fb_icon_325x325.png",
            "target": "한철연",
            "topMessage": "뭐함",
            "time": "2020-01-01 12:00:00",
            "unread": 3
        },
        # 기타 파라미터들...
    ],
    "contents": [
        {
            "platform": "Facebook",
            "account": "AEK",
            "time": "2020-01-01 12:00:00",
            "text": "TTTT",
            "image": "https://cdn.mos.cms.futurecdn.net/2aeE963L5B7jnfCAWFoFYW-1920-80.jpg.webp"
        },
        # 기타 콘텐츠들...
    ],
    "accounts": [
        {
            "connected": 1,
            "platform": "Facebook",
            "id": "gskids053",
            "name": "DireRaven22075",
            "tag": "hanyoonsoo"
        },
        # 기타 계정들...
    ]
}

def Welcome(request):
    return render(request, 'home.html', parameters)

def Home(request):
    return render(request, 'home.html', parameters)

def Post(request):
    return render(request, 'post.html', parameters)

def Find(request):
    return render(request, 'find.html', parameters)

def Menu(request):
    return render(request, 'menu.html', parameters)

def DBINIT(request):
    sql.Account.deleteDataAll()
    sql.Account.addData('Facebook', 'gskids053')
    return render(request, 'menu.html', parameters)

def DBTest(request):
    result = sql.get_account()
    sql.Account.test()
    return HttpResponse(result)

def Disconnect(request):
    platform = request.POST.get('platform')
    sql.Account.deleteData(platform)
    return render(request, 'menu.html', parameters)