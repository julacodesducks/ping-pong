import pygame, math, sys

def ballMovement(ball, left, right, vector, screen_height):
    MAX_SPEED=15 #maksymalna prędkość piłki
    if ball.top<=0 or ball.bottom>=screen_height: #Zderzenie z górną lub dolną krawędzią
        vector[1]=-vector[1] #odbijanie od góry i dołu (zmiana kierunku w osi Y)
        odbicie.play() #odtwarzanie dźwięku odbicia piłki
    
    #centerx to środek obiektu x, centery to środek obiektu y, colliderect to funkcja sprawdzająca kolizję między dwoma obiektami (zwraca True, jeśli obiekty się stykają)
    if ball.colliderect(left): # Zderzenie z lewą paletką
        odbicie.play()
        distance=ball.centery-left.centery # Odległość między środkiem piłki a środkiem paletki (kierunek lotu piłki zależy od miejsca uderzenia)
        vector[1]=distance/15 # Im większa odległość, tym większy kąt odbicia (15 to współczynnik regulujący)
        if ball.centerx > left.centerx: # Piłka uderzyła od strony boiska
            ball.left=left.right # Zapobiega "wpadnięciu" piłki w paletkę
            vector[0] = MAX_SPEED  # Lot w prawo
        else:  
            ball.right=left.left # Piłka uderzyła od tyłu (od ściany)
            vector[0] = -MAX_SPEED # Lot w lewo
        currentSpeed=math.sqrt(vector[0]**2+vector[1]**2) # normalizacja wektora (liczymy z pitagorasa aktualną prędkość piłki)
        vector[0]=vector[0]/currentSpeed * MAX_SPEED #dzielimy przez ten za długi wektor i zostaje nam 1, mnożymy to przez max prędkość
        vector[1]=vector[1]/currentSpeed * MAX_SPEED
            

    elif ball.colliderect(right): # Zderzenie z prawą paletką
        odbicie.play() 
        distance=ball.centery-right.centery 
        vector[1]=distance/15 # im większy współczynnik, tym mniejszy kąt odbicia (łagodniejszy)
        if ball.centerx < right.centerx: # Piłka uderzyła od strony boiska
            ball.right=right.left # Zapobiega "wpadnięciu" piłki w paletkę
            vector[0] = -MAX_SPEED  # Lot w lewo
        else: 
            ball.left=right.right
            vector[0] = MAX_SPEED   # Lot w prawo
        currentSpeed=math.sqrt(vector[0]**2+vector[1]**2) 
        vector[0]=vector[0]/currentSpeed * MAX_SPEED 
        vector[1]=vector[1]/currentSpeed * MAX_SPEED

    return vector


pygame.init() #inicjalizacja biblioteki
pygame.mixer.init() #inicjalizacja modułu dźwiękowego
odbicie=pygame.mixer.Sound("ballBounce.mp3")
odbicie.set_volume(0.5)
wygrana=pygame.mixer.Sound("winning.mp3") 
wygrana.set_volume(0.6)
przegrana=pygame.mixer.Sound("gameOver.mp3") 
przegrana.set_volume(0.6)


pygame.font.init() #inicjalizacja modułu czcionek
pygame.font.get_init() #sprawdzenie, czy moduł czcionek jest zainicjalizowany (zwraca True lub False)
clock=pygame.time.Clock() #utworzenie obiektu zegara do kontrolowania prędkości gry

screen=pygame.display.set_mode((800, 600), pygame.RESIZABLE) #ustawienie rozmiaru okna (bez parametrów jest domyślnie fullscreen). RESIZABLE pozwala na zmianę rozmiaru okna
screen.fill((127, 150, 255))
pygame.display.update()
pygame.display.set_caption("Ping Pong") #tytuł okna
pygame.display.set_icon(pygame.image.load("pingpong.png")) #ikona okna (może być też w formacie .ico)

left = pygame.Rect(50, 175, 25, 250)
right = pygame.Rect(725, 175, 25, 250)

# Piłkę zamykamy w niewidzialnym kwadracie 20x20 (bo promień to 10)
# Ustawiamy lewy górny róg na 390, 290, żeby jej środek wypadł idealnie na (400, 300)
ball = pygame.Rect(390, 290, 20, 20)
vector=[5, 0] #wektor ruchu piłki (przesunięcie w osi X, przesunięcie w osi Y)
#rysowanie koła (powierzchnia, kolor RGB, (pozycja X, pozycja Y), promień, grubość linii)

