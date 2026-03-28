import matplotlib

TITLE_PREFIX = "校园无人机起降点选址分析："

DISPLAY_LABELS = {
    "service_distance": "服务区距离",
    "logistics_distance": "物流中心距离",
    "openness": "场地开阔度",
    "obstacle_risk": "障碍物风险",
    "crowd_risk": "人流风险",
    "route_access": "航线通达性",
    "operation_convenience": "运维便利性",
}

SHORT_DISPLAY_LABELS = {
    "service_distance": "服务区",
    "logistics_distance": "物流中心",
    "openness": "开阔度",
    "obstacle_risk": "障碍风险",
    "crowd_risk": "人流风险",
    "route_access": "航线通达",
    "operation_convenience": "运维便利",
}

COLOR_PALETTE = {
    "primary": "#2f6f89",
    "secondary": "#5fa8a8",
    "accent": "#f4a259",
    "grid": "#d9e6ec",
    "text": "#1f2d3d",
}


def configure_matplotlib():
    """Configure matplotlib to display Chinese text when supported fonts are available."""
    matplotlib.rcParams["font.sans-serif"] = [
        "Microsoft YaHei",
        "SimHei",
        "Noto Sans CJK SC",
        "WenQuanYi Zen Hei",
        "Arial Unicode MS",
        "DejaVu Sans",
    ]
    matplotlib.rcParams["axes.unicode_minus"] = False
    matplotlib.rcParams["text.color"] = COLOR_PALETTE["text"]
    matplotlib.rcParams["axes.labelcolor"] = COLOR_PALETTE["text"]
    matplotlib.rcParams["axes.edgecolor"] = COLOR_PALETTE["grid"]
