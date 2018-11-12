from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from pdf2image import convert_from_path
from django.views.decorators.csrf import csrf_exempt
from .models import Book, Page
from PyPDF2 import PdfFileReader
import os

# Global Variables:

_file = None
_dirName = None
_dirPath = None
_pdfPath = None
_imgsPath = None
_pagesNumber = None


# Create your views here.
@csrf_exempt
def uploadBookMain(request):
    result = uploadBook(request)
    if result[0] == True:
        try:
            print("1 - Starting to upload book informations to the database.")
            result = uploadBook2DataBase()
        except Exception as err:
            print("1.c.2 - error at uploadBook2DataBase execution.")
            print(err)
        if result[0] == True:
            print("2 - Successfully uploaded book informations.")
            response = JsonResponse({'result': True, 'post-operation': "success"})
            response['Access-Control-Allow-Origin'] = "*"
            return response
        else:
            print(result[1].__str__())
            print(result[2])
            response = JsonResponse(
                {'result': result[0], 'Error': result[1].__str__(), 'errorMsg': result[2], 'POST-operation': 'failed'})
            response['Access-Control-Allow-Origin'] = "*"
            return response
    else:
        print(result[1].__str__())
        print(result[2])
        response = JsonResponse(
            {'result': result[0], 'Error': result[1].__str__(), 'errorMsg': result[2], 'post-operation': 'fail'})
        response['Access-Control-Allow-Origin'] = "*"
        return response


@csrf_exempt
def uploadBook(request):
    global _file, _dirName, _dirPath, _pdfPath, _imgsPath, _pagesNumber
    '''
    if request.META['HTTP_REFERER'].find("http://localhost:4200/newbook") == -1:
        return [False, None, "Http Referer is non-authorized"]
    '''
    if request.method == 'POST':
        print("0 - request.META.get('HTTP_REFERER') = {0}".format(request.META.get('HTTP_REFERER')))
        print("1 - request method = {0}".format(request.method))
        if request.POST and request.FILES:
            try:
                _file = request.FILES.get('pdfInput')
                if _file == None:
                    return [False, None, "Couldn't find the book file"]
                else:
                    print("2 - caught book file")
                    fileType = _file.content_type
                    print("2.1 - file's content type: {0}".format(_file.content_type))
                    if fileType.find("pdf") == -1:
                        return [False, None, "File must be of pdf type. Try to put '.pdf' at the end of the file."]
                    else:
                        print("3 - book file is a pdf. it's name is: '{0}'.".format(_file.name))
                        if request.POST.get("pdfName") != "":
                            print("3.1 - received an alternative name to the file: '{0}'.".format(
                                request.POST.get("pdfName")))
                            _dirName = request.POST.get("pdfName")
                        else:
                            _dirName = _file.name.replace(".pdf", "[directory]")
                    try:
                        print("4 - trying to create the main directory")
                        result = createMainDir()
                        if result[0] == True:
                            print("5 - created the main folder: {0}".format(_dirPath))
                            print("6 - trying to save the book file")
                            result = saveFile()
                            if result[0] == True:
                                print("7 - saved the file at: {0}".format(_pdfPath))
                                print("8 - Trying to create the image folder")
                                result = createImgsDir()
                                if result[0] == True:
                                    print("9 - created the image folder at: {0}".format(_imgsPath))
                                    print("10 - trying to convert the pdf file to img files.")
                                    _file = open(file=_pdfPath, mode="rb")
                                    _pdf = PdfFileReader(_file)
                                    _pagesNumber = _pdf.getNumPages()
                                    _file.close()
                                    result = convertPDF2JPG()
                                    if result[0] == True:
                                        print("11 - we converted the pdf file at {0} in images".format(_imgsPath))
                                        return [True, _imgsPath, _pagesNumber]
                        return result
                    except Exception as err:
                        return [False, err, "An error has occurred at uploadBook function"]

            except Exception as err:
                return [False, err, "An error has occurred at uploadBook function"]

    else:
        return [False, None, "This function only accepts POST requests"]


