from dataclasses import asdict
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import shapiro, levene, ttest_ind, mannwhitneyu
import math

import warnings
warnings.filterwarnings("error")


class Data(object):
    def __init__(self, df, indep_variable = None, subgroup_variable = None, control_name = "Control", target_features = None):
        # attibutes
        self.target_features = target_features
        self.control = control_name
        self.indep_name = indep_variable
        self.subgroup_variable = subgroup_variable

        self.df = df.copy()
        self.ctl_df = self.grab_group(self.control)
        #self.subgroups = df[subgroup_variable].unique()
        

    def get_df(self):
        '''
        Return the cleaned version of the original dataframe
        '''
        return self.df


    def grab_group(self, treatment):
        '''
        Create a dataframe containing only the specified group
        This operation renames the drug to the user's entry
        '''
        #lower_df = df["Drug"].str.lower()
        lowered_series = self.df[self.indep_name].str.lower()
        treatment_df = self.df.copy()[lowered_series.str.contains(treatment.lower())]
        treatment_df.loc[:,self.indep_name] = treatment
        return treatment_df

    def descriptive(self, treatment, subgroup = None):
        '''
        Create a descriptive statistics table
        '''
        if self.subgroup_variable == None:
            treatment_df = self.grab_group(treatment)
            return treatment_df.loc[:, self.target_features].describe()

        else:
            treatment_df = self.grab_group(treatment)
            return treatment_df.loc[treatment_df[self.subgroup_variable] == subgroup, self.target_features].describe()

    def boxplot(self, treatment, subgroup = None):
        '''
        Create boxplots 
        '''
        treatment_df = self.grab_group(treatment)
        concat_df = pd.concat([treatment_df, self.ctl_df])
        if subgroup != None:
            concat_df = concat_df[concat_df[self.subgroup_variable] == subgroup]

        #fig, axs = plt.subplots(ncols=len(self.target_features), figsize=(20, 5)) # make this look better

        n = len(self.target_features)
        n_columns = 5
        n_rows = math.ceil(n/n_columns)

        fig, axs = plt.subplots(n_rows, n_columns, figsize=(18, 10))

        row = 0
        column = 0
        for feature in self.target_features:
            sns.boxplot(x=self.indep_name, y=feature, data=concat_df,
                        whis=[0, 100], width=.6, palette="vlag", ax=axs[row, column]).set_title(feature)
            sns.stripplot(x=self.indep_name, y=feature, data=concat_df,
                    size=4, color=".3", linewidth=0, ax=axs[row, column])
            plt.tight_layout()

            column += 1
            if column == 5:
                column = 0
                row += 1


    def hypothesis(self, treatment, subgroup = None):
        '''
        Perform hypothesis testing to determine significance
        '''
        treatment_df = self.grab_group(treatment)
        ctl_df = self.ctl_df

        if subgroup != None:
            treatment_df = treatment_df[treatment_df[self.subgroup_variable] == subgroup]
            ctl_df = ctl_df[ctl_df[self.subgroup_variable] == subgroup]
        
        stats_df = pd.DataFrame(columns = ['p-value', 'test'], index= self.target_features)
        
        for feature in self.target_features:
            
            exp_list = treatment_df[feature].dropna().to_list()
            ctl_list = ctl_df[feature].dropna().to_list()

            if (len(exp_list) < 3) | (len(ctl_list) < 3):
                stats_df.loc[feature] = [np.nan, 'Insufficient # Samples']
            
            else:
                # normality
                try:
                    stat, exp_norm = shapiro(exp_list)
                    stat, ctl_norm = shapiro(ctl_list)
                except UserWarning:
                    stats_df.loc[feature] = [np.nan, 'Insufficient variance']
                    continue

                # variance
                stat, variance = levene(ctl_list, exp_list)

                # decision tree
                if (exp_norm > 0.05) & (ctl_norm > 0.05):
                    stat, variance = levene(ctl_list, exp_list)
                    if variance > 0.05:
                        stat, p = ttest_ind(ctl_list, exp_list, alternative = 'two-sided', equal_var=True)
                        test, p_value = "Student t-test", p
                    else:
                        stat, p = ttest_ind(ctl_list, exp_list, alternative = 'two-sided', equal_var=False)
                        test, p_value = "Welch's t-test", p
                else:
                    stat, p = mannwhitneyu(ctl_list, exp_list, alternative = 'two-sided')
                    test, p_value = "Mann-Whitney U", p
                
                stats_df.loc[feature] = [p_value, test]

        return stats_df