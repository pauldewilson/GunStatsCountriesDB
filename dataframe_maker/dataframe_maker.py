import pandas as pd


class DFGuns:

    def __init__(self):
        self.url_one = "https://en.wikipedia.org/wiki/Estimated_number_of_civilian_guns_per_capita_by_country"
        self.url_two = "https://en.wikipedia.org/wiki/List_of_countries_by_guns_and_homicide"

    def return_dataframe(self):
        # read in all page tables as dataframe
        df = pd.read_html(self.url_one)

        # define relevant table as the df required
        df = df[0]

        # remove unnecessary columns
        try:
            df.drop(columns=["Unnamed: 0", "Notes", "Compu-tation method"], inplace=True)

            # remove blank first row
            df.drop(labels=[0], inplace=True)

            # remove "-" from est. no of firearms in civ pop
            df = df[df["Estimate of firearms in civilian possession"] != "–"]

            # rename column headers to more data-friendly titles
            df.rename(columns={"""Country (or dependent territory, subnational area, etc.)""": "country"}, inplace=True)
            df.rename(columns={"""Estimate of civilian firearms per 100 persons""": "firearms_per_100_persons"},
                      inplace=True)
            df.rename(columns={"""Region""": "region"}, inplace=True)
            df.rename(columns={"""Subregion""": "sub_region"}, inplace=True)
            df.rename(columns={"""Population 2017""": "pop_2017"}, inplace=True)
            df.rename(columns={"""Estimate of firearms in civilian possession""": "firearms_owned_civilians"},
                      inplace=True)
            df.rename(columns={"""Registered firearms""": "registered_firearms"}, inplace=True)
            df.rename(columns={"""Unregistered Firearms""": "unregistered_firearms"}, inplace=True)

            # bringing in death rates statistics
            df_rate = pd.read_html(self.url_two)
            df_rate = df_rate[0]

            # creating joined dataframe
            df_guns_rate = pd.merge(left=df,
                                    right=df_rate,
                                    left_on='country',
                                    right_on='Country', how='inner')

            # fill any missing values as median and convert civ firearms to float
            df_guns_rate.fillna(df_guns_rate.median(), inplace=True)
            df_guns_rate['firearms_owned_civilians'] = df_guns_rate['firearms_owned_civilians'].astype(float)

            return df_guns_rate
        except KeyError:
            print("Probable column name conflict, likely column names changed at source")
            return 0
