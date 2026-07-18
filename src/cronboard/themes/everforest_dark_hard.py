from textual.theme import Theme

everforest_dark_hard = Theme(
    name="everforest-dark-hard",
    primary="#A7C080",
    secondary="#7FBBB3",
    accent="#D699B6",
    foreground="#D3C6AA",
    background="#272E33",
    success="#A7C080",
    warning="#DBBC7F",
    error="#E67E80",
    surface="#374145",
    panel="#414B50",
    dark=True,
    variables={
        "block-cursor-text-style": "none",
        "footer-key-foreground": "#A7C080",
        "input-selection-background": "#7FBBB3 35%",
    },
)
