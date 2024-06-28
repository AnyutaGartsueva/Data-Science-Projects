from google_play_scraper import app, search
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from gspread_dataframe import set_with_dataframe

creds_file = #hereshouldbeyourcredentials#

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name(creds_file, scope)
client = gspread.authorize(creds)

result = search('learn English', lang='en', country='us')

apps_data = []
for app_info in result:
    app_id = app_info['appId']
    app_details = app(app_id, lang='en', country='us')
    apps_data.append(app_details)

df = pd.DataFrame(apps_data)

print(df.head())
print(f"Number of apps: {len(df)}")

# Correlation between rating and number of reviews
sns.scatterplot(x='ratings', y='reviews', data=df)
plt.title('Correlation between rating and number of reviews')
plt.xlabel('Rating')
plt.ylabel('Number of reviews')
plt.show()

# Analysis of the number of installations
sns.histplot(df['installs'])
plt.title('Distribution of the number of installations')
plt.xlabel('Number of installations')
plt.ylabel('Number of applications')
plt.show()

# Impact of price on rating
sns.boxplot(x='free', y='ratings', data=df)
plt.title('Impact of price on rating')
plt.xlabel('Free/Paid')
plt.ylabel('Rating')
plt.show()

# Impact of category on rating
sns.boxplot(x='genre', y='ratings', data=df)
plt.xticks(rotation=90)
plt.title('Impact of category on rating')
plt.xlabel('Category')
plt.ylabel('Rating')
plt.show()

high_rating_threshold = 4.5
high_rating_apps = df[df['ratings'] > high_rating_threshold]

# Distribution of the number of installations among top-rated applications
plt.figure(figsize=(10, 6))
sns.histplot(high_rating_apps['installs'])
plt.title('Distribution of the number of installations among top-rated applications')
plt.xlabel('Number of installations')
plt.ylabel('Number of applications')
plt.show()

# Distribution of the number of reviews among highly rated applications
plt.figure(figsize=(10, 6))
sns.histplot(high_rating_apps['reviews'])
plt.title('Distribution of the number of reviews among highly rated applications')
plt.xlabel('Number of reviews')
plt.ylabel('Number of applications')
plt.show()

# The impact of fees on rankings among top-rated apps
plt.figure(figsize=(10, 6))
sns.boxplot(x='free', y='ratings', data=high_rating_apps)
plt.title('The impact of fees on rankings among top-rated apps')
plt.xlabel('Free/Paid')
plt.ylabel('Rating')
plt.show()

# Impact of category on ranking among top-rated apps
plt.figure(figsize=(12, 8))
sns.boxplot(x='genre', y='ratings', data=high_rating_apps)
plt.xticks(rotation=90)
plt.title('Impact of category on ranking among top-rated apps')
plt.xlabel('Category')
plt.ylabel('Rating')
plt.show()

spreadsheet = client.open('EngAppAnalytics')

try:
    sheet = spreadsheet.worksheet('EngAppAnalytics')
except gspread.exceptions.WorksheetNotFound:
    sheet = spreadsheet.add_worksheet(title='EngAppAnalytics', rows="100", cols="50")

sheet.clear()

if not df.empty:
    set_with_dataframe(sheet, df)
    print("Data uploaded successfully.")
else:
    print("DataFrame is empty. No data to upload.")