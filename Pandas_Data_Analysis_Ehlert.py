"""
Program Name: Pandas_Data_Analysis_Ehlert.py
Author: Tony Ehlert
Date: 9/22/2023

Program Description: This program continues to use the Pandas library on the results from the
Import_And_Prep_Dataset_Ehlert.py program to perform data analysis on a csv file.
"""
import pandas as pd

pd.options.display.width = 0

####### START OF "Import_And_Prep_Dataset_Ehlert.py" CODE #######

# Load the dataset into a Pandas dataframe
base_steam_df = pd.read_csv("steam.csv")

# Familiarize yourself with the data by looking it over
#print(f"Head of \"base_steam_df\":\n{base_steam_df.head()}")
#print()
#print(f"Shape of \"base_steam_df\": {base_steam_df.shape}")
#print()

#### Create new df from original that only contains data for publishers with at least 50 positive ratings. To do this:
# Create a temp frame that is grouped by publisher and summed
steam_group_by_pub_df = base_steam_df.groupby("publisher")
steam_group_by_pub_df = steam_group_by_pub_df.sum()
#print(f"Shape of \"steam_group_by_pub_df\": {steam_group_by_pub_df.shape}")
#print()

# From this grouped frame create a list of rows that need to be deleted based on having less than 50 positive ratings
pub_to_delete_df = steam_group_by_pub_df[steam_group_by_pub_df["positive_ratings"] < 50].index
# print(f"Shape of \"pub_to_delete_df\": {pub_to_delete_df.shape}")
# print()
pub_to_delete_list = list(pub_to_delete_df)

# Using list of publishers to delete & your original df, create new df that has publishers with at least 50 ratings
pub_50_pos_df = base_steam_df[~base_steam_df["publisher"].isin(pub_to_delete_list)]

# Sort your new dataframe descending on positive ratings.  Your top name should be "Counter-Strike: Global Offensive"
sorted_pub_50_pos_df = pub_50_pos_df.sort_values(by=["positive_ratings"], ascending=False).copy()
# print(f"Head of \"sorted_pub_50_pos_df\":\n{sorted_pub_50_pos_df.head()}")
# print()
# print(f"Shape of \"sorted_pub_50_pos_df\": {pub_50_pos_df.shape}")
# print()

# Do a describe on the frame to see some quick stats on it
# print(f"Describe of \"pub_50_pos_df\":\n{pub_50_pos_df.describe()}")
# print()

# Remove the appid column using iloc because we don't need it
no_appid_pub_50_pos_df = sorted_pub_50_pos_df.drop(sorted_pub_50_pos_df.iloc[:, 0:1], axis=1)
# print(f"Shape of \"no_appid_pub_50_pos_df\": {no_appid_pub_50_pos_df.shape}")
no_appid_pub_50_pos_df.to_csv("no_appid_pub_50_pos_df.csv")
# print()

# Remove any rows for games that have less than 20000 owners
under_20k_owners_to_delete = no_appid_pub_50_pos_df[no_appid_pub_50_pos_df["owners"] == "0-20000"].index
over_20k_owners_df = no_appid_pub_50_pos_df.drop(under_20k_owners_to_delete)
# print(f"Shape of \"over_20k_owners_steam_df\": {over_20k_owners_df.shape}")

####### END OF "Import_And_Prep_Dataset_Ehlert.py" CODE #######

#### Using the result from your topic 1 assignment, let's do some data analysis
#### First, let's determine if games with more owners get higher ratings:
# Create a frame from your original dataset that includes owners, positive ratings, and negative ratings
owners_and_ratings_df = over_20k_owners_df[["owners", "positive_ratings", "negative_ratings"]].copy()

# Group the frame by owners
group_by_owners_df = owners_and_ratings_df.groupby("owners")

# Sum the grouped frame
sum_group_by_owners_df = group_by_owners_df.sum()

# print the grouped, summed frame
print(sum_group_by_owners_df.to_string())
print()

