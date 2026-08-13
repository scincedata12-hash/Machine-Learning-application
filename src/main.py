import pandas as pd
import numpy as np
import time
from sklearn.metrics import roc_curve, roc_auc_score,precision_recall_curve,precision_score,recall_score,f1_score
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats
from sklearn.preprocessing import OrdinalEncoder
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import GridSearchCV
import pickle

def time_decorator(function):
    def Wrapeer(self):
        start_time = time.time()
        function(self)
        end_time = time.time()
        print("Total time is", end_time - start_time)
    return Wrapeer

class CREDITSCORECARD:

    def __init__(self):

        print("The Logestic regresssion model")



    @time_decorator
    def data_collection(self):

        self.df = pd.read_csv(r"src/credit_card_scorecard.txt", sep="|", )
        print(self.df.head())

        #df.to_csv("credit_card_scorecard.txt",sep="|")
    @time_decorator
    def Pre_processing(self):

        '''Performing the basic EDA on the data'''
        # checking the rows and column in the data frame

        rows, columns = self.df.shape[0],self.df.shape[1]
        print(f"Total rows and col are {rows} \n {columns}")


        # checking the information about the data
        self.df.info()

        # filling NA values of Age column with mean of the same column
        #self.df["Age"]= self.df["Age"].fillna(self.df["Age"].mean())
        #self.df["Dependents"] = self.df["Dependents"].fillna(self.df["Dependents"].mean())


        df_nan = self.df[self.df.isna().any(axis=1)]
        print(df_nan)
        df_nan.to_csv("Null.csv",index=False)
        # checking the sum of nan value \
        print(df_nan.isna().sum())
        # checking the  column of the data dframe

        print(self.df.columns)

        # checking the stats of the data frame
        print(self.df.describe())


        # categorical column

        cat_df = self.df.select_dtypes(include="str")
        num_df = self.df.select_dtypes(include="number")
        print(f"Total numerical column are \n {num_df} \n and categorical columns are \n {cat_df}")


        # duplicates data
        print(self.df.duplicated().sum())
        '''There is no duplicates value'''


        for col in self.df.select_dtypes(include="number").columns:

            print("******************"*10)
            temp = self.df[col].value_counts(normalize=True,dropna=False)
            print(temp)
            print("############"*10)
            print("Unique count of value \n", self.df[col].unique())

            # distrubution of numerical features

            '''plt.figure(figsize = (6,4))
            sns.histplot(self.df[col],kde=True)
            plt.title(f"{col} distrubution ")
            plt.show()'''

            # checking the outliers using the z-score method


            z_score = np.abs(stats.zscore(self.df[col].dropna()))
            outliers = self.df[col].dropna()[z_score > 3]

            if len(outliers) > 0:
                print(f"outliers {col} is {outliers} and {len(outliers)}")


            # checking the outliers using teh IQR method

            q1 = self.df[col].dropna().quantile(0.25)

            q3 = self.df[col].dropna().quantile(0.75)

            iqr = q3 - q1

            upper_tail =  q3+1.5*iqr
            print(upper_tail)
            lower_tail = q1 - 1.5*iqr
            print(lower_tail)

            outliers   = self.df[(self.df[col]>upper_tail) | (self.df[col]<lower_tail)]


            if len(outliers) > 0:
                print(f"outliers in {col} is \n {outliers[col]} and {len(outliers)}")


        #box plot for detecting outliers

        for col in num_df.columns:
            pass
            #plt.figure(figsize=(6,4))
            #sns.boxplot(x= num_df[col])
            #plt.title(f"outliers : {col}")
            #plt.show()

        # sharpi test to check if data is normally distrubted or not


        print(self.df.nunique())

        # Feature Engineering steps

        '''below code is responsible for outlier handling and also to drop the column that is not required for model tarning'''
        # droping the column that is not required
        self.df2 = self.df.drop(columns=["Gender","Unnamed: 0","Applicant_ID"])
        print("The data frame after deleting the gender",self.df2.columns)


        # handling the outlier values as per domanin study working with age column to drop age which is invalid.
        print(len(self.df2["Age"]))
        index_to_drop = np.where((self.df2["Age"] > 65) | (self.df2["Age"]<18))[0]


        print(len(index_to_drop))

        self.df2 = self.df2.drop(index=index_to_drop)

        # handing the Bureau_Score column as score will be in a range of 1 -999
        self.df2 = self.df2[
            (self.df2["Bureau_Score"] >= 0) &
            (self.df2["Bureau_Score"] <= 1000)
            ]

       # feature scaling using log1p to scale all the valid outlier in same unit so there is no impact on the model
        self.df2["Annual_Income"]  = np.log1p(self.df2["Annual_Income"])
        self.df2["Total_Existing_Debt"] = np.log1p(self.df2["Total_Existing_Debt"])
        self.df2["Requested_Credit_Limit"] = np.log1p(self.df2["Requested_Credit_Limit"])
        self.df2["Bureau_Score"] = np.log1p(self.df2["Bureau_Score"])




       # filling na values in the data frame
        columns_with_nas = ["Age","Dependents","Years_Employed","Annual_Income","Bureau_Score"]
        for col in columns_with_nas:

            print(self.df2[col].isna().sum())
            # filling na is Age column as observation
            col_mean = (self.df2[col].median())
            print(col_mean)

            self.df2[col] = self.df2[col].fillna(col_mean)
            print(self.df2[col].isna().sum())



        # label Encoding and ordinal-encoding one hot encoding

        '''befor converting the catgorical column into encoding we must take them all in lower cases'''

        for col in self.df2.select_dtypes(include="str").columns:
            self.df2[col] = self.df2[col].str.lower()
            print(self.df2[col].unique())

            if col == "Marital_Status":
                self.df2[col] = self.df2[col].map({"single":0,"married":1,"divorced":2,"widowed":3}).astype(int)
            elif col == "Employment_Status":
                self.df2[col] = self.df2[col].replace({"retired": 0, "salaried": 1, "self-employed": 2, "unemployed": 3,"student":4}).astype(int)
            elif col == "Housing_Type":
                self.df2[col] = self.df2[col].map({"mortgage": 0, "own": 1, "rent": 2, "unemployed": 3,"with parents":4}).astype(int)
            else:
                encoder = OrdinalEncoder(categories=[["high school","graduation","post-grad","bachelor","master","doctorate","other"]])
                self.df2[col] = encoder.fit_transform(self.df2[[col]])

                with open("models/education_encoder.pkl", "wb") as file:
                    pickle.dump(encoder, file)

            self.df2.info()




        # feature selection  -  corr

        corr_trix = self.df2.corr(numeric_only=True).abs()
        upper_matrix = corr_trix.where(np.triu(np.ones(corr_trix.shape),k=1).astype(bool))
        for col in upper_matrix.columns:
            high_corr = upper_matrix[col] > 0.3
            if high_corr.any():
                correlated_features =  high_corr[high_corr].index.to_list()
                print(correlated_features)

        '''plt.figure(figsize=(40,30))
        sns.heatmap(self.df2.corr(numeric_only= True),annot=True,cmap="Blues",fmt=".2f")
        plt.title("Correlation matrix")
        plt.show()

        corr_matrix = self.df2.corr(numeric_only=True)

        target_corr = corr_matrix["Target_Default_12M"].sort_values(ascending=False)

        print(target_corr)'''''





        '''self.df3 = self.df2.drop(columns=["Target_Default_12M"]).select_dtypes(include="number")
        x_vif = sm.add_constant(self.df3)
        vif_data = pd.DataFrame()
        vif_data["Features"] = x_vif.columns
        vif_data["vif_value"] = [variance_inflation_factor(x_vif.values,i) for i in range(x_vif.shape[1])]
        print(vif_data)'''

    @time_decorator
    def model_training(self):
        print(self.df2["Target_Default_12M"].value_counts(normalize=True))

        x = self.df2.drop(["Target_Default_12M"],axis=1) # 100 %
        y = self.df2["Target_Default_12M"] # 100 %  0  = 35% 1 = 65%

        x_train,x_test,y_train,y_test = train_test_split(x,y,train_size = 0.8,test_size = 0.2,random_state = 12,stratify=y)
        # x_train = 80 %
        #x_test = 20 %
        # y_train = 80 %
        # y_test = 20 %


        scalar = StandardScaler()
        x_train_scaled = scalar.fit_transform(x_train)
        print(x_train.columns)
        x_test_scaled  =  scalar.transform(x_test)
        
        

        with open("models/std_scalar.pkl", "wb") as file:
            pickle.dump(scalar, file)


        params = {
            "C": [0.001, 0.01, 0.1, 1, 10,100],

            "solver": ["liblinear", "saga"]
        }

        grid = GridSearchCV(
            LogisticRegression(max_iter=1000, random_state=42),
            param_grid=params,
            scoring="accuracy",
            cv=5,
            n_jobs=-1
        )

        #grid.fit(x_train_scaled, y_train)

        #print(grid.best_params_)
        #print(grid.best_score_)


        lg_model = LogisticRegression( class_weight="balanced",max_iter=1000,random_state=42)
        lg_model.fit(x_train_scaled,y_train)

        with open("models/lg_model.pkl", "wb") as file:
            pickle.dump(lg_model, file)

        print("Logistic Regression model saved successfully!")

        ## checking the model coeffients

        coef = pd.DataFrame({"Features":x_train.columns,"Cpeffients":lg_model.coef_[0]})
        print(coef)


        # model evaluation
        y_pred_test = lg_model.predict(x_test_scaled)
        print(y_pred_test)
        y_prob_test = lg_model.predict_proba(x_test_scaled)[:,1]


        y_pred_train = lg_model.predict(x_train_scaled)
        print(y_pred_train)

        conf_mat = confusion_matrix(y_test,y_pred_test)
        print(conf_mat)
        acc_score = accuracy_score(y_test,y_pred_test)
        print(acc_score)
        print(classification_report(y_test, y_pred_test))
        conf_mat_trian = confusion_matrix(y_train,y_pred_train)
        print(conf_mat_trian)
        print(classification_report(y_train,y_pred_train))




        # checking roc

        fpr , tpr ,threshould = roc_curve(y_test,y_pred_test)
        plt.figure(figsize=(6,4))
        plt.plot(fpr,tpr,label="ROC Curve")
        plt.xlabel("False positive rate")
        plt.ylabel("True positive rate")
        plt.show()


        auc = roc_auc_score( y_test,y_pred_test)
        print(auc)

        print(tpr,fpr)


        # to decide which threshould value is best for model

        threshould = np.arange(0.1,1.0,0.1)


        for th in threshould:
            pred = (y_prob_test>=th).astype(int)
            print("**************************")
            print("Threshould is", th)
            print("Accuracy", accuracy_score(y_test,pred))
            print("precision score is", precision_score(y_test,pred))
            print("f1 score is", f1_score(y_test,pred))
            print("recall score is", recall_score(y_test,pred))

            print()
            print()
















        self.df2.to_csv("Cleaned_1.csv",index=False)








if __name__ == "__main__":
    # object creation
    obj = CREDITSCORECARD()
    obj.data_collection()
    obj.Pre_processing()
    obj.model_training()
