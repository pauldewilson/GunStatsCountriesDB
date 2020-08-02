import plotly.graph_objs as go


class PlotMaker:

    def __init__(self, dataframe):
        self.df = dataframe

    def firearms_per_100_and_region(self):
        # data list to be plotted
        data = []

        # for loop to insert into data list
        for each_region in self.df["sub_region"].unique():
            df_reg = self.df[self.df["sub_region"] == each_region]
            data.append(go.Scatter(x=df_reg["firearms_per_100_persons"],
                                   y=df_reg["firearms_owned_civilians"],
                                   mode='markers',
                                   text=df_reg["country"],
                                   marker=dict(size=df_reg["Rate"],
                                               opacity=0.5,
                                               sizemin=5),
                                   name=each_region),
                        )

        # layout params
        layout = go.Layout(title="Firearms statistics by Region and Country",
                           xaxis=dict(
                               title="X: Firearms per 100 people",
                               type='log'),
                           yaxis=dict(
                               title="Y: Total firearms owned by civilians",
                               type='log'),
                           height=1000)

        # fig to be plot
        return go.Figure(data=data, layout=layout)
