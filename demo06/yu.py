import curses
import random
import time

# 初始化curses
stdscr = curses.initscr()
curses.curs_set(0)  # 隐藏光标
sh, sw = stdscr.getmaxyx()  # 获取屏幕大小
w = curses.newwin(sh, sw, 0, 0)  # 创建一个新的窗口
w.keypad(1)  # 启用键盘映射
w.timeout(100)  # 设置非阻塞模式，100毫秒超时

# 定义蛇和食物的初始状态
snake = [(sh // 2, sw // 2)]
food = None
while True:
    if not food:
        food = (random.randint(1, sh - 2), random.randint(1, sw - 2))
        while food in snake:
            food = (random.randint(1, sh - 2), random.randint(1, sw - 2))

    next_dir = curses.KEY_RIGHT

    try:
        c = w.getch()
        if c == curses.KEY_UP:
            next_dir = curses.KEY_UP
        elif c == curses.KEY_DOWN:
            next_dir = curses.KEY_DOWN
        elif c == curses.KEY_LEFT:
            next_dir = curses.KEY_LEFT
        elif c == curses.KEY_RIGHT:
            next_dir = curses.KEY_RIGHT
        elif c == ord('q'):
            break
    except curses.error:
        pass

    new_head = list(snake[0])

    if next_dir == curses.KEY_UP:
        new_head[0] -= 1
    elif next_dir == curses.KEY_DOWN:
        new_head[0] += 1
    elif next_dir == curses.KEY_LEFT:
        new_head[1] -= 1
    elif next_dir == curses.KEY_RIGHT:
        new_head[1] += 1

    if new_head in snake or new_head[0] in [0, sh - 1] or new_head[1] in [0, sw - 1]:
        stdscr.addstr(sh // 2, (sw - 10) // 2, "Game Over!", curses.color_pair(1))
        stdscr.refresh()
        time.sleep(2)
        break

    if new_head == food:
        food = None
    else:
        snake.pop()

    snake.insert(0, new_head)

    w.erase()

    for pos in snake:
        w.addch(pos[0], pos[1], 'o', curses.color_pair(1))

    if food:
        w.addch(food[0], food[1], '*', curses.color_pair(2))

    w.refresh()

    time.sleep(0.1)

# 结束curses模式
curses.endwin()