import numpy as np
import time
import matplotlib.pyplot as plt


# 欧氏距离计算
def distEclud(x, y):
    return np.sqrt(np.sum((x - y) ** 2))  # 计算欧氏距离


# 为给定数据集构建一个包含K个随机质心的集合
def randCent(dataSet, k):
    m, n = dataSet.shape
    centroids = np.zeros((k, n))
    for i in range(k):
        index = int(np.random.uniform(0, m))  #
        centroids[i, :] = dataSet[index, :]
    return centroids


# k均值聚类
def kmeans_open(dataSet, k):
    m = np.shape(dataSet)[0]  # 行的数目
    # 第一列存样本属于哪一簇
    # 第二列存样本的到簇的中心点的误差
    clusterAssment = np.mat(np.zeros((m, 2)))
    clusterChange = True

    # 第1步 初始化centroids
    centroids = randCent(dataSet, k)
    update_times = 1

    while clusterChange:
        clusterChange = False

        # 遍历所有的样本（行数）
        for i in range(m):
            minDist = 100000.0
            minIndex = -1

            # 遍历所有的质心
            # 第2步 找出最近的质心
            for j in range(k):
                # 计算该样本到质心的欧式距离
                distance = distEclud(centroids[j, :], dataSet[i, :])
                if distance < minDist:
                    minDist = distance
                    minIndex = j
            # 第 3 步：更新每一行样本所属的簇
            if clusterAssment[i, 0] != minIndex:
                clusterChange = True
                clusterAssment[i, :] = minIndex, minDist ** 2
        # 第 4 步：更新质心
        for j in range(k):
            pointsInCluster = dataSet[np.nonzero(clusterAssment[:, 0].A == j)[0]]  # 获取簇类所有的点
            centroids[j, :] = np.mean(pointsInCluster, axis=0)  # 对矩阵的行求均值

        # 每一次更新就记录一次其变化过程
        # plt.scatter() API详解 https://blog.csdn.net/qiu931110/article/details/68130199
        plt.scatter(dataSet[:, 0], dataSet[:, 1], s=1, c=clusterAssment.A[:, 0].astype(int))
        plt.scatter(centroids[:, 0], centroids[:, 1], marker='x', c=np.arange(k))
        plt.savefig('./result/update_{}.png'.format(update_times))  # 保存图片

        update_times += 1

    return clusterAssment.A[:, 0], centroids


def create_data_set(*cores):
    """生成k-means聚类测试用数据集"""
    ds = list()
    for x0, y0, z0 in cores:
        x = np.random.normal(x0, 0.1 + np.random.random() / 3, z0)
        y = np.random.normal(y0, 0.1 + np.random.random() / 3, z0)
        ds.append(np.stack((x, y), axis=1))

    return np.vstack(ds)


if __name__ == "__main__":
    k = 4
    ds = create_data_set((0, 0, 2500), (0, 2, 2500), (2, 0, 2500), (2, 2, 2500))

    # 绘制初始数据
    plt.scatter(ds[:, 0], ds[:, 1], s=1)
    plt.savefig('./result/init-dataSet.png')

    t0 = time.time()
    result, cores = kmeans_open(ds, k)
    t = time.time() - t0

    plt.scatter(ds[:, 0], ds[:, 1], s=1, c=result.astype(np.int))
    plt.scatter(cores[:, 0], cores[:, 1], marker='x', c=np.arange(k))
    plt.savefig('./result/kmeans_open.png')

    print(u'使用kmeans_open算法，1万个样本点，耗时%f0.3秒' % t)
