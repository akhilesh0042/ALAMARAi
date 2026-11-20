import os
import json
import re

from dotenv import load_dotenv
from google import genai
from google.genai import types
from PIL import Image


load_dotenv()


def get_gemini_client():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return None
    try:
        return genai.Client(api_key=api_key)
    except Exception as e:
        print("Gemini client initialization error:", e)
        return None


# ---------------------------------------------------------
# SEASON DETECTION
# ---------------------------------------------------------

def detect_season(data):

    text = " ".join([
        str(data.get("description", "")),
        str(data.get("fabric", "")),
        str(data.get("material", "")),
        str(data.get("style", "")),
        str(data.get("category", "")),
    ]).lower()

    # Rainy
    if any(word in text for word in [
        "raincoat",
        "rain jacket",
        "waterproof",
        "water resistant",
        "windbreaker",
        "poncho"
    ]):
        return "Rainy"

    # Winter
    if any(word in text for word in [
        "wool",
        "sweater",
        "jumper",
        "cardigan",
        "coat",
        "puffer",
        "thermal",
        "fleece",
        "thick knit",
        "heavy knit",
        "turtleneck"
    ]):
        return "Winter"

    # Summer
    if any(word in text for word in [
        "cotton",
        "linen",
        "chiffon",
        "lightweight",
        "light fabric",
        "sleeveless",
        "short sleeve",
        "shorts",
        "tank top",
        "crop top"
    ]):
        return "Summer"

    return "All Season"


# ---------------------------------------------------------
# GEMINI CLOTHING ANALYSIS
# ---------------------------------------------------------

