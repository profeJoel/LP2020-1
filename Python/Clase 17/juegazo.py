import pygame
from pygame.locals import *

pygame.init()

ANCHO_VENTANA = 850
ALTO_VENTANA = 480
ventana = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
pygame.display.set_caption("EL JUEGAZO DE LP")
reloj = pygame.time.Clock()

# Seccion del personaje
class personaje(object):
    def __init__(self, x, y, fuente, limite):
        self.x = x
        self.y = y
        self.velocidad = 5
        # variables de movimiento
        self.ha_saltado = False
        self.va_izquierda = False
        self.va_derecha = False
        self.contador_pasos = 0
        self.impulso_salto = 10
        self.camino = [self.x, limite]
        self.salud = 10
        self.es_visible = True
        # jugabilidad
        self.zona_impacto = (self.x+15, self.y+10, 30, 50) # ajuste al cuerpo del personaje
        self.camina_izquierda = []
        self.camina_derecha = []
        self.quieto = pygame.image.load("img/"+fuente+"/standing.png")
        self.ancho = self.quieto.get_width()
        self.alto = self.quieto.get_height()
        for x in range(1,10):
            self.camina_izquierda.append(pygame.image.load("img/"+fuente+"/L"+str(x)+".png"))
            self.camina_derecha.append(pygame.image.load("img/"+fuente+"/R"+str(x)+".png"))

    def dibujar(self, cuadro): #cuadro es la ventana en donde se juega

        if self.contador_pasos + 1 > 27:
            self.contador_pasos = 0

        if self.es_visible:
            if self.va_izquierda:
                cuadro.blit(self.camina_izquierda[self.contador_pasos//3], (self.x, self.y))
                self.contador_pasos += 1

            elif self.va_derecha:
                cuadro.blit(self.camina_derecha[self.contador_pasos//3], (self.x, self.y))
                self.contador_pasos += 1

            else:
                cuadro.blit(self.quieto, (self.x,self.y))
            
            self.zona_impacto = (self.x+15, self.y+10, 30, 50)
            #crear la barra de vida
            pygame.draw.rect(cuadro, (255,0,0), (self.zona_impacto[0], self.zona_impacto[1] - 20, 50, 10))
            pygame.draw.rect(cuadro, (0,128,0), (self.zona_impacto[0], self.zona_impacto[1] - 20, 50 - (5 * (10 - self.salud)), 10)) # 45, 245, 0

            pygame.draw.rect(cuadro, (255,0,0), self.zona_impacto, 2)
        
        else:
            if self.zona_impacto[0] != -1:
                texto = pygame.font.SysFont('comicsans', 100)
                marcador = texto.render("GANASTE!", 1, (255,0,0))
                cuadro.blit(marcador, (250 - (marcador.get_width()//2), 200))
                pygame.display.update()
                pygame.time.delay(2000)
            self.zona_impacto = (-1,-1,-1,-1)

    def se_mueve_segun(self, t, iz, de, ar, ab, sa):
        if t[iz] and self.x > self.velocidad:
            self.va_izquierda = True
            self.va_derecha = False
            self.x -= self.velocidad
        
        elif t[de] and self.x < ANCHO_VENTANA - self.ancho - self.velocidad:
            self.x += self.velocidad
            self.va_derecha = True
            self.va_izquierda = False
        else:
            self.va_izquierda = False
            self.va_derecha = False
            self.contador_pasos = 0

        if self.ha_saltado: # accion de saltar
            if self.impulso_salto >= -10:
                if self.impulso_salto < 0:
                    self.y -= (self.impulso_salto**2) * 0.5 * -1
                else:
                    self.y -= (self.impulso_salto**2) * 0.5
                self.impulso_salto -= 1
            else:
                self.ha_saltado = False
                self.impulso_salto = 10
        else:
            if t[ar] and self.y > self.velocidad:
                self.y -= self.velocidad
            if t[ab] and self.y < ALTO_VENTANA - self.alto - self.velocidad:
                self.y += self.velocidad

            if t[sa]:
                self.ha_saltado = True
                self.va_derecha = False
                self.va_izquierda = False
                self.contador_pasos = 0

    def se_mueve_solo(self):
        if self.velocidad > 0:
            if self.x + self.velocidad < self.camino[1]: # dentro del rango del camino predefinido
                self.x += self.velocidad
                self.va_derecha = True
                self.va_izquierda = False
            else:
                self.velocidad *= -1
                self.contador_pasos = 0
        else:
            if self.x - self.velocidad > self.camino[0]: # dentro del rango del camino
                self.x += self.velocidad
                self.va_izquierda = True
                self.va_derecha = False
            else:
                self.velocidad *= -1
                self.contador_pasos = 0

    def se_encuentra_con(self, alguien):
        R1_ab = self.zona_impacto[1] + self.zona_impacto[3] # posicion de y+alto
        R1_ar = self.zona_impacto[1] # posicion y
        R1_iz = self.zona_impacto[0] # posicion x
        R1_de = self.zona_impacto[0] + self.zona_impacto[2] # posicion x+ancho

        R2_ab = alguien.zona_impacto[1] + alguien.zona_impacto[3] # posicion de y+alto
        R2_ar = alguien.zona_impacto[1] # posicion y
        R2_iz = alguien.zona_impacto[0] # posicion x
        R2_de = alguien.zona_impacto[0] + alguien.zona_impacto[2] # posicion x+ancho

        return R1_de > R2_iz and R1_iz < R2_de and R1_ar < R2_ab and R1_ab > R2_ar

    def es_golpeado(self):
        self.ha_saltado = False
        self.va_derecha = False
        self.va_izquierda = False
        self.impulso_salto = 10
        self.contador_pasos = 0
        self.x = 100
        self.y = 410
        self.salud -= 5
        pygame.time.delay(2000)


class proyectil(object):
    def __init__(self, x, y, radio, color, direccion):
        self.x = x
        self.y = y
        self.radio = radio
        self.color = color
        self.direccion = direccion
        self.velocidad = 8 * direccion
        self.zona_impacto = (self.x - self.radio, self.y - self.radio, self.radio * 2, self.radio * 2)

    def dibujar(self, cuadro):
        self.zona_impacto = (self.x - self.radio, self.y - self.radio, self.radio * 2, self.radio * 2)
        pygame.draw.circle(cuadro, self.color, (self.x, self.y), self.radio)
        pygame.draw.rect(cuadro, (255, 0, 0), self.zona_impacto, 2)

    def impacta_a(self, alguien):
        if alguien.salud > 0:
            alguien.salud -= 1
        else:
            alguien.es_invisible = False
            del(alguien)




def repitar_cuadro_juego():
    ventana.blit(imagen_fondo, (0,0))
    heroe.dibujar(ventana)
    villano.dibujar(ventana)
    for bala in balas:
        bala.dibujar(ventana)
    pygame.display.update()

# Dentro del Ciclo principal
repetir = True

while repetir:

    heroe = personaje(ANCHO_VENTANA//2, ALTO_VENTANA//2, "heroe", ANCHO_VENTANA)
    villano = personaje(0, ALTO_VENTANA//2, "villano", ANCHO_VENTANA)

    imagen_fondo = pygame.image.load('img/bg.jpg')

    balas = []
    direccion = 0 # 1 se mueve a la derecha -> -1 se mueve a la izquierda -> 0 no se mueve
    tanda_disparos = 0
    tiempo_entre_disparo = 0
    sonido_disparo = pygame.mixer.Sound("snd/bullet.wav")
    sonido_impacto = pygame.mixer.Sound("snd/hit.wav")


    esta_jugando = True

    while esta_jugando:
        reloj.tick(27)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()

        teclas = pygame.key.get_pressed()
        heroe.se_mueve_segun(teclas, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN, pygame.K_SPACE)
        #villano.se_mueve_segun(teclas, pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s, pygame.K_x)
        villano.se_mueve_solo()

        if villano.se_encuentra_con(heroe):
            heroe.es_golpeado()

        #Manejo de los disparos
        if tanda_disparos > 0:
            tanda_disparos += 1
        if tanda_disparos > 3:
            tanda_disparos = 0
        
        # manejo del tiempo entre disparos
        tiempo_entre_disparo += 1
        if tiempo_entre_disparo > 5:
            tiempo_entre_disparo = 0

        if teclas[pygame.K_x] and tanda_disparos == 0 and tiempo_entre_disparo == 0:
            if heroe.va_izquierda:
                direccion = -1
            elif heroe.va_derecha:
                direccion = 1
            else:
                direccion = 0
            
            if len(balas) < 5 and direccion != 0:
                balas.append(proyectil(round(heroe.x + heroe.ancho//2), round(heroe.y + heroe.alto//2), 10, (0, 0, 0), direccion))
                sonido_disparo.play()
                #print(len(balas))

        for bala in balas:
            if villano.se_encuentra_con(bala):
                bala.impacta_a(villano)
                balas.pop(balas.index(bala))
                sonido_impacto.play()

            # Movimiento del proyectil (cada proyectil)
            if bala.x < ANCHO_VENTANA and bala.x > 0:
                bala.x += bala.velocidad
            else:
                balas.pop(balas.index(bala))

        # COnsultar si se sube de nivel o se pierde
        if villano.salud <= 0:
            print("El Heroe ha ganado")

        if heroe.salud <= 0:
            esta_jugando = False
            repetir = False
            print("El Heroe ha perdido")

        repitar_cuadro_juego()
pygame.quit()