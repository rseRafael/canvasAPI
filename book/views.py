from django.shortcuts import render
from bookupload.models import Book, Page, Markup
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect, FileResponse
from django.views.decorators.csrf import csrf_exempt
import json
import base64
from canvasAPI.settings import STATICFILES_DIRS
import os
import json

response = None

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
def sendbook(bookId, pageNumber):
    _book = Book.objects.filter(id=bookId)
    if len(_book) == 1:
        imgsList = os.listdir(_book._imgsPath)
        imgsList.sort()
        if pageNumber > 0 and pageNumber <= len(imgsList):
            img = open(_book._imgsPath + imgsList[pageNumber-1], 'rb')
            print(type(img))
            _json = dict() #could be {}
            _json['image'] = img
            _json['result'] = True
            _jsonResponse = JsonResponse(_json)
            _jsonResponse['Allow-Access-Control-Origin'] = "*"
            return _jsonResponse
    _json = {}
    _json['result'] = False
    _jsonResponse = JsonResponse(_json)
    return _jsonResponse


def getbooks2(request, darkness):
    return getbooks(request)

@csrf_exempt
def getPages2(request, bookId, pageNumber):
    global response
    _book = Book.objects.filter(id=bookId)
    if len(_book) == 1:
        _page = Page.objects.filter(_book=bookId, _page=pageNumber)
        if len(_page) == 1:
            _path = _book[0]._imgsPath
            print(_path)
            _imgList = os.listdir( _path )
            _imgList.sort()
            print(_imgList)
            _file = open( _path + _imgList[pageNumber - 1], 'rb')
            print("worked")
            response = FileResponse(_file)
            return response
        else:
            response = HttpResponse("Sorry, mate. There is no pages in this book.")
    else:
        response = HttpResponse("Sorry, mate. There is no book with this id.")
    response['Access-Control-Allow-Origin'] = "*"
    return response

#@Produces()
#@Consumes()
@csrf_exempt
def receiveMarkups(request):
    if request.method == 'POST':
        if len(request.POST) >= 1:
            try:
                for prop in request.POST:
                    print(prop)
                book_id = request.POST["book_id"]
                page_number = request.POST['page_number']
                markups = json.loads(request.POST['markups'])
                # print(book_id)
                # print(page_number)
                # print(markups)
            except Exception as err:
                print("an exception has occured")
                print(err)
                print("- - - - - - ")
    _json = {}
    _json['result'] = True
    _json['prettyMessage'] = "Hello, stranger. I know you are a nice person but you are not me. I am the back-end and so more important than you."
    jsonResponse = JsonResponse(_json)
    jsonResponse['Access-Control-Allow-Origin'] = "*"
    return jsonResponse

def setMarkups(book_id):
    pass

def getPages(request, bookId, pageNumber):
    _book = Book.objects.filter(id=bookId)
    if len( _book ) == 1:
        _page = Page.objects.filter(_book=bookId, _page=pageNumber)
        if len( _page ) == 1:
            _path = _book[0]._imgsPath
            STATICFILES_DIRS.append( _path )
            print("path: {0}".format( _path ) )
            _imgFile = _book[0]._name.replace(".pdf", "({0}).jpg".format(_page[0]._page))
            response = JsonResponse( { 'host': "http://localhost:8000/static/" + _imgFile, })
            response['Access-Control-Allow-Origin'] = "*"
            return response
        

@csrf_exempt
def setStack(request):
    if request.method == "POST":
        print("imgPATH: ", request.POST['imgPATH'])
        print(request.FILES)
        imgPath = request.POST['imgPATH']
        arr = imgPath.split("/")
        img = arr.pop()
        book_id = int(arr.pop().replace("book", ""))
        books = Book.objects.filter(id = book_id)
        if len(books) == 1:
            book = books[0]
            path = book.mainPATH + "editedImgs/"
            f = open(file=path + img.replace(".jpg", ".png"), mode="wb")
            IMG = request.POST['image'].encode()
            f.write( base64.decodebytes(IMG) )
            f.close()
            print("Saved the {0} img at {1} path".format(img,path))
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