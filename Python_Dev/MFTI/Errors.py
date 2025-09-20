import sklearn.metrics as skm

#Mean Squared Error
def mse(y_pred, y_test):
    return skm.mean_squared_error(y_pred, y_test)

#Mean Absolute Error
def msa(y_pred, y_test):
    return skm.mean_absolute_error(y_pred, y_test)