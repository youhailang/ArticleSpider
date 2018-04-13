from zheye import zheye
z = zheye()
positions = z.Recognize('captcha_cn.gif')
print(positions)
positions = [(x[1], x[0]) for x in positions]
print(positions)
positions.sort(key=lambda x: x[0])
print(positions)
