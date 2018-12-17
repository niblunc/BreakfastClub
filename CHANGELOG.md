# Changelog
All notable changes to this project will be documented in this file.  
  
  
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Changed
  
  
## [0.0.1] - 2018-11-06  
### Added  
- Complete BIDS data for all sessions(1,2), subjects (1-21, minus subject 7,total 20 subjects), task-resting
- Complete fmriprep data for all sessions(1,2), task-resting
- Completed skull stripped functionals for each session, using fsl "bet" command  
- Smoothed functionals for each session, using nilearn 
- Motion correction and confound text files assessed using fsl command 
- Decoding with SVM + ANOVA and nested CV with nilearn  
- Nifti images derived from decoding, currently 2 available using 1) nilearn generated ROI mask, 2) given power ROI mask

