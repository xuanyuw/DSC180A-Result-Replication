""" This file contains the model used in the project."""

# import packages here

def train(data, train_pct, out_path=None, **kwargs):
    """
    train the model. and output the model if out_path is not None
    """
    X_train, y_train, X_test, y_test = ...  #split data using train_pct
    mdl = ...  
    
    if out_path is not None:
        mdl.save(out_path)

    return mdl