state=0 #stan gry (0 - menu, 1 - gra, 2 - pauza, 3 - koniec gry)
running = True

font=pygame.font.SysFont("comicsansms", 50) #ustawienie czcionki (nazwa, rozmiar)

title=font.render("PING PONG!", True, (255, 252, 242)) #renderowanie tekstu (tekst, wygładzanie, kolor)
title_rect=title.get_rect(center=(400, 50)) #ustawienie pozycji

startSolo=font.render("Play solo", True, (255, 252, 242)) #renderowanie tekstu (tekst, wygładzanie, kolor)
startSolo_rect=startSolo.get_rect(center=(400, 200)) #ustawienie pozycji tekstu (środek ekranu)

startMulti=font.render("Play multiplayer", True, (255, 252, 242))
startMulti_rect=startMulti.get_rect(center=(400, 300))

kursor=font.render(">", True, (255, 54, 51))
kursor_rect=kursor.get_rect()
chosenOption=0

quit=font.render("Quit", True, (255, 252, 242))
quit_rect=quit.get_rect(center=(400, 400))

tryAgain=font.render("Try Again", True, (255, 252, 242))
tryAgain_rect=tryAgain.get_rect(center=(400, 300))

gameOverText=font.render("Game Over!", True, (255, 252, 242))
gameOverText_rect=gameOverText.get_rect(center=(400, 100))

pause=font.render("Game Paused", True, (255, 252, 242))
pause_rect=pause.get_rect(center=(400, 300))

menuOptions=[(startSolo, startSolo_rect), (startMulti, startMulti_rect), (quit, quit_rect)] #lista opcji menu (do sprawdzania kolizji z kursorem)
gameOverOptions=[(tryAgain, tryAgain_rect), (quit, quit_rect)] #lista opcji menu po przegranej (do sprawdzania kolizji z kursorem)

