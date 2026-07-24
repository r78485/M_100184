import shutil
import os
import urllib.request
import ssl
import subprocess

ssl._create_default_https_context = ssl._create_unverified_context

try:
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    logo = os.path.join(base, 'static', 'logo.png')
    target192 = os.path.join(base, 'static', 'icon-192x192.png')
    target512 = os.path.join(base, 'static', 'icon-512x512.png')
    if os.path.exists(logo):
        shutil.copy(logo, target192)
        shutil.copy(logo, target512)
        
    # Copy user-uploaded real school photo to static/school_campus.png
    user_img_path = r"C:\Users\Islam Talicom\.gemini\antigravity-ide\brain\e39cf3a2-d7f7-4918-b1b7-d518574d28e6\media__1784880243345.jpg"
    target_campus = os.path.join(base, 'static', 'school_campus.png')
    if os.path.exists(user_img_path):
        shutil.copy(user_img_path, target_campus)

    # Ensure vendor assets for full offline compatibility
    vendor_dir = os.path.join(base, 'static', 'vendor')
    vendor_downloads = [
        ("https://cdn.tailwindcss.com", os.path.join(vendor_dir, "tailwindcss", "tailwindcss.js")),
        ("https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css", os.path.join(vendor_dir, "bootstrap", "css", "bootstrap.min.css")),
        ("https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js", os.path.join(vendor_dir, "bootstrap", "js", "bootstrap.bundle.min.js")),
        ("https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.5/font/bootstrap-icons.css", os.path.join(vendor_dir, "bootstrap-icons", "bootstrap-icons.css")),
        ("https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.5/font/fonts/bootstrap-icons.woff", os.path.join(vendor_dir, "bootstrap-icons", "fonts", "bootstrap-icons.woff")),
        ("https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.5/font/fonts/bootstrap-icons.woff2", os.path.join(vendor_dir, "bootstrap-icons", "fonts", "bootstrap-icons.woff2")),
        ("https://cdn.jsdelivr.net/npm/chart.js@4.4.4/dist/chart.umd.min.js", os.path.join(vendor_dir, "chartjs", "chart.umd.min.js")),
        ("https://cdn.jsdelivr.net/npm/jsbarcode@3.11.5/dist/JsBarcode.all.min.js", os.path.join(vendor_dir, "jsbarcode", "JsBarcode.all.min.js")),
        ("https://cdnjs.cloudflare.com/ajax/libs/qrcodejs/1.0.0/qrcode.min.js", os.path.join(vendor_dir, "qrcodejs", "qrcode.min.js")),
        ("https://cdn.jsdelivr.net/npm/xlsx@0.18.5/dist/xlsx.full.min.js", os.path.join(vendor_dir, "sheetjs", "xlsx.full.min.js"))
    ]

    for url, file_path in vendor_downloads:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
            try:
                req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req) as response, open(file_path, 'wb') as out_file:
                    shutil.copyfileobj(response, out_file)
            except Exception as ve:
                print(f"Vendor download warning ({url}): {ve}")

    # Ensure launcher & desktop shortcut script run
    try:
        dt_script = os.path.join(base, 'create_desktop_shortcut.py')
        if os.path.exists(dt_script):
            subprocess.run(["python", dt_script], cwd=base, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception:
        pass

except Exception as e:
    print(f"ensure_icons error: {e}")
