import pandas as pd
import subprocess
import os
from shutil import copyfile
import re
from datetime import datetime

import seaborn as sns
import numpy as np
import itertools
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
from sklearn.metrics import precision_score, recall_score, accuracy_score

from datetime import datetime
from sklearn.preprocessing import LabelEncoder
from sklearn.manifold import TSNE


from sklearn import linear_model
from sklearn import metrics


# from sklearn.model_selection import GridSearchCV
# from sklearn.svm import LinearSVC
# from sklearn.svm import SVC
# from sklearn.tree import DecisionTreeClassifier
# from sklearn.ensemble import RandomForestClassifier
# from sklearn.ensemble import GradientBoostingClassifier
# from sklearn.model_selection import train_test_split




def get_exp_stage(time, dpps=4, baseline=2, absorb=4, pause=1, desorb=5, flush=18):
    
    # dpps: data point per second

    baseline_time = baseline*dpps
    if time <= baseline_time:
        return 'baseline'
    absorb_time = baseline_time + absorb*dpps
    if time <= absorb_time:
        return 'absorb'
    pause_time = absorb_time + pause*dpps
    if time <= pause_time:
        return 'pause'
    desorb_time = pause_time + desorb*dpps
    if time <= desorb_time:
        return 'desorb'
    flush_time = desorb_time + flush*dpps
    if time <= flush_time:
        return 'flush'
    wait_time = flush_time + flush*dpps
    if time <= wait_time:
        return 'wait'
    
    




def rename_columns(df, has_label=False):
    for col in df.columns:
        if 'Sen' in col:
        # print(col[4:])
            new_col = re.findall('\d+', col)[0]
            # print(new_col)
            df.rename(columns={col:new_col}, inplace=True)
    df.rename(columns={'Data Points': 'data_points'}, inplace=True)
    df.rename(columns={'Humidity (%r.h.)':'humidity'}, inplace=True)
    if has_label:
        df['exp_type'] = df['exp_type'].apply(lambda x: 'Covid' if x == 'COVID' else x)
    return df



def preprocess_data(files, has_label=False, root_dir='./Raw_Data', control_dir='./Control', covid_dir='./Covid'):
    li = []
