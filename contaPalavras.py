from collections import Counter

def contar (texto, palavras):
    texto = texto.lower().split()
    palavras = palavras.lower().replace(',', '').split()

    lista = []

    for p in palavras:
        for t in texto:
            if p == t:
                lista.append(t)
    return Counter(lista)

print(contar("batata batata batata Batata", "batata"))