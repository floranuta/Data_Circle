from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.tree import plot_tree
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import randint

import config as c

def evaluate_model(y_test_all: list,
                  y_pred_all: list,
                  accuracy_all: list,
                  ) -> None:

    # flat out matrix into single list
    y_test_res = [val for y_test in y_test_all for val in y_test]
    y_pred_res = [val for y_pred in y_pred_all for val in y_pred]

    # create classification report
    cr = classification_report(y_test_res, y_pred_res, target_names=list(c.TARGET_MAPPING.keys()))
    print(cr)

    plt.figure(figsize=[8,6])
    plt.plot(accuracy_all)
    plt.title("Accuracy")
    plt.xlabel("Number of iteration")
    plt.ylabel("Accuracy")
    plt.show()
    plt.close()

    # Create a confusion matrix
    # https://medium.com/@sanyagubrani/evaluating-multi-class-classification-model-using-confusion-matrix-in-python-4d9344084dfa
    cm = confusion_matrix(y_test_res, y_pred_res, normalize="all")

    # Plot the confusion matrix
    plt.figure(figsize=[8,6])
    sns.heatmap(cm, annot=True, cmap='YlGnBu', xticklabels=list(c.TARGET_MAPPING.keys()), yticklabels=list(c.TARGET_MAPPING.keys()))
    plt.xlabel('Predicted', fontsize=12)
    plt.ylabel('Actual', fontsize=12)
    plt.title('Confusion Matrix',fontsize=16)
    plt.show()
    

def interpret_decision_tree(clf):
  """ This function uses to interpret decision tree classifier. """

  print(f"Depth of tree: {clf.get_depth()}")

  plt.figure()
  plot_tree(clf, filled=True)
  plt.title("Decision tree trained on all the iris features")
  plt.show()