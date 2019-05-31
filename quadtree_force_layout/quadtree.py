from matplotlib import pyplot as plt
from itertools import product
import random
import math
nodes_data =  [
    {"name": "Travis", "sex": "M"},
    {"name": "Rake", "sex": "M"},
    {"name": "Diana", "sex": "F"},
    {"name": "Rachel", "sex": "F"},
    {"name": "Shawn", "sex": "M"},
    {"name": "Emerald", "sex": "F"}
]
links_data = [
    {"source": "Travis", "target": "Rake"},
    {"source": "Diana", "target": "Rake"},
    {"source": "Diana", "target": "Rachel"},
    {"source": "Rachel", "target": "Rake"},
    {"source": "Rachel", "target": "Shawn"},
    {"source": "Emerald", "target": "Rachel"}
]

##  Config
class Config():
    width = 500
    height = 500
    K = 0.7
    Air = 0.2
    iterations = 500
    L = 200
    iter_time = 0.01

class Point():
    v_x = 0
    v_y = 0
    f_x = 0
    f_y = 0
    x = 0
    y = 0
    value = 100
    def __init__(self, name, *args, **kwargs):
        self.name = name
    def init_position(self, config):
        self.x = random.randint(0, config.width)
        self.y = random.randint(0, config.height)
    
points = {
    raw_node['name']: Point(name = raw_node['name'])
    for raw_node in nodes_data
}
for name in points:
    points[name].init_position(Config)


def zero_F():
    for name in points:
        points[name].f_x = 0
        points[name].f_y = 0

def step():
    def cal_distance(pa:Point, pb:Point, p=1):
        if p == 1:
            return  ((pa.x - pb.x) **2 + (pa.y - pb.y)**2) ** 0.5
        elif p == 2:
            return ((pa.x - pb.x) **2 + (pa.y - pb.y)**2)
    def cal_p2p(pa:Point, pb:Point):
        """
            return F from pa to pb
        """
        _dis = cal_distance(pa, pb, 1)
        _F = pa.value * pb.value / cal_distance(pa, pb, 2)
        # print("point : ", _F)
        return (pb.x - pa.x) / _dis * _F, (pb.y - pa.y) / _dis * _F

    def cal_edge(pa:Point, pb:Point):
        """
            return edge F from pa to pb
        """
        _dis = cal_distance(pa, pb, 1)
        _F = Config.K * (Config.L - _dis)
        # print("edge: ", _F)
        return (pb.x - pa.x) / _dis * _F, (pb.y - pa.y) / _dis * _F

    # calculate pi*pj
    for src, tgt in product(points, points):
        if src == tgt:
            continue
        _fx, _fy = cal_p2p(points[src], points[tgt])
        points[tgt].f_x += _fx
        points[tgt].f_y += _fy

    for edge in links_data:
        src, tgt = edge['source'], edge['target']
        _fx, _fy = cal_edge(points[src], points[tgt])
        points[tgt].f_x += _fx
        points[tgt].f_y += _fy
        _fx, _fy = cal_edge(points[tgt], points[src])
        points[src].f_x += _fx
        points[src].f_y += _fy

    for name in points:
        points[name].f_x -= Config.Air * points[name].v_x
        points[name].f_y -= Config.Air * points[name].v_y
        points[name].x += points[name].v_x * Config.iter_time
        points[name].y += points[name].v_y * Config.iter_time
        points[name].v_x += points[name].f_x
        points[name].v_y += points[name].f_y

