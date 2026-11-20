import os
import sys
import shutil
import django

# Setup Django
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User

OUTPUT_DIR = os.path.join(BASE_DIR, 'docs')

os.makedirs(OUTPUT_DIR, exist_ok=True)

# 1. Copy static files
static_src = os.path.join(BASE_DIR, 'static')
static_dest = os.path.join(OUTPUT_DIR, 'static')
if os.path.exists(static_src):
    shutil.copytree(static_src, static_dest, dirs_exist_ok=True)
    print("Copied static/ to docs/static/")

# 2. Copy media files
media_src = os.path.join(BASE_DIR, 'media')
media_dest = os.path.join(OUTPUT_DIR, 'media')
if os.path.exists(media_src):
    shutil.copytree(media_src, media_dest, dirs_exist_ok=True)
    print("Copied media/ to docs/media/")

auth_client = Client()
user = User.objects.filter(username='mypro').first()
if user:
    auth_client.force_login(user)
    print("Authenticated as 'mypro' for protected views")

anon_client = Client()

routes = [
    # (url, filename, client)
    ('/', 'index.html', anon_client),
    ('/dashboard/', 'dashboard/index.html', auth_client),
    ('/wardrobe/', 'wardrobe/index.html', auth_client),
    ('/stylist/', 'stylist/index.html', auth_client),
    ('/profile/', 'profile/index.html', auth_client),
    ('/accounts/login/', 'accounts/login/index.html', anon_client),
    ('/accounts/signup/', 'accounts/signup/index.html', anon_client),
]

def adjust_html_for_gh_pages(html_content, route):
    depth = route.strip('/').count('/') if route.strip('/') else 0
    rel_root = '../' * depth if depth > 0 else './'

    banner = f'''
    <div style="background: linear-gradient(90deg, #111111, #1e1e1e); color: #C8A96A; text-align: center; padding: 10px 16px; font-size: 13px; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; position: sticky; top: 0; z-index: 999999; border-bottom: 1px solid rgba(200,169,106,0.3); display: flex; align-items: center; justify-content: center; gap: 15px; flex-wrap: wrap;">
        <span>✨ <strong>ALAMARAi Live Preview on GitHub Pages</strong> (43 Wardrobe Items Loaded)</span>
        <div style="display: flex; gap: 10px;">
            <a href="{rel_root}dashboard/index.html" style="color: #fff; background: rgba(200,169,106,0.25); padding: 3px 10px; border-radius: 4px; text-decoration: none; font-size: 12px; border: 1px solid #C8A96A;">Dashboard</a>
            <a href="{rel_root}wardrobe/index.html" style="color: #fff; background: rgba(200,169,106,0.25); padding: 3px 10px; border-radius: 4px; text-decoration: none; font-size: 12px; border: 1px solid #C8A96A;">Wardrobe</a>
            <a href="{rel_root}stylist/index.html" style="color: #fff; background: rgba(200,169,106,0.25); padding: 3px 10px; border-radius: 4px; text-decoration: none; font-size: 12px; border: 1px solid #C8A96A;">Stylist</a>
            <a href="https://github.com/akhilesh0042/ALAMARAi" target="_blank" style="color: #C8A96A; text-decoration: underline; font-size: 12px; margin-left: 5px;">GitHub Repo</a>
        </div>
    </div>
    '''

    if '<body' in html_content:
        parts = html_content.split('<body', 1)
        tag_end = parts[1].find('>')
        html_content = parts[0] + '<body' + parts[1][:tag_end+1] + banner + parts[1][tag_end+1:]

    # Relative static & media assets
    html_content = html_content.replace('href="/static/', f'href="{rel_root}static/')
    html_content = html_content.replace('src="/static/', f'src="{rel_root}static/')
    html_content = html_content.replace('href="/media/', f'href="{rel_root}media/')
    html_content = html_content.replace('src="/media/', f'src="{rel_root}media/')
    html_content = html_content.replace('url(\'/static/', f'url(\'{rel_root}static/')
    html_content = html_content.replace('url(\'/media/', f'url(\'{rel_root}media/')
    html_content = html_content.replace('url("/static/', f'url("{rel_root}static/')
    html_content = html_content.replace('url("/media/', f'url("{rel_root}media/')

    # Relative navigation links
    html_content = html_content.replace('href="/dashboard/"', f'href="{rel_root}dashboard/index.html"')
    html_content = html_content.replace('href="/wardrobe/"', f'href="{rel_root}wardrobe/index.html"')
    html_content = html_content.replace('href="/stylist/"', f'href="{rel_root}stylist/index.html"')
    html_content = html_content.replace('href="/profile/"', f'href="{rel_root}profile/index.html"')
    html_content = html_content.replace('href="/accounts/profile/"', f'href="{rel_root}profile/index.html"')
    html_content = html_content.replace('href="/accounts/login/"', f'href="{rel_root}accounts/login/index.html"')
    html_content = html_content.replace('href="/accounts/signup/"', f'href="{rel_root}accounts/signup/index.html"')
    html_content = html_content.replace('href="/"', f'href="{rel_root}index.html"')
    html_content = html_content.replace('href="/home/"', f'href="{rel_root}dashboard/index.html"')

    return html_content

for url, rel_file, client in routes:
    res = client.get(url, HTTP_HOST='127.0.0.1')
    if res.status_code == 200:
        html = res.content.decode('utf-8', errors='ignore')
        html = adjust_html_for_gh_pages(html, url)
        dest_path = os.path.join(OUTPUT_DIR, rel_file)
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
        with open(dest_path, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"Exported {url:18} -> docs/{rel_file} ({len(html)} bytes)")
    else:
        print(f"Failed to fetch {url}: status {res.status_code}")

# Copy index.html to 404.html so GitHub Pages SPA routing works
shutil.copy2(os.path.join(OUTPUT_DIR, 'index.html'), os.path.join(OUTPUT_DIR, '404.html'))
print("Created docs/404.html")

# Create .nojekyll
with open(os.path.join(OUTPUT_DIR, '.nojekyll'), 'w') as f:
    f.write('')
print("Created docs/.nojekyll")

print("\nStatic export completed successfully in docs/!")