#     li1 = []
    x = 0
    for f in files:
        if f.endswith(".txt"):
            filename = os.path.join(root_dir, f)
            # exp = !grep "Name of the experiment" "$filename"
            

            exp = subprocess.run(['grep', 'Name of the experiment', filename],
                        check=True, text=True, capture_output=True).stdout

            time = subprocess.run(['grep', '-m', '1', 'Time', filename],
                    check=True, text=True, capture_output=True).stdout

            date = subprocess.run(['grep', '-m', '1', 'Date', filename],
                    check=True, text=True, capture_output=True).stdout

            # time = !grep -m 1 "Time" "$filename"
            # date = !grep -m 1 "Date" "$filename"
        
            
            temp_string = subprocess.run(['awk', 'NR>=39', filename],
                        check=True, text=True, capture_output=True).stdout

            temp_file = open(r'./temp.txt', 'w')
            temp_file.write(temp_string)
            temp_file.close()


            
            
            df = pd.read_csv("temp.txt", sep="\t")
            df['exp_stage'] = df['Data Points'].apply(get_exp_stage)
            
            df['series_id'] = x 
            x += 1

            if has_label:
                exp = subprocess.run(['grep', 'Name of the experiment', filename],
                        check=True, text=True, capture_output=True).stdout

                cult_time, repeat_num, exp_type = exp.split('=')[1].strip().replace('"','').split()
                if exp_type == "COVID":
                    copyfile(filename, os.path.join(covid_dir, f))
                if exp_type == "Control":
                    copyfile(filename, os.path.join(control_dir, f))

                _, _, df['exp_type'] = cult_time, repeat_num, exp_type


            
            df['date'] = date.split('=')[1].strip()
            d = date.split('/n')[0].split('=')[1].strip()
            # print(date)
            # print(d)
            # print(time.split('/n')[0].split('=')[1])

            df['time_start'] = time.split('=')[1].strip()
            df['time_elapsed'] = df.index / 4

            # print(time)
            df['exp_name'] = f

            df['timestamp'] = pd.to_datetime(d + " " + df['time_start'])
           
            df['time'] = pd.to_datetime(d + " " + df['time_start']) + pd.to_timedelta(df['time_elapsed'], unit='s')

            # for i, data in df.groupby('exp_stage'):
                

                # if data['exp_stage'].str.contains('baseline').all():
                #     stage_data_points = data['exp_stage'].str.contains('baseline')
                #     if len(stage_data_points) > 8:
                #         n = len(stage_data_points) - 8
                #         data.drop(data.tail(n).index, inplace=True)
                #         li1.append(data)

                # if data['exp_stage'].str.contains('absorb').all():
                #     stage_data_points = data['exp_stage'].str.contains('absorb')
                #     if len(stage_data_points) > 16:
                #         n = len(stage_data_points) - 16
                #         data.drop(data.tail(n).index, inplace=True)
                #         li1.append(data)

                # if data['exp_stage'].str.contains('pause').all():
                #     stage_data_points = data['exp_stage'].str.contains('pause')
                #     if len(stage_data_points) > 4:
                #         n = len(stage_data_points) - 4
                #         data.drop(data.tail(n).index, inplace=True)
                #         li1.append(data)
                        
                # if data['exp_stage'].str.contains('desorb').all():
                #     stage_data_points = data['exp_stage'].str.contains('desorb')
                #     if len(stage_data_points) > 20:
                #         n = len(stage_data_points) - 20
                #         data.drop(data.tail(n).index, inplace=True)
                #         li1.append(data)

                # if data['exp_stage'].str.contains('flush').all():
                #     stage_data_points = data['exp_stage'].str.contains('flush')
                #     if len(stage_data_points) > 72:
                #         n = len(stage_data_points) - 72
                #         data.drop(data.tail(n).index, inplace=True)
                #         li1.append(data)

                # if data['exp_stage'].str.contains('wait').all():
                #     stage_data_points = data['exp_stage'].str.contains('wait')
                #     if len(stage_data_points) > 20:
                #         n = len(stage_data_points) - 20
                #         data.drop(data.tail(n).index, inplace=True)
                #         li1.append(data)
                
            
            li.append(df)


    frame = pd.concat(li, axis=0, ignore_index=True)
    frame  = rename_columns(frame, has_label)
    frame = frame.set_index('time')

    # frame1 = pd.concat(li1, axis=0, ignore_index=True)
    # frame1  = rename_columns(frame1, has_label)
    # frame1 = frame1.set_index('time')

    os.remove('temp.txt')
    return frame


# def perform_tsne(X_data, y_data, perplexities, markers, n_iter=1000):
    
#     for index, perplexity in enumerate(perplexities):
#         # perform t-sne
#         print("\nPerforming tsne with perplexity {} and with {} iterations at max".format(perplexity, n_iter))
#         X_reduced = TSNE(verbose=2, perplexity=perplexity).fit_transform(X_data)
#         print('Done..')
        
#         # prepare data for seaborn
#         print("Creating plot for this t-sne visualization")
#         df = pd.DataFrame({'x':X_reduced[:,0], 'y':X_reduced[:,1], 'label':y_data})
        
#         # draw the plot in appropriate palce in the grid
#         sns.lmplot(data=df, x='x', y='y', hue='label', fit_reg=False, height=8, palette="Set1",markers=markers)
#         plt.title("perplexity : {} and max_iter: {}".format(perplexity, n_iter))
#         plt.show()
#         print("Done")
#     return X_reduced





# def plot_confusion_matrix(cm, classes,
#                         normalize=False,
#                         title='Confusion matrix',
#                         cmap=plt.cm.Blues):
#     if normalize:
#         cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]

