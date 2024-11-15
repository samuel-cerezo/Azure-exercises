import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient

key = '#################'
endpoint = 'https://language-ai23435.cognitiveservices.azure.com/'

text_analytics_client = TextAnalyticsClient(endpoint=endpoint, credential=AzureKeyCredential(key))
documents = [
    """
     Tristemente when we arrived the elevator was broken, but with Paulette's help we barely noticed this inconvenience.
    Ella arreglo nuestro equipaje y no nos cobro la habitacion. She arranged for our baggage to be brought up to our room with no extra charge and gave us a free meal to refurbish all of the calories we lost from
    walking up the stairs.
    """,
    """
    最近由于工作压力太大，我们决定去富酒店度假。那儿的温泉实在太舒服了，我跟我丈夫都完全恢复了工作前的青春精神！加油！
    """
]

result = text_analytics_client.detect_language(documents)
print(result)