import re

# https://www.cse.msu.edu/~cse231/Online/Projects/Project10/Project10.pdf
default_value = 0
black_value = 1
white_value = 2
# 默认 黑色棋子 白色棋子
pieces = [' ', chr(0x2591), chr(0x2593)]
size = 4
directions = {
  'e': lambda i, j: (i, j + 1),
  'w': lambda i, j: (i, j - 1),
  'n': lambda i, j: (i - 1, j),
  's': lambda i, j: (i + 1, j),
  'ne': lambda i, j: (i - 1, j + 1),
  'nw': lambda i, j: (i - 1, j - 1),
  'se': lambda i, j: (i + 1, j + 1),
  'sw': lambda i, j: (i + 1, j - 1)
}
abbreviate = r'([a-z]+)([0-9]+)'


# 棋盘
class Board(object):

  def __init__(self):
    self.matrix = []
    for i in range(size):
      self.matrix.append([default_value] * size)
    test = re.match(abbreviate, deindexify(size - 1, size - 1))
    # 行名填充字符
    self.row_fill_len = 1 + len(test.group(1))
    # 列名填充字符
    self.col_fill_len = 2 + len(test.group(2))

  # 打印出棋盘
  def draw(self):
    header = ' ' * (self.row_fill_len + 1 + int((self.col_fill_len - 1) / 2))
    sep = ' ' * self.row_fill_len + '+'
    for i in range(len(self.matrix)):
      col_name = re.match(abbreviate, deindexify(0, i)).group(2)
      header = header + col_name + ' ' * (self.col_fill_len + 1 - len(col_name))
      sep = sep + '-' * self.col_fill_len + '+'
    print(header)
    print(sep)
    for i in range(len(self.matrix)):
      row_name = re.match(abbreviate, deindexify(i, 0)).group(1)
      line = row_name + ' ' * (self.row_fill_len - len(row_name))
      for j in range(len(self.matrix[i])):
        line += '|' + (' ' * int((self.col_fill_len - 1) / 2)) + pieces[self.matrix[i][j]] + ' ' * (
            self.col_fill_len - int((self.col_fill_len - 1) / 2) - 1)
      line += '|'
      print(line)
      print(sep)


def initialize(board):
  half = int(size / 2) - 1
  board.matrix[half][half] = white_value
  board.matrix[half][half + 1] = black_value
  board.matrix[half + 1][half] = black_value
  board.matrix[half + 1][half + 1] = white_value


# a1 -> 0,0
def indexify(position):
  test = re.match(abbreviate, position)
  x = 0
  v_chars = test.group(1)
  v_len = len(v_chars)
  for i in range(v_len):
    v_c = v_chars[i]
    x += (ord(v_c) - ord('a') + 1) * pow(26, v_len - 1 - i)

  y = 0
  v_chars = test.group(2)
  v_len = len(v_chars)
  for i in range(v_len):
    v_c = v_chars[i]
    y += (ord(v_c) - ord('0')) * pow(10, v_len - 1 - i)
  return x - 1, y - 1


# 0,0 -> a1
def deindexify(row, col):
  def s(n, l, c):
    if 1 <= n <= l:
      return chr(n - 1 + ord(c))
    else:
      return s(int(n / l), l, c) + s(n % l, l, c)

  return s(row + 1, 26, 'a') + str(col + 1)


# 计算分数
def count_pieces(board):
  black = 0
  white = 0
  for i in range(len(board.matrix)):
    for j in range(len(board.matrix[i])):
      if board.matrix[i][j] == black_value:
        black += 1
      elif board.matrix[i][j] == white_value:
        white += 1
  return black, white


# 计算八个方向的可消除情况
def get_all_streaks(board, row, col, piece):
  streaks = {}
  for key, value in directions.items():
    i = row
    j = col
    result = []
    next_i, next_j = value(i, j)
    stop = False
    find = False
    while not stop:
      if not (0 <= next_i < size and 0 <= next_j < size):
        stop = True
      else:
        next_v = board.matrix[next_i][next_j]
        if next_v == default_value:
          stop = True
        elif next_v == piece:
          stop = True
          find = True
        else:
          result.append((next_i, next_j))
          next_i, next_j = value(next_i, next_j)
    if not find:
      result.clear()
    streaks[key] = result
  return streaks


