from src.simulation.engine import get_next_zone
import pygame
import sys


class Config:
    WIDTH, HEIGHT = 1000, 1000
    SCALE = 80
    OFFSET_X = 100
    OFFSET_Y = 300
    RADIUS = 25


class Colors:
    BG = (30, 30, 30)
    ZONE = (100, 100, 100)
    RED = (220, 50, 50)
    GREEN = (50, 220, 50)
    WHITE = (255, 255, 255)

    @staticmethod
    def get_color(color_name):
        if color_name == "red":
            return Colors.RED
        elif color_name == "green":
            return Colors.GREEN
        elif color_name == "yellow":
            return (220, 220, 50)
        elif color_name == "blue":
            return (50, 100, 220)
        elif color_name == "purple":
            return (128, 0, 128)
        elif color_name == "black":
            return (0, 0, 0)
        elif color_name == "brown":
            return (139, 69, 19)
        elif color_name == "orange":
            return (255, 165, 0)
        elif color_name == "maroon":
            return (128, 0, 0)
        elif color_name == "gold":
            return (255, 215, 0)
        elif color_name == "darkred":
            return (139, 0, 0)
        elif color_name == "violet":
            return (238, 130, 238)
        elif color_name == "crimson":
            return (220, 20, 60)
        elif color_name == "rainbow":
            return (255, 105, 180)
        else:
            return Colors.ZONE


class PygameVisualizer:
    def __init__(self, graph):
        pygame.init()
        self.graph = graph
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        Config.WIDTH, Config.HEIGHT = self.screen.get_size()
        pygame.display.set_caption("Fly-in Simulation")
        Config.OFFSET_X, Config.OFFSET_Y = (
            Config.WIDTH // 15, Config.HEIGHT // 2
        )

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def draw_zone(self, x, y, color, name=""):
        xcer = x * Config.SCALE + Config.OFFSET_X
        ycer = y * Config.SCALE + Config.OFFSET_Y
        pos = (xcer, ycer)

        pygame.draw.circle(self.screen, color, pos, Config.RADIUS)
        pygame.draw.circle(self.screen, Colors.WHITE, pos, Config.RADIUS, 2)

        if name:
            font = pygame.font.SysFont("consolas", 12, bold=True)
            label = font.render(name, True, Colors.WHITE)
            self.screen.blit(
                label,
                (xcer - label.get_width() // 2,
                 ycer + Config.RADIUS + 5)
            )

    def draw_connection(self, x1, y1, x2, y2, color):
        start_x = x1 * Config.SCALE + Config.OFFSET_X
        start_y = y1 * Config.SCALE + Config.OFFSET_Y
        pos_s = start_x, start_y

        end_x = x2 * Config.SCALE + Config.OFFSET_X
        end_y = y2 * Config.SCALE + Config.OFFSET_Y
        pos_e = end_x, end_y

        pygame.draw.line(self.screen, color, pos_s, pos_e, 4)

    def draw_drone(self, x, y, drone_id):
        xcer = x * Config.SCALE + Config.OFFSET_X
        ycer = y * Config.SCALE + Config.OFFSET_Y
        pos = (xcer, ycer)
        pygame.draw.circle(self.screen, Colors.WHITE, pos, Config.RADIUS // 2)
        font = pygame.font.SysFont("consolas", 9, bold=True)
        label = font.render(drone_id, True, (30, 30, 30))
        self.screen.blit(
            label,
            (pos[0] - label.get_width() // 2,
             pos[1] - label.get_height() // 2)
        )

    def draw_turn(self, turn, drones):
        self.screen.fill(Colors.BG)

        for conn in self.graph.map.connections:
            z1 = self.graph.zones[conn.zone1]
            z2 = self.graph.zones[conn.zone2]
            if z2.zone_type == "restricted":
                conn_color = Colors.get_color("yellow")
            else:
                conn_color = Colors.ZONE
            self.draw_connection(z1.x, z1.y, z2.x, z2.y, conn_color)

        for zone_name, zone in self.graph.zones.items():
            zone_color = Colors.get_color(zone.color)
            self.draw_zone(zone.x, zone.y, zone_color, zone_name)

        for d in drones:
            zone = self.graph.zones[d.current_zone]
            next_z_name = get_next_zone(d)

            if d.in_transit and next_z_name:
                next_zone = self.graph.zones[next_z_name]
                self.draw_drone(
                    (zone.x + next_zone.x) / 2,
                    (zone.y + next_zone.y) / 2,
                    d.id
                )
            else:
                self.draw_drone(zone.x, zone.y, d.id)

        font = pygame.font.SysFont("consolas", 28, bold=True)
        turn_text = font.render(f"TURN  {turn:03d}", True, (255, 255, 255))
        self.screen.blit(turn_text, (20, 20))
        pygame.display.flip()