#### It looks like games w/ more owners might have higher pos. ratings but hard to tell with raw numbers.  Let's add %'s
# add a column to your grouped, summed frame showing the % of positive reviews (pos reviews/(neg reviews+pos reviews))
sum_group_by_owners_df["percent_positive"] = sum_group_by_owners_df["positive_ratings"] / (
        sum_group_by_owners_df["positive_ratings"] + sum_group_by_owners_df["negative_ratings"])

# add a column that does the same for % of negative reviews
sum_group_by_owners_df["percent_negative"] = sum_group_by_owners_df["negative_ratings"] / (
        sum_group_by_owners_df["positive_ratings"] + sum_group_by_owners_df["negative_ratings"])

# print the output
print(sum_group_by_owners_df.to_string())
print()

#### It's hard to tell what's highest rated still
# Sort the frame descending by % positive ratings
sum_group_by_owners_df = sum_group_by_owners_df.sort_values(by="percent_positive", ascending=False)
print(sum_group_by_owners_df.to_string())
print()

#### It isn't perfect but it does appear that games with more owners have higher ratings (does that make sense?)
#### Now let's find out which publishers have the highest ratings
# Create a frame that has publisher, positive_ratings, negative ratings
publishers_and_ratings_df = over_20k_owners_df[["publisher", "positive_ratings", "negative_ratings"]].copy()

# Group by publisher
ratings_group_by_pub_df = publishers_and_ratings_df.groupby("publisher")

# Sum the grouped frame
sum_ratings_group_by_pub_df = ratings_group_by_pub_df.sum()

# add in the % positive and % negative reviews
sum_ratings_group_by_pub_df["percent_positive"] = sum_ratings_group_by_pub_df["positive_ratings"] / (
        sum_ratings_group_by_pub_df["positive_ratings"] + sum_ratings_group_by_pub_df["negative_ratings"])
sum_ratings_group_by_pub_df["percent_negative"] = sum_ratings_group_by_pub_df["negative_ratings"] / (
        sum_ratings_group_by_pub_df["positive_ratings"] + sum_ratings_group_by_pub_df["negative_ratings"])

# Sort the frame descending by % positive reviews
sum_ratings_group_by_pub_df = sum_ratings_group_by_pub_df.sort_values(by=["percent_positive"], ascending=False)

# print the grouped, summed frame
print(sum_ratings_group_by_pub_df.to_string())
print()

#### That's strange...It appears that Dexion Games got the highest overall rating but only has 1 rating...
#### but we removed all publishers that didn't have at least 50 ratings.  EXPLAIN WHY THIS IS HERE IN YOUR SUBMISSION
# Let's drop any rows that don't have at least 1000 positive ratings
at_least_1k_pos_rating_df = sum_ratings_group_by_pub_df[sum_ratings_group_by_pub_df["positive_ratings"] >= 1000]

#### Now Wube Software is the winner...but they only have 1 game (and everyone loves it).
#### I want to see how publishers do overall so let's drop any publisher that doesn't have at least 5 games listed
# create a copy of the over_20k_owners_df and assign to new df variable
pub_at_least_5_game_df = over_20k_owners_df.copy()

# add a "count" column to pub_at_least_5_games_df to help with code readability
pub_at_least_5_game_df["count"] = ''

# group df by "publisher" and then count
pub_at_least_5_game_df = pub_at_least_5_game_df.groupby("publisher")
pub_at_least_5_game_df = pub_at_least_5_game_df.count()

# create df of publishers with less than 5 counts/games
less_than_5_games_pubs = pub_at_least_5_game_df[pub_at_least_5_game_df["count"] < 5].index

# convert df to list
less_than_5_games_pubs_list = list(less_than_5_games_pubs)

# using list & at_least_1k_pos_rating_df(ending df from "import_And_Prep_Ehlert.py", remove publishers w/ games < 5
final_df = at_least_1k_pos_rating_df[~at_least_1k_pos_rating_df.index.isin(less_than_5_games_pubs_list)]

# print your final dataframe with Nicalis Inc. as the highest rated publisher
print(final_df.to_string())