def createMainDir():
    global _file, _dirName, _dirPath, _pdfPath, _imgsPath, _pagesNumber

    if _dirName == None or type(_dirName) != str:
        return [False, None, "_dirName must be of string type"]
    else:
        try:
            _dirPath = "/home/rse/DataBase/Library/{0}/".format(_dirName)
            os.mkdir(_dirPath)
            return [True, _dirPath]

        except FileExistsError as err:
            index = 1

            while True:

                try:
                    _dirPath = "/home/rafael/DataBase/Library/{0}/".format(_dirName + "[directory({0})]".format(index))
                    print("4.{0} - trying to create main directory at path: {1}".format(index, _dirPath))
                    os.mkdir(_dirPath)
                    return [True, _dirPath]

                except FileExistsError as e:
                    index += 1
                    _dirPath = _dirPath.replace("[directory]({0})".format(index - 1), "[directory({0})]".format(index))
                    pass

                except Exception as e:
                    return [False, e,
                            "An error has occurred while trying to create the main directory. last path: {0}".format(
                                _dirPath)]

        except Exception as err:
            return [False, err,
                    "An error has occurred while trying to create the main directory. last _dirPath: {0}".format(
                        _dirPath)]


def saveFile():
    global _file, _dirName, _dirPath, _pdfPath, _imgsPath, _pagesNumber

    if _dirPath == None or _file == None or type(_dirPath) != str or type(_file.name) != str:
        return [False, None, "type of _dirName must be a string and _file must be an object"]
    else:
        try:
            _pdfPath = _dirPath + _file.name
            newFile = open(file=_pdfPath, mode='wb')
            data = _file.read()
            newFile.write(data)
            newFile.close()
            return [True]
        except Exception as err:
            return [False, err, "An error has occurred while writing and saving the new book file"]


def createImgsDir():
    global _file, _dirName, _dirPath, _pdfPath, _imgsPath, _pagesNumber

    if _dirPath == None or type(_dirPath) != str:
        return [False, None, "_dirPath must be of string type"]
    else:
        try:
            _imgsPath = _dirPath + "imgs/"
            _editedImgsPath = _dirPath + "editedImgs/"
            os.mkdir(_imgsPath)
            os.mkdir(_editedImgsPath)
            return [True]
        except Exception as err:
            return [False, err,
                    "An error has occurred while trying to create the main folder. _imgsPath: {0}".format(_imgsPath)]


def convertPDF2JPG():
    global _file, _dirName, _dirPath, _pdfPath, _imgsPath, _pagesNumber

    if _imgsPath == None or _pdfPath == None or type(_imgsPath) != str or type(_pdfPath) != str:
        return [False, None, "_imgsPath and _pdfPath must be of type str"]

    try:
        page = 1
        while True:

            if _pagesNumber < page:
                break
            else:
                print("\t\t10.a.{0} - converting page {0}".format(page))
                _imgList = convert_from_path(pdf_path=_pdfPath, output_folder=_imgsPath, first_page=page,
                                             last_page=page, fmt="jpg", dpi=600)
                _list = _imgList[0].filename.split("-")
                _number = _list[len(_list) - 1].replace(".jpg", "")
                _src = _imgList[0].filename
                _dst = _imgsPath + _dirName + "({0})".format(_number) + ".jpg"
            os.rename(src=_src, dst=_dst)
            print("\t\t\t10.b.{0} - renamed page {0}".format(page))
            page = page + 1
        return [True, ]
    except Exception as err:
        errMsg = "10.c - An error has occurred while converting a pdf( '{0}' ) to images files".format(_pdfPath)
        print(errMsg)
        return [False, err, errMsg]


def uploadBook2DataBase():
    global _file, _dirName, _dirPath, _pdfPath, _imgsPath, _pagesNumber

    try:
        print("1.a.1 = About to create a book in the database.")
        _book = Book(_name=_dirName + ".pdf", _imgsPath=_imgsPath, _pages=_pagesNumber, _dirPath=_dirPath)
        _book.save()
        print("1.a.2 - created a book named '{0}' in the database with images path = {1} ".format(_dirName + ".pdf",
                                                                                                  _imgsPath))
        _imgsList = os.listdir(_imgsPath)
        _imgsList.sort()
        _page = 1
        for img in _imgsList:
            p = Page(_book=_book, _page=_page, _filename=img)
            p.save()
            print("1.b.{2}  - saved page {0} of the book with id = {1}".format(img, _book.id, _page))
            _page = _page + 1
        return [True]

    except Exception as err:
        print("1.c.1 - error at uploadBook2DataBase execution.")
        print(err)
        return [False, err, "An error has occurred at uploadBook2DataBase function."]
