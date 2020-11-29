class Grid:
    def __init__(self, cols, rows, width, height, hamiltonian=False):
        self.grid = [] # (x, y, w, h)
        x = 0
        y = 0

        if not hamiltonian:
            for r in range(rows):
                y = r * height

                for c in range(cols):
                    x = c * width
                    rect = (x, y, width, height)
                    self.grid.append(rect)

        else:
            for c in range(cols):
                x = c * width
                rect = (x, 0, width, height)
                self.grid.append(rect)

            for r in range(1, rows):
                y = r * height
                rect = (x, y, width, height)
                self.grid.append(rect)

            x -= width
            rect = (x, y, width, height)
            self.grid.append(rect)

            decreasing = True
            while 1:
                while 1:
                    if decreasing:
                        y -= height
                    else:
                        y += height

                    if decreasing and y == 0:
                        y += height
                        break
                    elif not decreasing and y == (rows * height):
                        y -= height
                        break

                    rect = (x, y, width, height)
                    self.grid.append(rect)
                decreasing = not decreasing

                x -= width
                if x < 0: break
                rect = (x, y, width, height)
                self.grid.append(rect)

        self.width = cols * width
        self.height = rows * height