pointsLeft=0
pointsRight=0
minScore=5
winner=""

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and 
        (event.key == pygame.K_ESCAPE or event.key == pygame.K_q or event.key == pygame.K_BACKSPACE or event.key == pygame.K_ESCAPE)):
            running = False

        if state==0 and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                chosenOption=(chosenOption-1)%len(menuOptions) #zmiana wybranej opcji (modulo, żeby wracać do końca listy po osiągnięciu początku)
            if event.key == pygame.K_DOWN:
                chosenOption=(chosenOption+1)%len(menuOptions)
            if event.key == pygame.K_RETURN: #Enter
                if chosenOption==0: #Play
                    state=4 #solo
                elif chosenOption==1: #Quit
                    state=1
                elif chosenOption==2:
                    running=False

        if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
            if state == 1:
                state = 3  # Przejście do stanu pauzy
            elif state == 3:
                state = 1  # Powrót do gry

        if state==2 and event.type==pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                chosenOption=(chosenOption-1)%len(gameOverOptions)
            if event.key == pygame.K_DOWN:
                chosenOption=(chosenOption+1)%len(gameOverOptions)
            if event.key == pygame.K_RETURN:
                wygrana.stop() 
                przegrana.stop()
                if chosenOption == 0: # Try Again
                    ball.center = (400, 300)
                    vector = [5, 0]
                    left.y = 175
                    right.y = 175
                    pointsLeft = 0
                    pointsRight = 0
                    
                    if winner != "": # Jeśli był zwycięzca, wracamy do Multi
                        state = 1
                        winner = "" # Czyścimy zwycięzcę na nową rundę
                    else: # Jeśli nie było zwycięzcy (napis pusta), wracamy do Solo
                        state = 4
                        
                elif chosenOption == 1: # Quit
                    winner = "" # Czyścimy zwycięzcę przy powrocie do menu
                    state = 0

    if state==0: #menu
        screen.fill((127, 150, 255)) #czyszczenie tła
        swiat_rect = screen.get_rect()
        
        title_rect.center = (swiat_rect.centerx, 50)
        screen.blit(title, title_rect)
        
        startSolo_rect.center = (swiat_rect.centerx, swiat_rect.centery - 100)
        startMulti_rect.center = (swiat_rect.centerx, swiat_rect.centery)
        quit_rect.center = (swiat_rect.centerx, swiat_rect.centery + 100)
        
        for option in menuOptions:
            screen.blit(option[0], option[1])

        chosenBox = menuOptions[chosenOption][1]
        kursor_rect.midright = (chosenBox.left - 10, chosenBox.centery)
        screen.blit(kursor, kursor_rect)

    elif state==1 or state==4: #gra
        swiat_rect = screen.get_rect()
        right.right = swiat_rect.right - 50
        keys = pygame.key.get_pressed() #sprawdzanie, które klawisze są aktualnie wciśnięte 
        if keys[pygame.K_w] and left.top>0:
            left.y-=5
        if keys[pygame.K_s] and left.bottom<swiat_rect.height:
            left.y+=5
        if keys[pygame.K_UP] and right.top>0:
            right.y-=5
        if keys[pygame.K_DOWN] and right.bottom<swiat_rect.height:
            right.y+=5

        ball.x+=vector[0] #aktualizacja X
        ball.y+=vector[1] #aktualizacja Y
        vector=ballMovement(ball, left, right, vector, swiat_rect.height) #aktualizacja wektora ruchu piłki

        #ponowne rysowanie elementów, żeby były widoczne po poruszeniu paletkami           
        screen.fill((0, 0, 0)) #czyszczenie tła

        if state==1: #rysowanie wyników tylko w trybie multiplayer
            score=font.render(f"{pointsLeft} : {pointsRight}", True, (255, 252, 242)) #renderowanie wyniku
            score_rect = score.get_rect(center=(swiat_rect.centerx, 50))
            screen.blit(score, score_rect) #rysowanie wyniku

        pygame.draw.rect(screen, (255, 0, 255), left) #rysowanie prostokąta
        pygame.draw.rect(screen, (0, 255, 0), right)
        pygame.draw.circle(screen, (255, 255, 0), ball.center, 10) #rysowanie koła

        if ball.left <= 0 or ball.right >= screen.get_width():
            if state==1:
                if ball.left <= 0:
                    pointsRight += 1
                elif ball.right >= screen.get_width():
                    pointsLeft += 1

                if pointsLeft >= minScore or pointsRight >= minScore:
                    wygrana.play()
                    state = 2 # Przejście do ekranu końcowego

                    if pointsLeft >= minScore:
                        winner = "Left Player"
                    else:
                        winner = "Right Player"

                else:
                    ball.center = swiat_rect.center 
                    vector = [5, 0]
                    left.centery = swiat_rect.centery
                    right.centery = swiat_rect.centery
            else:
                przegrana.play()
                state=2 #koniec gry w trybie solo

    elif state==2: #game over
        swiat_rect = screen.get_rect()
        screen.fill((127, 150, 255))
        if winner:
            winnerText=font.render(f"{winner} Wins!", True, (255, 252, 242))
            winnerText_rect = winnerText.get_rect(center=(swiat_rect.centerx, swiat_rect.height // 4))
            screen.blit(winnerText, winnerText_rect)
        else:
            gameOverText_rect.center = (swiat_rect.centerx, swiat_rect.height // 4)
            screen.blit(gameOverText, gameOverText_rect)

        tryAgain_rect.center = (swiat_rect.centerx, swiat_rect.centery)
        quit_rect.center = (swiat_rect.centerx, swiat_rect.centery + 100)

        for option in gameOverOptions:
            screen.blit(option[0], option[1]) #rysowanie opcji menu po przegranej
        chosenBox=gameOverOptions[chosenOption][1] 
        kursor_rect.midright=(chosenBox.left-10, chosenBox.centery) 
        screen.blit(kursor, kursor_rect) 

    elif state==3: #pauza
        swiat_rect = screen.get_rect()
        screen.fill((0, 0, 0))
        score_rect = score.get_rect(center=(swiat_rect.centerx, 50))
        pause_rect = pause.get_rect(center=swiat_rect.center)
        screen.blit(score, score_rect)
        pygame.draw.rect(screen, (255, 0, 255), left)
        pygame.draw.rect(screen, (0, 255, 0), right)
        pygame.draw.circle(screen, (255, 255, 0), ball.center, 10)
        screen.blit(pause, pause_rect)

    pygame.display.update()
    clock.tick(60) #ustawienie limitu klatek na sekundę

    
pygame.quit() #zamykanie biblioteki