import scrapy
# Use CrawlerRunner for more control over reactor lifecycle in interactive environments
from scrapy.crawler import CrawlerRunner
from supabase import create_client, Client
import asyncio
import threading
from twisted.internet import reactor, defer
# Import and install the asyncio reactor explicitly
from twisted.internet.asyncioreactor import AsyncioSelectorReactor
from twisted.internet.asyncioreactor import install as install_asyncio_reactor # Import the install function directly

# Ensure the asyncio reactor is installed early
# This needs to be done once per process
try:
    # Correctly install the AsyncioSelectorReactor
    if not reactor.running: # Only install if reactor is not already running
        install_asyncio_reactor() # Call the imported install function
        # Set a new asyncio event loop if needed, to avoid conflicts with Colab's default loop
        asyncio.set_event_loop(asyncio.new_event_loop())
        print("AsyncioSelectorReactor installed successfully.")
    else:
        print("Reactor already running, skipping AsyncioSelectorReactor installation.")
except Exception as e:
    print(f"Error installing AsyncioSelectorReactor: {e}")

# 1. CONFIGURAÇÃO DO SUPABASE (Use sua URL e Chave Mestra)
SUPABASE_URL = "https://sjlcecjluuyrqwznwkcg.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InNqbGNlY2psdXV5cnF3em53a2NnIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2MzM5MDM3MCwiZXhwIjoyMDc4OTY2MzcwfQ.3boxrrak80EdAulnnOxhjBkB8uC7OPlRJsDfoaisEac"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# 2. DEFINIÇÃO DO SPIDER (O Jacaré Caçador)
class PepeSpider(scrapy.Spider):
    name = "pepe_scraper"
    # Site de teste para extrair Textos e Autores
    start_urls = ['http://quotes.toscrape.com/page/1/']

    def parse(self, response):
       if response.url.endswith('page/2/'):
            return
        # Encontra o container de todas as cotações na página
        quotes = response.css('div.quote')

        for quote in quotes:
            # 1. EXTRAÇÃO DOS DADOS DE TESTE
            text = quote.css('span.text::text').get()
            author = quote.css('small.author::text').get()

            # 2. PREPARAÇÃO DO DICIONÁRIO PARA O BANCO DE DADOS
            data_to_insert = {
                "title": text, # Usamos o texto da citação como título
                "url": response.url, # Usamos a URL da página como URL
                "price": 1000.0, # Preço fixo para teste, pois o site não tem preço
                "offer_type": "Scrapy Test",
                "location": author, # Usamos o autor como localidade
                "source_portal": "Quotes to Scrape",
                "is_active": True
            }

          



