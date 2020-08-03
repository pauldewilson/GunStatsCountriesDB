import plotly.graph_objs as go


class PlotMaker:

    def __init__(self, dataframe):
        self.df = dataframe.fillna(dataframe.median()).sort_values('country', ascending=True)

    def main_scatter(self, value_selection, x_axis, y_axis, z_axis):
        # data list to be plotted
        data = []
        if value_selection == 'country':
            # sort values of df
            self.df.sort_values('country', inplace=True, ascending=True)
            # for loop to insert into data list
            for each_country in self.df["country"].unique():
                df_reg = self.df[self.df["country"] == each_country]
                data.append(go.Scatter(x=df_reg[x_axis],
                                       y=df_reg[y_axis],
                                       mode='markers',
                                       text=df_reg["country"],
                                       marker=dict(size=[i/2000000 if i > 50 else i for i in df_reg[z_axis].values],
                                                   opacity=0.5,
                                                   sizemin=5),
                                       name=each_country),
                            )
        elif value_selection == 'region':
            # sort values of df
            self.df.sort_values('Rate', inplace=True, ascending=True)
            # for loop to insert into data list
            for each_region in self.df["region"].unique():
                df_reg = self.df[self.df["region"] == each_region]
                data.append(go.Scatter(x=df_reg[x_axis],
                                       y=df_reg[y_axis],
                                       mode='markers',
                                       text=df_reg["country"],
                                       marker=dict(size=[i/2000000 if i > 50 else i for i in df_reg[z_axis].values],
                                                   opacity=0.5,
                                                   sizemin=5),
                                       name=each_region),
                            )

        elif value_selection == 'sub_region':
            # sort values of df
            self.df.sort_values('region', inplace=True, ascending=True)
            # for loop to insert into data list
            for sub_region in self.df["sub_region"].unique():
                df_reg = self.df[self.df["sub_region"] == sub_region]
                data.append(go.Scatter(x=df_reg[x_axis],
                                       y=df_reg[y_axis],
                                       mode='markers',
                                       text=df_reg["sub_region"],
                                       marker=dict(size=[i/2000000 if i > 50 else i for i in df_reg[z_axis].values],
                                                   opacity=0.5,
                                                   sizemin=5),
                                       name=sub_region),
                            )

        # rename the values of callback inputs to something more user friendly
        ux_axes_labels = {'pop_2017': 'Population',
                          'firearms_owned_civilians': 'Civilian Firearms',
                          'Unregistered firearms': 'Unregistered Firearms',
                          'registered_firearms': 'Registered Firearms',
                          'firearms_per_100_persons': 'Firearms per 100 people',
                          'Rate': 'Murder Rate per 100,000'}
        # layout params
        layout = go.Layout(title=f"Scatter Graph showing {ux_axes_labels[x_axis]} (X-Axis) "
                                 f"against {ux_axes_labels[y_axis]} (Y-Axis) where"
                                 f" marker size represents {ux_axes_labels[z_axis]} (Z-axis)",
                           xaxis=dict(
                               title=ux_axes_labels[x_axis],
                               type='log'),
                           yaxis=dict(
                               title=ux_axes_labels[y_axis],
                               type='log'),
                           height=1000)

        # fig to be plot
        return go.Figure(data=data, layout=layout)