# 计算消除的对方棋子
def get_all_capturing_cells(board, piece):
  result = {}
  for i in range(len(board.matrix)):
    for j in range(len(board.matrix[i])):
      if board.matrix[i][j] == default_value:
        combine = []
        for key, value in get_all_streaks(board, i, j, piece).items():
          if len(value) > 0:
            combine += value
        if len(combine) > 0:
          result[(i, j)] = combine
  return result


def get_hint(board, piece):
  result = []
  for key, value in get_all_capturing_cells(board, piece).items():
    result.append((deindexify(key[0], key[1]), key, len(value)))
  result.sort(key=lambda x: (x[2], x[1][0], x[1][1]), reverse=True)
  return list(map(lambda x: x[0], result))


def place_and_flip(board, row, col, piece):
  if not 0 <= row < size and 0 <= col < size:
    raise ValueError("The	%s,%s is	outside	of	the	board" % (row, col))
  v_value = board.matrix[row][col]
  if v_value != default_value:
    raise ValueError("The	%s,%s is	already occupied" % (row, col))
  count = 0
  for key, value in get_all_streaks(board, row, col, piece).items():
    count += len(value)
    for i, j in value:
      board.matrix[i][j] = piece
  if count == 0:
    raise ValueError("The	%s,%s does not yield any capture" % (row, col))
  board.matrix[row][col] = piece


def is_game_finished(board):
  fill_flag = True
  for i in range(len(board.matrix)):
    if not fill_flag:
      break
    for j in range(len(board.matrix[i])):
      if board.matrix[i][j] == default_value:
        fill_flag = False
        break
  return fill_flag or (len(get_hint(board, black_value)) == 0 and len(get_hint(board, white_value)) == 0)


def get_winner(board):
  black_score, white_score = count_pieces(board)
  result = 'draw'
  if black_score > white_score:
    result = 'black'
  elif black_score < white_score:
    result = 'white'
  return result


def choose_color():
  opponent_color = 'white'
  my_color = input('Pick a color: ')
  while my_color not in ('black', 'white'):
    print('Please choose one color of (black,white).')
    my_color = input('Pick a color: ')
  if my_color == 'white':
    opponent_color = 'black'
  return my_color, opponent_color


def game_play_human():
  my_color, opponent_color = choose_color()
  print("You are '%s' and your opponent is '%s'." % (my_color, opponent_color))
  board = Board()
  initialize(board)
  turn = 'white'
  turn_piece = white_value
  while not is_game_finished(board):
    print('Current board:')
    board.draw()
    print('  Black: %d, White: %d' % count_pieces(board))
    cmd = input("[%s's turn] :> " % turn)
    if cmd == 'pass':
      if len(get_hint(board, turn_piece)) > 0:
        print("  Can't hand over to opponent, you have moves, type 'hint'.")
        continue
    elif cmd == 'hint':
      print("  Hint: %s" % ' ,'.join(get_hint(board, turn_piece)))
      continue
    elif cmd == 'exit':
      break
    elif not re.match(abbreviate, cmd):
      print("  Command is Error: %s" % cmd)
      continue
    else:
      print('  %s played %s' % (turn, cmd))
      row, col = indexify(cmd)
      place_and_flip(board, row, col, turn_piece)
    if turn == 'white':
      turn = 'black'
      turn_piece = black_value
    elif turn == 'black':
      turn = 'white'
      turn_piece = white_value
  print('Current board:')
  board.draw()
  black_score, white_score = count_pieces(board)
  print('  Black: %d, White: %d' % (black_score, white_score))
  print("  '%s' wines by %d! yay!! " % (get_winner(board), abs(black_score - white_score)))


if __name__ == "__main__":
  game_play_human()
