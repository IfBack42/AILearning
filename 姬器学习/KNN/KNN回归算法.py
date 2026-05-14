from sklearn.neighbors import KNeighborsRegressor
estimator = KNeighborsRegressor(n_neighbors=2)

# x_train = [[0,0,1],[1,1,0],[3,10,10],[4,11,12]]
x_train = [[12,27,3],[13,15,10],[23,16,9],[21,22,6]]

y_train = [0.1,0.2,0.3,0.4]

x_test = [[3,10,11]]

estimator.fit(x_train,y_train)

y_test = estimator.predict(x_test)

print(y_test)