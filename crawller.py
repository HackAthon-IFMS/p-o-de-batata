import feedparser as rss
from scrap_utils import getDataByDict as scrap_data
from requests import get

"""
Importa esse arquivo e chama a funçao "pegar_texto_dos_sites_google" passando os termos numa lista com o dic com as info do nome do site e o texto do site.
Ele vai retorna um dicionario com 
[
    {
    site: nome do site,
    texto:  texto do site
    },
]
implementação
import crawller
SITES_TEXTOS_lista = crawller.pegar_texto_dos_sites_google([TERMOS])
for site_texto_dict in SITES_TEXTOS:
    Nome_site = site_texto['site']
    Texto_do_site = site_texto['texto']
"""

sites = {
    'google-rss':"https://news.google.com/rss/search?q={}&hl=pt-BR&gl=BR&ceid=BR%3Apt-419",
    'cnn':'https://www.cnnbrasil.com.br/search?q={}',
    'bbc':'https://www.bbc.co.uk/search?q={}',
    'g1':'https://www.cnnbrasil.com.br/search?q={}',
    'tech-tudo':'https://www.techtudo.com.br/busca/?q={}',
    'scielo':'https://search.scielo.org/?lang=en&count=15&from=0&output=site&sort=&format=summary&fb=&page=1&q={}',
    # 'uol':'https://busca.uol.com.br/result.html?term={}#gsc.tab=0&gsc.q={}&gsc', # não funfa
    'r7':'https://busca.r7.com/?q={}#gsc.tab=0&gsc.q={}&gsc',
    'folha':'https://search.folha.uol.com.br/?q={}&site=todos', # não funfa
    'estadao':'https://busca.estadao.com.br/?q={}'
}

def pegar_texto_dos_sites_google(termos: list):
    noticias = pesquisar_google_news(termos)
    # print(noticias)
    textos = list()

    for sla in noticias:
        link = sla['url']
        texto = get_texto_site(link)
        # if texto == "Sem data":
        # print(texto)
        # print(sla)
        print(sla["sitedanoticia"])
        textos.append({'site': sla["sitedanoticia"], 'texto': texto})
        
    return textos

def get_rss(link: str):
    rss_obj = rss.parse(link)
    
    return rss_obj

def get_texto_site(site: str):
    resposta = get(site)
    texto = scrap_data(resposta.text, tag='body', value='text')
    return texto

def termos_sla(termos: list):
    termos_query = str()
    quant_termos = len(termos)
    for (termo, num_termo)  in zip(termos, range(1, quant_termos+1)):
        if num_termo != quant_termos:
            termos_query += termo + "+"
        else:
            termos_query += termo
    
    print(termos_query)

    return termos_query

def pesquisar_google_news(termos: list) -> list:
    """
    Organização do return
    [{
        "titulo": titulo, 
        "sitedanoticia"  : nome_do_site,
        "url"   : url   
    }, ...
    ]
    """
    termos_query = termos_sla(termos)
    news = list()

    google_rss = get_rss(sites['google-rss'].format(termos_query))
    i = 0
    for key in google_rss:
        data = google_rss[key]
        # print(data)
        # print(data)
        try:
            for new in data:
                # print(news, end='\n\n')
                print(new)
                news.append({
                    'title'         : new['title'],
                    'url'           : new['link'],
                    'sitedanoticia' : new['source']['title']
                    })
                i += 1
                if i > 3:
                    return news 
        except Exception:
            pass
            # print(news, end="\n\n")

    return news

def teste() -> None:
    # google_rss = get_rss(sites['google-rss'].format('basebol'))

    # for i in google_rss:
    #     if type(google_rss[i]) is list:
    #         for news in google_rss[i]:
    #             print(news['title'])
    textos = pegar_texto_dos_sites_google(['basebol'])
    for key in textos:
        for i in key:
            print(i)
    pass

if __name__ == "__main__":
    teste()