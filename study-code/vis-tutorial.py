from pymnet import *
import matplotlib
matplotlib.use('TkAgg')

net = models.er_multilayer(5, 2, 0.2)
# fig = draw(net, show=True)
# fig.savefig('docs/net.pdf')

# fig = draw(er(10, 3*[0.4]), layout="spring", show=True)

# fig = draw(er(10, 3*[0.3]),
#            layout="circular",
#            layershape="circle",
#            nodeColorDict={(0, 0): "r", (1, 0): "r", (0, 1): "r"},
#            layerLabelRule={},
#            nodeLabelRule={},
#            nodeSizeRule={"rule": "degree", "propscale": 0.05}, show=True)
