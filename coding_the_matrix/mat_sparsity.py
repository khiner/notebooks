'''
>>> from mat import Mat
>>> from vec import Vec
>>> (Mat((set(range(10000)),set(range(100000))),{(0,0):1})*Vec(set(range(100000)),{0:2}))[0]
2
>>> (Vec(set(range(100000)),{0:2})*Mat((set(range(10000)),set(range(100000))),{(0,0):1}).transpose())[0]
2
>>> (Mat((set(range(10000)),set(range(100000))),{(0,0):1})*Mat((set(range(100000)), set(range(9999))), {(0,0):2}))[0,0]
2
'''
