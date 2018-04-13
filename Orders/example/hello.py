def normal_test():
  # 打印可显示字符,如果超出ascii范围,打印对应的编码, 中 -> \u4e2d
  print(ascii('中'))
  # 返回i对应的unicode 0 <= i <= 0x10ffff
  print(hex(ord('中')))
  # 打印一个int的二进制字符（前缀为0b）
  print(bin(0xaa))
  # 检查一个对象是否是可调用的
  print(callable(lambda x: x))
  print(callable(1))
  # 返回i对应的unicode 0 <= i <= 0x10ffff
  print(chr(0x4e2d))
  # 返回 商和余数
  print(divmod(10, 3))
  # 字符格式化
  print(format("字符串:%s,数字:%d,百分比:%.2f%%" % ('11', 1, 99.812)))
  # 返回十六进制 hex(12648430) -> '0xc0ffee'
  print(hex(12648430))
  # 返回八进制 oct(12648430) -> '0o60177756'
  print(oct(12648430))
  # 测试对象类型
  print(isinstance('a', (int, float)))
  # 测试是否子类
  print(issubclass(int, str), issubclass(str, object), issubclass(int, object))


def code_test():
  # 编译 与 执行函数
  exec(compile('print("hello")', '', 'exec'))
  eval(compile('print("hello")', '', 'eval'))
  # 传递参数
  scope = {}
  exec("a = 4", scope)
  print(scope['a'])
  # eval 可以直接返回执行结果
  scope['b'] = 5
  print(eval("a + b", scope))
  # 返回全局所有的变量
  print(globals().keys())
  # 返回局部所有的变量
  print(locals().keys())
  # 返回对象id
  print(id(scope))


def collection_test():
  # 打印range
  print(range(10))
  print(list(range(0, 10, 2)))
  # 对所有元素进平方
  print(list(map(lambda x: x * x, range(10))))
  # 取出所有的偶数
  print(list(filter(lambda x: x % 2 == 0, range(10))))
  # 按照元素下标 合并两个list (取其中最小的一个list长度)
  print(list(map(lambda x, y: x + y, [1, 3, 5, 7, 9, 1], [2, 4, 6, 8, 10])))
  # *args：（表示的就是将实参中按照位置传值，多出来的值都给args，且以元祖的方式呈现）
  # **kwargs：（表示的就是形参中按照关键字传值把多余的传值以字典的方式呈现）

  # 测试参数中是否全部非空
  print(all(['1', '2', '']))
  # 测试参数中是否有一个非空
  print(any(['', '', '']))
  # 转换可迭代对象
  print(list(iter(range(10))))

  # 返回对象大小
  print(len('abc'), len(range(10)), len({'a': 1}))
  # 取最大值
  print(max(range(10), key=lambda k: k))
  # 取最小值
  print(min(range(10), key=lambda k: k))
  # 取下个元素
  print(next(iter(range(10))))
  # 排序
  print(sorted([(1, 2), (1, 3)], reverse=True))
  print(sorted([(1, 2), (1, 3)], key=lambda x: x[0], reverse=True))
  # 求和
  print(sum([1, 2, 3]))


def function_test():
  from functools import reduce, partial
  # reduce 函数
  print(reduce(lambda x, y: x + y, [1, 2, 3, 4, 5]))
  print(reduce(lambda u, v: (min(u[0], v), max(u[1], v)), [1, 2, 3, 4, 5], (0, 0)))

  # partial 生成一个函数
  print(partial(lambda a, b: a + b, 99)(1))


if __name__ == "__main__":
  # normal_test()
  # collection_test()
  function_test()
