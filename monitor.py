import asyncio
import json
import os
from bs4 import BeautifulSoup
from telegram import Bot

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# ==============================
# CONFIG (Via Variáveis de Ambiente para Segurança)
# ==============================

LAST_FILE = "last_ad.txt"
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "") #insira o TOKEN do bot aqui
CHAT_ID = os.getenv("CHAT_ID", "") #insira o id do chat com o bot aqui (tudo o que tiver depois do #, em grupos incluir o '-')
KEYWORD = os.getenv("KEYWORD", "") #insira a palavra chave aqui
SEARCH_URL = os.getenv("SEARCH_URL", f"https://www.olx.com.br/brasil?q={KEYWORD}&sf=1")

# ==============================

bot = Bot(token=TELEGRAM_TOKEN)

# ==============================
# BROWSER SETUP
# ==============================

options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--window-size=1920,1080")
options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

# ==============================
# Persistência de Dados
# ==============================

def load_last_ad():
    if os.path.exists(LAST_FILE):
        try:
            with open(LAST_FILE, "r") as f:
                return f.read().strip()
        except:
            return None
    return None

def save_last_ad(url):
    with open(LAST_FILE, "w") as f:
        f.write(url)

# ==============================
# TELEGRAM FUNCTIONS
# ==============================

async def send_telegram_message(text):
    try:
        await bot.send_message(chat_id=CHAT_ID, text=text)
    except Exception as e:
        print(f"❌ Erro ao enviar mensagem para o Telegram: {e}")

# ==============================
# OLX SCRAPING FUNCTIONS
# ==============================

def get_olx_ads():
    print(f"🌐 Abrindo OLX: {SEARCH_URL}")
    driver.get(SEARCH_URL)

    try:
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "__NEXT_DATA__"))
        )
    except Exception as e:
        print(f"⚠️ Aviso: __NEXT_DATA__ não encontrado ou demora no carregamento.")

    soup = BeautifulSoup(driver.page_source, "html.parser")
    ads = []

    script_tag = soup.find("script", id="__NEXT_DATA__")
    
    if script_tag:
        try:
            data = json.loads(script_tag.string)
            ad_list = data.get("props", {}).get("pageProps", {}).get("ads", [])
            
            if not ad_list:
                ad_list = data.get("props", {}).get("pageProps", {}).get("initialData", {}).get("ads", [])

            for ad in ad_list:
                title = ad.get("subject", "Anúncio OLX")
                price = ad.get("priceValue", "A combinar")
                url = ad.get("url")
                
                if url:
                    ads.append({
                        "title": title,
                        "price": price,
                        "url": url
                    })
        except Exception as e:
            print(f"❌ Erro ao processar JSON: {e}")
    
    if not ads:
        print("🔄 Tentando busca alternativa por links...")
        links = soup.find_all("a", href=True)
        for link in links:
            href = link["href"]
            if "/d/anuncio/" in href or "/item/" in href:
                if not href.startswith("http"):
                    href = "https://www.olx.com.br" + href
                if href not in [a["url"] for a in ads]:
                    ads.append({"title": "Anúncio OLX", "price": "Ver no site", "url": href})

    return ads

# ==============================
# MAIN EXECUTION (GitHub Actions style)
# ==============================

async def run_once():
    print("🔎 Iniciando verificação...")
    last_ad_url = load_last_ad()
    current_ads = get_olx_ads()
    
    print(f"📦 {len(current_ads)} anúncios encontrados")
    
    new_ads = []
    for ad in current_ads:
        if ad["url"] == last_ad_url:
            break
        new_ads.append(ad)
    
    if new_ads:
        print(f"🆕 {len(new_ads)} novos anúncios!")
        for ad in reversed(new_ads):
            message = f"🚨 Novo anúncio!\n\n📦 {ad['title']}\n💵 {ad['price']}\n🔗 {ad['url']}"
            print(f"Enviando: {ad['title']}")
            await send_telegram_message(message)
        
        # Salva o mais recente para a próxima execução
        save_last_ad(current_ads[0]["url"])
    else:
        print("✅ Nenhum anúncio novo desde a última verificação.")

if __name__ == "__main__":
    try:
        asyncio.run(run_once())
    except Exception as e:
        print(f"❌ Erro fatal: {e}")
    finally:
        driver.quit()
