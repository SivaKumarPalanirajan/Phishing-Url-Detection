# Phishing Url Detection Using RandomForest Classifier, DVC, MLflow, Docker, Redis Queues and Streamlit

A project which uses a url to build the required features and identifies whether it is Phishing or not.

Redis Queues Integration is also available along with the Streamlit app.

The Producer/Consumer and Worker Scripts are present inside the RedisComponents. 

# Dataset & Attribution
This project uses the URL-Phish dataset. The dataset was obtained from Kaggle, where it is available as [Phishing URL Detection (111K URLs, 22 Features)](https://www.kaggle.com/datasets/sahandnamvar/phishing-url-detection-111k-urls-22-features).

The dataset is licensed under **[Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/)**, 
which permits sharing, redistribution, and adaptation with appropriate credit.

**Dataset citation**<br>
>Dam Minh, Linh; Tran Cong, Hung (2025).<br>
>URL-Phish: A Feature-Engineered Dataset for Phishing Detection.<br>
>Mendeley Data, V1.<br>
>DOI: https://doi.org/10.17632/65z9twcx3r.1<br>

**Original data sources referenced by the dataset authors**<br>
>PhishTank – Community-driven phishing URL repository<br>
>Research Organization Registry (ROR) dataset – Source of trusted benign domain URLs<br>

**Paper citation**<br>
>Dam Minh Linh, Tran Cong Hung, <br>
>A feature-engineered dataset of benign and phishing URLs for machine learning and large language models evaluation,<br>
>Data in Brief,<br>
>Volume 63,<br>
>2025,<br>
>112162,<br>
>ISSN 2352-3409,<br>
>https://doi.org/10.1016/j.dib.2025.112162.

**Modifications:** <br>
The following preprocessing was applied to the original dataset:
- Duplicate rows and null/missing values were checked for and removed, if present
- Feature scaling applied to selected numeric features
- TF-IDF encoding applied to selected URL/text-derived feature(s)
- Data split into train / validation / test sets

**Feature usage:** <br>
The final model was trained using a selected subset 
of the features; the remaining 
features were excluded at training time via feature selection, not by removing them from 
the stored datasets.

# License
- **Code**: MIT License — see `LICENSE`
- **Data**: Raw and processed datasets are redistributed under **Creative Commons Attribution 4.0 International (CC BY 4.0) license**, consistent with the original dataset's license (see Dataset & Attribution above).
- **Model & preprocessors**: MIT License — trained artifacts are provided under the same 
  terms as the codebase. Model trained on **Creative Commons Attribution 4.0 International (CC BY 4.0) license** data; see Dataset & Attribution section for details.