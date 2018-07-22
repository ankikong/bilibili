from PIL import Image
import numpy as np
to = [(0, 1), (0, -1), (1, 0), (-1, 0)]
represent = {
    # 362 是6或9
    358: "0", 166: "1", 300: "2", 326: "3", 276: "4", 317: "5", 362: "6", 244: "7", 402: "8", 128: "+", 36: "-"
}


def bfs_count(start, vis, a):
    q = [start]
    count = 0
    while len(q) > 0:
        tmp = q[0]
        q.pop(0)
        for i in to:
            if vis[tmp[0] + i[0]][tmp[1] + i[1]] == 1:
                continue
            if a[tmp[0] + i[0]][tmp[1] + i[1]] != 255:
                count += 1
                vis[tmp[0] + i[0]][tmp[1] + i[1]] = 1
                q.append((tmp[0] + i[0], tmp[1] + i[1]))
#    print(represent[count])
    return represent[count]


def findblack(file):
    data = ""
    im = Image.open(file)
    im = im.convert("L")
    y, x = im.size
    a = np.array(im)
    vis = np.full((x, y), 0)
    for i in range(y):
        for j in range(x):
            if a[j][i] != 255 and vis[j][i] == 0:
                data += bfs_count((j, i), vis, a)
            else:
                vis[j][i] = 1
    print(data)
    return eval(data)


def cmp(file):
    data = []
    for i in range(12):
        tmp = Image.open(".\\data\\{}.png".format(i))
        tmp = tmp.convert("L")
        data.append(np.array(tmp))
    im = Image.open(file)
    im = im.convert("L")
    x, y = im.size
    print(x, y)
    a = np.array(im)
    i = 0
    where = []
    print(len(a))

    while i < x:
        j = 0
        while j < y:
            end = True
            if a[j][i] != 255:
                start = [i, ]
                while end:
                    i += 1
                    for j in range(y):
                        if a[j][i] != 255:
                            break
                        elif j == y - 1:
                            end = False
                start.append(i)
                where.append(start)
                print(start)
            if end is False:
                    break
            j += 1
            if end is False:
                break
        i += 1
    for j in where:
        print(j)
        test = im.crop((j[0], 0, j[1], y))
        test.save("{}.png".format(i))
        i += 1



if __name__ == "__main__":
    cmp(file="0.png")
