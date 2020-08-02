# import libraries
from dataframe_maker.dataframe_maker import DFGuns
from plot_maker.plot_maker import PlotMaker
import plotly.graph_objs as go
from dash import Dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

# initialise Dash app
app = Dash(__name__,
           external_stylesheets=[dbc.themes.BOOTSTRAP])

# generate dataframe
df = DFGuns().return_dataframe()

# generate charts
charts = PlotMaker(df)

app.layout = html.Div([
    # header
    html.Div(className='jumbotron',

             children=[
                 html.H1('Firearms & Gun Homicide statistics Dashboard')
             ]),
    dcc.Graph(figure=charts.firearms_per_100_and_region())
])

# run app
if __name__ == '__main__':
    app.run_server(debug=True,
                   port=5000)
