import requests
import os
from dotenv import load_dotenv

load_dotenv()

print("STORE:", os.getenv("SHOPIFY_STORE"))
print("TOKEN:", os.getenv("SHOPIFY_TOKEN"))

SHOPIFY_STORE = os.getenv("SHOPIFY_STORE")
SHOPIFY_TOKEN = os.getenv("SHOPIFY_TOKEN")
SKETCHFAB_TOKEN = os.getenv("SKETCHFAB_TOKEN")
API_VERSION = "2026-01"

class ShopifySketchfabSync:
    def __init__(self):
        self.shopify_headers = {"X-Shopify-Access-Token": SHOPIFY_TOKEN}
        self.sketchfab_headers = {"Authorization": f"Token {SKETCHFAB_TOKEN}"}

    def get_products(self):
        url = f"https://{SHOPIFY_STORE}/admin/api/{API_VERSION}/products.json"
        response = requests.get(url, headers=self.shopify_headers)
        response.raise_for_status()
        return response.json().get("products", [])

    def find_sketchfab_model(self, product_title):
        url = "https://api.sketchfab.com/v3/models"
        params = {"q": product_title, "count": 1}
        
        try:
            res = requests.get(url, headers=self.sketchfab_headers, params=params)
            data = res.json()
            if data.get("results"):
                uid = data["results"][0]["uid"]
                return f"https://sketchfab.com/models/{uid}/embed"
        except Exception as e:
            print(f"Error for: {product_title}: {e}")
        return None

    def update_shopify_metafield(self, product_id, embed_url):
        url = f"https://{SHOPIFY_STORE}/admin/api/{API_VERSION}/products/{product_id}/metafields.json"
        payload = {
            "metafield": {
                "namespace": "custom",
                "key": "sketchfab_embed",
                "value": embed_url,
                "type": "single_line_text_field"
            }
        }
        res = requests.post(url, headers=self.shopify_headers, json=payload)
        return res.status_code

    def run(self):
        products = self.get_products()
        for product in products:
            title = product["title"]
            print(f"Processing: {title}...")

            embed_url = self.find_sketchfab_model(title)
            if embed_url:
                status = self.update_shopify_metafield(product["id"], embed_url)
                print(f"Success! Shopify status: {status}")
            else:
                print(f"No model found for: {title}")

if __name__ == "__main__":
    sync = ShopifySketchfabSync()
    sync.run()