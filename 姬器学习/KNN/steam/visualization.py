import math


def svg_bar_chart(path, title, labels, values, width=920, height=520, color="#3b82f6"):
    """生成简单的 SVG 横向柱状图，用来展示类别数量分布。"""
    max_value = max(values) if values else 1
    left, right, top, bottom = 210, 40, 70, 50
    plot_w = width - left - right
    row_h = (height - top - bottom) / max(1, len(labels))
    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}">',
        '<rect width="100%" height="100%" fill="#ffffff"/>',
        f'<text x="{width / 2}" y="34" text-anchor="middle" font-size="22" font-family="Arial" fill="#111827">{title}</text>',
    ]

    for i, (label, value) in enumerate(zip(labels, values)):
        y = top + i * row_h + 8
        bar_w = plot_w * value / max_value
        lines.append(f'<text x="{left - 12}" y="{y + row_h * 0.55:.1f}" text-anchor="end" font-size="13" font-family="Arial" fill="#374151">{label}</text>')
        lines.append(f'<rect x="{left}" y="{y}" width="{bar_w:.1f}" height="{max(14, row_h - 12):.1f}" rx="4" fill="{color}"/>')
        lines.append(f'<text x="{left + bar_w + 8:.1f}" y="{y + row_h * 0.55:.1f}" font-size="12" font-family="Arial" fill="#111827">{value}</text>')

    lines.append("</svg>")
    path.write_text("\n".join(lines), encoding="utf-8")


def svg_scatter(path, title, rows, width=920, height=560):
    """生成 SVG 散点图，用来观察价格和好评率之间的大致关系。"""
    left, right, top, bottom = 70, 40, 70, 70
    plot_w = width - left - right
    plot_h = height - top - bottom
    xs = [row["price"] for row in rows]
    max_x = max(xs) if xs else 1
    colors = {
        "highly_positive": "#16a34a",
        "positive": "#2563eb",
        "mixed": "#f59e0b",
        "negative": "#dc2626",
    }
    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}">',
        '<rect width="100%" height="100%" fill="#ffffff"/>',
        f'<text x="{width / 2}" y="34" text-anchor="middle" font-size="22" font-family="Arial" fill="#111827">{title}</text>',
        f'<line x1="{left}" y1="{top + plot_h}" x2="{left + plot_w}" y2="{top + plot_h}" stroke="#374151"/>',
        f'<line x1="{left}" y1="{top}" x2="{left}" y2="{top + plot_h}" stroke="#374151"/>',
        f'<text x="{left + plot_w / 2}" y="{height - 22}" text-anchor="middle" font-size="14" font-family="Arial">Price</text>',
        f'<text x="22" y="{top + plot_h / 2}" transform="rotate(-90 22 {top + plot_h / 2})" text-anchor="middle" font-size="14" font-family="Arial">Positive Rate</text>',
    ]

    for row in rows:
        x = left + (row["price"] / max_x) * plot_w
        y = top + (1 - row["positive_rate"] / 100) * plot_h
        radius = min(8, 2 + math.log1p(row["review_count"]) / 3)
        lines.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{radius:.1f}" fill="{colors[row["target"]]}" fill-opacity="0.55"/>')

    legend_x = left + plot_w - 170
    for i, (label, color) in enumerate(colors.items()):
        y = top + i * 24
        lines.append(f'<circle cx="{legend_x}" cy="{y}" r="6" fill="{color}"/>')
        lines.append(f'<text x="{legend_x + 12}" y="{y + 5}" font-size="13" font-family="Arial" fill="#111827">{label}</text>')

    lines.append("</svg>")
    path.write_text("\n".join(lines), encoding="utf-8")
