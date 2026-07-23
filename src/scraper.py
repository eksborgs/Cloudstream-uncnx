import urllib.request
import urllib.parse
import re

class WebScraper:
    def __init__(self, target_url):
        if not target_url.startswith(('http://', 'https://')):
            self.target_url = 'https://' + target_url
        else:
            self.target_url = target_url

    def fetch_html(self):
        try:
            req = urllib.request.Request(
                self.target_url, 
                headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'}
            )
            with urllib.request.urlopen(req, timeout=10) as response:
                return response.read().decode('utf-8', errors='ignore')
        except Exception as e:
            print(f"[ERROR] Gagal mengambil HTML dari {self.target_url}: {e}")
            return None

    def analyze_structure(self, html):
        title_match = re.search(r'<title>(.*?)</title>', html, re.IGNORECASE)
        page_title = title_match.group(1).strip() if title_match else "Unknown"

        # Regex Fleksibel: Mencari blok pautan yang mengandungi imej
        catalog_items = []
        seen_urls = set()

        # Ekstraksi semua tag <a> ... </a>
        links = re.findall(r'<a\s+[^>]*href=["\']([^"\']+)["\'][^>]*>(.*?)</a>', html, re.DOTALL | re.IGNORECASE)

        for href, inner_html in links:
            # Cari imej di dalam pautan (menyokong src, data-src, data-lazy-src)
            img_match = re.search(r'<img\s+[^>]*(?:src|data-src|data-lazy-src)=["\']([^"\']+)["\'][^>]*>', inner_html, re.IGNORECASE)
            
            if img_match:
                img_url = img_match.group(1)
                
                # Cari tajuk dari alt, title, atau teks di dalam pautan
                alt_match = re.search(r'alt=["\']([^"\']+)["\']', inner_html, re.IGNORECASE)
                title = alt_match.group(1) if alt_match else ""
                
                if not title:
                    clean_text = re.sub(r'<[^>]+>', '', inner_html).strip()
                    title = clean_text if clean_text else "Untitled Video"

                # Penapis URL untuk mengelakkan pautan navigasi utama
                if href and img_url and not href.startswith(('#', 'javascript:')):
                    full_link = urllib.parse.urljoin(self.target_url, href)
                    full_img = urllib.parse.urljoin(self.target_url, img_url)

                    if full_link not in seen_urls and full_link != self.target_url:
                        seen_urls.add(full_link)
                        catalog_items.append({
                            'title': title,
                            'url': full_link,
                            'poster': full_img
                        })

        return {
            'title': page_title,
            'catalog_items': catalog_items
        }
