import sys
import os
from urllib.parse import urlparse

# Memastikan direktori 'src' ditambahkan ke sys.path secara mutlak
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(CURRENT_DIR, 'src')
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

try:
    from scraper import WebScraper
    from generator import KotlinGenerator
except ImportError as e:
    print(f"[ERROR] Fail modul tidak dijumpai: {e}")
    sys.exit(1)

def print_banner():
    print("=" * 60)
    print("       CSAutoPluginGen v2.0 - Universal Provider Engine     ")
    print("=" * 60)

def extract_plugin_name(url):
    parsed = urlparse(url)
    domain = parsed.netloc or parsed.path
    domain = domain.replace('www.', '').split('.')[0]
    return domain.capitalize() if domain else "Custom"

def main():
    print_banner()
    
    if len(sys.argv) > 1:
        target_url = sys.argv[1]
    else:
        target_url = input("[+] Masukkan URL Laman Web Sasaran: ").strip()

    if not target_url:
        print("[ERROR] URL tidak boleh kosong.")
        return

    print(f"\n[PHASE 1] Memulakan Analisis Web: {target_url}")
    scraper = WebScraper(target_url)
    html_content = scraper.fetch_html()

    if not html_content:
        print("[ERROR] Proses dihentikan kerana gagal mengambil HTML.")
        return

    analysis_result = scraper.analyze_structure(html_content)
    catalog_items = analysis_result.get('catalog_items', [])

    print(f"\n[SCRAPE SUCCESS] Tajuk Laman: {analysis_result['title']}")
    print(f"[CATALOG REPORT] Jumpa {len(catalog_items)} kandungan video terfilter.")

    if not catalog_items:
        print("[WARNING] Tiada kandungan terfilter ditemui. Sila semak semula struktur laman web.")
        return

    plugin_name = extract_plugin_name(target_url)
    output_filename = f"{plugin_name}Provider.kt"
    output_dir = os.path.join(CURRENT_DIR, 'output')
    output_path = os.path.join(output_dir, output_filename)

    print(f"\n[PHASE 2] Menjana Kod Provider CloudStream ({plugin_name}Provider)...")
    generator = KotlinGenerator(plugin_name, scraper.target_url)
    kt_code = generator.generate_provider_code(catalog_items)

    generator.save_code(kt_code, output_path)

    print("\n" + "=" * 60)
    print("                  PROSES SELESAI DENGAN JAYANYA               ")
    print("=" * 60)
    print(f"[OUTPUT FILE] : {output_path}")
    print(f"[PROVIDER]    : {plugin_name}Provider")
    print(f"[TOTAL ITEMS] : {len(catalog_items)} items included in MainPage")
    print("=" * 60)

if __name__ == "__main__":
    main()
