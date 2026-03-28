import matplotlib

# 所有图表共用的标题、标签和配色都集中定义在这里，
# 这样三张图可以保持统一的文字风格和视觉风格。
TITLE_PREFIX = "校园无人机起降点选址分析："

# 完整标签适合用在空间更充足的图里，比如热力图。
DISPLAY_LABELS = {
    "service_distance": "服务区距离",
    "logistics_distance": "物流中心距离",
    "openness": "场地开阔度",
    "obstacle_risk": "障碍物风险",
    "crowd_risk": "人流风险",
    "route_access": "航线通达性",
    "operation_convenience": "运维便利性",
}

# 简短标签适合用在雷达图上，避免一圈文字太长导致拥挤。
SHORT_DISPLAY_LABELS = {
    "service_distance": "服务区",
    "logistics_distance": "物流中心",
    "openness": "开阔度",
    "obstacle_risk": "障碍风险",
    "crowd_risk": "人流风险",
    "route_access": "航线通达",
    "operation_convenience": "运维便利",
}

# 统一配色可以让三张图看起来更像同一套成果图。
COLOR_PALETTE = {
    "primary": "#2f6f89",
    "secondary": "#5fa8a8",
    "accent": "#f4a259",
    "grid": "#d9e6ec",
    "text": "#1f2d3d",
}


def configure_matplotlib():
    """配置 matplotlib，使其尽量支持中文显示。"""
    # 按顺序尝试多个常见中文字体。
    # matplotlib 会使用当前电脑上第一个可用的字体。
    matplotlib.rcParams["font.sans-serif"] = [
        "Microsoft YaHei",
        "SimHei",
        "Noto Sans CJK SC",
        "WenQuanYi Zen Hei",
        "Arial Unicode MS",
        "DejaVu Sans",
    ]

    # 同时处理负号显示问题，并设置几项默认颜色，
    # 让不同图表的坐标轴和文字风格保持一致。
    matplotlib.rcParams["axes.unicode_minus"] = False
    matplotlib.rcParams["text.color"] = COLOR_PALETTE["text"]
    matplotlib.rcParams["axes.labelcolor"] = COLOR_PALETTE["text"]
    matplotlib.rcParams["axes.edgecolor"] = COLOR_PALETTE["grid"]