def quadtree_step():
    def generate_quadtree():
        class Quadtree():
            def __init__(self, points, left_top=(0,0), width=0, height=0, *args, **kwargs):
                self.left_top = left_top
                self.width = width
                self.height = height
                self.childrens = []
                self.points = points
                self.mode = 0
                # mode 0 single pixel
                # mode 1 only x-axies pixels
                # mode 2 only y-axies pixels
                # mode 3 x-y-axies pixels
                
                if self.width >2 and self.height>2:
                    mid_width = width/2 + self.left_top
                    mid_height = height/2 + self.left_top
                    self.childrens.append(Quadtree(
                        points = filter(lambda point: True if point[0]<mid_width and point[1]<mid_height else False, self.points),
                        left_top = self.left_top,
                        width = width / 2,
                        height = height /2,
                    ))
                    self.childrens.append(Quadtree(
                        points = filter(lambda point: True if point[0]<mid_width and point[1]>=mid_height else False, self.points),
                        left_top = (self.left_top[0], mid_height),
                        width = width / 2,
                        height = height /2,
                    ))
                    self.childrens.append(Quadtree(
                        points = filter(lambda point: True if point[0]>=mid_width and point[1]<mid_height else False, self.points),
                        left_top = (mid_width, self.left_top[1]),
                        width = width / 2,
                        height = height /2,
                    ))
                    self.childrens.append(Quadtree(
                        points = filter(lambda point: True if point[0]>=mid_width and point[1]>=mid_height else False, self.points),
                        left_top = (mid_width, mid_height),
                        width = width / 2,
                        height = height /2,
                    ))
                elif self.width <=2 and self.height >2:
                    mid_height = height/2 + self.left_top
                    self.childrens.append(Quadtree(
                        points = filter(lambda point: True if point[1]<mid_height else False, self.points),
                        left_top = self.left_top,
                        width = width / 2,
                        height = height /2,
                    ))
                    self.childrens.append(Quadtree(
                        points = filter(lambda point: True if point[1]>=mid_height else False, self.points),
                        left_top = (self.left_top[0], mid_height),
                        width = width / 2,
                        height = height /2,
                    ))
                elif self.width >2 and self.height<=2:
                    mid_width = width/2 + self.left_top
                    self.childrens.append(Quadtree(
                        points = filter(lambda point: True if point[0]<mid_width and point[1]<mid_height else False, self.points),
                        left_top = self.left_top,
                        width = width / 2,
                        height = height /2,
                    ))
                    self.childrens.append(Quadtree(
                        points = filter(lambda point: True if point[0]>=mid_width and point[1]<mid_height else False, self.points),
                        left_top = (mid_width, self.left_top[1]),
                        width = width / 2,
                        height = height /2,
                    ))
                else:
                    # no need to calculate
                    self.sum_point_x = sum([point.x for point in self.points]) / len(self.points)
                    self.sum_point_y = sum([point.y for point in self.points]) / len(self.points)
                    self.sum_value = sum([point.value for point in self.points])
    def cal_distance(pa:Point, pb:Point, p=1):
        if p == 1:
            return  ((pa.x - pb.x) **2 + (pa.y - pb.y)**2) ** 0.5
        elif p == 2:
            return ((pa.x - pb.x) **2 + (pa.y - pb.y)**2)
    def cal_p2p(pa:Point, pb:Point):
        """
            return F from pa to pb
        """
        _dis = cal_distance(pa, pb, 1)
        _F = pa.value * pb.value / cal_distance(pa, pb, 2)
        # print("point : ", _F)
        return (pb.x - pa.x) / _dis * _F, (pb.y - pa.y) / _dis * _F

    def cal_edge(pa:Point, pb:Point):
        """
            return edge F from pa to pb
        """
        _dis = cal_distance(pa, pb, 1)
        _F = Config.K * (Config.L - _dis)
        # print("edge: ", _F)
        return (pb.x - pa.x) / _dis * _F, (pb.y - pa.y) / _dis * _F

    # calculate pi*pj
    for src, tgt in product(points, points):
        if src == tgt:
            continue
        _fx, _fy = cal_p2p(points[src], points[tgt])
        points[tgt].f_x += _fx
        points[tgt].f_y += _fy

    for edge in links_data:
        src, tgt = edge['source'], edge['target']
        _fx, _fy = cal_edge(points[src], points[tgt])
        points[tgt].f_x += _fx
        points[tgt].f_y += _fy
        _fx, _fy = cal_edge(points[tgt], points[src])
        points[src].f_x += _fx
        points[src].f_y += _fy

    for name in points:
        points[name].f_x -= Config.Air * points[name].v_x
        points[name].f_y -= Config.Air * points[name].v_y
        points[name].x += points[name].v_x * Config.iter_time
        points[name].y += points[name].v_y * Config.iter_time
        points[name].v_x += points[name].f_x
        points[name].v_y += points[name].f_y


import time

from matplotlib.animation import FuncAnimation

# ln.plot()
# for edge in links_data:
#     src, tgt = edge['source'], edge['target']
#     plt.plot([points[src].x, points[tgt].x], [points[src].y, points[tgt].y])
# print(plt.plot([[1,2], [3,4]], [[200,300],[400,500]]))
# # print([[1,2], [3,4]] + [[p.x] for p in points.values()])
# pp = plt.scatter([p.x for p in points.values()], [p.y for p in points.values()])
# print(pp)
# ln = plt.plot([[1,2], [3,4]], [[200,300],[400,500]])
# plt.show()

# step()
# pp.set_offsets([p.x for p in points.values()], [p.y for p in points.values()])
# plt.show()

# fig, ax = plt.subplots()

src = time.time()
for i in range(Config.iterations):
    zero_F()
    step()
    plt.cla()
    plt.axis([-Config.width, 2*Config.width, -Config.height, 2*Config.height])

    plt.scatter([p.x for p in points.values()], [p.y for p in points.values()])
    # print("f", [(p.f_x**2+p.f_y**2)**0.5 for p in points.values()])
    plt.plot([[points[edge['source']].x, points[edge['target']].x] for edge in links_data],
            [[points[edge['source']].y, points[edge['target']].y] for edge in links_data])
    plt.show(block=False)
    # plt.set_title("frame {}".format(i))
    # Note that using time.sleep does *not* work here!
    plt.pause(0.001)

print (time.time() - src)