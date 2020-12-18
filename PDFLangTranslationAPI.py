import requests
import json
import jsonpath
import fitz
import os
import pytest
import pdb
import PyPDF2

print(PyPDF2.__file__)
def POSTLangTranslation():
    url = "https://api.cognitive.microsofttranslator.com/translate"
	// Path to folder where all PDF are placed
    PDF_FILES_TO_TRANSLATE_PATH = ""
	// File name for translated files
    PDF_FILES_TRANSLATED_FILENAME = ""
    JSON_PAYLOAD_FILENAME = "payload.json"
    payloadJSONFilePath = os.path.join(PDF_FILES_TO_TRANSLATE_PATH, JSON_PAYLOAD_FILENAME)
    FROM_LANGUAGE = 'es'
    TO_LANGUAGE = 'en'

    if not os.path.isdir(PDF_FILES_TO_TRANSLATE_PATH):
        raise ValueError('Directory does not exists!')
    elif not os.listdir(PDF_FILES_TO_TRANSLATE_PATH):
        raise ValueError('Directory is empty... FileNotFound!')

    filenames = os.listdir(PDF_FILES_TO_TRANSLATE_PATH)

    for filename in filenames:
        if os.path.splitext(filename)[1].lower() != '.pdf':
            continue
        singlePDFFilePath = os.path.join(PDF_FILES_TO_TRANSLATE_PATH, filename)
        # pdf = fitz.open(singlePDFFilePath)
        # pdf1 = fitz.open()
        f = open(singlePDFFilePath,'rb')
        pdf_reader = PyPDF2.PdfFileReader(f)
        pages_all = pdf_reader.numPages
        page1 = pdf_reader.getPage(0).extractText()

        if pdf.pageCount > 10:
            totalPageToTranslate = 10
        else:
            totalPageToTranslate = pdf.pageCount

        params = {'api-version': 3.0, 'to': TO_LANGUAGE, 'from': FROM_LANGUAGE}
		// Subscription-Key for Test to be generated and used as 'Ocp-Apim-Subscription-Key' value
        headers = {'content-type': 'application/json', 'Ocp-Apim-Subscription-Key': ''}
        pdf_r = pdf_reader.getPage(0)
        text = pdf_r.extractText()
        for i in range(1, pages_all):
            page = pdf_reader.getPage(i).extractText()
            page1text = page.getText("text")

            fileJson = open(payloadJSONFilePath, 'r')
            jsonRequest = json.loads(fileJson.read())
            jsonRequest[0]["Text"] = page1text
            jsonnew = json.dumps(jsonRequest)

            responsePost = requests.post(url, data=jsonnew, params=params, headers=headers)
            assert responsePost.status_code == 200
            jsonr = responsePost.json()
            json_path_test = json.loads(responsePost.text)

            fileJson = open(PDF_FILES_TO_TRANSLATE_PATH + 'Translated_' + FROM_LANGUAGE + 'TO' + TO_LANGUAGE + '_' +
                            os.path.splitext(filename)[0] + '.txt', 'a', encoding='utf-8')
            fileJson.write('    ---------------------Page' + str(i) + '-------------------- \n')
            fileJson.write(json_path_test[0]['translations'][0]['text'])
            print('page' + str(i) + ' Done')
            fileJson.close()
        print('Completed Translation for file - ' + filename)

POSTLangTranslation()
