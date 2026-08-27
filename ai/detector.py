import os
import json

from dotenv import load_dotenv

from google import genai

from PIL import Image



load_dotenv()



def get_client():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return None
    try:
        return genai.Client(api_key=api_key)
    except Exception as e:
        print("Gemini Client Error:", e)
        return None






def detect_season(data):


    text = (

        data.get("description","")

        +

        data.get("fabric","")

        +

        data.get("style","")

    ).lower()



    if any(word in text for word in [

        "wool",

        "sweater",

        "jacket",

        "coat",

        "thick",

        "thermal"

    ]):

        return "Winter"




    if any(word in text for word in [

        "raincoat",

        "waterproof",

        "windbreaker"

    ]):

        return "Rainy"




    if any(word in text for word in [

        "cotton",

        "linen",

        "short",

        "sleeveless",

        "light",

        "chiffon"

    ]):

        return "Summer"




    return "All Season"







def analyze_image(image_path):


    image = Image.open(image_path)



    prompt = """

You are an AI fashion expert.

Analyze this clothing image.

Return ONLY JSON.

Format:

{
"name":"",
"category":"",
"brand":"",
"color":"",
"fabric":"",
"sleeves":"",
"style":"",
"occasion":"",
"description":""
}



Rules:



category must be one:

Top
Bottom
Dress
Shirt
T-shirt
Hoodie
Jacket
Shoes
Bag
Accessory



brand:

If no logo:
Unknown



color:

Only dominant color.



occasion:

Choose:

Casual
College
Office
Party
Wedding



fabric:

Estimate fabric.



sleeves:

Short
Long
Sleeveless



style:

Describe style briefly.



description:

One sentence.



Do not add markdown.

"""



    try:
        client = get_client()
        if not client:
            raise ValueError("GEMINI_API_KEY is not set or client initialization failed.")

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[
                prompt,
                image
            ]
        )



        text=response.text.strip()



        text=(

            text.replace(
                "```json",
                ""
            )

            .replace(
                "```",
                ""
            )

            .strip()

        )



        result=json.loads(text)



        result.setdefault(
            "name",
            "Unknown Item"
        )


        result.setdefault(
            "brand",
            "Unknown"
        )


        result.setdefault(
            "color",
            "Unknown"
        )


        result.setdefault(
            "occasion",
            "Casual"
        )


        result.setdefault(
            "description",
            ""
        )



        # ADD SEASON AUTOMATICALLY

        result["season"] = detect_season(result)



        return result



    except Exception as e:



        print(
            "Gemini Error:",
            e
        )



        return {


            "name":
            "Unknown Item",


            "category":
            "Top",


            "brand":
            "Unknown",


            "color":
            "Unknown",


            "season":
            "All Season",


            "occasion":
            "Casual",


            "description":
            "AI unavailable"

        }