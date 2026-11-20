import os
import sys
import shutil
import re
import urllib.parse
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
    print("Authenticated as 'mypro' for export")

anon_client = Client()

routes = [
    ('/', 'index.html', anon_client),
    ('/dashboard/', 'dashboard/index.html', auth_client),
    ('/wardrobe/', 'wardrobe/index.html', auth_client),
    ('/wardrobe/ai-upload/', 'wardrobe/ai-upload/index.html', auth_client),
    ('/wardrobe/upload/', 'wardrobe/upload/index.html', auth_client),
    ('/stylist/', 'stylist/index.html', auth_client),
    ('/profile/', 'profile/index.html', auth_client),
    ('/accounts/login/', 'accounts/login/index.html', anon_client),
    ('/accounts/signup/', 'accounts/signup/index.html', anon_client),
]

def adjust_html_for_gh_pages(html_content, rel_file):
    # Calculate relative root accurately from file location
    file_dir = os.path.dirname(os.path.join(OUTPUT_DIR, rel_file))
    rel_path = os.path.relpath(OUTPUT_DIR, file_dir).replace('\\', '/')
    rel_root = (rel_path + '/') if rel_path != '.' else './'

    # 1. Assets: static & media
    html_content = re.sub(r'(href|src)=["\']/static/([^"\']*)["\']', rf'\1="{rel_root}static/\2"', html_content)
    html_content = re.sub(r'(href|src)=["\']/media/([^"\']*)["\']', rf'\1="{rel_root}media/\2"', html_content)
    html_content = re.sub(r'url\(["\']?/static/([^"\')]+)["\']?\)', rf'url("{rel_root}static/\1")', html_content)
    html_content = re.sub(r'url\(["\']?/media/([^"\')]+)["\']?\)', rf'url("{rel_root}media/\1")', html_content)

    # 2. Navigation routes
    html_content = re.sub(r'href=["\']/wardrobe/(?:ai-upload|upload)(?:/[^"\']*)?["\']', f'href="{rel_root}wardrobe/ai-upload/index.html"', html_content)
    html_content = re.sub(r'href=["\']/wardrobe/(?:\?[^"\']*)?["\']', f'href="{rel_root}wardrobe/index.html"', html_content)
    html_content = re.sub(r'href=["\']/dashboard/(?:\?[^"\']*)?["\']', f'href="{rel_root}dashboard/index.html"', html_content)
    html_content = re.sub(r'href=["\']/stylist/(?:\?[^"\']*)?["\']', f'href="{rel_root}stylist/index.html"', html_content)
    html_content = re.sub(r'href=["\']/profile/(?:\?[^"\']*)?["\']', f'href="{rel_root}profile/index.html"', html_content)
    html_content = re.sub(r'href=["\']/accounts/profile/(?:\?[^"\']*)?["\']', f'href="{rel_root}profile/index.html"', html_content)
    html_content = re.sub(r'href=["\']/accounts/login/(?:\?[^"\']*)?["\']', f'href="{rel_root}accounts/login/index.html"', html_content)
    html_content = re.sub(r'href=["\']/accounts/signup/(?:\?[^"\']*)?["\']', f'href="{rel_root}accounts/signup/index.html"', html_content)
    html_content = re.sub(r'href=["\']/wardrobe/(?:edit|delete)/\d+/?["\']', 'href="javascript:void(0)" onclick="alert(\'Note: Dynamic item modification (edit/delete) requires the full Django backend (e.g. on Render/Railway). This GitHub Pages preview showcases your 43 items in read-only mode.\')"', html_content)
    html_content = re.sub(r'href=["\']/accounts/password_reset/(?:\?[^"\']*)?["\']', f'href="{rel_root}accounts/login/index.html"', html_content)
    html_content = re.sub(r'href=["\']/accounts/logout/(?:\?[^"\']*)?["\']', f'href="{rel_root}index.html"', html_content)
    html_content = re.sub(r'href=["\']/(home/?)?["\']', f'href="{rel_root}index.html"', html_content)

    return html_content

    return html_content

for url, rel_file, client in routes:
    res = client.get(url, HTTP_HOST='127.0.0.1')
    if res.status_code == 200:
        html = res.content.decode('utf-8', errors='ignore')
        html = adjust_html_for_gh_pages(html, rel_file)
        dest_path = os.path.join(OUTPUT_DIR, rel_file)
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
        with open(dest_path, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"Exported {url:18} -> docs/{rel_file} ({len(html)} bytes)")
    else:
        print(f"Failed to fetch {url}: status {res.status_code}")

# Copy index.html to 404.html
shutil.copy2(os.path.join(OUTPUT_DIR, 'index.html'), os.path.join(OUTPUT_DIR, '404.html'))
print("Created docs/404.html")

# Create .nojekyll
with open(os.path.join(OUTPUT_DIR, '.nojekyll'), 'w') as f:
    f.write('')
print("Created docs/.nojekyll")

# 3. VERIFY ALL ASSETS ACROSS ALL EXPORTED HTML FILES
print("\n=== VERIFYING EXPORTED ASSETS ===")
total_checks = 0
broken_checks = []

for root, _, files in os.walk(OUTPUT_DIR):
    for f in files:
        if f.endswith('.html'):
            html_path = os.path.join(root, f)
            with open(html_path, 'r', encoding='utf-8') as hf:
                doc = hf.read()
            # find all src and href
            matches = re.findall(r'(src|href)=["\']([^"\']+)["\']', doc)
            for attr, val in matches:
                # ignore external or anchor or tel/mailto or JS template literals
                if val.startswith(('http://', 'https://', '//', '#', 'mailto:', 'tel:', 'javascript:')) or '${' in val:
                    continue
                # strip query string
                clean_val = val.split('?')[0]
                # decode url
                clean_val = urllib.parse.unquote(clean_val)
                # resolve relative to html file
                target_path = os.path.normpath(os.path.join(root, clean_val))
                total_checks += 1
                if not os.path.exists(target_path):
                    broken_checks.append((os.path.relpath(html_path, OUTPUT_DIR), attr, val, target_path))

print(f"Total internal asset & link references verified: {total_checks}")
if broken_checks:
    print(f"WARNING: Found {len(broken_checks)} broken references:")
    for src_file, attr, val, tpath in broken_checks[:10]:
        print(f"  In {src_file} ({attr}={val}) -> Missing: {tpath}")
else:
    print("SUCCESS: 0 broken assets or links found! All images, CSS, and routes exist.")