#     plt.imshow(cm, interpolation='nearest', cmap=cmap)
#     plt.title(title)
#     plt.colorbar()
#     tick_marks = np.arange(len(classes))
#     plt.xticks(tick_marks, classes, rotation=90)
#     plt.yticks(tick_marks, classes)

#     fmt = '.2f' if normalize else 'd'
#     thresh = cm.max() / 2.
#     for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
#         plt.text(j, i, format(cm[i, j], fmt),
#                 horizontalalignment="center",
#                 color="white" if cm[i, j] > thresh else "black")

#     plt.tight_layout()
#     plt.ylabel('True label')
#     plt.xlabel('Predicted label')



def model_run(model, X_train, y_train, X_test, y_test, class_labels, cm_normalize='all', \
                 print_cm=True, cm_cmap=plt.cm.Blues):
    
    
    # to store results at various phases
    results = dict()
    
    # time at which model starts training 
    train_start_time = datetime.now()
    print('training the model..')
    model.fit(X_train, y_train)
    print('Done....!\n')
    train_end_time = datetime.now()
    results['training_time'] =  train_end_time - train_start_time
    print('==> training time:- {}\n'.format(results['training_time']))
    
    
    # predict test data
    print('Predicting test data')
    test_start_time = datetime.now()
    y_pred = model.predict(X_test)
    test_end_time = datetime.now()
    print('Done....!\n')
    results['testing_time'] = test_end_time - test_start_time
    print('==> testing time:- {}\n'.format(results['testing_time']))
    results['predicted'] = y_pred
   

    # calculate overall accuracy, precision and recall of the model
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)



    # store accuracy, precision and recall in results
    results['accuracy'] = accuracy
    results['precision'] = precision
    results['recall'] = recall

    print('==> Accuracy:- {}\n'.format(accuracy))
    print('==> Recall:- {}\n'.format(recall))
    print('==> Precision:- {}\n'.format(precision))


   
    
    
    # # confusion matrix
    cm = metrics.confusion_matrix(y_test, y_pred, normalize='all')
    # results['confusion_matrix'] = cm
    # if print_cm: 
    #     print('\n ********Confusion Matrix********')
    #     print('\n {}'.format(cm))
        
    # # plot confusin matrix
    # plt.figure(figsize=(6,6))
    # plt.grid(b=False)
    # plot_confusion_matrix(cm, classes=class_labels, normalize='all', title='Normalized confusion matrix', cmap = cm_cmap)
    # plt.show()





    ax= plt.subplot()
    sns.heatmap(cm, annot=True, fmt='.3g', ax=ax);  #annot=True to annotate cells, ftm='g' to disable scientific notation

    # labels, title and ticks
    ax.set_xlabel('Predicted labels');ax.set_ylabel('True labels'); 
    ax.set_title('Confusion Matrix'); 
    ax.xaxis.set_ticklabels(['Covid', 'Control']); ax.yaxis.set_ticklabels(['Covid', 'Control']);
    

    # target_names = ['Covid', 'Control']



    # cmn = cm.astype('float') / cm.sum(axis=1)#[:, np.newaxis]
    # fig, ax = plt.subplots(figsize=(10,10))
    # sns.heatmap(cmn, annot=True, fmt='.2f', xticklabels=target_names, yticklabels=target_names)
    # plt.ylabel('Actual')
    # plt.xlabel('Predicted')
    # plt.show(block=False)



    # get classification report
    print('****************| Classifiction Report |****************')
    classification_report = metrics.classification_report(y_test, y_pred)
   
    # store report in results
    results['classification_report'] = classification_report
    print(classification_report)
    
    # add the trained  model to the results
    results['model'] = model
    
    return results
    






