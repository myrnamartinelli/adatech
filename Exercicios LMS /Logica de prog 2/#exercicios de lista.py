#exercicios de lista
vetor = [1,2,3,4,5,6,7,8,9,10]
def showlist(vetor):
    print(vetor)
    return

showlist(vetor)

def vetorinverso(vetor):
    vetor.sort(reverse=True)
    print(vetor)
    return

vetorinverso(vetor)

lista_notas = [3.5, 8.9, 6, 9]

def medianotas(lista_notas):
    media_notas = sum(lista_notas)/len(lista_notas)
    print(media_notas)
    return f"As notas do aluno foram {lista_notas}.Portanto, sua media foi de {media_notas}"

teste = medianotas(lista_notas)

lista_letras = ['a','b','c','d','e','f','g','h','i','j']

def getvogais(lista_letras):
    vogais = 'a' and 'e' and 'i' and 'o' and 'u'
    vogais_lista = []
    consoante_lista = []
    for caracter in lista_letras:
        if caracter != vogais:
            consoante_lista.append(caracter)
        else:
            vogais_lista.append(caracter)

            
    return consoante_lista

print(getvogais(lista_letras))



