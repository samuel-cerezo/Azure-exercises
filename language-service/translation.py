from azure.ai.translation.text import TextTranslationClient
import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient

key = '#################'
endpoint = 'https://samuel-translator132.cognitiveservices.azure.com/'

credential = AzureKeyCredential(key)
text_translator = TextTranslationClient(credential=credential, endpoint=endpoint)

input_text = ["This is a test. I prefer people to call me Samu instead of Samuel Adrian Cerezo"]

response = text_translator.translate(
    body=input_text, to_language=['ja'])

print(response)