def print_grid_search_attributes(model):
    # Estimator that gave highest score among all the estimators formed in GridSearch
    print('\n\n==> Best Estimator:')
    print('\t{}\n'.format(model.best_estimator_))


    # parameters that gave best results while performing grid search
    print('\n==> Best parameters:')
    print('\tParameters of best estimator : {}'.format(model.best_params_))


    #  number of cross validation splits
    print('\n==> No. of CrossValidation sets:')
    print('\tTotal numbre of cross validation sets: {}'.format(model.n_splits_))


    # Average cross validated score of the best estimator, from the Grid Search 
    print('\n==> Best Score:')
    print('\tAverage Cross Validate scores of best estimator : {}'.format(model.best_score_))



def plot_algorithm_performance(names, results, metrics, savefig=False, ylim=False):
# boxplot algorithm comparison
    fig = plt.figure(figsize=(16,6))
    fig.suptitle('Comparison of algorithm performance')
    ax = fig.add_subplot(111)
    plt.boxplot(results)
    ax.set_xticklabels(names)
    plt.ylabel(metrics)
    plt.xlabel('models')

    if savefig:
        fig.savefig(f'{metrics}.jpeg', transparent = False)
    
    if ylim:
        plt.ylim([0,1])
        
    plt.show()



def run_models_cv(models, X_train, y_train, scoring='accuracy'):
    results = []
    names = []

    if scoring == 'specificity':
        scoring = make_scorer(recall_score, pos_label=0)
    else:
        for name, model in models:
            kfold = model_selection.KFold(n_splits=10, random_state=seed, shuffle=True)
            cv_results = model_selection.cross_val_score(model, X_train, y_train, cv=kfold, scoring=scoring)
            results.append(cv_results)
            names.append(name)



def plot_sensor_signals(df, sensors_signals_col, target_col_name):
        
    facetgrid = sns.FacetGrid(df, hue=target_col_name, height=5,aspect=3)
    facetgrid.map(sns.distplot, sensors_signals_col, hist=False).add_legend()


def signals_plot_by_target(df, target_col_name, labels):
    fig, axes = plt.subplots(nrows=24,ncols=2, figsize=(20,36))
    df[df[target_col_name]==labels[0]].iloc[:, 1:25].plot(ax=axes[:,0], subplots=True, sharex=True, figsize=(10,25))

    df[df[target_col_name]==labels[1]].iloc[:, 1:25].plot(ax=axes[:,1], subplots=True, sharex=True, figsize=(10,25));

    # plt.legend()

    axes[0][0].set_title(labels[0])
    axes[0][1].set_title(labels[1])

    plt.show();




def plot_by_exp_stage():
    fig, axes = plt.subplots(nrows=24,ncols=5, figsize=(20,36))
    df[df['exp_stage']=='baseline'].iloc[:, 1:25].plot(ax=axes[:,0], subplots=True, sharex=True, figsize=(10,25))

    df[df['exp_stage']=='absorb'].iloc[:, 1:25].plot(ax=axes[:,1], subplots=True, sharex=True, figsize=(10,25));
    df[df['exp_stage']=='pause'].iloc[:, 1:25].plot(ax=axes[:,2], subplots=True, sharex=True, figsize=(10,25));
    df[df['exp_stage']=='desorb'].iloc[:, 1:25].plot(ax=axes[:,3], subplots=True, sharex=True, figsize=(10,25));
    df[df['exp_stage']=='flush'].iloc[:, 1:25].plot(ax=axes[:,4], subplots=True, sharex=True, figsize=(10,25));

    # plt.legend()

    axes[0][0].set_title('baseline')
    axes[0][1].set_title('absorb')
    axes[0][2].set_title('pause')
    axes[0][3].set_title('desorb')
    axes[0][4].set_title('flush')





def plot_new_sample(model, x_train, x):
    fig, ax = plt.subplots()
    x = x.reshape(1,-1)
    ax.scatter(x_train[:,0], x_train[:,1], c=l)
    ax.scatter(x[:,0], x[:,1])