import h5py
import sklearn.datasets
import sklearn.linear_model
import numpy as np
layers_strcuture=[2,2,2]
w=dict()
b=dict()
for l in range(1, 2):
    w["w" + str(l)] = np.random.randn(layers_strcuture[l], layers_strcuture[l - 1]) / np.sqrt(
        layers_strcuture[l - 1])
    b["b" + str(l)] = np.zeros((layers_strcuture[l], 1))
print(type(w["w1"]))
print(b)

def sigmoid(input_sum):
    """

    函数：
        激活函数Sigmoid
    输入：
        input_sum: 输入，即神经元的加权和
    返回：

        output: 激活后的输出
        input_sum: 把输入缓存起来返回
    """

    output = 1.0 / (1 + np.exp(-input_sum))
    return output, input_sum
# print(np.random.randn(2,4 ))#随机生成一个2行4列的矩


a=[[1,2,3],[2,3,4],[2,1,3]]
w=np.array(a)
print(w.T)
print(w)
print(w.shape)
print(sigmoid(w))
