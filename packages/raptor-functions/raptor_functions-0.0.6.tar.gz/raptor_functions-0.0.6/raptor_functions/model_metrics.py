import pandas as pd
from sklearn.metrics import plot_confusion_matrix
from sklearn.metrics import accuracy_score, precision_score, recall_score, roc_curve, auc, \
        plot_precision_recall_curve
import matplotlib.pyplot as plt
import pandas as pd
import shap
import random

cmap = plt.cm.Blues

def confusion_matrix_plot(model,X_test,X_train, y_train, y_test):
  # 
  y_pred = model.predict(X_test)
  print("Accuracy: %.2f%%" % (accuracy_score(y_test, y_pred) * 100))
  print("Recall: %.2f%%" % (recall_score(y_test, y_pred, average="binary", pos_label=1) * 100.0))
  print("Precision: %.2f%%" % (precision_score(y_test, y_pred, average="binary", pos_label=1) * 100.0))

  plot_confusion_matrix(model, X_test, y_test,
                            display_labels=['Covid', 'Non-Covid'], cmap=cmap)
  plt.savefig('confusion_matrix.eps')

  fea_imp = pd.DataFrame({'imp': model.feature_importances_, 'col': X_train.columns})
  fea_imp = fea_imp.sort_values(['imp', 'col'], ascending=[True, False]).iloc[-30:]
  fea_imp.plot(kind='barh', x='col', y='imp', figsize=(10, 7), legend=None)
  plt.title('XGBoost - Feature Importance')
  plt.ylabel('Features')
  plt.xlabel('Importance')
  plt.savefig('feature_importance.eps')

  disp = plot_precision_recall_curve(model, X_test, y_test)
  disp.ax_.set_title('Binary class Precision-Recall curve')
  plt.savefig('precision_recall_curve.eps')

def model_explanation(model,X,X_test):
  # 
  explainer = shap.TreeExplainer(model)
  shap_values = explainer.shap_values(X_test) 
  # shap.initjs()
  # 
  # Summary plot
  shap.summary_plot(shap_values, X_test)
  # 
  for name in X.columns:
    shap.dependence_plot(name, shap_values, X_test, display_features = X)


def random_prediction(X_test,y_test,model):
  explainer = shap.TreeExplainer(model)
  shap_values = explainer(X_test)
  i = random.randint(0, len(X_test))
  shap.plots.waterfall(shap_values[i])
  print('Category: ' + str(y_test.values[i][0]))
  print('Prediction: ' + str(model.predict(X_test.iloc[[i]])[0]))
  print('Prediction Probability: ' + str(model.predict_proba(X_test.iloc[[i]])[0]))







