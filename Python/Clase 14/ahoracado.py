#Ahorcado
import os
import random as r
import io

print("Bienvenido al juego del Ahorcado!")

#archivo = open("lemario-espanol.txt", "r")
#archivo = io.open("lemario-espanol.txt", mode="r",encoding="latin-1")
archivo = io.open("lemario-general-del-espanol.txt", mode="r",encoding="utf-8")

palabras = []

for palabra in archivo:
    palabras.append(palabra)
    #print(palabra)

posicion_aleatoria = r.randrange(0,len(palabras))
#print(">> " + palabras[posicion_aleatoria][:-1] + " >> " + str(posicion_aleatoria))
print(">> " + palabras[24][:-1] + ">>"+ str(len(palabras[24][:-1])))
if palabras[24][:-1][4:-1] in 'áéíóúü':
    print("si")
else:
    print("NO lo reconoce")
palabra_secreta = palabras[posicion_aleatoria][:-1]
letras_ingresadas = ""

vidas = 5
letras_ocultas = 0
letra = ""

while vidas > 0:
    letras_ocultas = 0

    # Mostrar palabra al usuario y contar letras ocultas
    for letra in palabra_secreta:
        if letra in letras_ingresadas:
            print(letra, end="")
        else:
            print("*", end="")
            letras_ocultas += 1
    
    # consultar si ganamos
    if letras_ocultas == 0:
        os.system("cls")
        print("\nEnbuenahora! Has Ganado Copito de nieve")
        break

    # INgresar letras
    tuletra = input("\nAdivine una letra: ")
    letras_ingresadas += tuletra

    # consultamos si existen en la palabra
    if tuletra not in palabra_secreta:
        vidas -= 1
        os.system("cls")
        print("\nOh No! te has equivocado, te quedan " + str(vidas) + " vidas")
    else:
        os.system("cls")
        print("\nCorrecto! sigue pequeño saltamotes")

    # en caso de terminar las vidas
    if vidas == 0:
        os.system("cls")
        print("\nHas fallado como ser Humano!!!, has perdido!")
        print("\nLa palabra secreta era: " + palabra_secreta)

print("\nNos vemos en otro juego")