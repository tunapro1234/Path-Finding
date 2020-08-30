import pygame
import time

WIDTH = HEIGHT = 400

colors = {
    "RED": (255, 0, 0),
    "BLUE": (0, 0, 255),
    "GREEN": (0, 255, 0),
    "WHITE": (255, 255, 255),
    "BLACK": (0, 0, 0),
    "TURQ": (64, 224, 208),
    "ORANGE": (255, 69, 0),
}


class Node:
    def __init__(self, x, y, state="open"):
        self.rect = pygame.Rect(
            (Board.pixel_width * x + 1, Board.pixel_height * y + 1),
            (Board.pixel_width - 1, Board.pixel_height - 1))
        self.x = x
        self.y = y
        self.prev = None
        self.score = None
        self.color = None
        self.state = state
        self.neighbors = []

    @property
    def state(self):
        if self.color == colors["BLACK"]:
            return "open"
        elif self.color == colors["BLUE"]:
            return "closed"
        elif self.color == colors["GREEN"]:
            return "next"
        elif self.color == colors["WHITE"]:
            return "barrier"
        elif self.color == colors["TURQ"]:
            return "start"
        elif self.color == colors["RED"]:
            return "end"
        elif self.color == colors["ORANGE"]:
            return "finished"

    @state.setter
    def state(self, value):
        # open
        if value.startswith("o"):
            self.color = colors["BLACK"]
        # closed
        elif value.startswith("c"):
            self.color = colors["BLUE"]
        # next
        elif value.startswith("n"):
            self.color = colors["GREEN"]
        # barrier
        elif value.startswith("b"):
            self.color = colors["WHITE"]
        # start
        elif value.startswith("s"):
            self.color = colors["TURQ"]
        # end
        elif value.startswith("e"):
            self.color = colors["RED"]
        # finished
        elif value.startswith("f"):
            self.color = colors["ORANGE"]

    def __repr__(self):
        return f"{self.state} ({self.x}, {self.y})"


class Board:
    pixel_height = pixel_width = pixel_num = None

    def __init__(self,
                 screen,
                 width,
                 height,
                 pixel_num,
                 caption="TUNAPRO1234"):

        Board.pixel_num = pixel_num
        self.caption = caption
        self.screen = screen
        self.height = height
        self.width = width
        self.nodes = []

        self.start_node = None
        self.end_node = None

        Board.pixel_num = pixel_num = (
            pixel_num, pixel_num) if type(pixel_num) == int else pixel_num

        if type(pixel_num) == tuple:
            Board.pixel_width = width // pixel_num[0]
            Board.pixel_height = height // pixel_num[1]

        self.init_nodes()

    def update(self):
        self.reset()
        self.draw_grid()
        self.draw_nodes()

    def draw_nodes(self):
        for y in range(Board.pixel_num[1]):
            # yapf: disable
            [self.draw_node(self.nodes[y][x]) for x in range(Board.pixel_num[0])]

    def draw_grid(self):
        grid_color = colors["WHITE"]
        for x in range(Board.pixel_num[0] + 1):
            pygame.draw.line(self.screen, grid_color,
                             (x * Board.pixel_width, 0),
                             (x * Board.pixel_width, self.height))

        for y in range(Board.pixel_num[1] + 1):
            pygame.draw.line(self.screen, grid_color,
                             (0, y * Board.pixel_height),
                             (self.width, y * Board.pixel_width))

    def init_nodes(self):
        for y in range(Board.pixel_num[1]):
            self.nodes.append([])
            for x in range(Board.pixel_num[0]):
                self.nodes[-1].append(Node(x, y))

    def set_special_nodes(self):
        for y in range(len(self.nodes)):
            for x in range(len(self.nodes[y])):
                if self.nodes[y][x].state == "start":
                    self.start_node = self.nodes[y][x]
                elif self.nodes[y][x].state == "end":
                    self.end_node = self.nodes[y][x]

    def calc_node_neighbors(self):
        self.set_special_nodes()
        last_y, last_x = self.nodes[-1][-1].y, self.nodes[-1][-1].y
        for y in range(Board.pixel_num[1]):
            for x in range(Board.pixel_num[0]):
                # left
                if x != 0 and self.nodes[y][x - 1].state != "barrier":
                    self.nodes[y][x].neighbors.append(self.nodes[y][x - 1])
                # right
                if x != last_x and self.nodes[y][x + 1].state != "barrier":
                    self.nodes[y][x].neighbors.append(self.nodes[y][x + 1])
                # up
                if y != 0 and self.nodes[y - 1][x].state != "barrier":
                    self.nodes[y][x].neighbors.append(self.nodes[y - 1][x])
                # down
                if y != last_y and self.nodes[y + 1][x].state != "barrier":
                    self.nodes[y][x].neighbors.append(self.nodes[y + 1][x])

    def calc_node_score(self, node):
        return abs(self.end_node.x - node.x) + abs(self.end_node.y - node.y)

    def sort_by_score(self, nodes):
        for i in range(len(nodes)):
            nodes[i].score = self.calc_node_score(node)

        for i in range(len(nodes) - 1):
            for j in range(len(nodes) - i):
                if len(nodes) > j + 1 and nodes[j].score > nodes[j + 1].score:
                    nodes[j], nodes[j + 1] = nodes[j + 1], nodes[j]
        return nodes

    def reset(self):
        self.fill(colors["BLACK"])

    def fill(self, *args, **kwargs):
        self.screen.fill(*args, **kwargs)

    def set_pixel_state(self, state, location):
        x, y = location
        self.nodes[y][x].state = state

    def draw_pixel(self, location):
        y, x = location
        draw_node(self.nodes[y][x])

    def draw_node(self, node):
        pygame.draw.rect(self.screen, node.color, node.rect)

    def get_clicked_pos(self, mouse_location):
        x, y = mouse_location
        x, y = x // Board.pixel_width, y // Board.pixel_height
        if x > (self.pixel_num[0] - 1) or y > (self.pixel_num[1] - 1):
            return False

        return x, y

    def __repr__(self):
        return "".join([str(i) + "\n" for i in self.nodes])


