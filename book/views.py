from django.shortcuts import render
from bookupload.models import Book, Page, Object
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

def getbooks(request):
    #if request.META['HTTP_REFERER'].find("http://localhost:4200") != -1:
    try:
        print(request.META['HTTP_REFERER'])
    except Exception as err:
        print("Erro: ")
        print(err)
    if True: 
        if request.method == "GET":
            if Book.objects.exists() == True:
                json = {}
                book = 1
                for value in Book.objects.values():
                    json['book{0}'.format(book)] = value
                    book += 1
                response = JsonResponse(json)
                response['Access-Control-Allow-Origin'] = "*"
                return response
    response  = JsonResponse({"info" : "books not found"})
    response['Access-Control-Allow-Origin'] = "*"
    return response

@csrf_exempt
def setStack(request):
    if request.method == "POST":
        print("Data posted: ", request.POST)
        imgPath = request.POST['imgPATH']
        arr = imgPath.split("/")
        img = arr.pop()
        book_id = int(arr.pop().replace("book", ""))
        print("image: ", img, "BOOK_id: ", book_id)
        pg = Page.objects.get(BOOK_id = book_id, PAGINA = img)
        print("PAGE_id: ", pg.id, "BOOK_id", book_id)
        objs = Object.objects.filter(BOOK_id = book_id, PAGE_id = pg.id)
        print(1)
        for obj in objs:
            print("deleting Object of id = {0} from the PAGE_id = {1} and BOOK_id = {2}".format(obj.id, pg.id, book_id))
            obj.delete()
        print(2)
        for elem in request.POST:
            if elem.find("obj")!= -1:   
                obj = json.loads(request.POST[elem])
                Obj = Object(X = obj['x'], Y = obj['y'], MODE = obj['mode'], COLOR = obj['color'], WIDTH = obj['width'], SIZE = obj['size'], BOOK_id = book_id, PAGE_id = pg.id)
                Obj.save()
                print("Saved Object  of PAGE_id = {0} and BOOK_id = {1} and id = {2}".format(book_id, pg.id, Obj.id))
    else:
        print("not post")
    print("--------------------------------------------")
    res = JsonResponse({ "info": "OK"})
    res['Access-Control-Allow-Origin'] = "*"
    return res

def getStack(request, book_id, page):
    print(book_id, page)
    try:
        print(type(page), page)
        page_id = Page.objects.get(PAGINA = page, BOOK_id = book_id).id
        print(page_id)
        Objs = Object.objects.filter(BOOK_id = book_id, PAGE_id = page_id)
        print(Objs)
        myJson = {}
        index = 1
        for obj in Objs:
            new_obj = {}
            new_obj['x'] = obj.X
            new_obj['y'] =  obj.Y
            new_obj['color'] = obj.COLOR
            new_obj['width'] = obj.WIDTH
            new_obj['size'] = obj.SIZE
            new_obj['mode'] = obj.MODE
            print(new_obj)
            myJson["stack{0}".format(index)] = json.dumps(new_obj)
            index += 1
        res = JsonResponse(myJson)
        res['Access-Control-Allow-Origin'] = "*"
        return res
    except Exception as err:
        print(err)
        res = JsonResponse({"info": "fail"})
        res['Access-Control-Allow-Origin'] = "*"
        return res