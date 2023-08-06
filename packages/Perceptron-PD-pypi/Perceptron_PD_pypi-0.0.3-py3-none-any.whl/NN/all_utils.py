import os
import joblib
from matplotlib.colors import ListedColormap
import numpy as np
import matplotlib.pyplot as plt

def prepare_data(df):
    """This function accepts a dataframe and returns the X and y values
    Args:
        df (pd.DataFrame): Pandas dataframe containing the data
    Returns:
        Tuple: It returns a tuple containing the X and y values
    """
    X = df.drop("y", axis =1)
    y = df["y"]
    return X, y

def save_model(model, filename):
    """This function accepts a model and saves it to a file
    Args:
        model (Python Object): A trained model
        filename (str): It is the name of the file 
    """

    model_dir = "models"
    os.makedirs(model_dir , exist_ok = True)
    filePath = os.path.join(model_dir, filename)
    joblib.dump(model, filePath)

def save_plot(df, file_name , model):
    def _create_base_plot(df):
        df.plot(kind = 'scatter' , x = "x1" , y = "x2" , c = "y" , s =100 , cmap = "winter" )
        plt.axhline(y = 0 , color = 'black' , linestyle = "--" , linewidth = 1)
        plt.axvline(x = 0 , color = 'black' , linestyle = "--" , linewidth = 1)
        figure = plt.gcf()
        figure.set_size_inches(10,8)
        
        
    def _plot_decision_regions(X, y , classifier, resolution =0.2):
        colors = ("cyan", "lightgreen")
        cmap = ListedColormap(colors)
        
        X = X.values # as an array
        x1 = X[:, 0]
        x2 = X[:, 1]
        
        x1_min, x1_max = x1.min() - 1, x1.max() + 1 
        x2_min, x2_max = x2.min() - 1, x2.max() + 1
        
        xx1, xx2 = np.meshgrid(np.arange(x1_min, x1_max, resolution),
                               np.arange(x2_min, x2_max, resolution)
                              )
        y_hat = classifier.predict(np.array([xx1.ravel(), xx2.ravel()]).T)
        y_hat = y_hat.reshape(xx1.shape)
        
        plt.contourf(xx1, xx2, y_hat, alpha=0.3, cmap=cmap)
        plt.xlim(xx1.min(), xx1.max())
        plt.ylim(xx2.min(), xx2.max())
        
        plt.plot()    

    X, y = prepare_data(df)
    _create_base_plot(df)
    _plot_decision_regions(X, y, model)
    
    
    plot_dir = "plots"    
    os.makedirs(plot_dir , exist_ok = True)
    plotPath = os.path.join(plot_dir, file_name)
    plt.savefig(plotPath)    