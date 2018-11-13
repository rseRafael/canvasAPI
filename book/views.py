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


@csrf_exempt
def getBooks(request):
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
    response = JsonResponse({"info": "books not found"})
    response['Access-Control-Allow-Origin'] = "*"
    return response


@csrf_exempt
def getMarkups(request, bookId, page):
    book = Book.objects.filter(id=bookId)
    if len(book) == 1:
        book = book[0]
        if page > 0 and page <= book._pages:
            markups = Markup.objects.filter(_book=book._id, _page=page)
            index = 1
            name = "markup"
            markupsJson = {}
            for markup in markups:
                markupsJson[name + index] = turnMarkupIntoDict(markup)
                index += 1
            jsonResponse = JsonResponse(markupsJson)
            jsonResponse['Access-Control-Allow-Origin'] = "*"
            return jsonResponse
    failureJson = {'result': False}
    jsonResponse = JsonResponse(failureJson)
    jsonResponse['Access-Control-Allow-Origin'] = "*"
    return jsonResponse


@csrf_exempt
def getPage(request, bookId, pageNumber):
    global response
    _book = Book.objects.filter(id=bookId)
    if len(_book) == 1:
        _page = Page.objects.filter(_book=bookId, _page=pageNumber)
        if len(_page) == 1:
            _path = _book[0]._imgsPath
            _imgList = os.listdir(_path)
            _imgList.sort()
            _file = open(_path + _imgList[pageNumber - 1], 'rb')
            response = FileResponse(_file)
            return response
        else:
            response = HttpResponse("Sorry, mate. There is no pages in this book.")
    else:
        response = HttpResponse("Sorry, mate. There is no book with this id.")
    response['Access-Control-Allow-Origin'] = "*"
    return response


def turnMarkupIntoDict(markup):
    jsonDict = {}
    jsonDict["_x"] = markup._x
    jsonDict["_y"] = markup._y
    jsonDict["_sizeX"] = markup._sizeX
    jsonDict["_sizeY"] = markup._sizeY
    jsonDict["_orgWidth"] = markup._orgWidth
    jsonDict["_orgHeight"] = markup._orgHeight
    jsonDict["_type"] = markup._type
    jsonDict["_color"] = markup._color
    jsonDict["_lineWidth"] = markup._lineWidth
    return jsonDict


@csrf_exempt
def setMarkups(request):
    print(request.method)
    if request.method == 'POST':
        print(len(request.POST))
        if len(request.POST) >= 1:
            try:
                bookId = request.POST["bookId"]
                page = request.POST['page']
                markups = json.loads(request.POST['markups'])
                deleteMarkups(bookId, page)
                for markup in markups:
                    markup = markups[markup]
                    markupObj = Markup(_x=markup["x"],
                                       _y=markup["y"],
                                       _sizeX=markup["sizeX"],
                                       _sizeY=markup["sizeY"],
                                       _orgWidth=markup["orgWidth"],
                                       _orgHeight=markup["orgHeight"],
                                       _type=markup["type"],
                                       _color=markup["color"],
                                       _lineWidth=markup["lineWidth"],)
                    markupObj.save()
            except Exception as err:
                print("an exception has occured at setMarkups method.")
                print(err)
                print("- - - - - - ")
    _json = {}
    _json['result'] = False
    _json[
        'prettyMessage'] = "Hello, stranger. I know you are a nice person but you are not me. I am the back-end and so more important than you."
    jsonResponse = JsonResponse(_json)
    jsonResponse['Access-Control-Allow-Origin'] = "*"
    return jsonResponse

def deleteMarkups(bookId, page):
    markups = Markup.objects.filter(_page=page, _book=bookId)
    for markup in markups:
        markup.delete()


def getwholebook(request, bookId):
    if request.method == "GET":
        _book = Book.objects.filter(id=bookId)
        if len(_book) == 1:
            _book = _book[0]
            imgsList = os.listdir(_book._imgsPath)
            imgsList.sort()
            # _json = {}
            # _json['result'] = True
            # _json['pages'] = len(imgsList)
            # _json['img'] = open(_book._imgsPath + imgsList[0], 'rb')
            # _jsonResponse = JsonResponse(_json)
            # _jsonResponse['Allow-Access-Control-Origin'] = "*"
            response = FileResponse(open(_book._imgsPath + imgsList[0], 'rb'))
            response['Access-Control-Allow-Origin'] = "*"
            response['param-test'] = "supose it is a test"
            return response
    _json = dict()
    _json['result'] = False
    _jsonResponse = JsonResponse(_json)
    return _jsonResponse


