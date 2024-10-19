import plotly.express as px
from dash import Dash, Input, Output, dcc, html
from plotly import graph_objects as go

from preprocess import geojson, pop_ratio_df

app = Dash(__name__)


app.layout = html.Div(
    [
        html.H1("Japan Population"),
        dcc.Dropdown(
            ["Population", "Ratio"], None, id="dropdown", style={"width": "50%"}
        ),
        html.P("Select a year:"),
        dcc.RadioItems(
            id="radio",
            options=[],
            value=None,
            inline=True,
        ),
        dcc.Graph(id="graph"),
    ]
)


@app.callback(
    Output("radio", "options"), Output("radio", "value"), Input("dropdown", "value")
)
def update_radio_options(selected_value):
    if selected_value == "Population":
        return ["2005", "2010", "2015", "2020", "2025", "2030", "2035"], "2025"
    elif selected_value == "Ratio":
        return [
            f"ratio_{year}_2005"
            for year in ["2010", "2015", "2020", "2025", "2030", "2035"]
        ], f"ratio_2025_2005"
    else:
        return [], None


def blank_fig():
    fig = go.Figure(go.Scatter(x=[], y=[]))
    fig.update_layout(template=None)
    fig.update_xaxes(showgrid=False, showticklabels=False, zeroline=False)
    fig.update_yaxes(showgrid=False, showticklabels=False, zeroline=False)

    return fig


@app.callback(
    Output("graph", "figure"), Input("radio", "value"), Input("dropdown", "value")
)
def display_choropleth(year, dropdown):
    if dropdown is None:
        return blank_fig()
    else:
        fig = px.choropleth(
            pop_ratio_df,
            geojson=geojson,
            color=year,
            locations="id",
            featureidkey="properties.id",
            projection="mercator",
        )

    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

    return fig


app.run_server(debug=True)
