import os
import urllib.request
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

BASE_DIR = r"f:\M_100184\static\vendor"
os.makedirs(BASE_DIR, exist_ok=True)

downloads = [
    {
        "url": "https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css",
        "path": os.path.join(BASE_DIR, "bootstrap", "css", "bootstrap.min.css")
    },
    {
        "url": "https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js",
        "path": os.path.join(BASE_DIR, "bootstrap", "js", "bootstrap.bundle.min.js")
    },
    {
        "url": "https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.5/font/bootstrap-icons.css",
        "path": os.path.join(BASE_DIR, "bootstrap-icons", "bootstrap-icons.css")
    },
    {
        "url": "https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.5/font/fonts/bootstrap-icons.woff",
        "path": os.path.join(BASE_DIR, "bootstrap-icons", "fonts", "bootstrap-icons.woff")
    },
    {
        "url": "https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.5/font/fonts/bootstrap-icons.woff2",
        "path": os.path.join(BASE_DIR, "bootstrap-icons", "fonts", "bootstrap-icons.woff2")
    },
    {
        "url": "https://cdn.jsdelivr.net/npm/chart.js@4.4.4/dist/chart.umd.min.js",
        "path": os.path.join(BASE_DIR, "chartjs", "chart.umd.min.js")
    },
    {
        "url": "https://cdn.tailwindcss.com",
        "path": os.path.join(BASE_DIR, "tailwindcss", "tailwindcss.js")
    },
    {
        "url": "https://cdn.jsdelivr.net/npm/jsbarcode@3.11.5/dist/JsBarcode.all.min.js",
        "path": os.path.join(BASE_DIR, "jsbarcode", "JsBarcode.all.min.js")
    },
    {
        "url": "https://cdnjs.cloudflare.com/ajax/libs/qrcodejs/1.0.0/qrcode.min.js",
        "path": os.path.join(BASE_DIR, "qrcodejs", "qrcode.min.js")
    },
    {
        "url": "https://cdn.jsdelivr.net/npm/xlsx@0.18.5/dist/xlsx.full.min.js",
        "path": os.path.join(BASE_DIR, "sheetjs", "xlsx.full.min.js")
    }
]

for d in downloads:
    os.makedirs(os.path.dirname(d["path"]), exist_ok=True)
    if not os.path.exists(d["path"]) or os.path.getsize(d["path"]) == 0:
        print(f"Downloading {d['url']} ...")
        try:
            urllib.request.urlretrieve(d["url"], d["path"])
            print(f"Saved to {d['path']}")
        except Exception as e:
            print(f"Failed {d['url']}: {e}")

print("Vendor downloads complete.")
