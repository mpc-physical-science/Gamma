import math
import random
import sys
import matplotlib.pyplot as plt
import pygame

# ==========================================
# CONSTANTS & SETUP
# ==========================================
WIDTH, HEIGHT = 800, 600
SUN_RADIUS = 4 * WIDTH // 11
SUN_RADIUS_SQRD = SUN_RADIUS**2

# Turbo Pascal EGA/VGA Palette Colors
COLORS = [
    (0, 0, 0),  # 0: Black
    (0, 0, 170),  # 1: Blue
    (0, 170, 0),  # 2: Green
    (0, 170, 170),  # 3: Cyan
    (170, 0, 0),  # 4: Red
    (170, 0, 170),  # 5: Magenta
    (170, 85, 0),  # 6: Brown
    (170, 170, 170),  # 7: Light Gray
    (85, 85, 85),  # 8: Dark Gray
    (85, 85, 255),  # 9: Light Blue
    (85, 255, 85),  # 10: Light Green
    (85, 255, 255),  # 11: Light Cyan
    (255, 85, 85),  # 12: Light Red
    (255, 85, 255),  # 13: Light Magenta
    (255, 255, 85),  # 14: Yellow
    (255, 255, 255),  # 15: White
]


def get_photon_color(index):
    """Maps photon index (1-based) to BGI palette cycling logic from Pascal source."""
    # Pascal logic:
    # 1..13 -> i+1, 14..26 -> i-12, 27..39 -> i-25, etc.
    mapped_idx = ((index - 1) % 13) + 1
    return COLORS[mapped_idx % len(COLORS)]


# ==========================================
# SIMULATION DATA STRUCTURES
# ==========================================
class GammaSimulation:

    def __init__(
        self,
        mode,
        num_groups=1,
        num_rays=100,
        mfp=10.0,
        delays=0,
        num_before_next=0,
        raytrace=True,
    ):
        self.mode = mode
        self.num_groups = num_groups
        self.num_rays = num_rays
        self.mfp = mfp
        self.delays = delays
        self.num_before_next = num_before_next
        self.raytrace = raytrace

        # Tracking state
        self.x = {}
        self.y = {}
        self.inside = {}
        self.sumx = {}
        self.sumy = {}
        self.sumr = {}
        self.sumtimes = {}
        self.num_left_per_20 = [0] * 101

        self.num_out = 0
        self.maxr = 0.0
        self.minr = 2.0 * SUN_RADIUS

        self.init_variables()

    def init_variables(self):
        self.num_out = 0
        self.maxr = 0.0
        self.minr = 2.0 * SUN_RADIUS

        for g in range(1, self.num_groups + 1):
            for i in range(1, self.num_rays + 1):
                key = (g, i)
                self.x[key] = 0
                self.y[key] = 0
                self.inside[key] = True
                self.sumx[key] = 0.0
                self.sumy[key] = 0.0
                self.sumr[key] = 0.0
                self.sumtimes[key] = 0

    def get_angle(self):
        return random.random() * 2 * math.pi

    def get_r(self):
        # Pascal math formula: (mfp * random * 2) / (100 + 17 + (mfp/5)*(-4)) * sunradius
        denom = 100 + 17 + (self.mfp / 5.0) * (-4)
        return (self.mfp * random.random() * 2) / denom * SUN_RADIUS

    def update_stats(self, g, i, xnew, ynew, step_r):
        key = (g, i)
        self.sumx[key] += xnew
        self.sumy[key] += ynew
        self.sumr[key] += step_r
        self.sumtimes[key] += 1

        if step_r > self.maxr:
            self.maxr = step_r
        if step_r < self.minr:
            self.minr = step_r


# ==============================================
# Modern Dark Slate Palette
THEME = {
    "bg_dark": (15, 23, 42),  # Slate 900
    "bg_card": (30, 41, 59),  # Slate 800
    "text_main": (241, 245, 249),  # Slate 100
    "text_muted": (148, 163, 184),  # Slate 400
    "accent": (56, 189, 248),  # Light Blue/Cyan
    "hotkey": (250, 204, 21),  # Warm Yellow
    "sun_border": (71, 85, 105),  # Slate 600
}


