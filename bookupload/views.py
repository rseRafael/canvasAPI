from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from pdf2image import convert_from_path
import os
from django.views.decorators.csrf import csrf_exempt
from .models import Book, Object, Page
from PyPDF2 import PdfFileReader


#Global Variables:

_file = None
_dirName = None
_dirPath = None
_pdfPath = None
_imgsPath = None


# Create your views here.
@csrf_exempt
def uploadBookMain(request):
    result = uploadBook(request)
    if result[0] == True:
        try: 
            result = uploadBookDataBase(request, result[1], result[2])
        except Exception as err:
            print("erro na execucao de uploadBookDataBase")
            print(err)
        if result[0] == True:
            print("deu certo")
            response = JsonResponse({'result': True, 'post-operation': "success"})
            response['Access-Control-Allow-Origin'] = "*"
            return response
    else:
        print(result[1].__str__())
        print(result[2])
        response = JsonResponse({ 'result': result[0], 'Error': result[1].__str__(), 'errorMsg': result[2], 'post-operation': 'fail' })
        response['Access-Control-Allow-Origin'] = "*"
        return response


@csrf_exempt
def uploadBook(request):
    global _file, _dirName, _dirPath, _pdfPath, _imgsPath
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
                    if fileType.find(".pdf") == -1:
                        return [False, None, "File must be of pdf type. Try to put '.pdf' at the end of the file."]
                    else:
                        print("3 - book file is a pdf. it's name is: '{0}'.".format(_file.name))
                        if request.POST.get("pdfName") != "":
                            print( "3.1 - received an alternative name to the file: '{0}'.".format( request.POST.get("pdfName") ) )
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
                                    result = convertPDF2JPG()
                                    if result[0] == True:
                                        print("11 - we converted the pdf file at {0} in images".format(_imgsPath))
                                        _file = open(file=_pdfPath,mode="rb")
                                        _pdf = PdfFileReader(_file)
                                        _pagesNumber = _pdf.getNumPages()
                                        _file.close()
                                        return [True, _imgsPath, _pagesNumber]
                        return result
                    except Exception as err:
                        return [False, err, "An error has occurred at uploadBook function"]

            except Exception as err:
                return [False, err, "An error has occurred at uploadBook function"]
                
    else:
       return [False, None, "This function only accepts POST requests"]


def createMainDir():
    global _file, _dirName, _dirPath, _pdfPath, _imgsPath

    if _dirName == None or type(_dirName) != str:
        return [False, None, "_dirName must be of string type"]
    else:
        try:
            _dirPath = "/home/rse/DataBase/Library/{0}/".format(_dirName)
            os.mkdir(_dirPath)
            return [True, _dirPath]
        except FileExistsError as err:
            index = 2
            while True:

                try:
                    _dirPath = _dirPath.replace("[directory]({0})".format(index-1), "[directory({0})]".format(index))
                    index += 1
                    print("4.{0} - trying to create main fold path at: {1}".format( index-1 , _dirPath ))
                    os.mkdir( _dirPath )
                    return [True, _dirPath]

                except FileExistsError as e:
                    pass

                except Exception as e:
                    return [False, e, "An error has occurred while trying to create the main directory. last path: {0}".format(_dirPath)]

        except Exception as err:
            return [False, err, "An error has occurred while trying to create the main directory. last _dirPath: {0}".format(_dirPath)]


def saveFile():
    global _file, _dirName, _dirPath, _pdfPath, _imgsPath

    if _dirPath == None or _file == None or type(_dirPath) != str or type(_file.name) != str:
        return [False, None, "type of _dirName must be a string and _file must be an object"]
    else:
        try:
            _pdfPath = _dirPath + _file.name
            newFile = open(file = _pdfPath, mode='wb')
            data = _file.read()
            newFile.write(data)
            newFile.close()
            return [True]
        except Exception as err:
            return [False, err, "An error has occurred while writing and saving the new book file"]


def createImgsDir():
    global _file, _dirName, _dirPath, _pdfPath, _imgsPath

    if _dirPath == None or type(_dirPath) != str:
        return [False, None, "_dirPath must be of string type" ]
    else:
        try:
            _imgsPath = _dirPath + "imgs/"
            _editedImgsPath = _dirPath + "editedImgs/"
            os.mkdir(_imgsPath)
            os.mkdir(_editedImgsPath)
            return [True]
        except Exception as err:
            return [False, err, "An error has occurred while trying to create the main folder. _imgsPath: {0}".format(_imgsPath)]



def convertPDF2JPG():
    global _file, _dirName, _dirPath, _pdfPath, _imgsPath

    if _imgsPath == None or _pdfPath == None or type(_imgsPath) != str or type(_pdfPath) != str:
        return [False, None, "_imgsPath and _pdfPath must be of type str"]
    try:
        page = 1
        while True:
            print( "\t\t10.a.{0} - converting page {0}".format(page) )
            _imgList = convert_from_path(pdf_path = _pdfPath, output_folder = _imgsPath, first_page = page, last_page = page, fmt="jpg", dpi=1000)
            if len(_imgList) == 0:
                print( "10.c - finished converting the pdf file" )
                break
            else:
                _list = _imgList[0].filename.split("-")
                _number = _list[len(_list) - 1].replace(".jpg", "")
                _src = _imgList[0].filename
                _dst = _imgsPath + _dirName + "({0})".format(_number) + ".jpg"
                os.rename( src = _src, dst = _dst)
                print( "\t\t10.b.{0} - renamed page {0}}".format(page) )
                page = page + 1
        return [True,]

    except Exception as err:
        errMsg = "10.b - An error has occurred while converting a pdf( '{0}') to images files".format(_pdfPath)
        print(errMsg)
        return [False, err,  errMsg]

def formatNumber(number=None, length=None):
    if number == None or length == None or type(number) != int or type(length) != int:
        return [False, None, "number an length must be of type int"]
    if length <= 0:
        return [False, None, "length must be an integer greater than 0"]
    else:
        try:
            n = str(number)
            while len(n) < length:
                n = '0' + n
            return n
        except Exception as err:
            return [False, None, "An error has occurred while formating a number: {0}".format(number)]

def uploadBookDataBase(request, imgPath, pgsNumber):
    try:
        _file = request.FILES.get('book')
        capa = formatNumber(1, len(str(len(os.listdir(imgPath))))) + ".jpg"
        mainPath = ""
        path = imgPath.split("/")
        path.pop()
        path.pop()
        for txt in path:
            mainPath += txt + "/"
        book = Book(NAME = _file.name, SIZE = _file.size, imgsPATH = imgPath, mainPATH = mainPath, capaPATH = capa, PAGES = pgsNumber)
        book.save()
        print("1 - criamos o book no banco de dados with the imagePath = {0} ".format(imgPath))
        imgList = os.listdir(imgPath)
        for img in imgList: 
            number = int(img.replace(".jpg", ""))
            p = Page(BOOK_id = book.id,  NUMERO = number, PAGINA = img) 
            p.save()
            print("Salvamos a pagina {0} do livro de id {1}".format(img, book.id))
            print("Salvamos a stack da pagina {0} do livro {1}".format(p.id, book.id))
        return [True]
    except Exception as err:
        return [False, err, "Deu erro na uploadBookDataBase function"]
