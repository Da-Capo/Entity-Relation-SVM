# Requirement
anaconda
jieba
scikit-learn

# Run
 step1 move the `\Chinese` folder in ace2005 data to the this folder 

step2 extract the feature `feature.pkl`
```bash
python feature_extract
```
step3 train the svm_model and test it 
```bash
python svm_model.py
```