def render_menu_item(
    surface, font, label, hotkey_char, x, y, base_color, hotkey_color
):
    """Renders menu text and highlights the hotkey character inline.

    Prioritizes exact case matches (e.g. capital 'B' in 'Batches') over
    case-insensitive matches (e.g. 'b' in 'Number').
    """
    # 1. Try exact case match first
    idx = label.find(hotkey_char)

    # 2. Fall back to case-insensitive match if exact case isn't found
    if idx == -1:
        idx = label.upper().find(hotkey_char.upper())

    # 3. If hotkey still isn't found at all, render plain label
    if idx == -1:
        surf = font.render(label, True, base_color)
        surface.blit(surf, (x, y))
        return

    part1, part2, part3 = label[:idx], label[idx], label[idx + 1 :]
    curr_x = x

    part1, part2, part3 = label[:idx], label[idx], label[idx + 1 :]
    curr_x = x

    if part1:
        s1 = font.render(part1, True, base_color)
        surface.blit(s1, (curr_x, y))
        curr_x += s1.get_width()

    s2 = font.render(part2, True, hotkey_color)
    surface.blit(s2, (curr_x, y))
    curr_x += s2.get_width()

    if part3:
        s3 = font.render(part3, True, base_color)
        surface.blit(s3, (curr_x, y))


