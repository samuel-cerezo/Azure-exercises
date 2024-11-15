import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient

key = '#################'
endpoint = 'https://language-ai23435.cognitiveservices.azure.com/'

text_analytics_client = TextAnalyticsClient(endpoint=endpoint, credential=AzureKeyCredential(key))

documents = [
    """
    Microsoft was founded by Bill Gates with some friends he met at Harvard. One of his friends,
    Steve Ballmer, eventually became CEO after Bill Gates as well. Steve Ballmer eventually stepped
    down as CEO of Microsoft, and was succeeded by Satya Nadella.
    Microsoft originally moved its headquarters to Bellevue, Washington in January 1979, but is now
    headquartered in Redmond.
    """
]

result = text_analytics_client.recognize_linked_entities(documents)

docs = [doc for doc in result]
for doc in docs:
    for entity in doc.entities:
        print('Nombre: ', entity['name'], ' -> Link: ', entity['url'])
