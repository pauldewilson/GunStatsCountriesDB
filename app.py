# import libraries
from dataframe_maker.dataframe_maker import DFGuns
from plot_maker.plot_maker import PlotMaker
from dash import Dash
import dash_table
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

# initialise Dash app
app = Dash(__name__,
           external_stylesheets=[dbc.themes.FLATLY])

# generate dataframe
df = DFGuns().return_dataframe()

# generate charts
charts = PlotMaker(df)

app.layout = dbc.Container([
    dbc.Row(children=[  # header
        dbc.Row(className='jumbotron',

                children=[
                    html.H1('Firearms & Gun Homicide statistics Dashboard.'),
                    html.P('Data has been provided where it exists. Median values provided where numeric data absent.')
                ])]),
    dbc.Row([
        dbc.Col(children=[
            dbc.Label('Chunk size',
                      style={'color': 'pink'}),
            dbc.FormGroup(dbc.RadioItems(id='main_chart_dd_viewby',
                                         options=[{'label': 'Country', 'value': 'country'},
                                                  {'label': 'Region', 'value': 'region'},
                                                  {'label': 'Sub-Region', 'value': 'sub_region'}],
                                         value='country')),
            dbc.Label('X-Axis',
                      style={'color': 'pink'}),
            dbc.FormGroup(dbc.RadioItems(id='main_chart_x',
                                         options=[{'label': 'Population', 'value': 'pop_2017'},
                                                  {'label': 'Civilian Firearms',
                                                   'value': 'firearms_owned_civilians'},
                                                  {'label': 'Registered Firearms',
                                                   'value': 'registered_firearms'},
                                                  {'label': 'Unregistered Firearms',
                                                   'value': 'Unregistered firearms'},
                                                  {'label': 'Firearms per 100 people',
                                                   'value': 'firearms_per_100_persons'},
                                                  {'label': 'Murder Rate per 100,000', 'value': 'Rate'}],
                                         value='pop_2017')),
            dbc.Label('Y-Axis',
                      style={'color': 'pink'}),
            dbc.FormGroup(dbc.RadioItems(id='main_chart_y',
                                         options=[{'label': 'Population', 'value': 'pop_2017'},
                                                  {'label': 'Civilian Firearms',
                                                   'value': 'firearms_owned_civilians'},
                                                  {'label': 'Registered Firearms',
                                                   'value': 'registered_firearms'},
                                                  {'label': 'Unregistered Firearms',
                                                   'value': 'Unregistered firearms'},
                                                  {'label': 'Firearms per 100 people',
                                                   'value': 'firearms_per_100_persons'},
                                                  {'label': 'Murder Rate per 100,000', 'value': 'Rate'}],
                                         value='firearms_owned_civilians')),
            dbc.Label('Marker Size',
                      style={'color': 'pink'}),
            dbc.FormGroup(dbc.RadioItems(id='main_chart_z',
                                         options=[{'label': 'Population', 'value': 'pop_2017'},
                                                  {'label': 'Civilian Firearms',
                                                   'value': 'firearms_owned_civilians'},
                                                  {'label': 'Registered Firearms',
                                                   'value': 'registered_firearms'},
                                                  {'label': 'Unregistered Firearms',
                                                   'value': 'Unregistered firearms'},
                                                  {'label': 'Firearms per 100 people',
                                                   'value': 'firearms_per_100_persons'},
                                                  {'label': 'Murder Rate per 100,000', 'value': 'Rate'}],
                                         value='Rate'))
        ]),
        dcc.Graph(id='main_chart')
    ]),
    dash_table.DataTable(
        id='table-dark',
        columns=[{'name': 'Country', 'id': 'country'},
                 {'name': 'Region', 'id': 'region'},
                 {'name': 'Sub Region', 'id': 'sub_region'},
                 {'name': 'Population', 'id': 'pop_2017'},
                 {'name': 'Civilian Firearms', 'id': 'firearms_owned_civilians'},
                 {'name': 'Registered Firearms', 'id': 'registered_firearms'},
                 {'name': 'Unregistered Firearms', 'id': 'Unregistered firearms'},
                 {'name': 'Firearms per 100 people', 'id': 'firearms_per_100_persons'},
                 {'name': 'Murder Rate per 100,000', 'id': 'Rate'}],
        data=charts.df.to_dict('records'),
        sort_action='native',
        style_table={'width': '98%',
                     'align': 'center'}
    )
])


# callback for main_chart
@app.callback(output=Output(component_id='main_chart',
                            component_property='figure'),
              inputs=[Input(component_id='main_chart_dd_viewby',
                            component_property='value'),
                      Input(component_id='main_chart_x',
                            component_property='value'),
                      Input(component_id='main_chart_y',
                            component_property='value'),
                      Input(component_id='main_chart_z',
                            component_property='value')
                      ])
def callback(selector_region, x_axis, y_axis, z_axis):
    return charts.main_scatter(value_selection=selector_region,
                               x_axis=x_axis,
                               y_axis=y_axis,
                               z_axis=z_axis)


# run app
if __name__ == '__main__':
    app.run_server(debug=False,
                   port=5000)
