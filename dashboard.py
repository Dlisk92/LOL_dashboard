import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_table

import pandas as pd

external_stylesheets = [
    "assets/stylesheet.css"
]


app = dash.Dash(
    __name__,
    external_stylesheets=external_stylesheets,
    )

app.css.append_css({
    "external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css",
})

app.css.config.serve_locally = False

champs = pd.read_csv('champs.csv')

champ_dict = champs['name'].unique()

df_matchup = pd.read_csv('df_matchup.csv')

position = df_matchup['adjposition'].unique()

app.layout = html.Div([


    html.Div([
    html.Img(src='/assets/league-of-legends.jpg',
    ),
    html.H2(
        '''
        Choose your opponent and role

        ''',
    ),
], className='banner'),
html.Div([
    dcc.Dropdown(
        id='opponent',
        options=[{'label' : i, 'value' : i} for i in champ_dict],
        className='h1'
    ),

    dcc.RadioItems(
        id='position',
        options=[{'label' : i, 'value': i} for i in position],
    ),
    dash_table.DataTable(
        id='data-table',

        style_header={'backgroundColor': 'rgb(30, 30, 30)'},
        style_cell={
        'backgroundColor': 'rgb(50, 50, 50)',
        'color': 'white'
    },
        style_data_conditional=[{
        "if": {"row_index": 0},
        "backgroundColor": "#3D9970",
        'color': 'white'
        
        }],
    )
])
])
@app.callback([
    Output('data-table', 'data'),
    Output('data-table', 'columns')],
    [Input('opponent', 'value'),
     Input('position', 'value')])
def get_best_counter(champion, role):
    df_matchup_temp = df_matchup[(df_matchup['match up'].str.contains(champion)) & (df_matchup['adjposition'] == role)]
    df_matchup_temp['champion'] = df_matchup_temp['match up'].apply(lambda x: x.split(' vs ')[0] if x.split(' vs ')[1] == champion else x.split(' vs ')[1])
    df_matchup_temp['advantage'] = df_matchup_temp.apply(lambda x: x['dominant score']*-1 if x['match up'].split(' vs ')[0] == champion else x['dominant score'], axis = 1)
    df_matchup_temp = df_matchup_temp[df_matchup_temp['advantage']>0].sort_values('advantage', ascending = False)
    print('Best counter for {} - {}:'.format(role, champion))
    print(df_matchup_temp[['champion', 'total matches', 'advantage']])
    data = df_matchup_temp[['champion', 'total matches', 'advantage']].to_dict(orient='records')
    print(data)
    columns = [{'id' : i, 'name' : i} for i in ['champion', 'total matches', 'advantage']]
    
    return  data, columns


if __name__ == '__main__':
    app.run_server(debug=True)