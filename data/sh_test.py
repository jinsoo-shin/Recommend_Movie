# # %matplotlib inline
# import pandas as pd
# import matplotlib
# import matplotlib.pyplot as plt
# from matplotlib import style
# import numpy as np
# from sklearn.datasets import make_blobs
#
# style.use('seaborn-talk')
#
# krfont = {'family':'NanumGothic', 'weight':'bold', 'size':10}
# matplotlib.rc('font', **krfont)
# matplotlib.rcParams['axes.unicode_minus'] = False
#
# X, y = make_blobs(n_samples=150, n_features=2, centers=3, cluster_std=0.5, shuffle=True, random_state=0)
#
# plt.scatter(X[:,0], X[:,1], c='lightgray', marker='o', s=50)
# plt.grid(True)
# plt.show()
#
# from sklearn.datasets import make_blobs
#
# init_centroid = 'random'
# # init_centroid = 'k-means++'
#
# km = KMeans(n_clusters=3, init=init_centroid, random_state=0)
# y_km = km.fit_predict(X)
#
# plt.scatter(X[y_km == 0, 0], X[y_km == 0, 1], c='lightgreen', marker='s', s=50, label='cluster1')
# plt.scatter(X[y_km == 1, 0], X[y_km == 1, 1], c='orange', marker='o', s=50, label='cluster2')
# plt.scatter(X[y_km == 2, 0], X[y_km == 2, 1], c='lightblue', marker='v', s=50, label='cluster3')
# plt.scatter(km.cluster_centers_[:, 0], km.cluster_centers_[:, 1], c='red', marker='*', s=50, label='cluster_center')
#
# plt.legend()
# plt.grid(True)
# plt.show()
# print('finish to any key press')
#
# input()
