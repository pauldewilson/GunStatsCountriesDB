# import libraries
import pandas as pd
import plotly.graph_objs as go
import plotly.offline as pyo

# url
url = "https://en.wikipedia.org/wiki/Estimated_number_of_civilian_guns_per_capita_by_country"

# read in all page tables as dataframe
df = pd.read_html(url)

# define relevant table as the df required
df = df[0]
print(df)
print(df.columns)
# remove unnecessary columns
df.drop(columns=["Unnamed: 0", "Notes", "Compu-tation method"], inplace=True)

# remove blank first row
df.drop(labels=[0], inplace=True)

# remove "-" from est. no of firearms in civ pop
df = df[df["Estimate of firearms in civilian possession"] != "–"]

# rename column headers to more data-friendly titles
df.rename(columns={"""Country (or dependent territory, subnational area, etc.)""": "country"}, inplace=True)
df.rename(columns={"""Estimate of civilian firearms per 100 persons""": "firearms_per_100_persons"}, inplace=True)
df.rename(columns={"""Region""": "region"}, inplace=True)
df.rename(columns={"""Subregion""": "sub_region"}, inplace=True)
df.rename(columns={"""Population 2017""": "pop_2017"}, inplace=True)
df.rename(columns={"""Estimate of firearms in civilian possession""": "firearms_owned_civilians"}, inplace=True)
df.rename(columns={"""Registered firearms""": "registered_firearms"}, inplace=True)
df.rename(columns={"""Unregistered Firearms""": "unregistered_firearms"}, inplace=True)

# bringing in death rates statistics
df_rate = pd.read_html("https://en.wikipedia.org/wiki/List_of_countries_by_guns_and_homicide")
df_rate = df_rate[0]

# creating joined dataframe
df_guns_rate = pd.merge(left=df,
                        right=df_rate,
                        left_on='country',
                        right_on='Country', how='inner')

# data list to be plotted
data = []

# for loop to insert into data list
for each_region in df_guns_rate["sub_region"].unique():
    df_reg = df_guns_rate[df_guns_rate["sub_region"] == each_region]
    data.append(go.Scatter(x=df_reg["firearms_per_100_persons"],
                           y=df_reg["firearms_owned_civilians"],
                           mode='markers',
                           text=df_reg["country"],
                           marker=dict(size=df_reg["Rate"],
                                       opacity=0.5),
                           name=each_region),
                )

# layout params
layout = go.Layout(title="Firearms statistics by Region and Country",
                   xaxis=dict(
                       title="X: Firearms per 100 people",
                       type='log'),
                   yaxis=dict(
                       title="Y: Total firearms owned by civilians",
                       type='log'))

# fig to be plot
fig = go.Figure(data=data, layout=layout)

# run plot

pyo.plot(fig)
