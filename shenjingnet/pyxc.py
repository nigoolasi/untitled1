import numpy as np


# 定义双曲函数
def tanh(x):
    return np.tanh(x)


# 定义双曲函数的导数
def tanh_deriv(x):
    return 1.0 - np.tanh(x) ** 2


def logistic(x):
    return 1 / (1 + np.exp(-x))


def logistic_derivative(x):
    return logistic(x) * (1 - logistic(x))


# 定义NeuralNetwork 神经网络算法
class NeuralNetwork:
    # 初始化，layes表示的是一个list，eg：[10,10,3]表示第一层10个神经元，第二层10个神经元，第三层3个神经元
    def __init__(self, layers, activation='tanh'):
        """
        :param layers: A list containing the number of units in each layer.
        Should be at least two values
        包含每个层中单元数量的列表。
        应该至少有两个值（至少两层，输入层不算）
        :param activation: The activation function to be used. Can be
        激活函数
        "logistic" or "tanh"
        """
        # 选择激活函数与其对应的导数
        if activation == 'logistic':
            self.activation = logistic
            self.activation_deriv = logistic_derivative
        elif activation == 'tanh':
            self.activation = tanh
            self.activation_deriv = tanh_deriv

        self.weights = []
        # 循环从1开始，相当于以第二层为基准，进行权重的初始化
        for i in range(1, len(layers) - 1):  # len(layers)代表了神经元的层数（输入层不算）
            # 对当前神经节点的前驱随机赋值[-0.25,0.25]
            self.weights.append((2 * np.random.random((layers[i - 1] + 1, layers[i] + 1)) - 1) * 0.25)  # i指当前层神经元
            # 对当前神经节点的后继赋值
            self.weights.append((2 * np.random.random((layers[i] + 1, layers[i + 1])) - 1) * 0.25)

    # 训练函数
    # X：训练集，传入的数据，通常模拟成二维矩阵，即x的每一行对应一个实例的各个特征，即行为实例个数，列为实例特征个数
    # Y:分类的标记，每个实例对应的结果，即输出层单元
    # learning_rate 学习率，即阶层
    # epochs，表示抽样的方法对神经网络进行更新的最大次数，
    def fit(self, X, y, learning_rate=0.2, epochs=10000):
        X = np.atleast_2d(X)  # 确定X至少是二维的数据
        # shape功能是查看矩阵或者数组的维数，0为行数，1为列数
        temp = np.ones([X.shape[0], X.shape[1] + 1])  # 初始化矩阵，建立一个新矩阵[x,y]，其其行数与X一样多，其列数比X多1
        #:代表所有列数，0:-1代表第一列到倒数最后一列
        temp[:, 0:-1] = X  # 将偏置单元bias 添加到输入层
        X = temp
        y = np.array(y)  # 把list转换成array的形式
        # 每次随机选一个，共循环epochs次
        for k in range(epochs):
            # 随机选取一行，对神经网络进行训练
            i = np.random.randint(X.shape[0])
            a = [X[i]]

            # 完成所有正向的更新
            # 分为两步，先计算实例值与权重的乘积，再调用激活函数进行非线性转化
            for l in range(len(self.weights)):
                a.append(self.activation(np.dot(a[l], self.weights[l])))
            # y[i]是实例值a[-1]是输出层的值
            error = y[i] - a[-1]  # 它们之间的误差
            deltas = [error * self.activation_deriv(a[-1])]

            # 开始反向计算误差，更新权重
            for l in range(len(a) - 2, 0, -1):  # 我们从倒数第二层开始，倒数第一层是输出层，循环到第0层，阶层是-1
                deltas.append(deltas[-1].dot(self.weights[l].T) * self.activation_deriv(a[l]))  # .T表示转置，dot表示矩阵的行列式计算
            # 将层数颠倒
            deltas.reverse()
            for i in range(len(self.weights)):
                # 权重更新
                layer = np.atleast_2d(a[i])
                # 偏向bias更新
                delta = np.atleast_2d(deltas[i])
                self.weights[i] += learning_rate * layer.T.dot(delta)

    # 预测函数
    # 参考正向输入
    def predict(self, x):
        x = np.array(x)
        temp = np.ones(x.shape[0] + 1)
        temp[0:-1] = x
        a = temp
        for l in range(0, len(self.weights)):
            # 这里的话我们不需要保存每一个值，因为我们只需要输出层的值
            a = self.activation(np.dot(a, self.weights[l]))
        return a


nn = NeuralNetwork([2, 2, 1], 'tanh')
X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
Y = np.array([0, 1, 1, 0])
nn.fit(X, Y)
for i in [[0, 0], [0, 1], [1, 0], [1, 1]]:
    if nn.predict(i) < 0.5:
        p = 0
    else:
        p = 1
    print(i, nn.predict(i), p)
