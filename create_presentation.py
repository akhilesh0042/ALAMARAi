import sys
import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

def create_deck():
    prs = Presentation()
    # Set standard widescreen 16:9 dimensions
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # -------------------------------------------------------------
    # BRAND COLOR PALETTE (Alamara i - Luxury Fashion Aesthetic)
    # -------------------------------------------------------------
    COLOR_BG = RGBColor(250, 247, 242)          # Warm Cream Background (#FAF7F2)
    COLOR_TEXT_MAIN = RGBColor(34, 34, 34)      # Deep Charcoal Text (#222222)
    COLOR_GOLD = RGBColor(197, 160, 89)          # Muted Warm Gold (#C5A059)
    COLOR_GOLD_DARK = RGBColor(165, 130, 65)     # Deep Gold (#A58241)
    COLOR_MUTED = RGBColor(118, 113, 104)       # Warm Muted Gray (#767168)
    COLOR_WHITE = RGBColor(255, 255, 255)       # Pure White
    COLOR_CARD_BG = RGBColor(255, 255, 255)     # Card Background (White)
    COLOR_CARD_BORDER = RGBColor(230, 224, 212) # Soft Tan Border (#E6E0D4)
    COLOR_ACCENT_BG = RGBColor(245, 240, 230)   # Warm Soft Tan Card Tint (#F5F0E6)
    COLOR_RED_TINT = RGBColor(253, 242, 242)    # Soft Rose Tint for Limitations
    COLOR_RED_BORDER = RGBColor(240, 200, 200)

    FONT_SERIF = "Georgia"
    FONT_SANS = "Segoe UI"

    blank_layout = prs.slide_layouts[6]

    # Helper: Set Slide Background
    def add_bg(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = COLOR_BG
        bg.line.color.rgb = COLOR_BG
        return bg

    # Helper: Add Alamara i Brand Header
    def add_header(slide, title_text, subtitle_text):
        # Top Logo Brand Text Box
        tb_logo = slide.shapes.add_textbox(Inches(0.6), Inches(0.2), Inches(6), Inches(0.6))
        tf_logo = tb_logo.text_frame
        tf_logo.word_wrap = True
        p_logo = tf_logo.paragraphs[0]
        
        r1 = p_logo.add_run()
        r1.text = "ALAMARA"
        r1.font.name = FONT_SERIF
        r1.font.size = Pt(15)
        r1.font.bold = True
        r1.font.color.rgb = COLOR_TEXT_MAIN

        r2 = p_logo.add_run()
        r2.text = " i"
        r2.font.name = FONT_SERIF
        r2.font.size = Pt(15)
        r2.font.italic = True
        r2.font.color.rgb = COLOR_GOLD

        p_sub = tf_logo.add_paragraph()
        p_sub.text = "INTELLIGENT DIGITAL WARDROBE"
        p_sub.font.name = FONT_SANS
        p_sub.font.size = Pt(7.5)
        p_sub.font.bold = True
        p_sub.font.color.rgb = COLOR_MUTED

        # Slide Title & Subtitle Box
        tb_title = slide.shapes.add_textbox(Inches(5.0), Inches(0.18), Inches(7.7), Inches(0.85))
        tf_title = tb_title.text_frame
        tf_title.word_wrap = True
        
        p_t = tf_title.paragraphs[0]
        p_t.alignment = PP_ALIGN.RIGHT
        p_t.text = title_text
        p_t.font.name = FONT_SERIF
        p_t.font.size = Pt(20)
        p_t.font.bold = True
        p_t.font.color.rgb = COLOR_TEXT_MAIN

        if subtitle_text:
            p_s = tf_title.add_paragraph()
            p_s.alignment = PP_ALIGN.RIGHT
            p_s.text = subtitle_text
            p_s.font.name = FONT_SERIF
            p_s.font.italic = True
            p_s.font.size = Pt(11.5)
            p_s.font.color.rgb = COLOR_GOLD

        # Divider Line
        line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.6), Inches(1.05), Inches(12.133), Inches(0.015))
        line.fill.solid()
        line.fill.fore_color.rgb = COLOR_CARD_BORDER
        line.line.color.rgb = COLOR_CARD_BORDER

    # Helper: Add Footer
    def add_footer(slide, current_slide, total_slides=10):
        tb = slide.shapes.add_textbox(Inches(0.6), Inches(7.1), Inches(12.133), Inches(0.35))
        tf = tb.text_frame
        p = tf.paragraphs[0]
        p.text = f"ALAMARAi  |  Fashion Outfit Analyzer Presentation  |  Slide {current_slide} of {total_slides}"
        p.font.name = FONT_SANS
        p.font.size = Pt(9)
        p.font.color.rgb = COLOR_MUTED

    # Helper: Add Card Box
    def add_card(slide, left, top, width, height, title, body_bullets, bg_color=COLOR_CARD_BG, border_color=COLOR_CARD_BORDER, title_color=None):
        shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
        shape.fill.solid()
        shape.fill.fore_color.rgb = bg_color
        shape.line.color.rgb = border_color
        shape.line.width = Pt(1.2)

        tb = slide.shapes.add_textbox(Inches(left + 0.25), Inches(top + 0.2), Inches(width - 0.5), Inches(height - 0.4))
        tf = tb.text_frame
        tf.word_wrap = True

        if title:
            p = tf.paragraphs[0]
            p.text = title
            p.font.name = FONT_SERIF
            p.font.size = Pt(15)
            p.font.bold = True
            p.font.color.rgb = title_color if title_color else COLOR_TEXT_MAIN
            p.space_after = Pt(8)

        first = True if not title else False
        for bullet in body_bullets:
            p = tf.add_paragraph() if not first else tf.paragraphs[0]
            first = False
            p.text = "• " + bullet if isinstance(bullet, str) else bullet
            p.font.name = FONT_SANS
            p.font.size = Pt(11.5)
            p.font.color.rgb = COLOR_TEXT_MAIN
            p.space_after = Pt(5)

    # -------------------------------------------------------------
    # SLIDE 1: Title Slide (Matching Alamara i Reference Image)
    # -------------------------------------------------------------
    slide1 = prs.slides.add_slide(blank_layout)
    add_bg(slide1)

    # Top Brand Logo
    tb1_logo = slide1.shapes.add_textbox(Inches(0), Inches(0.6), Inches(13.333), Inches(1.0))
    tf1_logo = tb1_logo.text_frame
    tf1_logo.word_wrap = True
    p1_logo = tf1_logo.paragraphs[0]
    p1_logo.alignment = PP_ALIGN.CENTER
    
    r1 = p1_logo.add_run()
    r1.text = "ALAMARA"
    r1.font.name = FONT_SERIF
    r1.font.size = Pt(28)
    r1.font.bold = True
    r1.font.color.rgb = COLOR_TEXT_MAIN

    r2 = p1_logo.add_run()
    r2.text = " i"
    r2.font.name = FONT_SERIF
    r2.font.size = Pt(28)
    r2.font.italic = True
    r2.font.color.rgb = COLOR_GOLD

    p1_sublogo = tf1_logo.add_paragraph()
    p1_sublogo.alignment = PP_ALIGN.CENTER
    p1_sublogo.text = "INTELLIGENT DIGITAL WARDROBE"
    p1_sublogo.font.name = FONT_SANS
    p1_sublogo.font.size = Pt(9.5)
    p1_sublogo.font.bold = True
    p1_sublogo.font.color.rgb = COLOR_MUTED
    p1_sublogo.space_before = Pt(4)

    # Subtle Divider Line
    div1 = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(5.666), Inches(1.7), Inches(2.0), Inches(0.015))
    div1.fill.solid()
    div1.fill.fore_color.rgb = COLOR_CARD_BORDER
    div1.line.color.rgb = COLOR_CARD_BORDER

    # Main Headline & Subtitle Box
    tb1_main = slide1.shapes.add_textbox(Inches(1.5), Inches(2.2), Inches(10.333), Inches(3.0))
    tf1_main = tb1_main.text_frame
    tf1_main.word_wrap = True

    p1_h1 = tf1_main.paragraphs[0]
    p1_h1.alignment = PP_ALIGN.CENTER
    p1_h1.text = "Your wardrobe."
    p1_h1.font.name = FONT_SERIF
    p1_h1.font.size = Pt(46)
    p1_h1.font.color.rgb = COLOR_TEXT_MAIN

    p1_h2 = tf1_main.add_paragraph()
    p1_h2.alignment = PP_ALIGN.CENTER
    p1_h2.text = "Reimagined."
    p1_h2.font.name = FONT_SERIF
    p1_h2.font.italic = True
    p1_h2.font.size = Pt(46)
    p1_h2.font.color.rgb = COLOR_GOLD
    p1_h2.space_before = Pt(2)

    p1_desc = tf1_main.add_paragraph()
    p1_desc.alignment = PP_ALIGN.CENTER
    p1_desc.text = "Organize your clothing collection, discover smart outfit ideas,\nand build a timeless digital wardrobe designed for your everyday style."
    p1_desc.font.name = FONT_SANS
    p1_desc.font.size = Pt(14)
    p1_desc.font.color.rgb = COLOR_MUTED
    p1_desc.space_before = Pt(18)

    # Buttons Container (Pill Shapes matching image)
    # Button 1: Gold Pill "Get Started"
    btn1 = slide1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(4.5), Inches(5.4), Inches(2.0), Inches(0.55))
    btn1.fill.solid()
    btn1.fill.fore_color.rgb = COLOR_GOLD
    btn1.line.color.rgb = COLOR_GOLD
    tf_b1 = btn1.text_frame
    p_b1 = tf_b1.paragraphs[0]
    p_b1.alignment = PP_ALIGN.CENTER
    p_b1.text = "Get Started"
    p_b1.font.name = FONT_SANS
    p_b1.font.size = Pt(12)
    p_b1.font.bold = True
    p_b1.font.color.rgb = COLOR_WHITE

    # Button 2: White Pill "LEARN MORE"
    btn2 = slide1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(5.4), Inches(2.0), Inches(0.55))
    btn2.fill.solid()
    btn2.fill.fore_color.rgb = COLOR_WHITE
    btn2.line.color.rgb = COLOR_CARD_BORDER
    btn2.line.width = Pt(1.5)
    tf_b2 = btn2.text_frame
    p_b2 = tf_b2.paragraphs[0]
    p_b2.alignment = PP_ALIGN.CENTER
    p_b2.text = "LEARN MORE"
    p_b2.font.name = FONT_SANS
    p_b2.font.size = Pt(11)
    p_b2.font.bold = True
    p_b2.font.color.rgb = COLOR_TEXT_MAIN

    # Sub metadata
    tb1_meta = slide1.shapes.add_textbox(Inches(1.5), Inches(6.6), Inches(10.333), Inches(0.4))
    tf1_meta = tb1_meta.text_frame
    p1_m = tf1_meta.paragraphs[0]
    p1_m.alignment = PP_ALIGN.CENTER
    p1_m.text = "Project: Fashion Outfit Analyzer  |  Built with Django & Google Gemini 2.5 Flash AI"
    p1_m.font.name = FONT_SANS
    p1_m.font.size = Pt(10)
    p1_m.font.italic = True
    p1_m.font.color.rgb = COLOR_MUTED

    # -------------------------------------------------------------
    # SLIDE 2: What Project is About
    # -------------------------------------------------------------
    slide2 = prs.slides.add_slide(blank_layout)
    add_bg(slide2)
    add_header(slide2, "1. What the Project is About", "Project Overview & Core Vision")
    add_footer(slide2, 2)

    add_card(slide2, 0.6, 1.4, 3.8, 5.3, "Smart Digital Wardrobe", [
        "Digitizes physical clothing items into a structured online repository.",
        "Allows users to manage, catalog, search, and filter their entire wardrobe efficiently.",
        "Tracks wear history, last worn dates, and item favorites to optimize wardrobe utility."
    ], bg_color=COLOR_CARD_BG)

    add_card(slide2, 4.7, 1.4, 3.8, 5.3, "Multimodal AI Analysis", [
        "Integrates Google Gemini 2.5 Flash Computer Vision model for instant visual recognition.",
        "Automatically identifies garment categories (Top, Bottom, Dress, Shoes, Bags, Accessories).",
        "Extracts dominant color, fabric/material type, styling classification, and occasion suitability."
    ], bg_color=COLOR_ACCENT_BG, title_color=COLOR_GOLD_DARK)

    add_card(slide2, 8.8, 1.4, 3.8, 5.3, "Automated Personal Stylist", [
        "Algorithmic outfit recommendation engine combining clothing pieces into complete looks.",
        "Evaluates occasion alignment, seasonal appropriateness, style harmony, and color contrast.",
        "Provides 3 distinct look options: 'Best Match', 'Alternative Style', and 'Trending Look'."
    ], bg_color=COLOR_CARD_BG)

    # -------------------------------------------------------------
    # SLIDE 3: Objectives of the Project
    # -------------------------------------------------------------
    slide3 = prs.slides.add_slide(blank_layout)
    add_bg(slide3)
    add_header(slide3, "2. Objectives of the Project", "Core Goals & Intended Capabilities")
    add_footer(slide3, 3)

    add_card(slide3, 0.6, 1.4, 5.8, 2.5, "Automated Feature Extraction", [
        "Eliminate manual data entry by extracting clothing attributes from single uploaded images.",
        "Achieve zero-shot identification of category, fabric, style, occasion, and dominant colors."
    ], bg_color=COLOR_CARD_BG)

    add_card(slide3, 6.8, 1.4, 5.8, 2.5, "Organized Inventory Management", [
        "Build a robust database structure supporting fast multi-attribute search and filtering.",
        "Enable seamless organizing across categories (Tops, Bottoms, Shoes), seasons, and occasions."
    ], bg_color=COLOR_ACCENT_BG, title_color=COLOR_GOLD_DARK)

    add_card(slide3, 0.6, 4.2, 5.8, 2.5, "Intelligent Outfit Compatibility", [
        "Develop a multi-criteria scoring algorithm based on color theory and style principles.",
        "Provide tailored outfit suggestions matched specifically to weather conditions and events."
    ], bg_color=COLOR_ACCENT_BG, title_color=COLOR_GOLD_DARK)

    add_card(slide3, 6.8, 4.2, 5.8, 2.5, "Wardrobe Insights & Analytics", [
        "Provide users with visual statistics on wardrobe balance and clothing usage.",
        "Automatically detect wardrobe gaps (e.g., missing rainwear or formal accessories) to guide purchasing."
    ], bg_color=COLOR_CARD_BG)

    # -------------------------------------------------------------
    # SLIDE 4: Existing Systems & Limitations
    # -------------------------------------------------------------
    slide4 = prs.slides.add_slide(blank_layout)
    add_bg(slide4)
    add_header(slide4, "3. Existing Systems & Limitations", "Analysis of Current Solutions and Challenges")
    add_footer(slide4, 4)

    add_card(slide4, 0.6, 1.4, 5.8, 5.3, "Existing Systems & Practices", [
        "Manual Photo Storage:",
        "Users store images in unorganized smartphone galleries or simple cloud folders.",
        "Spreadsheets & Manual Lists:",
        "Cataloging clothes using manual data entry in Excel/Notion, requiring immense setup effort.",
        "Basic Closet Apps:",
        "Existing apps require users to manually type tags, colors, and categories for every item.",
        "Physical Trial & Error:",
        "Trying on multiple clothes physically before events, causing unnecessary waste of time."
    ], bg_color=COLOR_CARD_BG)

    add_card(slide4, 6.8, 1.4, 5.8, 5.3, "Key Limitations of Existing Systems", [
        "High Friction & Manual Burden:",
        "Manual entry of 10+ metadata fields per item leads to rapid user abandonment.",
        "Lack of Aesthetic Intelligence:",
        "Simple apps lack computer vision to understand color harmony, style rules, or fabric weight.",
        "No Automated Outfit Generation:",
        "Existing solutions don't generate intelligent top+bottom combinations dynamically.",
        "Overlooked Wardrobe Potential:",
        "Unsorted clothing remains hidden, leading to over-purchasing duplicate items."
    ], bg_color=COLOR_RED_TINT, border_color=COLOR_RED_BORDER, title_color=RGBColor(180, 50, 50))

    # -------------------------------------------------------------
    # SLIDE 5: Proposed System & Key Advantages
    # -------------------------------------------------------------
    slide5 = prs.slides.add_slide(blank_layout)
    add_bg(slide5)
    add_header(slide5, "4. Proposed System & Key Advantages", "Innovative Solution & Value Deliverables")
    add_footer(slide5, 5)

    add_card(slide5, 0.6, 1.4, 12.133, 5.3, "Proposed Solution: Fashion Outfit Analyzer", [
        "Zero-Effort AI Tagging:",
        "Users upload a photo, and Google Gemini 2.5 Flash automatically populates category, color, fabric, style, and occasion within seconds.",
        "Algorithmic Compatibility Engine:",
        "Evaluates top+bottom and dress ensembles across 4 key vectors: Occasion Score, Weather/Season Score, Style Consistency, and Color Harmony.",
        "Interactive Wardrobe Dashboard:",
        "Provides real-time visual progress metrics, wear counts, color breakdown analytics, and intelligent wardrobe health suggestions.",
        "Curated Look Suggestions with E-Commerce Search:",
        "Generates top 3 distinct outfit combinations and outputs keyword query strings for missing shopping accessories.",
        "User-Controlled Refinement:",
        "Users retain full control to manually adjust AI-detected tags, mark favorite items, and track wear history."
    ], bg_color=COLOR_ACCENT_BG, title_color=COLOR_GOLD_DARK)

    # -------------------------------------------------------------
    # SLIDE 6: How It Is Developed (Tech Stack & Architecture)
    # -------------------------------------------------------------
    slide6 = prs.slides.add_slide(blank_layout)
    add_bg(slide6)
    add_header(slide6, "5. Development Methodology & Tech Stack", "Technologies, Frameworks, and Tools Utilized")
    add_footer(slide6, 6)

    add_card(slide6, 0.6, 1.4, 5.8, 2.5, "Frontend Framework", [
        "HTML5, CSS3, JavaScript (ES6+)",
        "Bootstrap 5 Responsive Grid System",
        "Modern UI/UX with warm luxury theme, cards, and dynamic micro-animations."
    ], bg_color=COLOR_CARD_BG)

    add_card(slide6, 6.8, 1.4, 5.8, 2.5, "Backend Infrastructure", [
        "Python 3.12 Programming Language",
        "Django 6.0 Web Framework (MVT Architecture)",
        "Robust ORM, URL Routing, Forms, Session Management, and Secure Authentication."
    ], bg_color=COLOR_ACCENT_BG, title_color=COLOR_GOLD_DARK)

    add_card(slide6, 0.6, 4.2, 5.8, 2.5, "AI & Computer Vision Integration", [
        "Google GenAI SDK & Gemini 2.5 Flash Model",
        "Pillow (PIL) & OpenCV for image preprocessing",
        "Structured JSON Prompting & Rule-Based Heuristics for fabric/season detection."
    ], bg_color=COLOR_ACCENT_BG, title_color=COLOR_GOLD_DARK)

    add_card(slide6, 6.8, 4.2, 5.8, 2.5, "Database & Storage", [
        "SQLite Relational Database Engine",
        "Django FileSystemStorage for image assets",
        "Configured for seamless migration to MySQL/PostgreSQL in production environments."
    ], bg_color=COLOR_CARD_BG)

    # -------------------------------------------------------------
    # SLIDE 7: Key Features of the System
    # -------------------------------------------------------------
    slide7 = prs.slides.add_slide(blank_layout)
    add_bg(slide7)
    add_header(slide7, "6. Key Features of the Application", "Comprehensive System Functionalities")
    add_footer(slide7, 7)

    add_card(slide7, 0.6, 1.4, 3.8, 5.3, "1. AI Upload & Vision", [
        "Single-click image upload.",
        "Multimodal LLM vision analysis.",
        "Automatic metadata extraction (Name, Category, Color, Fabric, Style, Occasion).",
        "Automated Season Heuristic (Summer, Winter, Rainy, All Season)."
    ], bg_color=COLOR_CARD_BG)

    add_card(slide7, 4.7, 1.4, 3.8, 5.3, "2. Digital Wardrobe", [
        "Grid layout of digital wardrobe.",
        "Real-time multi-criteria filtering by category, color, season, and occasion.",
        "Full CRUD functionality (Add, Edit, View, Delete items).",
        "Item wear counter & favorite flagging."
    ], bg_color=COLOR_ACCENT_BG, title_color=COLOR_GOLD_DARK)

    add_card(slide7, 8.8, 1.4, 3.8, 5.3, "3. Outfit Stylist & Analytics", [
        "Interactive Outfit Generator based on event, weather, style, and color preferences.",
        "Top 3 recommendation cards ('Best Match', 'Alternative Style', 'Trending Look').",
        "Visual Wardrobe Analytics & Smart Health Insights."
    ], bg_color=COLOR_CARD_BG)

    # -------------------------------------------------------------
    # SLIDE 8: Techniques & AI Algorithms Used
    # -------------------------------------------------------------
    slide8 = prs.slides.add_slide(blank_layout)
    add_bg(slide8)
    add_header(slide8, "7. Techniques & AI Algorithms Used", "Algorithmic & Machine Learning Foundations")
    add_footer(slide8, 8)

    add_card(slide8, 0.6, 1.4, 5.8, 2.5, "Multimodal Generative Vision AI", [
        "Uses Google Gemini 2.5 Flash model with structured JSON schema constraints.",
        "Zero-shot feature extraction converting visual pixels into structured database records."
    ], bg_color=COLOR_CARD_BG)

    add_card(slide8, 6.8, 1.4, 5.8, 2.5, "Rule-Based Season Detection", [
        "NLP heuristic parsing garment descriptions & fabric keywords.",
        "Maps fabrics (wool, sweater, coat -> Winter; cotton, linen, short -> Summer; raincoat -> Rainy)."
    ], bg_color=COLOR_ACCENT_BG, title_color=COLOR_GOLD_DARK)

    add_card(slide8, 0.6, 4.2, 5.8, 2.5, "Multi-Factor Outfit Scoring", [
        "Evaluates 4 compatibility vectors: Occasion Fit, Weather Fit, Style Consistency, & Color Contrast.",
        "Produces normalized numerical scores to rank candidate outfit combinations objectively."
    ], bg_color=COLOR_ACCENT_BG, title_color=COLOR_GOLD_DARK)

    add_card(slide8, 6.8, 4.2, 5.8, 2.5, "Combinatorial Optimization & Diversity", [
        "Utilizes Cartesian products (itertools.product) across filtered Top, Bottom, Shoe, & Bag items.",
        "Prunes duplicate items to present diverse, high-ranking top 3 outfit configurations."
    ], bg_color=COLOR_CARD_BG)

    # -------------------------------------------------------------
    # SLIDE 9: Module Description
    # -------------------------------------------------------------
    slide9 = prs.slides.add_slide(blank_layout)
    add_bg(slide9)
    add_header(slide9, "8. Module Description & Software Structure", "Detailed Component Decomposition")
    add_footer(slide9, 9)

    add_card(slide9, 0.6, 1.4, 5.8, 2.5, "Module: `ai/` (AI Engine)", [
        "detector.py: Initializes Gemini API client, formats visual prompt, parses clean JSON responses, and executes seasonal rule-based fallback detection."
    ], bg_color=COLOR_CARD_BG)

    add_card(slide9, 6.8, 1.4, 5.8, 2.5, "Module: `wardrobe/` (Inventory)", [
        "models.py & views.py: Manages ClothingItem schema, manual and AI image upload views (ai_upload, save_ai_item), search filtering, edit, and deletion logic."
    ], bg_color=COLOR_ACCENT_BG, title_color=COLOR_GOLD_DARK)

    add_card(slide9, 0.6, 4.2, 5.8, 2.5, "Module: `stylist/` (Recommendation)", [
        "recommendation.py, scoring.py, selectors.py: Orchestrates outfit generation, filters suitable items, calculates multi-vector scores, and builds human-readable outfit rationale."
    ], bg_color=COLOR_ACCENT_BG, title_color=COLOR_GOLD_DARK)

    add_card(slide9, 6.8, 4.2, 5.8, 2.5, "Module: `core/`, `dashboard/` & `accounts/`", [
        "Handles landing page, user metrics dashboard (calc_pct distribution stats, activity logs), user registration, login authentication, and user profile management."
    ], bg_color=COLOR_CARD_BG)

    # -------------------------------------------------------------
    # SLIDE 10: Conclusion & Future Scope
    # -------------------------------------------------------------
    slide10 = prs.slides.add_slide(blank_layout)
    add_bg(slide10)
    add_header(slide10, "9. Conclusion & Future Enhancements", "Summary and Strategic Growth Roadmap")
    add_footer(slide10, 10)

    add_card(slide10, 0.6, 1.4, 5.8, 5.3, "Conclusion", [
        "Successful AI Integration:",
        "Successfully bridges modern computer vision (Gemini 2.5 Flash) with web development to solve everyday fashion decisions.",
        "Enhanced User Experience:",
        "Reduces wardrobe organization effort by 90% through automated tagging.",
        "Algorithmic Precision:",
        "Provides objective, color-coordinated, weather-appropriate outfit combinations.",
        "Production-Ready Architecture:",
        "Built on robust Django web architecture following clean MVT design patterns."
    ], bg_color=COLOR_CARD_BG)

    add_card(slide10, 6.8, 1.4, 5.8, 5.3, "Future Scope & Enhancements", [
        "Live Weather API Integration:",
        "Connect OpenWeather API to dynamically fetch user location weather and refine seasonal scoring.",
        "Virtual AR Try-On:",
        "Integrate 3D avatar visualization for realistic augmented reality outfit preview.",
        "Smart Shopping Integration:",
        "Automate affiliate product suggestions for missing wardrobe essentials.",
        "Social Outfit Sharing:",
        "Enable community style sharing, voting, and collaborative styling consultations."
    ], bg_color=RGBColor(240, 248, 242), border_color=RGBColor(180, 220, 190), title_color=RGBColor(40, 120, 60))

    # Save presentation
    output_path = os.path.join(r"c:\Users\LOQ\OneDrive\Desktop\fashion-outfit-analyzer-main", "Fashion_Outfit_Analyzer_Presentation.pptx")
    prs.save(output_path)
    print(f"Presentation successfully updated at: {output_path}")

if __name__ == "__main__":
    create_deck()