# ==========================================
# GUI & ENGINE CLASS
# ==========================================
class GammaApp:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Gamma Ray 2-D Monte Carlo Simulation")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Courier", 18, bold=True)
        # Try loading common Gothic / Old English system fonts matching Turbo Pascal's Gothic style
        # Pygame will try them in order and fall back to a default serif if unavailable
        self.title_font = pygame.font.SysFont(
            [
                "oldenglishtextmt",
                "unifrakturmaguntia",
                "cloisterblack",
                "diploma",
                "gothic",
                "georgia",
            ],
            36,
            bold=True,
        )

    def draw_menu(self, screen_id, config):
        self.screen.fill(THEME["bg_dark"])

        # Configure Menu Titles & Items (without brackets)
        if screen_id == 1:
            title_text = "Gamma Ray Monte Carlo"
            items = [
                ("Introduction", "I"),
                ("Single Photon", "S"),
                ("Multiple Photons", "M"),
                ("Batches of Photons", "B"),
                ("Dying Sun Simulation", "D"),
                ("", ""),
                ("Quit", "Q"),
            ]
        else:
            titles = {
                2: "Introduction",
                3: "Single Photon",
                4: "Multiple Photons",
                5: "Batches of Photons",
                6: "Dying Sun",
            }
            title_text = titles[screen_id]

            items = []
            if screen_id in [2, 4, 5, 6]:
                items.append((f"Number of Photons: {config['num_rays']}", "P"))
            if screen_id in [5, 6]:
                items.append(
                    (f"Number of Batches: {config['num_groups']}", "B")
                )
                items.append(
                    (
                        f"Collisions between Batches: {config['numbeforenext']}",
                        "C",
                    )
                )
            items.extend(
                [
                    (f"Delay between Collisions: {config['delays']} ms", "D"),
                    (f"Mean Free Path: L={config['mfp']:.2f}", "L"),
                    (f"Ray Tracing: {'ON' if config['raytrace'] else 'OFF'}", "R",),
                    ("", ""),
                    ("Start Simulation", "S"),
                    ("", ""),
                    ("Main Menu", "M"),
                    ("Quit", "Q"),
                ]
            )

        # Render Header Title
        title = self.title_font.render(title_text, True, THEME["accent"])
        self.screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 35))

        # Draw Container Card
        card_rect = pygame.Rect(
            WIDTH // 8, 90, (WIDTH * 3) // 4, HEIGHT - 120
        )
        pygame.draw.rect(
            self.screen, THEME["bg_card"], card_rect, border_radius=10
        )

        # Render Menu Options with Hotkey Highlighting
        y = 115
        for text, hotkey in items:
            if text:
                render_menu_item(
                    surface=self.screen,
                    font=self.font,
                    label=text,
                    hotkey_char=hotkey,
                    x=WIDTH // 8 + 30,
                    y=y,
                    base_color=THEME["text_main"],
                    hotkey_color=THEME["hotkey"],
                )
            y += 28

        pygame.display.flip()

    def get_input_dialog(self, prompt, current_val=None):
        """Input dialog styled with the Modern Dark theme, displaying the current setting below the input line."""
        input_text = ""
        active = True
        while active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        active = False
                    elif event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                    else:
                        input_text += event.unicode

            # Clear background
            self.screen.fill(THEME["bg_dark"])

            # Card Dimensions & Setup
            card_w, card_h = 620, 150 if current_val is not None else 120
            card_x = (WIDTH - card_w) // 2
            card_y = (HEIGHT - card_h) // 2
            card_rect = pygame.Rect(card_x, card_y, card_w, card_h)

            pygame.draw.rect(
                self.screen, THEME["bg_card"], card_rect, border_radius=10
            )
            pygame.draw.rect(
                self.screen,
                THEME["accent"],
                card_rect,
                width=1,
                border_radius=10,
            )

            curr_y = card_y + 30

            # 1. Prompt & Active Input Line (Top)
            prompt_surf = self.font.render(f"{prompt}:", True, THEME["accent"])
            val_surf = self.font.render(
                f" {input_text}_", True, THEME["hotkey"]
            )

            self.screen.blit(prompt_surf, (card_x + 30, curr_y))
            self.screen.blit(
                val_surf, (card_x + 30 + prompt_surf.get_width(), curr_y)
            )

            # 2. Render "Current Setting" line below the input line
            if current_val is not None:
                curr_y += 40
                curr_lbl = self.font.render(
                    f"Current Setting: {current_val}",
                    True,
                    THEME["text_muted"],
                )
                self.screen.blit(curr_lbl, (card_x + 30, curr_y))

            pygame.display.flip()
            self.clock.tick(30)

        return input_text

    def get_photon_color(index):
        """Maps photon index (1-based) to BGI palette cycling logic from Pascal source."""
        # Pascal logic:
        # 1..13 -> i+1, 14..26 -> i-12, 27..39 -> i-25, etc.
        mapped_idx = ((index - 1) % 13) + 1
        return COLORS[mapped_idx % len(COLORS)]

    def run_simulation(self, sim):
        cx, cy = WIDTH // 2, HEIGHT // 2

        bg_color = THEME["bg_dark"]  # Sleek dark navy instead of pure black/white
        self.screen.fill(bg_color)

        # Draw sun boundary with subtle slate blue border
        pygame.draw.circle(
            self.screen, THEME["sun_border"], (cx, cy), SUN_RADIUS, 1
        )
        pygame.display.flip()

        possible_groups = 1 if sim.num_groups > 1 else sim.num_groups
        counter = 1
        num_previous = 0

        running = True
        paused = False

        # Pick a single random color ONCE for the entire run if single photon mode
        single_photon_color = (
            get_photon_color(random.randint(1, 100))
            if sim.num_rays == 1
            else None
        )

        while running and sim.num_out < (sim.num_groups * sim.num_rays):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "QUIT"
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE or event.key == pygame.K_p:
                        paused = True

            if paused:
                pause_lbl = self.font.render(
                    "PAUSED - Press 'R' to Resume, 'M' for Main Menu",
                    True,
                    (255, 0, 0),
                )
                self.screen.blit(pause_lbl, (10, 10))
                pygame.display.flip()

                while paused:
                    for ev in pygame.event.get():
                        if ev.type == pygame.KEYDOWN:
                            if ev.key == pygame.K_r:
                                paused = False
                            elif ev.key == pygame.K_m:
                                return "MENU"
                    self.clock.tick(10)

            iterations = sim.num_before_next if sim.num_before_next > 0 else 1
            for _ in range(iterations):
                for g in range(1, possible_groups + 1):
                    for i in range(1, sim.num_rays + 1):
                        key = (g, i)
                        if not sim.inside[key]:
                            continue

                        # Select color based on mode
                        if sim.num_groups == 1:
                            if sim.num_rays == 1:
                                # Use the single random color generated before the loop
                                color = single_photon_color
                            else:
                                # Multiple photons: color per photon index
                                color = get_photon_color(i)
                        else:
                            # Batch groups: color per group index
                            color = get_photon_color(g)

                        theta = sim.get_angle()
                        step_r = sim.get_r()

                        x_old, y_old = sim.x[key], sim.y[key]
                        x_new = x_old + int(round(step_r * math.cos(theta)))
                        y_new = y_old + int(round(step_r * math.sin(theta)))

                        sim.update_stats(g, i, x_new, y_new, step_r)

                        if (x_new**2 + y_new**2) >= SUN_RADIUS_SQRD:
                            sim.inside[key] = False

                            b_val = x_old * math.cos(theta) + y_old * math.sin(
                                theta
                            )
                            disc = (
                                SUN_RADIUS_SQRD
                                - (x_old**2 + y_old**2)
                                + (b_val**2)
                            )
                            root = math.sqrt(disc) if disc >= 0 else 0

                            bound_r = root - b_val
                            if bound_r < 0:
                                bound_r = -root - b_val

                            x_bound = x_old + int(
                                round(bound_r * math.cos(theta))
                            )
                            y_bound = y_old + int(
                                round(bound_r * math.sin(theta))
                            )

                            if sim.raytrace:
                                pygame.draw.line(
                                    self.screen,
                                    color,
                                    (cx + x_old, cy + y_old),
                                    (cx + x_bound, cy + y_bound),
                                )
                                pygame.draw.line(
                                    self.screen,
                                    color,
                                    (cx + x_bound, cy + y_bound),
                                    (cx + 2 * x_bound, cy + 2 * y_bound),
                                )
                            else:
                                pygame.draw.line(
                                    self.screen,
                                    color,
                                    (cx + x_bound, cy + y_bound),
                                    (cx + 2 * x_bound, cy + 2 * y_bound),
                                )

                            sim.num_out += 1
                        else:
                            if sim.raytrace:
                                pygame.draw.line(
                                    self.screen,
                                    color,
                                    (cx + x_old, cy + y_old),
                                    (cx + x_new, cy + y_new),
                                )
                            else:
                                for dx, dy in [
                                    (0, 0),
                                    (-1, 1),
                                    (1, -1),
                                    (1, 1),
                                    (-1, -1),
                                ]:
                                    self.screen.set_at(
                                        (cx + x_new + dx, cy + y_new + dy),
                                        color,
                                    )

                            sim.x[key] = x_new
                            sim.y[key] = y_new

            if sim.num_groups > 1:
                if counter < 101:
                    sim.num_left_per_20[counter] = sim.num_out - num_previous
                    num_previous = sim.num_out
                    counter += 1
                if possible_groups < sim.num_groups:
                    possible_groups += 1

            pygame.display.flip()
            if sim.delays > 0:
                pygame.time.delay(sim.delays)

        # Draw Top-Left Overlay Panel before showing statistics
        overlay_text = "Press any key to continue..."
        txt_surf = self.font.render(overlay_text, True, THEME["hotkey"])

        panel_rect = pygame.Rect(
            15, 15, txt_surf.get_width() + 20, txt_surf.get_height() + 14
        )
        pygame.draw.rect(
            self.screen, THEME["bg_card"], panel_rect, border_radius=6
        )
        pygame.draw.rect(
            self.screen, THEME["accent"], panel_rect, width=1, border_radius=6
        )
        self.screen.blit(txt_surf, (25, 22))
        pygame.display.flip()

        # Wait for keypress
        waiting_for_key = True
        while waiting_for_key:
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    return "QUIT"
                elif ev.type == pygame.KEYDOWN:
                    waiting_for_key = False
            self.clock.tick(30)

        return "FINISHED"

    def show_statistics(self, sim):
        tot_x, tot_y, tot_dist, tot_times = 0.0, 0.0, 0.0, 0
        tot_gammas = 0
        ave_dist_per_coll = 0.0

        max_dist_traveled = list(sim.sumr.values())[0] if sim.sumr else 0
        min_dist_traveled = max_dist_traveled
        max_collisions = list(sim.sumtimes.values())[0] if sim.sumtimes else 0
        min_collisions = max_collisions

        for g in range(1, sim.num_groups + 1):
            for i in range(1, sim.num_rays + 1):
                key = (g, i)
                r_val = sim.sumr[key]
                t_val = sim.sumtimes[key]

                if r_val > max_dist_traveled:
                    max_dist_traveled = r_val
                if r_val < min_dist_traveled:
                    min_dist_traveled = r_val
                if t_val > max_collisions:
                    max_collisions = t_val
                if t_val < min_collisions:
                    min_collisions = t_val

                tot_x += sim.sumx[key]
                tot_y += sim.sumy[key]
                tot_dist += r_val
                tot_times += t_val

                if t_val != 0:
                    ave_dist_per_coll += r_val / t_val
                    tot_gammas += 1

        tot_gammas = sim.num_groups * sim.num_rays
        ave_dist_per_coll = (
            ave_dist_per_coll / tot_gammas if tot_gammas else 0
        )
        avg_collisions = tot_times / tot_gammas if tot_gammas else 0
        avg_dist_traveled = tot_dist / tot_gammas if tot_gammas else 0

        # Render Stats Screen
        self.screen.fill(THEME["bg_dark"])

        # Title Header (Centered at top)
        title_surf = self.title_font.render(
            "Photon Statistics", True, THEME["accent"]
        )
        self.screen.blit(
            title_surf, (WIDTH // 2 - title_surf.get_width() // 2, 25)
        )

        lines = [
            f"Total Distance Traveled (as % of Sun's Radius):",
            f"\t\t\tMaximum: {max_dist_traveled / SUN_RADIUS * 100:.3f}%",
            f"\t\t\tMinimum: {min_dist_traveled / SUN_RADIUS * 100:.3f}%",
            f"\t\t\tAverage: {avg_dist_traveled / SUN_RADIUS * 100:.3f}%",
            "",
            f"Distance Traveled Between Collisions (as % of Sun's Radius):",
            f"\t\t\tMaximum: {sim.maxr / SUN_RADIUS * 100:.5f}%",
            f"\t\t\tMinimum: {sim.minr / SUN_RADIUS * 100:.5f}%",
            f"\t\t\tAverage: {ave_dist_per_coll / SUN_RADIUS * 100:.5f}%",
            "",
            f"Number of Collisions:",
            f"\t\t\tMaximum: {max_collisions}",
            f"\t\t\tMinimum: {min_collisions}",
            f"\t\t\tAverage: {avg_collisions:.2f}",
        ]

        # Draw Statistics Lines starting well below the title header
        y = 90
        for line in lines:
            if line:
                txt = self.font.render(line, True, THEME["text_main"])
                self.screen.blit(txt, (40, y))
            y += 25

        # Render Bottom-Right Overlay Box
        overlay_text = "Press any key to continue..."
        overlay_surf = self.font.render(overlay_text, True, THEME["hotkey"])

        margin = 15
        panel_w = overlay_surf.get_width() + 20
        panel_h = overlay_surf.get_height() + 14
        panel_x = WIDTH - panel_w - margin
        panel_y = HEIGHT - panel_h - margin

        panel_rect = pygame.Rect(panel_x, panel_y, panel_w, panel_h)
        pygame.draw.rect(
            self.screen, THEME["bg_card"], panel_rect, border_radius=6
        )
        pygame.draw.rect(
            self.screen, THEME["accent"], panel_rect, width=1, border_radius=6
        )
        self.screen.blit(overlay_surf, (panel_x + 10, panel_y + 7))

        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type in (pygame.QUIT, pygame.KEYDOWN):
                    waiting = False

    def plot_graph_results(self, sim):
        """Plotting function using Matplotlib for mode 6 ('Dying Sun')."""
        # Build full x-axis array matching the exact length of num_left_per_20
        x_collisions = [
            i * sim.num_before_next for i in range(len(sim.num_left_per_20))
        ]

        plt.figure(figsize=(8, 5))
        plt.plot(x_collisions, sim.num_left_per_20, color="blue", linewidth=2)
        plt.title("Number that Escape per Collision")
        plt.xlabel("Number of Group Collision Intervals")
        plt.ylabel("Number that Escape")
        plt.grid(True, linestyle=":")

        # Y-axis ticks step by 25
        max_y = max(sim.num_left_per_20) if sim.num_left_per_20 else 100
        plt.yticks(range(0, max_y + 25, 25))
        plt.ylim(bottom=0)

        # Find the index of the last non-zero data point
        last_nonzero_idx = 0
        for idx, val in enumerate(sim.num_left_per_20):
            if val > 0:
                last_nonzero_idx = idx

        # Target index: 5 steps higher than the last non-zero entry
        cutoff_idx = min(last_nonzero_idx + 5, len(sim.num_left_per_20) - 1)
        max_x = x_collisions[cutoff_idx] if x_collisions else 100

        # Scale X-axis bounds dynamically without altering array dimensions
        plt.xlim(left=0, right=max_x)

        plt.show()


# ==========================================
# MAIN ROUTINE
# ==========================================
def main():
    app = GammaApp()

    # Defaults
    config = {
        "mfp": 1.0,
        "num_rays": 100,
        "num_groups": 1,
        "numbeforenext": 0,
        "raytrace": True,
        "delays": 0,
    }

    screen_id = 1

    while True:
        app.draw_menu(screen_id, config)

        # Menu Input Handling
        choice = None
        while choice is None:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    key_name = pygame.key.name(event.key).upper()
                    choice = key_name

        if screen_id == 1:
            if choice == "I":
                screen_id = 2  # Introduction
            elif choice == "S":
                screen_id = 3  # Single Photon
            elif choice == "M":
                screen_id = 4  # Multiple Photons
            elif choice == "B":
                screen_id = 5  # Batches of Photons
            elif choice == "D":
                screen_id = 6  # Dying Sun
            elif choice == "Q":
                break  # Quit

            # Apply Pascal menu defaults
            # Pascal defaults commented out
            # and updated to Python defaults
            if screen_id == 2:  # Introduction
                config.update(
                    {
                        "mfp": 1.0,
                        "num_rays": 100,
                        "num_groups": 1,
                        "numbeforenext": 0,
                        "delays": 0,
                    }
                )
            elif screen_id == 3:  # Single Photon
                # config.update({'mfp': 10.0, 'num_rays': 1, 'num_groups': 1, 'numbeforenext': 0, 'delays': 500})
                config.update(
                    {
                        "mfp": 10.0,
                        "num_rays": 1,
                        "num_groups": 1,
                        "numbeforenext": 0,
                        "delays": 200,
                    }
                )
            elif screen_id == 4:  # Multiple Photons
                # config.update({'mfp': 10.0, 'num_rays': 2000, 'num_groups': 1, 'numbeforenext': 0, 'delays': 0})
                config.update(
                    {
                        "mfp": 10.0,
                        "num_rays": 2000,
                        "num_groups": 1,
                        "numbeforenext": 0,
                        "delays": 10,
                    }
                )
            elif screen_id == 5:  # Batches of Photons
                # config.update({'mfp': 10.0, 'num_rays': 100, 'num_groups': 20, 'numbeforenext': 10, 'delays': 0})
                config.update(
                    {
                        "mfp": 10.0,
                        "num_rays": 100,
                        "num_groups": 20,
                        "numbeforenext": 10,
                        "delays": 100,
                    }
                )
            elif screen_id == 6:  # Dying Sun
                # config.update({'mfp': 10.0, 'num_rays': 100, 'num_groups': 20, 'numbeforenext': 20, 'delays': 0})
                config.update(
                    {
                        "mfp": 10.0,
                        "num_rays": 100,
                        "num_groups": 20,
                        "numbeforenext": 20,
                        "delays": 10,
                    }
                )

        else:
            if choice == "Q":
                break
            elif choice == "M":
                screen_id = 1
            elif choice == "P" and screen_id in [2, 4, 5, 6]:
                val = app.get_input_dialog(
                    "How many Photons (no more than 2000)",
                    current_val=config["num_rays"],
                )
                if val.isdigit():
                    config["num_rays"] = min(int(val), 2000)

            elif choice == "B" and screen_id in [5, 6]:
                val = app.get_input_dialog(
                    "How many Batches (no more than 20)",
                    current_val=config["num_groups"],
                )
                if val.isdigit():
                    config["num_groups"] = min(int(val), 20)

            elif choice == "C" and screen_id in [5, 6]:
                val = app.get_input_dialog(
                    "Collisions between batches (no more than 5000)",
                    current_val=config["numbeforenext"],
                )
                if val.isdigit():
                    config["numbeforenext"] = min(int(val), 5000)

            elif choice == "D":
                val = app.get_input_dialog(
                    "Delay in ms (no more than 3000)",
                    current_val=config["delays"],
                )
                if val.isdigit():
                    config["delays"] = min(int(val), 3000)

            elif choice == "L":
                val = app.get_input_dialog(
                    "Mean Free Path",
                    current_val=f"{config['mfp']:.2f}",
                )
                try:
                    config["mfp"] = float(val)
                except ValueError:
                    pass
            elif choice == "R":
                config["raytrace"] = not config["raytrace"]
            elif choice == "S":
                # Run Simulation
                sim = GammaSimulation(
                    mode=screen_id,
                    num_groups=config["num_groups"],
                    num_rays=config["num_rays"],
                    mfp=config["mfp"],
                    delays=config["delays"],
                    num_before_next=config["numbeforenext"],
                    raytrace=config["raytrace"],
                )

                res = app.run_simulation(sim)
                if res == "FINISHED":
                    if screen_id == 6:
                        app.plot_graph_results(sim)
                    app.show_statistics(sim)

    pygame.quit()


if __name__ == "__main__":
    main()