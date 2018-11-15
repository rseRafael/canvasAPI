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
            markups = Markup.objects.filter(_book=book.id, _page=page)
            index = 1
            name = "markup"
            markupsJson = {}
            for markup in markups:
                markupsJson[name + str(index)] = turnMarkupIntoDict(markup)
                index += 1
            jsonResponse = JsonResponse(markupsJson)
            jsonResponse['Access-Control-Allow-Origin'] = "*"
            return jsonResponse
    failureJson = {'result': False}
    jsonResponse = JsonResponse(failureJson)
    jsonResponse['Access-Control-Allow-Origin'] = "*"
    return jsonResponse


@csrf_exempt
def getMarkups2(request, bookId, pageNumber):
    if request.method == "GET":
        if validateGetMarkupsParam(bookId, pageNumber):
            book = Book.objects.filter(id=bookId)
            if len(book) == 1:
                book = book[0]
                page = Page.objects.filter(_book=book, _page=pageNumber)
                if len(page) == 1:
                    page = page[0]
                    markups = Markup.objects.filter(_book=book, _page=page)
                    if len(markups) > 0:
                        markupsJson = {}
                        name = 'markup'
                        index = 1
                        markupArray = markups.values()
                        print("markups quantity:{2} for bookId: {0} and pageNumber: {1}".format(bookId, pageNumber, len(markupArray)))
                        for markup in markups.values():
                            markupsJson[name + str(index)] = markup
                            index+=1
                        jsonRes = JsonResponse({'result': True, 'markups': markupsJson})
                        jsonRes['Access-Control-Allow-Origin'] = "*"
                        return jsonRes
    jsonRes = JsonResponse({'result': False, 'markups': {}})
    jsonRes['Access-Control-Allow-Origin'] = "*"
    return jsonRes


def validateGetMarkupsParam(bookId, pageNumber):
    if type(bookId) == int and type(pageNumber) == int:
        if bookId > 0 and pageNumber > 0:
            return True
    return False


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


def showMeWhatWeGot(markup):
    print("inside of it: ")
    for prop in markup:
        eval("type(markup.{0})".format(prop))
        print(prop)


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
    if request.method == 'POST':
        if len(request.POST) >= 1:
            try:
                bookId = request.POST["bookId"]
                page = request.POST['pageNumber']
                markups = json.loads(request.POST['markups'])
                print("setMarkups(request): request.POST: {0}".format(request.POST))
                _book = Book.objects.filter(id=bookId)
                if len(_book) == 1:
                    _book = _book[0]
                    _page = Page.objects.filter(_book=_book, _page=page)
                    if len(_page) == 1:
                        _page = _page[0]
                        deleteMarkups(_book, _page)
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
                                               _lineWidth=markup["lineWidth"],
                                               _book=_book,
                                               _page=_page)
                            markupObj.save()
            except Exception as err:
                print("an exception has occured at setMarkups method.")
                print(err)
    _json = {}
    _json['result'] = False
    _json[
        'prettyMessage'] = "Hello, stranger. I know you are a nice person but you are not me. I am the back-end and so more important than you."
    jsonResponse = JsonResponse(_json)
    jsonResponse['Access-Control-Allow-Origin'] = "*"
    return jsonResponse


def deleteMarkups(book, page):
    markups = Markup.objects.filter(_page=page, _book=book)
    index = 0
    for markup in markups:
        index += 1
        markup.delete()
    print("deleteMarkups({0}, {1}): {2} deleted.".format(book.id, page._page, index))



