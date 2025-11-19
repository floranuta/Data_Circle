import pandas as pd
import config as c
from sampler import oversample
from sklearn.model_selection import KFold
from sklearn.metrics import accuracy_score


def run(data: pd.DataFrame,
        is_oversample: bool,
        classifier: object,
        k_fold_split: int = 10,
        method: str=None) -> list:

    # separte feature and target values
    X = data.drop(c.TARGET_COLUMN, axis=1).to_numpy()
    y = data[c.TARGET_COLUMN].to_numpy()

    # apply oversampling
    if is_oversample == True:
        X, y = oversample(X, y, method)

    # define number of fold
    kf = KFold(n_splits=k_fold_split)

    y_test_all = []
    y_pred_all = []
    iteration = 1
    accuracy_all = []


    # apply K-fold cross validation
    # https://neptune.ai/blog/cross-validation-in-machine-learning-how-to-do-it-right

    for train_index, test_index in kf.split(X):

        print(f"ITERATION {iteration} / {kf.n_splits}")

        # split data into train and test data
        # print("TRAIN:", len(train_index), "TEST:", len(test_index))
        # print("TRAIN:", train_index, "TEST:", test_index)
        X_train, X_test = X[train_index], X[test_index]
        y_train, y_test = y[train_index], y[test_index]


        # train a model
        classifier.fit(X_train, y_train)

        # predict pump status
        y_pred = classifier.predict(X_test)

        # print("Tuned Hyperparameters: {}".format(classifier.best_params_))

        # show accuracy
        # https://scikit-learn.org/stable/modules/generated/sklearn.metrics.accuracy_score.html
        acc_score = accuracy_score(y_test, y_pred, normalize=True)
        accuracy_all.append(acc_score)
        print("accuracy_score: ", acc_score)

        # save all true and predicted value
        y_test_all.append(y_test)
        y_pred_all.append(y_pred)

        iteration += 1

    return y_test_all, y_pred_all, accuracy_all, classifier