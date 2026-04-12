from rich.theme import Theme
from rich.console import Console

custom_theme = Theme({
    "info": "white",
    "warning": "#FFDAB9",
    "error": "#FF69B4",
    "critical": "bold #FF69B4",
    "success": "bold white",
    "muted": "grey50",
    "prompt": "bold white",
    "panel_border": "grey50",
    "highlight": "#FF69B4",
})

console = Console(theme=custom_theme)
