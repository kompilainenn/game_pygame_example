from dataclasses import dataclass

@dataclass
class Settings():
    display_widht: int = 1440
    display_height: int = 900
    FPS: int = 80
    volume: int = 50
