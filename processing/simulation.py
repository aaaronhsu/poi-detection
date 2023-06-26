import pygame
import math

pygame.init()

width, height = 1000, 1000
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("coordinate generator")


points = []

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # check if the space bar is pressed
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # get the mouse position
                pos = pygame.mouse.get_pos()
                points.append(pos)
                print("added", pos, "to points")
            elif event.key == pygame.K_RETURN:
                running = False

                with open("processing/test.txt", "w") as f:
                    for point in points:
                        f.write(
                            str(point[0] / 1000) + "," + str(point[1] / 1000) + "\n"
                        )
            elif event.key == pygame.K_BACKSPACE:
                if len(points) > 0:
                    points.pop()
            # if the user presses q, quit
            elif event.key == pygame.K_q:
                running = False

        screen.fill((0, 0, 0))
        for point in points:
            pygame.draw.circle(screen, (255, 255, 255), point, 5)
        pygame.display.update()


pygame.quit()
