from pymnet import *


net = MultilayerNetwork(aspects=0)

net.add_node(1)
net.add_node(2)
list(net)

net[1].deg()
net[1, 2] = 1
net[1, 3] = 2

# In the weighted networks the degree and the weighted degree, i.e. strength, of a node are different:
# print(net[1].deg())
# print(net[1].str())

dirnet = MultilayerNetwork(aspects=0, directed=True)
dirnet[1, 2] = 1

# print(dirnet[1, 2])
# print(dirnet[2, 1])

mnet = MultilayerNetwork(aspects=1)
mnet.add_node(1)
mnet.add_layer('a')
mnet[1, 'a'].deg()

mnet[1, 2, 'a', 'a'] = 1
mnet[3, 4, 'b', 'b'] = 1
mnet[1, 'a'][2, 'b'] = 2
list(mnet[1, 'a'])
# print(mnet[2, 'b'].deg())


mnet2 = MultilayerNetwork(aspects=2)
mnet2[1, 'a', 'x'][2, 'b', 'y'] = 1
mnet2.add_layer('c', 1)
mnet2.add_layer('z', 2)
# print(list(mnet2[1, 'a', 'z']))

mplex = MultiplexNetwork(couplings='none')
mplex[1, 'a'][2, 'a'] = 1
mplex.A['a'][1, 2]
mplex.A['a'][1, 3] = 2
mplex.add_layer('b')
# print(mplex[1, 'b'][2, 'b'])
# print(mplex.A['a'][2, 3])
# print(list(mplex.A))

cnet = MultiplexNetwork(couplings='categorical')
cnet.add_node(1)
cnet.add_layer('a')
cnet.add_layer('b')
cnet.add_layer('c')
cnet[1, 1, 'a', 'b']
# print(list(cnet.A))
# print(cnet[1, 1, 'a', 'c'])
# print(cnet[1, 1, 'a', 'b'])

onet = MultiplexNetwork(couplings='ordinal')
onet.add_node('node')
onet.add_layer(1)
onet.add_layer(2)
onet.add_layer(3)
onet['node', 'node', 1, 2]
onet['node', 'node', 1, 3]
# print(list(onet.A))
# print(onet['node', 'node', 1, 3])

cnet = MultiplexNetwork(couplings=('categorical', 10))
cnet.add_node(1)
cnet.add_node(2)
cnet.add_layer('a')
cnet.add_layer('b')
cnet[1, 1, 'a', 'b']
# print(list(cnet.A))
# print(cnet[1, 2, 'a', 'b'])

conet = MultiplexNetwork(couplings=['categorical', 'ordinal'])
conet.add_node('node')
conet.add_layer('a', 1)
conet.add_layer('b', 1)
conet.add_layer(1, 2)
conet.add_layer(2, 2)
# conet.add_layer(3, 3)
conet['node', 'node', 'a', 'a', 1, 2]
conet.A[('a', 1)]['node', 'node2'] = 1

# print(list(conet.A))
# print(conet['node', 'node', 'a', 'a', 1, 2])
