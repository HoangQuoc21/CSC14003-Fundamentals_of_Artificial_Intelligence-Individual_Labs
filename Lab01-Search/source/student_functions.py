from collections import deque # BFS
import heapq # UCS, Astar
import math # Astar

# Cài đặt thuật toán BFS sử dụng hàng đợi:
def BFS(matrix, start_node, end_node):
    visited = {start_node: None}
    path = []
    # Khởi tạo hàng đợi
    queue = deque([start_node])
    # Duyệt qua các node trong hàng đợi
    while queue:
        current_node = queue.popleft()
        # Nếu node hiện tại là node kết thúc, ta dừng thuật toán
        if current_node == end_node:
            # Tạo đường đi từ node kết thúc đến node bắt đầu
            while current_node is not None:
                path.append(current_node)
                current_node = visited[current_node]
            path.reverse()  # Đảo ngược đường đi
            return visited, path
        # Duyệt qua các node kề của node hiện tại
        for node, is_connected in enumerate(matrix[current_node]):
            # Nếu node kề chưa được duyệt và có kết nối với node hiện tại
            # thì thêm node kề vào hàng đợi và đánh dấu node kề đã được duyệt
            if is_connected and node not in visited:
                queue.append(node)
                visited[node] = current_node

# Cài đặt thuật toán DFS sử dụng đệ quy:
def DFS(matrix, start_node, end_node, visited=None, path=None):
    if visited is None:
        visited = {start_node: None}
    if path is None:
        path = []

    # Nếu node hiện tại là node kết thúc, ta dừng thuật toán
    if start_node == end_node:
        # Tạo đường đi từ node kết thúc đến node bắt đầu
        current_node = end_node
        while current_node is not None:
            path.append(current_node)
            current_node = visited[current_node]
        # Đảo ngược đường đi
        path.reverse()
        return visited, path

    # Duyệt qua các node kề của node hiện tại
    for node, is_connected in enumerate(matrix[start_node]):
        # Nếu node kề chưa được duyệt và có kết nối với node hiện tại
        # thì đánh dấu node kề đã được duyệt và gọi đệ quy với node kề làm node hiện tại
        if is_connected and node not in visited:
            visited[node] = start_node
            return DFS(matrix, node, end_node, visited, path)
        
# Cài đặt thuật toán UCS sử dụng hàng đợi ưu tiên:
def UCS(matrix, start, end):
    # Khởi tạo hàng đợi ưu tiên
    queue = [(0, start, [start])] 
    visited = {}
    costs = {start: 0}

    # Duyệt qua các node trong hàng đợi
    while queue:
        # Lấy node có chi phí nhỏ nhất ra khỏi hàng đợi
        (cost, node, path) = heapq.heappop(queue)
        # Nếu node hiện tại chưa được duyệt thì đánh dấu node hiện tại đã được duyệt
        if node not in visited:
            visited[node] = path
            # Nếu node hiện tại là node kết thúc, ta dừng thuật toán và trả về đường đi
            if node == end:
                return visited, path
            # Duyệt qua các node kề của node hiện tại và thêm node kề vào hàng đợi ưu tiên
            # nếu node kề chưa được duyệt hoặc có chi phí nhỏ hơn chi phí hiện tại của node kề đó
            # thì cập nhật chi phí của node kề và thêm node kề vào hàng đợi ưu tiên
            for i, is_connected in enumerate(matrix[node]):
                if is_connected:
                    total_cost = cost + matrix[node][i]
                    if i not in costs or total_cost < costs[i]:
                        costs[i] = total_cost
                        heapq.heappush(queue, (total_cost, i, path + [i]))
    # Nều không tìm thấy đường đi, ta trả về đường đi rỗng
    return visited, []

# Cài đặt thuật toán GBFS sử dụng hàng đợi ưu tiên:
# Với heristic là trọng số của cạnh
def GBFS(matrix, start, end):
    # Khởi tạo hàng đợi ưu tiên
    queue = [(0, start, [start])]
    visited = {}

    # Duyệt qua các node trong hàng đợi
    while queue:
        # Lấy node có chi phí nhỏ nhất ra khỏi hàng đợi
        (cost, node, path) = heapq.heappop(queue)
        # Nếu node hiện tại chưa được duyệt thì đánh dấu node hiện tại đã được duyệt
        if node not in visited:
            visited[node] = path
            # Nếu node hiện tại là node kết thúc, ta dừng thuật toán và trả về đường đi
            if node == end:
                return visited, path
            # Duyệt qua các node kề của node hiện tại và thêm node kề vào hàng đợi ưu tiên
            for i, is_connected in enumerate(matrix[node]):
                # Nếu node kề chưa được duyệt thì thêm node kề vào hàng đợi ưu tiên
                # với chi phí là trọng số của cạnh và heristic là trọng số của cạnh
                if is_connected and i not in visited:
                    total_cost = matrix[node][i]
                    heapq.heappush(queue, (total_cost, i, path + [i]))
    # Nều không tìm thấy đường đi, ta trả về đường đi rỗng
    return visited, []

# Cài đặt thuật toán A* sử dụng hàng đợi ưu tiên:
# Với heristic là khoảng cách Euclidean giữa node hiện tại và node kết thúc
def Astar(matrix, start, end, pos):
    # Hàm heristic
    def heuristic(node, goal):
        return math.sqrt((pos[node][0] - pos[goal][0]) ** 2 + (pos[node][1] - pos[goal][1]) ** 2)

    # Khởi tạo hàng đợi ưu tiên
    queue = [(0, start, [start])]
    visited = {}
    costs = {start: 0}

    # Duyệt qua các node trong hàng đợi
    while queue:
        # Lấy node có chi phí nhỏ nhất ra khỏi hàng đợi
        (cost, node, path) = heapq.heappop(queue)
        # Nếu node hiện tại chưa được duyệt thì đánh dấu node hiện tại đã được duyệt
        if node not in visited:
            visited[node] = path
            # Nếu node hiện tại là node kết thúc, ta dừng thuật toán và trả về đường đi
            if node == end:
                return visited, path
            # Duyệt qua các node kề của node hiện tại và thêm node kề vào hàng đợi ưu tiên
            for i, is_connected in enumerate(matrix[node]):
                # Nếu node kề chưa được duyệt 
                if is_connected and i not in visited:
                    # Tính chi phí của node kề và thêm node kề vào hàng đợi ưu tiên
                    total_cost = costs[node] + matrix[node][i]
                    # Nếu node kề chưa có chi phí hoặc chi phí hiện tại của node kề lớn hơn chi phí mới
                    # thì cập nhật chi phí của node kề và thêm node kề vào hàng đợi ưu tiên
                    if i not in costs or total_cost < costs[i]:
                        costs[i] = total_cost
                        priority = total_cost + heuristic(i, end)
                        heapq.heappush(queue, (priority, i, path + [i]))
    # Nều không tìm thấy đường đi, ta trả về đường đi rỗng
    return visited, []