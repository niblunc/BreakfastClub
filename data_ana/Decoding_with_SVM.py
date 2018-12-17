
# coding: utf-8

# # Decoding with the ANOVA + SVM: fed vs. fasted in the Breakfast Club data  
# 
#       
# Here we are decoding the Breakfast Club dataset following example code outlined in the nilearn pacakge. We are using a feature selection (ANOVA), followed by an SVM, using nested cross-validation.  
#   
# 

# Import packages:

# In[ ]:


import os
import numpy as np
import nilearn
import glob
#import matplotlib
import nibabel as nib
import pandas as pd 
from nilearn.input_data import NiftiMasker 
import numpy as np
np.seterr(divide='ignore', invalid='ignore')
import warnings
warnings.filterwarnings("ignore")
import matplotlib
matplotlib.use('Agg')


# # I . Nilearn Mask  
# #### Here we decode using a nilearn generated ROI mask.  
#   
# 
# #### First step is to load our relevant data:

# In[ ]:



# Behavioral csv file 
stim = '/projects/niblab/bids_projects/Experiments/BreakfastClub/bf_behavioral.csv'
# Dataset nifti image 
dataset='/projects/niblab/bids_projects/Experiments/BreakfastClub/images/bfclub_all.nii.gz'

# Load behavioral data into a pandas df
behavioral = pd.read_csv(stim, sep="\t")
#grab conditional labels 
y = behavioral["labels"]

# Here we look at our data variables to confirm we have the data loaded correctly
#print(y.unique())

# Restrict data to our target analysis variables and make a condition mask for analysis
condition_mask = y.isin(['fasted', 'fed'])
y = y[condition_mask]

# Confirm we have the unique conditions wanted 
print(conditions.unique())


# ### Prepare data now with NiftiMasker

# In[ ]:


masker = NiftiMasker(standardize=True, memory="nilearn_cache", memory_level=2)
X = masker.fit_transform(dataset)
# Apply our condition_mask
X = X[condition_mask]


# ### Build the decoder:  
# Here we are setting the prediction function used. Here we are using a Support Vector Classification, with a linear kernel. The dimension reduction technique used is ANOVA, *' a classical univariate feature selection based on the F-test.'* We set the number of features to be selected to 500. 

# In[ ]:



from sklearn.svm import SVC
svc = SVC(kernel='linear')

from sklearn.feature_selection import SelectKBest, f_classif
feature_selection = SelectKBest(f_classif, k=500)

# We have our classifier (SVC), our feature selection (SelectKBest), and now,
# we can plug them together in a *pipeline* that performs the two operations
# successively:
from sklearn.pipeline import Pipeline
anova_svc = Pipeline([('anova', feature_selection), ('svc', svc)])


# ### Fit the decoder and predict

# In[ ]:


anova_svc.fit(X, conditions)
y_pred = anova_svc.predict(X)


# ### Nested cross-validation  
# Here we are using Nested Cross Validation, tuning the parameters 'k'.

# In[ ]:



k_range = [10, 15, 30, 50, 150, 300, 500, 1000, 1500, 3000, 5000]
    
# Here we run gridsearch
from sklearn.model_selection import GridSearchCV
# We are going to tune the parameter 'k' of the step called 'anova' in
# the pipeline. Thus we need to address it as 'anova__k'.

# Note that GridSearchCV takes an n_jobs argument that can make it go
# much faster'
grid = GridSearchCV(anova_svc, param_grid={'anova__k': k_range}, verbose=1, n_jobs=4, cv=3)
nested_cv_scores = cross_val_score(grid, X, conditions, cv=3)

print("Nested CV score: %.4f" % np.mean(nested_cv_scores))


#     Fitting 3 folds for each of 11 candidates, totalling 33 fits  
#     [Parallel(n_jobs=4)]: Using backend SequentialBackend with 1 concurrent workers.  
#     [Parallel(n_jobs=4)]: Done  33 out of  33 | elapsed:  2.1min finished
#     Fitting 3 folds for each of 11 candidates, totalling 33 fits  
#     [Parallel(n_jobs=4)]: Using backend SequentialBackend with 1 concurrent workers.  
#     [Parallel(n_jobs=4)]: Done  33 out of  33 | elapsed:  2.1min finished
#     Fitting 3 folds for each of 11 candidates, totalling 33 fits  
#     [Parallel(n_jobs=4)]: Using backend SequentialBackend with 1 concurrent workers.  
#     [Parallel(n_jobs=4)]: Done  33 out of  33 | elapsed:  2.1min finished  
#     Nested CV score: 0.5249  
# 

