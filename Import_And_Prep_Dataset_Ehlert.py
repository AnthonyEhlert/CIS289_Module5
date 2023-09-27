"""
Program Name: Import_And_Prep_Dataset_Ehlert.py
Author: Tony Ehlert
Date: 9/20/2023

Program Description: This program loads a dataset to a Pandas dataframe and then preps it for a future
assignment/program
"""
import pandas as pd

pd.options.display.width = 0

# Load the dataset into a Pandas dataframe
base_steam_df = pd.read_csv("steam.csv")

# Familiarize yourself with the data by looking it over
print(f"Head of \"base_steam_df\":\n{base_steam_df.head()}")
print()
print(f"Shape of \"base_steam_df\": {base_steam_df.shape}")
print()

# Create new df from original that only contains data for publishers that have at least 50 positive ratings. To do this:
#### Create a temp frame that is grouped by publisher and summed
steam_group_by_pub_df = base_steam_df.groupby("publisher")
steam_group_by_pub_df = steam_group_by_pub_df.sum()
print(f"Shape of \"steam_group_by_pub_df\": {steam_group_by_pub_df.shape}")
print()

#### From this grouped frame create a list of rows that need to be deleted based on having less than 50 positive ratings
pub_to_delete_df = steam_group_by_pub_df[steam_group_by_pub_df["positive_ratings"] < 50].index
print(f"Shape of \"pub_to_delete_df\": {pub_to_delete_df.shape}")
print()
pub_to_delete_list = list(pub_to_delete_df)

# Using list of publishers to delete & your original df, create new df that has publishers with at least 50 ratings
pub_50_pos_df = base_steam_df[~base_steam_df["publisher"].isin(pub_to_delete_list)]

# Sort your new dataframe descending on positive ratings.  Your top name should be "Counter-Strike: Global Offensive"
sorted_pub_50_pos_df = pub_50_pos_df.sort_values(by=["positive_ratings"], ascending=False).copy()
print(f"Head of \"sorted_pub_50_pos_df\":\n{sorted_pub_50_pos_df.head()}")
print()
print(f"Shape of \"sorted_pub_50_pos_df\": {pub_50_pos_df.shape}")
print()

# Do a describe on the frame to see some quick stats on it
print(f"Describe of \"pub_50_pos_df\":\n{pub_50_pos_df.describe()}")
print()

# Remove the appid column using iloc because we don't need it
no_appid_pub_50_pos_df = sorted_pub_50_pos_df.drop(sorted_pub_50_pos_df.iloc[:, 0:1], axis=1)
print(f"Shape of \"no_appid_pub_50_pos_df\": {no_appid_pub_50_pos_df.shape}")
print()

# Remove any rows for games that have less than 20000 owners
under_20k_owners_to_delete = no_appid_pub_50_pos_df[no_appid_pub_50_pos_df["owners"] == "0-20000"].index
over_20k_owners_df = no_appid_pub_50_pos_df.drop(under_20k_owners_to_delete)
print(f"Shape of \"over_20k_owners_steam_df\": {over_20k_owners_df.shape}")
