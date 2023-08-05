# DBFE: Distribution-Based Feature Extractor
![Python 3](https://img.shields.io/badge/python-3-blue.svg)
![License](https://img.shields.io/badge/license-BSD-blue.svg)
[![Discuss](https://img.shields.io/badge/discuss-github-blue.svg)](https://github.com/MNMdiagnostics/dbfe/discussions)

DBFE is a Python library with feature extraction methods that facilitate classifier learning from distributions of genomic variants. 

## Installing dbfe

To install dbfe, just execute:

```bash
pip install dbfe
```

## Quickstart

```python
import pandas as pd

from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

import dbfe

# sample data
stat_vals = pd.read_csv(f"../experiments/data/ovarian/ovarian_cnv.csv.gz", index_col='SAMPLEID')
stat_vals = stat_vals.loc[stat_vals.SVCLASS == "DEL", :]
stat_vals = stat_vals.groupby(stat_vals.index)['LEN'].apply(list).to_frame()

labels = pd.read_csv(f"../experiments/data/ovarian/labels.tsv", sep='\t', index_col=0)
labels = (labels == "RES") * 1
stat_df = stat_vals.join(labels.CLASS_LABEL, how='inner')

# splitting into training and testing data
X = stat_df.loc[:, "LEN"]
y = stat_df.loc[:, "CLASS_LABEL"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=23, stratify=y)

# DBFE in a classification pipeline
extractor = dbfe.DistributionBasedFeatureExtractor(breakpoint_type='supervised', n_bins='auto', cv=10)
pipe = make_pipeline(extractor, StandardScaler(), LogisticRegression())
pipe.fit(X_train, y_train)

extractor.plot_data_with_breaks(X_train, y_train, plot_type='kde')
y_prob = pipe.predict_proba(X_test)
print("AUC on test data: {:.3}".format(roc_auc_score(y_test, y_prob[:, 1])))
```

![](./examples/img/dbfe_plot.svg)


## License

- This project is released under a permissive new BSD open source license ([LICENSE-BSD3.txt](https://github.com/MNMdiagnostics/dbfe/blob/master/LICENSE-BSD3.txt)) and commercially usable. There is no warranty; not even for merchantability or fitness for a particular purpose.
- In addition, you may use, copy, modify and redistribute all artistic creative works (figures and images) included in this distribution under the directory
according to the terms and conditions of the Creative Commons Attribution 4.0 International License.  See the file [LICENSE-CC-BY.txt](https://github.com/MNMdiagnostics/dbfe/blob/master/LICENSE-CC-BY.txt) for details. (Computer-generated graphics such as the plots produced by seaborn/matplotlib fall under the BSD license mentioned above).

## Citing

If you use dbfe as part of your workflow in a scientific publication, please consider citing the associated paper:

- Piernik, M. *et al.* (2022) DBFE: Distribution-based feature extraction from copy number and structural variants in whole-genome data.
