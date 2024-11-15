# import namespaces
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient
import os

key = '#############################'
endpoint = 'https://textclassificator.cognitiveservices.azure.com/'
project_name = 'Clasificador24534'
deployment_name = 'Deploy1'

# Create client using endpoint and key
credential = AzureKeyCredential(key)
ai_client = TextAnalyticsClient(endpoint=endpoint, credential=credential)

# Read each text file in the ads folder
batchedDocuments = []
ads_folder = '/Users/samucerezo/dev/src/my-github/Azure-examples/language-service/mslearn-ai-language/Labfiles/05-custom-entity-recognition/Python/custom-entities/ads'
files = os.listdir(ads_folder)
for file_name in files:
    # Read the file contents
    text = open(os.path.join(ads_folder, file_name), encoding='utf8').read()
    batchedDocuments.append(text)

# Extract entities
operation = ai_client.begin_recognize_custom_entities(
    batchedDocuments,
    project_name=project_name,
    deployment_name=deployment_name
)

document_results = operation.result()
print (document_results)

for doc, custom_entities_result in zip(files, document_results):
    print(doc)
    if custom_entities_result.kind == "CustomEntityRecognition":
        for entity in custom_entities_result.entities:
            '''print(
                "\tEntity '{}' has category '{}' with confidence score of '{}'".format(
                    entity.text, entity.category, entity.confidence_score
                )
            )'''
            print("\t El objecto '{}' es identificado en la categoria '{}', con un nivel de confianza de '{}'.".format(entity['text'],entity['category'], entity['confidence_score']))
    elif custom_entities_result.is_error is True:
        print("\tError with code '{}' and message '{}'".format(
            custom_entities_result.error.code, custom_entities_result.error.message
            )
        )