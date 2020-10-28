def get_colors(step=5):
    colors = []
    for r in range(0, 255, step):
        for g in range(0, 255, step):
            for b in range(0, 255, step):
                colors.append((r, g, b))
    return colors
