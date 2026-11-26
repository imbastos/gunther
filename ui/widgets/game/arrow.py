import heapq

from textual.widgets import Label

from ui.widgets.game.diagram_node import DiagramNode


class Arrow:
    def __init__(self, source: DiagramNode, target: DiagramNode, diagram):
        self.source = source
        self.target = target
        self.diagram = diagram
        self.segments: list[Label] = []

    def mount(self):
        self.update_position()

    def remove(self):
        for seg in self.segments:
            if seg.is_mounted:
                seg.remove()
        self.segments.clear()

    def _make_segment(self, text: str, x: int, y: int, color: str) -> Label:
        lbl = Label(text)
        lbl.styles.position = "absolute"
        lbl.styles.layer = "arrows"
        lbl.styles.offset = (x, y)
        lbl.styles.width = 1
        lbl.styles.height = 1
        lbl.styles.padding = 0
        lbl.styles.margin = 0
        lbl.styles.color = color
        return lbl

    def _get_blocked_cells(self) -> set[tuple[int, int]]:
        base_reg = self.diagram.region
        blocked: set[tuple[int, int]] = set()

        for diagram_node in self.diagram.query(DiagramNode):
            if not diagram_node.is_mounted:
                continue
            reg = diagram_node.region
            x0 = reg.x - base_reg.x
            y0 = reg.y - base_reg.y
            for y in range(y0, y0 + reg.height):
                for x in range(x0, x0 + reg.width):
                    blocked.add((x, y))

        return blocked

    def _get_ports(
        self, diagram_node: DiagramNode, blocked: set[tuple[int, int]], width: int, height: int
    ) -> list[tuple[tuple[int, int], tuple[int, int]]]:
        """Retorna pares ((x, y), (dx, dy)) das 4 saídas adjacentes ao centro das bordas."""
        base_reg = self.diagram.region
        reg = diagram_node.region

        x0 = reg.x - base_reg.x
        y0 = reg.y - base_reg.y
        x1 = x0 + reg.width - 1
        y1 = y0 + reg.height - 1
        xm = x0 + reg.width // 2
        ym = y0 + reg.height // 2

        candidates = [
            ((x1 + 1, ym), (1, 0)),  # direita
            ((x0 - 1, ym), (-1, 0)),  # esquerda
            ((xm, y1 + 1), (0, 1)),  # baixo
            ((xm, y0 - 1), (0, -1)),  # cima
        ]

        valid = []
        for (px, py), direction in candidates:
            if 0 <= px < width and 0 <= py < height and (px, py) not in blocked:
                valid.append(((px, py), direction))
        return valid

    def _find_path(
        self,
        starts: list[tuple[tuple[int, int], tuple[int, int]]],
        goals: list[tuple[tuple[int, int], tuple[int, int]]],
        blocked: set[tuple[int, int]],
        width: int,
        height: int,
    ) -> list[tuple[int, int]]:
        if not starts or not goals:
            return []

        goal_map = {pos: direction for pos, direction in goals}
        goal_positions = list(goal_map.keys())

        def heuristic(pos: tuple[int, int]) -> int:
            return min(abs(pos[0] - gx) + abs(pos[1] - gy) for gx, gy in goal_positions)

        # Fila: (f_score, g_score, pos, dir)
        heap: list[tuple[int, int, tuple[int, int], tuple[int, int]]] = []
        best_cost: dict[tuple[tuple[int, int], tuple[int, int]], int] = {}
        came_from: dict[
            tuple[tuple[int, int], tuple[int, int]],
            tuple[tuple[int, int], tuple[int, int]] | None,
        ] = {}

        for pos, direction in starts:
            state = (pos, direction)
            best_cost[state] = 0
            came_from[state] = None
            heapq.heappush(heap, (heuristic(pos), 0, pos, direction))

        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        turn_penalty = 2

        while heap:
            _, g, pos, cur_dir = heapq.heappop(heap)
            state = (pos, cur_dir)

            if g > best_cost.get(state, 10**9):
                continue

            if pos in goal_map:
                path: list[tuple[int, int]] = []
                curr: tuple[tuple[int, int], tuple[int, int]] | None = state
                while curr is not None:
                    path.append(curr[0])
                    curr = came_from[curr]
                path.reverse()
                return path

            for ndx, ndy in directions:
                nx, ny = pos[0] + ndx, pos[1] + ndy
                if not (0 <= nx < width and 0 <= ny < height):
                    continue
                if (nx, ny) in blocked:
                    continue

                step_cost = 1 if (ndx, ndy) == cur_dir else 1 + turn_penalty
                new_g = g + step_cost
                next_state = ((nx, ny), (ndx, ndy))

                if new_g < best_cost.get(next_state, 10**9):
                    best_cost[next_state] = new_g
                    came_from[next_state] = state
                    heapq.heappush(
                        heap, (new_g + heuristic((nx, ny)), new_g, (nx, ny), (ndx, ndy))
                    )

        return []

    def _char_for_step(
        self,
        prev_pos: tuple[int, int] | None,
        curr_pos: tuple[int, int],
        next_pos: tuple[int, int] | None,
        target_port_dir: tuple[int, int] | None,
    ) -> str:
        # Ponta final apontando para dentro do DiagramNode de destino
        if next_pos is None:
            # target_port_dir aponta para FORA do target; a ponta aponta no sentido oposto
            if target_port_dir == (1, 0):
                return "◄"
            if target_port_dir == (-1, 0):
                return "►"
            if target_port_dir == (0, 1):
                return "▲"
            if target_port_dir == (0, -1):
                return "▼"
            return "●"

        if prev_pos is None:
            dx = next_pos[0] - curr_pos[0]
            return "─" if dx != 0 else "│"

        d1 = (curr_pos[0] - prev_pos[0], curr_pos[1] - prev_pos[1])
        d2 = (next_pos[0] - curr_pos[0], next_pos[1] - curr_pos[1])

        if d1 == d2:
            return "─" if d1[0] != 0 else "│"

        corners = {
            ((1, 0), (0, 1)): "┐",
            ((0, -1), (-1, 0)): "┐",
            ((1, 0), (0, -1)): "┘",
            ((0, 1), (-1, 0)): "┘",
            ((-1, 0), (0, 1)): "┌",
            ((0, -1), (1, 0)): "┌",
            ((-1, 0), (0, -1)): "└",
            ((0, 1), (1, 0)): "└",
        }
        return corners.get((d1, d2), "┼")

    def update_position(self):
        if not self.source.is_mounted or not self.target.is_mounted:
            return

        self.remove()

        width = self.diagram.region.width
        height = self.diagram.region.height
        if width <= 0 or height <= 0:
            return

        blocked = self._get_blocked_cells()
        starts = self._get_ports(self.source, blocked, width, height)
        goals = self._get_ports(self.target, blocked, width, height)

        path = self._find_path(starts, goals, blocked, width, height)
        if not path:
            return

        goal_dir_map = {pos: direction for pos, direction in goals}
        target_port_dir = goal_dir_map.get(path[-1])
        color = self.source.color

        for i, pos in enumerate(path):
            prev_pos = path[i - 1] if i > 0 else None
            next_pos = path[i + 1] if i + 1 < len(path) else None
            char = self._char_for_step(prev_pos, pos, next_pos, target_port_dir)
            self.segments.append(self._make_segment(char, pos[0], pos[1], color))

        if self.segments:
            self.diagram.mount(*self.segments)
