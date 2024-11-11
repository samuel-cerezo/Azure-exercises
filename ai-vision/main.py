import os
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv
from PIL import Image, ImageDraw
from matplotlib import pyplot as plt
import requests

# Set the values of your computer vision endpoint and computer vision key
# as environment variables:
try:
    endpoint = 'https://computer-vision2434.cognitiveservices.azure.com/'
    key = '1yFxha5Zf9cko0pXb2peEvaSsXeeZNuxgVkKOD8rxDHP5W3vmc8nJQQJ99AJACYeBjFXJ3w3AAAFACOGCaN2'
except KeyError:
    print("Missing environment variable 'VISION_ENDPOINT' or 'VISION_KEY'")
    print("Set them before running this sample.")
    exit()

# Create an Image Analysis client for synchronous operations,
# using API key authentication
client = ImageAnalysisClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(key)
)
# Get a caption for the image. This will be a synchronously (blocking) call.
result = client.analyze_from_url(
    image_url="https://aka.ms/azsdk/image-analysis/sample.jpg",
    visual_features=[VisualFeatures.CAPTION],
    gender_neutral_caption=True,  # Optional (default is False)
)


# Print caption results to the console
print("Image analysis results:")
print(" Caption:")
if result.caption is not None:
    print(f"   '{result.caption.text}', Confidence {result.caption.confidence:.4f}")

# Get image
image_file = '/Users/samucerezo/dev/src/my-github/Azure-examples/ai-vision/mslearn-ai-vision/Labfiles/01-analyze-images/Python/image-analysis/images/person.jpg'
image_file = '/Users/samucerezo/dev/src/my-github/Azure-examples/ai-vision/mslearn-ai-vision/Labfiles/01-analyze-images/Python/image-analysis/images/street.jpg'
#image_file = '/Users/samucerezo/dev/src/my-github/Azure-examples/ai-vision/mslearn-ai-vision/Labfiles/01-analyze-images/Python/image-analysis/images/building.jpg'

with open(image_file, "rb") as f:
    image_data = f.read()

# Get result with specified features to be retrieved
result = client.analyze(
    image_data=image_data,
    visual_features=[
        VisualFeatures.CAPTION,
        VisualFeatures.DENSE_CAPTIONS,
        VisualFeatures.TAGS,
        VisualFeatures.OBJECTS,
        VisualFeatures.PEOPLE],
)

# Display analysis results
# Get image captions
if result.caption is not None:
    print("\nCaption:")
    print(" Caption: '{}' (confidence: {:.2f}%)".format(result.caption.text, result.caption.confidence * 100))

# Get image dense captions
if result.dense_captions is not None:
    print("\nDense Captions:")
    for caption in result.dense_captions.list:
        print(" Caption: '{}' (confidence: {:.2f}%)".format(caption.text, caption.confidence * 100))
# Get image tags
if result.tags is not None:
    print("\nTags:")
    for tag in result.tags.list:
        print(" Tag: '{}' (confidence: {:.2f}%)".format(tag.name, tag.confidence * 100))

# Get objects in the image
if result.objects is not None:
    print("\nObjects in image:")

    # Prepare image for drawing
    image = Image.open(image_file)
    fig = plt.figure(figsize=(image.width/100, image.height/100))
    plt.axis('off')
    draw = ImageDraw.Draw(image)
    color = 'cyan'

    for detected_object in result.objects.list:
        # Print object name
        print(" {} (confidence: {:.2f}%)".format(detected_object.tags[0].name, detected_object.tags[0].confidence * 100))
        
        # Draw object bounding box
        r = detected_object.bounding_box
        bounding_box = ((r.x, r.y), (r.x + r.width, r.y + r.height)) 
        draw.rectangle(bounding_box, outline=color, width=3)
        plt.annotate(detected_object.tags[0].name,(r.x, r.y), backgroundcolor=color)

    # Save annotated image
    plt.imshow(image)
    plt.tight_layout(pad=0)
    outputfile = '/Users/samucerezo/dev/src/my-github/Azure-examples/ai-vision/objects.jpg'
    fig.savefig(outputfile)
    print('  Results saved in', outputfile)
    # Get people in the image
if result.people is not None:
    print("\nPeople in image:")

    # Prepare image for drawing
    image = Image.open(outputfile)
    fig = plt.figure(figsize=(image.width/100, image.height/100))
    plt.axis('off')
    draw = ImageDraw.Draw(image)
    color = 'red'

    for detected_people in result.people.list:
        # Draw object bounding box
        r = detected_people.bounding_box
        bounding_box = ((r.x, r.y), (r.x + r.width, r.y + r.height))
        draw.rectangle(bounding_box, outline=color, width=3)

        # Return the confidence of the person detected
        print(" {} (confidence: {:.2f}%)".format(detected_people.bounding_box, detected_people.confidence * 100))
        
    # Save annotated image
    plt.imshow(image)
    plt.tight_layout(pad=0)
    outputfile = '/Users/samucerezo/dev/src/my-github/Azure-examples/ai-vision/people.jpg'
    fig.savefig(outputfile)
    print('  Results saved in', outputfile)

    # Remove the background from the image or generate a foreground matte

print('\nRemoving background from image...')
api_version = "2023-02-01-preview"
mode="backgroundRemoval" # Can be "foregroundMatting" or "backgroundRemoval"
        
url = "{}computervision/imageanalysis:segment?api-version={}&mode={}".format(endpoint, api_version, mode)

headers= {
    "Ocp-Apim-Subscription-Key": key, 
    "Content-Type": "application/json" 
}

#image_url="https://github.com/MicrosoftLearning/mslearn-ai-vision/blob/main/Labfiles/01-analyze-images/Python/image-analysis/{}?raw=true".format(image_file)  
image_url="https://learn.microsoft.com/azure/ai-services/computer-vision/images/windows-kitchen.jpg"
body = {
    "url": image_url,
}

response = requests.post(url, headers=headers, json=body)

image=response.content
with open("/Users/samucerezo/dev/src/my-github/Azure-examples/ai-vision/background.png", "wb") as file:
    file.write(image)
print('  Results saved in background.png \n')