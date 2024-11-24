import pygame
import matplotlib.backends.backend_agg as agg
from pygame.locals import *
import matplotlib.pyplot as plt

size_of_w = pygame.display.get_desktop_sizes()
tela_x = int(size_of_w[0][0])
tela_y = int(size_of_w[0][1])

X_POS =  10 
Y_POS =  tela_y - 300

# Color:
FACECOLOR = (230 / 255, 230 / 255, 230 / 255)
CWHITE = (0 / 255, 0 / 255, 0 / 255)
PRIMARYCOLOR = (50 / 255, 168 / 255, 82 / 255)

# Updating x list:
def XValue(lst, i, limit):
    if len(lst) < limit:
        lst.append(len(lst))
    else:
        lst.pop(0)
        lst.append(i)
    return lst

def YValue(lst, limit, get_data):
    if len(lst) < limit:
        lst.append(get_data())
    else:
        lst.pop(0)
        lst.append(get_data())
    return lst



# Graph design:
def GraphDesign(ax, fig):
    # Couleur du graphe, des axes:
    ax.set_facecolor(FACECOLOR)
    fig.patch.set_facecolor(FACECOLOR)
    ax.tick_params(axis='x', colors = CWHITE)
    ax.tick_params(axis='y', colors = CWHITE)
    plt.setp(ax.spines.values(), color = CWHITE)
    # Couleur des bordures du tableau:
    for axis in ['top', 'bottom', 'left', 'right']:
        ax.spines[axis].set_linewidth(2)

# Plot in real time:
def LivePlot(Xval, Yval, position, size, screen):
    fig = plt.figure(figsize=size)
    ax = fig.gca()

    # GraphDesign(ax,fig)
    ax.plot(Xval, Yval, 'ro-', color=PRIMARYCOLOR)
    ax.set_title("Árvores vivas", color=PRIMARYCOLOR, fontweight="bold")

    canvas = agg.FigureCanvasAgg(fig)
    canvas.draw()

    renderer = canvas.get_renderer()
    raw_data = renderer.tostring_rgb()
    size = canvas.get_width_height()
    surf = pygame.image.fromstring(raw_data, size, "RGB")

    screen.blit(surf, position)
    plt.close(fig)