# @Consumes() nothing because it is a get method
# @Produces('application/json') a json with the number of books and pages of each book
@csrf_exempt
def getloadedbooks(request):
    if request.method == "GET":
        books = Book.objects.all()
        bookJson = {}
        index = 1
        for book in books:
            bookJson["book" + str(index)] = {'id': book.id, 'pages': book._pages, 'name': book._name}
        jsonResponse = JsonResponse(bookJson)
        jsonResponse['Acces-Control-Allow-Origin'] = "*"
        return jsonResponse
    aJson = {'result': False, 'method-required': request.method}
    jsonResponse = JsonResponse(aJson)
    jsonResponse['Access-Control-Allow-Origin'] = "*"
    return jsonResponse


# def getPages(request, bookId, pageNumber):
#     _book = Book.objects.filter(id=bookId)
#     if len( _book ) == 1:
#         _page = Page.objects.filter(_book=bookId, _page=pageNumber)
#         if len( _page ) == 1:
#             _path = _book[0]._imgsPath
#             STATICFILES_DIRS.append( _path )
#             print("path: {0}".format( _path ) )
#             _imgFile = _book[0]._name.replace(".pdf", "({0}).jpg".format(_page[0]._page))
#             response = JsonResponse( { 'host': "http://localhost:8000/static/" + _imgFile, })
#             response['Access-Control-Allow-Origin'] = "*"
#             return response


@csrf_exempt
def setStack(request):
    if request.method == "POST":
        print("imgPATH: ", request.POST['imgPATH'])
        print(request.FILES)
        imgPath = request.POST['imgPATH']
        arr = imgPath.split("/")
        img = arr.pop()
        book_id = int(arr.pop().replace("book", ""))
        books = Book.objects.filter(id=book_id)
        if len(books) == 1:
            book = books[0]
            path = book.mainPATH + "editedImgs/"
            f = open(file=path + img.replace(".jpg", ".png"), mode="wb")
            IMG = request.POST['image'].encode()
            f.write(base64.decodebytes(IMG))
            f.close()
            print("Saved the {0} img at {1} path".format(img, path))
        print("image: ", img, "BOOK_id: ", book_id)
        pg = Page.objects.get(BOOK_id=book_id, PAGINA=img)
        print("PAGE_id: ", pg.id, "BOOK_id", book_id)
        objs = Object.objects.filter(BOOK_id=book_id, PAGE_id=pg.id)
        print(1)
        for obj in objs:
            print("deleting Object of id = {0} from the PAGE_id = {1} and BOOK_id = {2}".format(obj.id, pg.id, book_id))
            obj.delete()
        print(2)
        for elem in request.POST:
            if elem.find("obj") != -1:
                obj = json.loads(request.POST[elem])
                Obj = Object(X=obj['x'], Y=obj['y'], MODE=obj['mode'], COLOR=obj['color'], WIDTH=obj['width'],
                             SIZE=obj['size'], BOOK_id=book_id, PAGE_id=pg.id)
                Obj.save()
                print("Saved Object  of PAGE_id = {0} and BOOK_id = {1} and id = {2}".format(book_id, pg.id, Obj.id))
    else:
        print("not post")
    print("--------------------------------------------")
    res = JsonResponse({"info": "OK"})
    res['Access-Control-Allow-Origin'] = "*"
    return res


def getStack(request, book_id, page):
    print(book_id, page)
    try:
        print(type(page), page)
        page_id = Page.objects.get(PAGINA=page, BOOK_id=book_id).id
        print(page_id)
        Objs = Object.objects.filter(BOOK_id=book_id, PAGE_id=page_id)
        print(Objs)
        myJson = {}
        index = 1
        for obj in Objs:
            new_obj = {}
            new_obj['x'] = obj.X
            new_obj['y'] = obj.Y
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