# ### Visualize and save the results  
# Look at the SVC's discriminating weights, and save the plot as a *.png* image and save the results to nifti image

# In[ ]:



# Here is the image 
coef = svc.coef_
# reverse feature selection
coef = feature_selection.inverse_transform(coef)
# reverse masking
weight_img = masker.inverse_transform(coef)


# Use the mean image as a background to avoid relying on anatomical data
from nilearn import image
mean_img = image.mean_img(dataset)
mean_img.to_filename('/projects/niblab/bids_projects/Experiments/BreakfastClub/derivatives/images/bfclub_mean_nimask.nii')

# Create the figure
from nilearn.plotting import plot_stat_map, show
display = plot_stat_map(weight_img, mean_img, title='SVM weights')
display.savefig('/projects/niblab/bids_projects/Experiments/BreakfastClub/derivatives/images/bfclub_nestCV_nimask.png')
# Saving the results as a Nifti file may also be important
weight_img.to_filename('/projects/niblab/bids_projects/Experiments/BreakfastClub/derivatives/images/bfclub_nestCV_nimask.nii')


# <img src="bfclub_nestCV_nimask.png" alt="nimask">

# # II. Power ROI mask
# ## Prepare NiftiMasker now with the power ROI mask 

# In[ ]:


#image mask
imag_mask='/projects/niblab/bids_projects/Experiments/ChocoData/images/power_roimask_4bi.nii.gz'

masker = NiftiMasker(mask_img=imag_mask, standardize=True, memory="nilearn_cache", memory_level=2)

X = masker.fit_transform(dataset)
# Apply our condition_mask
X = X[condition_mask]


# ### Fit the decoder and predict

# In[ ]:


anova_svc.fit(X, conditions)
y_pred = anova_svc.predict(X)


# ### Nested cross-validation  

# In[ ]:


# Here we run gridsearch
from sklearn.model_selection import GridSearchCV
# We are going to tune the parameter 'k' of the step called 'anova' in
# the pipeline. Thus we need to address it as 'anova__k'.

# Note that GridSearchCV takes an n_jobs argument that can make it go
# much faster'
grid = GridSearchCV(anova_svc, param_grid={'anova__k': k_range}, verbose=1, n_jobs=4, cv=3)
nested_cv_scores = cross_val_score(grid, X, conditions, cv=3)

print("Nested CV score: %.4f" % np.mean(nested_cv_scores))


#     Fitting 3 folds for each of 11 candidates, totalling 33 fits  
#     [Parallel(n_jobs=4)]: Using backend SequentialBackend with 1 concurrent workers.  
#     [Parallel(n_jobs=4)]: Done  33 out of  33 | elapsed:   36.7s finished  
#     Fitting 3 folds for each of 11 candidates, totalling 33 fits  
#     [Parallel(n_jobs=4)]: Using backend SequentialBackend with 1 concurrent workers.  
#     [Parallel(n_jobs=4)]: Done  33 out of  33 | elapsed:   37.7s finished  
#     Fitting 3 folds for each of 11 candidates, totalling 33 fits  
#     [Parallel(n_jobs=4)]: Using backend SequentialBackend with 1 concurrent workers.  
#     [Parallel(n_jobs=4)]: Done  33 out of  33 | elapsed:   42.1s finished  
#     Nested CV score: 0.5350  

# ### Visualize & save the results  
# Look at the SVC's discriminating weights, and save the plot as a *.png* image and save the results to nifti image

# In[ ]:



# Here is the image 
coef = svc.coef_
# reverse feature selection
coef = feature_selection.inverse_transform(coef)
# reverse masking
weight_img = masker.inverse_transform(coef)


# Use the mean image as a background to avoid relying on anatomical data
from nilearn import image
mean_img = image.mean_img(dataset)
mean_img.to_filename('/projects/niblab/bids_projects/Experiments/BreakfastClub/derivatives/images/bfclub_mean_powermask.nii')

# Create the figure
from nilearn.plotting import plot_stat_map, show
display = plot_stat_map(weight_img, mean_img, title='SVM weights')
display.savefig('/projects/niblab/bids_projects/Experiments/BreakfastClub/derivatives/images/bfclub_nestCV_powermask.png')
# Saving the results as a Nifti file may also be important
weight_img.to_filename('/projects/niblab/bids_projects/Experiments/BreakfastClub/derivatives/images/bfclub_nestCV_powermask.nii')


# <img src="bfclub_nestCV_powermask.png">
