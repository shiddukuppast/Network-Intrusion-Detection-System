import os   
import joblib
import logging
import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import make_pipeline,Pipeline
from sklearn.preprocessing import StandardScaler,OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.metrics import confusion_matrix,classification_report,roc_auc_score,roc_curve,precision_recall_curve, average_precision_score, accuracy_score
from sklearn.tree import DecisionTreeClassifier
columns = [
'duration',
'protocol_type',
'service',
'flag',
'src_bytes',
'dst_bytes',
'land',
'wrong_fragment',
'urgent',
'hot',
'num_failed_logins',
'logged_in',
'num_compromised',
'root_shell',
'su_attempted',
'num_root',
'num_file_creations',
'num_shells',
'num_access_files',
'num_outbound_cmds',
'is_host_login',
'is_guest_login',
'count',
'srv_count',
'serror_rate',
'srv_serror_rate',
'rerror_rate',
'srv_rerror_rate',
'same_srv_rate',
'diff_srv_rate',
'srv_diff_host_rate',
'dst_host_count',
'dst_host_srv_count',
'dst_host_same_srv_rate',
'dst_host_diff_srv_rate',
'dst_host_same_src_port_rate',
'dst_host_srv_diff_host_rate',
'dst_host_serror_rate',
'dst_host_srv_serror_rate',
'dst_host_rerror_rate',
'dst_host_srv_rerror_rate',
'attack',
'difficulty'
]

Model_File = "model.pkl"
Feature_File = "feature.pkl"

def train_model(x_train,y_train,num_attribute,cat_attribute):
    num_pipeline = Pipeline([
        ('Scaler',StandardScaler())
    ])
    cat_pipeline = Pipeline([
        ('Onehot',OneHotEncoder(handle_unknown='ignore'))
    ])
    full_pipeline = ColumnTransformer([
        ("num",num_pipeline,num_attribute),
        ("cat",cat_pipeline,cat_attribute)
    ])
    dt = make_pipeline(full_pipeline,DecisionTreeClassifier(random_state=42))
    param_grid = {
        "decisiontreeclassifier__max_depth":[10,20,None],
        "decisiontreeclassifier__min_samples_split":[2,5],
        "decisiontreeclassifier__min_samples_leaf":[1,2],
        "decisiontreeclassifier__criterion":["gini","entropy"]
    }
    grid_search = GridSearchCV(
        dt,
        param_grid,
        cv=5,
        n_jobs=-1,
        scoring="recall",
        error_score="raise"
    )
    grid_search.fit(x_train,y_train)
    return grid_search.best_estimator_, grid_search.best_params_

