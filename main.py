import shutil
import openai
import requests
from PIL import Image

api_key = ""
openai.api_key = api_key
def create_meals(ingredients, kcal=2000):
    prompt = f''' Create a healthy daily meal plan for breakfast, lunch, and dinner based on the following ingredients {ingredients}.
    Explain each recipe.
    The total daily calorie should be below {kcal}.
    Assign a suggestive and concise title to each meal.
    Your answer should end with 'Titles: ' and the title of each recipe.
    '''

    messages = [
        {'role': 'system', 'content': 'You are a talented cook.'},
        {'role': 'user', 'content': prompt}
    ]

    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=messages,
        temperature=1,
        max_tokens=1024,
        n=1
    )

    return response['choices'][0]['message']['content']


def create_and_saveimage(title, extra=''):
    image_prompt = f'{title} {extra} high quality food photography'
    response = openai.Image.create(
        prompt=image_prompt,
        n=1,
        size='1024x1024'
    )
    image_url = response['data'][0]['url']
    print()
    print(image_url)
    image_resource = requests.get(image_url, stream=True)
    print(image_resource.status_code)
    image_filename = f'{title}.png'
    if image_resource.status_code == 200:
        with open(image_filename, 'wb') as f:
            shutil.copyfileobj(image_resource.raw, f)
        return image_filename
    else:
        print('Error accessing image')
        return False

foods = 'broccoli,chicken,fish,eggs,olive oil'
output = create_meals(foods)
print(output)
titles = output.splitlines()[-3:]
print(titles)
titles = [t.strip('-') for t in titles]

# Open the saved image using PIL
for index in  range(len(titles)):
    image_filename = create_and_saveimage(titles[index], 'white background')
    print(image_filename)
    image = Image.open(image_filename)
