import sys


def main(argv):
  dict_map = {'a': 10, 'b': 5, 'c': 5, 'd': 2, 'e': 2, 'f': 2, 'g': 1}
  list = []
  for key, value in dict_map.items():
    list.append((key, value))
  list.sort(key=lambda x: x[1], reverse=True)

  freq = {}
  rank_num = 0
  for v in list:
    t = freq.get(v[1])
    rank_num += 1
    if t is None:
      t = {
        'rank': rank_num,
        'cnt': 0
      }
      freq[v[1]] = t
    t['cnt'] += 1
  rank_num = 0
  for v in list:
    key = v[0]
    frequency = v[1]
    rank_num = freq[frequency]['rank']
    cnt = freq[frequency]['cnt']
    print(key, frequency, rank_num + (cnt - 1) / 2)


if __name__ == "__main__":
  main(sys.argv)