def algorithm(update_func, board):
    board.calc_node_neighbors()

    # if board.end_node in (rv := calc_next_gen(board.start_node, board, update_func)):
    #     return draw_node_path(rv[0], update_func)
    # çok zaman kaybettirir
    # next_nodes = []
    # for y in range(len(board.nodes)):
    #     # yapf: disable
    #     next_nodes += [(x, y) for x in range(len(board.nodes[y])) if board.nodes[y][x].state == "next"]
    next_nodes = [board.start_node]

    while True:
        # eğer bittiyse
        if board.end_node in (rv := calc_next_gen(next_nodes[0], board, update_func)):
            return draw_node_path(rv[0], update_func)

        next_nodes += rv
        next_nodes = board.sort_by_score(next_nodes)


def calc_next_gen(node_pos, board, update_func):
    x, y = node_pos if type(node_pos) == tuple else node_pos.x, node_pos.y
    # nodeun kendisi (start değilse) kapatılıyor
    board.nodes[y][x].state = "closed" if board.nodes[y][x].state != "start" else board.nodes[y][x].state
    # nodun her bir komşusu için
    for index, neighbour in enumerate(board.nodes[y][x].neighbors):
        # yapf: disable
        if neighbour.state not in ["closed", "start", "end"]:
            # komşu sonraki eleman haline getiriliyor
            board.nodes[y][x].neighbors[index].state = "next"
            # eğer aktif komşunun geçmişi yoksa önceki node olarak bize verilen nodeu ekle
            if neighbour.prev is None:
                board.nodes[y][x].neighbors[index].prev = board.nodes[y][x]
            # eğer geçmişi varsa skorları karşılaştır

        if neighbour.state == "end":
            return [board.nodes[y][x]]

        update_func()
    return board.nodes[y][x].neighbors


def draw_node_path(last_node, update_func):
    while last_node.prev is not None:
        last_node.state = "finished"
        update_func()
        last_node = last_node.prev


def main():
    pygame.display.init()
    pygame.display.set_caption("caption")
    screen = pygame.display.set_mode((WIDTH + 1, HEIGHT + 1))
    board = Board(screen, WIDTH, HEIGHT, 40)

    start_pos = False
    end_pos = False

    is_running = True
    is_algorithm_started = False

    fps = 500

    while is_running:
        start_time = time.time()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
            if is_algorithm_started:
                continue

            if pygame.mouse.get_pressed()[0]:
                rv = board.get_clicked_pos(pygame.mouse.get_pos())
                if not rv:
                    continue
                x, y = rv

                if board.nodes[y][x].state == "open":
                    if not start_pos:
                        board.set_pixel_state("start", (x, y))
                        start_pos = True
                    elif not end_pos:
                        board.set_pixel_state("end", (x, y))
                        end_pos = True
                    else:
                        board.set_pixel_state("barrier", (x, y))

            elif pygame.mouse.get_pressed()[2]:
                rv = board.get_clicked_pos(pygame.mouse.get_pos())
                if not rv:
                    continue
                x, y = rv

                if board.nodes[y][x].state == "start":
                    start_pos = False
                elif board.nodes[y][x].state == "end":
                    end_pos = False
                board.nodes[y][x].state = "open"

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not is_algorithm_started and start_pos and end_pos:
                    is_algorithm_started = bool(1) # Düştüm
                    algorithm(lambda: update(board, start_time, fps), board)

        update(board, start_time, fps)

    # print(board)
    pygame.quit()

def update(board, start_time, fps):
    board.update()
    pygame.display.update()

    while time.time() - start_time < (1 / fps):
        pass

if __name__ == "__main__":
    main()