if not os.path.exists(Model_File):
    logging.basicConfig(
        filename="training.log",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )
    logging.info("Training Started")
    df1 = pd.read_csv("Data/train.txt",names=columns)
    df2 = pd.read_csv("Data/test.txt",names=columns)

    df1["attack"] = df1["attack"].apply(lambda x:0 if x=="normal" else 1)
    df2["attack"] = df2["attack"].apply(lambda x:0 if x=="normal" else 1)

    df1.drop("difficulty",axis=1,inplace=True)
    df2.drop("difficulty",axis=1,inplace=True)

    corr = df1.corr(numeric_only = True)
    corr_attack = corr["attack"].sort_values(ascending=False)
    plt.figure(figsize=(10, 12))
    colors = ["red" if x < 0 else "green" for x in corr_attack]
    plt.barh(corr_attack.index, corr_attack.values,color=colors)
    plt.axvline(0, color="black", linewidth=1)
    plt.title("Correlation of Numerical Features with Attack")
    plt.xlabel("Correlation")
    plt.ylabel("Numerical Features")
    plt.grid(axis="x", linestyle="--", alpha=0.6)
    plt.savefig("Graph/Correlation.png",dpi=300, bbox_inches="tight")
    plt.show()

    x_train = df1.drop("attack",axis=1)
    y_train = df1["attack"]
    x_test = df2.drop("attack",axis=1)
    y_test = df2["attack"]
    num_attribute = []
    cat_attribute = []
    for col in x_train.columns :
        if df1[col].dtype == "object":
            cat_attribute.append(col)
        else:
            num_attribute.append(col)

    model,best_param = train_model(x_train,y_train,num_attribute,cat_attribute)
    rf = model.named_steps["decisiontreeclassifier"]
    importance = rf.feature_importances_
    feature_names = model.named_steps["columntransformer"].get_feature_names_out()

    feature_importance = pd.DataFrame({
        "Feature":feature_names,
        "importance":importance
    }).sort_values("importance",ascending=False)
    feature_importance.head(20).plot(kind="barh",x="Feature",y="importance")
    plt.ylabel("Feature")
    plt.xlabel("Importance")
    plt.gca().invert_yaxis()
    plt.title("Top 20 Feature ")
    plt.savefig("Graph/Important_Feature.png", dpi=300, bbox_inches="tight")
    plt.show()

    imp = []
    for i in range(30):
        imp.append(feature_importance["Feature"][i])
    top_num_attribute = []
    top_cat_attribute = []
    names =[]
    for i in imp:
        ch = i.split("__")[1]
        if i.startswith("num__"):
            top_num_attribute.append(ch)
            names.append(ch)
        else:
            if ch[0]=='p' and "protocol_type" not in names:
                top_cat_attribute.append("protocol_type")
                names.append("protocol_type")
            elif ch[0]=='s' and "service" not in names:
                names.append("service")
                top_cat_attribute.append("service")
            elif ch[0]=='f' and "flag" not in names:
                top_cat_attribute.append("flag")
                names.append("flag")

    joblib.dump(names,Feature_File)

    x_top_train = x_train[names]
    y_top_train = y_train
    x_top_test = x_test[names]
    y_top_test = y_test

    model,best_param = train_model(x_top_train,y_top_train,top_num_attribute,top_cat_attribute)
    pred = model.predict(x_top_test)
    print("Best Parameters",best_param)
    print("Accuracy :  ",accuracy_score(y_top_test, pred))
    print("Confusion Matrix : ",confusion_matrix(y_top_test,pred))
    print("Classification Report : ",classification_report(y_top_test,pred))

    joblib.dump(model,Model_File)

    y_prob = model.predict_proba(x_top_test)[:,1]

    fpr, tpr, threshold = roc_curve(y_top_test, y_prob)
    roc_auc = roc_auc_score(y_top_test, y_prob)
    print("ROC-AUC Score:", roc_auc)
    plt.figure(figsize=(8,6))
    plt.plot(fpr, tpr, label=f"ROC Curve (AUC = {roc_auc:.4f})")
    plt.plot([0,1],[0,1],'--', color='gray')
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.title("ROC Curve")
    plt.legend()
    plt.grid(True)
    plt.savefig("Graph/ROC_Curve.png", dpi=300, bbox_inches="tight")
    plt.show()


    precision, recall, _ = precision_recall_curve(y_top_test, y_prob)
    ap = average_precision_score(y_top_test, y_prob)
    plt.figure(figsize=(8,6))
    plt.plot(recall, precision, label=f"AP = {ap:.4f}")
    plt.xlabel("Recall")
    plt.ylabel("Precision")
    plt.title("Precision-Recall Curve")
    plt.grid(True)
    plt.legend()
    plt.savefig("Graph/Precision_Recall.png", dpi=300, bbox_inches="tight")
    plt.show()
    logging.info("Model Trained Successfully")

else:
    model = joblib.load(Model_File)
    feature = joblib.load(Feature_File)
    input_data = pd.read_csv("Input.csv")
    input_data = input_data[feature]
    predict = model.predict(input_data)
    input_data["Attack"] = np.where(
        predict == 1,
        "Attack",
        "Normal"
    )
    input_data.to_csv("Output.csv",index=False)
    print("Result Saved Successfully in Output.csv")