def analyze_image(image_path):

    try:
        with Image.open(image_path) as img:
            image = img.convert("RGB")
    except Exception as img_err:
        print(f"Error opening image at {image_path}:", img_err)
        return {
            "name": "Unknown Item",
            "category": "Top",
            "brand": "Unknown",
            "color": "Unknown",
            "fabric": "Unknown",
            "sleeves": "Not Applicable",
            "season": "All Season",
            "occasion": "Casual",
            "style": "Casual",
            "description": f"Failed to load image: {img_err}",
        }

    prompt = """
You are an expert fashion stylist and clothing classification AI.

Analyze the clothing item shown in the image very carefully.

Your most important task is to identify the item's
PRIMARY and MOST CHARACTERISTIC style.

Do NOT classify an item as Casual simply because it can be
worn casually.

For example:
- A blazer is normally Formal or Business Casual.
- A tailored formal shirt is Formal.
- A polo shirt is usually Business Casual.
- An oversized graphic T-shirt is usually Streetwear.
- A hoodie is usually Streetwear or Sporty.
- A tracksuit or athletic jersey is Sporty.
- A saree, kurta, salwar or traditional Indian garment is Traditional or Ethnic.
- A highly embellished/sequined party garment is Party or Elegant.
- A simple, clean, understated garment may be Minimalist.
- A vintage-looking garment with a clearly recognizable older-era design is Vintage.
- A flowing artistic garment with bohemian characteristics is Bohemian.
- A normal everyday basic T-shirt or simple everyday clothing is Casual.

STYLE MUST DESCRIBE THE GARMENT'S DESIGN AND FASHION IDENTITY,
NOT JUST WHERE IT CAN BE WORN.

IMPORTANT:
Occasion and Style are DIFFERENT.

Example:
A formal white shirt:
    style = Formal
    occasion = Office

An oversized graphic T-shirt:
    style = Streetwear
    occasion = College

A simple cotton T-shirt:
    style = Casual
    occasion = Casual

A sequined evening dress:
    style = Party
    occasion = Party

A saree:
    style = Traditional
    occasion = Wedding

Choose the most appropriate values based on the actual visible
characteristics of the garment.

Do not guess a brand unless a logo, label, or brand name is
clearly visible.

If the exact color is difficult to determine, describe the
dominant visible color.

Return ONLY valid JSON.

JSON FORMAT:

{
    "name": "",
    "category": "",
    "brand": "",
    "color": "",
    "fabric": "",
    "sleeves": "",
    "style": "",
    "occasion": "",
    "description": ""
}

---------------------------------------------------------
CATEGORY
---------------------------------------------------------

Choose EXACTLY ONE:

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

Use the most specific category possible.

Examples:
- button-down shirt -> Shirt
- ordinary T-shirt -> T-shirt
- hoodie -> Hoodie
- blazer/jacket -> Jacket
- jeans/trousers/skirt -> Bottom
- saree or one-piece gown -> Dress

Do not use Top when a more specific category is available.

---------------------------------------------------------
BRAND
---------------------------------------------------------

If a brand logo or brand name is clearly visible, identify it.

Otherwise:

"Unknown"

Never invent a brand.

---------------------------------------------------------
COLOR
---------------------------------------------------------

Return the dominant visible color.

Use a simple color name such as:

Black
White
Blue
Navy Blue
Light Blue
Red
Maroon
Green
Olive Green
Yellow
Mustard
Pink
Purple
Brown
Beige
Grey
Orange
Cream
Silver
Gold

If the item has multiple strong colors, choose the dominant
color.

---------------------------------------------------------
FABRIC
---------------------------------------------------------

Estimate the most likely fabric from visible appearance.

Examples:

Cotton
Denim
Linen
Wool
Leather
Silk
Chiffon
Polyester
Knit
Unknown

Do not invent a very specific fabric if it cannot be determined.

---------------------------------------------------------
SLEEVES
---------------------------------------------------------

Choose EXACTLY ONE:

Short
Long
Sleeveless

For items where sleeves are not applicable, such as shoes,
bags or accessories, return:

"Not Applicable"

---------------------------------------------------------
STYLE
---------------------------------------------------------

Choose EXACTLY ONE from:

Casual
Formal
Business Casual
Party
Streetwear
Sporty
Traditional
Ethnic
Minimalist
Vintage
Elegant
Bohemian

Use these definitions:

CASUAL:
Simple everyday clothing with a relaxed, ordinary appearance.
Examples:
basic T-shirts, simple jeans, everyday tops, casual dresses.

FORMAL:
Structured and professional clothing intended for formal
settings.
Examples:
formal shirts, tailored trousers, suits, blazers, formal dresses.

BUSINESS CASUAL:
Smart but less formal professional clothing.
Examples:
polo shirts, chinos, smart trousers, modest blouses,
semi-formal shirts.

PARTY:
Clothing designed specifically for parties or nightlife,
especially when it has bold, glamorous or festive details.

Examples:
sequins, glitter, metallic finishes, party tops,
party dresses.

STREETWEAR:
Urban/fashion-forward casual clothing.
Examples:
oversized T-shirts, graphic tees, hoodies, cargo pants,
baggy clothing, statement sneakers.

SPORTY:
Athletic or performance-inspired clothing.
Examples:
sports jerseys, track pants, gym wear, athletic shorts,
sports shoes.

TRADITIONAL:
Clothing strongly associated with traditional cultural dress.
Examples:
saree, traditional kurta, mundu, traditional ethnic dresses.

ETHNIC:
Culturally inspired ethnic clothing, especially Indian ethnic
wear.
Examples:
salwar, churidar, ethnic kurtis, lehenga, ethnic sets.

MINIMALIST:
Simple, clean and understated design with minimal decoration,
usually with basic shapes and limited visual elements.

VINTAGE:
Clothing with a clearly recognizable older-era aesthetic,
such as retro cuts, old-fashioned prints or vintage styling.

ELEGANT:
Refined, polished and sophisticated clothing with a graceful
appearance.
Examples:
refined dresses, sophisticated blouses, polished evening wear.

BOHEMIAN:
Free-spirited clothing with artistic or relaxed details,
such as flowing silhouettes, earthy patterns, embroidery,
fringe or boho prints.

IMPORTANT STYLE RULE:

Do NOT choose Casual as a safe/default answer.

Only choose Casual when the garment's design itself is clearly
ordinary everyday casual clothing.

---------------------------------------------------------
OCCASION
---------------------------------------------------------

Choose EXACTLY ONE:

Casual
College
Office
Party
Wedding

Use the most suitable primary occasion.

CASUAL:
Normal everyday activities.

COLLEGE:
Student/campus environments and youthful everyday outfits.

OFFICE:
Professional workplace environments.

PARTY:
Parties, celebrations and nightlife.

WEDDING:
Weddings and formal cultural celebrations.

The occasion does NOT determine the style.

For example:
style = Streetwear
occasion = College

style = Formal
occasion = Office

style = Traditional
occasion = Wedding

---------------------------------------------------------
DESCRIPTION
---------------------------------------------------------

Write ONE short sentence describing the visible clothing item.

Mention important visual characteristics such as:
- silhouette
- pattern
- sleeves
- material appearance
- decorative details
- fit

Do not mention things that cannot be seen.

---------------------------------------------------------
FINAL RULES
---------------------------------------------------------

1. Return ONLY the JSON object.
2. Do NOT use markdown.
3. Do NOT add explanations.
4. Do NOT invent brands.
5. Do NOT automatically choose Casual.
6. Style must describe the garment itself.
7. Occasion must describe the most suitable use.
8. Category must be the most specific available category.
"""


    try:
        client = get_gemini_client()
        if not client:
            raise ValueError("GEMINI_API_KEY is not set or client could not be initialized.")

        model_name = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")

        try:
            config = types.GenerateContentConfig(response_mime_type="application/json")
        except Exception:
            config = None

        contents = [prompt, image]
        try:
            if config:
                response = client.models.generate_content(
                    model=model_name,
                    contents=contents,
                    config=config
                )
            else:
                response = client.models.generate_content(
                    model=model_name,
                    contents=contents
                )
        except Exception as primary_err:
            print(f"Model {model_name} failed ({primary_err}). Trying fallback to gemini-1.5-flash...")
            response = client.models.generate_content(
                model="gemini-1.5-flash",
                contents=contents
            )

        raw_text = (response.text or "").strip()

        # Extract JSON using regex to handle markdown or incidental text
        match = re.search(r'\{.*\}', raw_text, re.DOTALL)
        if match:
            clean_text = match.group(0)
        else:
            clean_text = (
                raw_text.replace("```json", "")
                .replace("```JSON", "")
                .replace("```", "")
                .strip()
            )

        result = json.loads(clean_text)

        # -------------------------------------------------
        # SAFE DEFAULTS
        # -------------------------------------------------

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
            "fabric",
            "Unknown"
        )

        result.setdefault(
            "sleeves",
            "Not Applicable"
        )

        result.setdefault(
            "occasion",
            "Casual"
        )

        result.setdefault(
            "style",
            "Casual"
        )

        result.setdefault(
            "description",
            ""
        )

        # -------------------------------------------------
        # CLEAN VALUES
        # -------------------------------------------------

        valid_categories = {
            "Top",
            "Bottom",
            "Dress",
            "Shirt",
            "T-shirt",
            "Hoodie",
            "Jacket",
            "Shoes",
            "Bag",
            "Accessory",
        }

        valid_occasions = {
            "Casual",
            "College",
            "Office",
            "Party",
            "Wedding",
        }

        valid_styles = {
            "Casual",
            "Formal",
            "Business Casual",
            "Party",
            "Streetwear",
            "Sporty",
            "Traditional",
            "Ethnic",
            "Minimalist",
            "Vintage",
            "Elegant",
            "Bohemian",
        }

        valid_sleeves = {
            "Short",
            "Long",
            "Sleeveless",
            "Not Applicable",
        }

        # Prevent invalid Gemini values from reaching Django
        if result.get("category") not in valid_categories:
            result["category"] = "Top"

        if result.get("occasion") not in valid_occasions:
            result["occasion"] = "Casual"

        if result.get("style") not in valid_styles:
            result["style"] = "Casual"

        if result.get("sleeves") not in valid_sleeves:
            result["sleeves"] = "Not Applicable"

        # -------------------------------------------------
        # SEASON
        # -------------------------------------------------

        result["season"] = detect_season(result)

        return result

    except Exception as e:

        print("Gemini Error:", e)

        return {
            "name": "Unknown Item",
            "category": "Top",
            "brand": "Unknown",
            "color": "Unknown",
            "fabric": "Unknown",
            "sleeves": "Not Applicable",
            "season": "All Season",
            "occasion": "Casual",
            "style": "Casual",
            "description": "AI unavailable",
        }


if __name__ == "__main__":
    import sys
    print("=" * 60)
    print(" ALAMARAi Clothing Detector Diagnostic")
    print("=" * 60)
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("[-] GEMINI_API_KEY is NOT set in environment or .env file.")
        print("    Add GEMINI_API_KEY=your_key_here to .env to enable AI clothing classification.")
    else:
        masked = api_key[:4] + "..." + api_key[-4:] if len(api_key) > 8 else "***"
        print(f"[+] GEMINI_API_KEY is configured ({masked}).")

    if len(sys.argv) > 1:
        test_path = sys.argv[1]
        print(f"\nAnalyzing test image: {test_path}")
        analysis = analyze_image(test_path)
        print("\nAnalysis Result:")
        print(json.dumps(analysis, indent=2))
    else:
        print("\nTo test with an image, run:")
        print('  python ai/detector.py "<path_to_image>"')
