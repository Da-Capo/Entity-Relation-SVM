# Requirements
anaconda    
jieba   
scikit-learn

# Run
 step1 move the `\Chinese`  in [ace2005](https://catalog.ldc.upenn.edu/LDC2006T06) to this folder

step2 extract the feature `feature.pkl`
```bash
python feature_extract
```
step3 train the svm_model and test it 
```bash
python svm_model.py
```