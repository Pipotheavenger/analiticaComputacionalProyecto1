# Importa el módulo de Dash
import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import pandas as pd
import base64
import io

# Inicializa la aplicación Dash
app = dash.Dash(__name__, external_stylesheets=['/assets/styles.css'])

# Define el diseño de la aplicación
app.layout = html.Div([
    html.H1("Linear Regression Model for Decision Making"),
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        multiple=False
    ),
    html.Br(),
    # Label que quieres ocultar
    html.Label('Select independent Variables:', id='label-indep-var', style={'margin-top': '10px', 'display': 'none'}), 
    dcc.Checklist(
        id='columns-list',
        options=[],
        value=[],
        labelStyle={'display': 'inline-block'}
    ),
    html.Br(),
    html.Div(id='output-data-upload')
])

# Callback para cargar el archivo y mostrar opciones de columna
@app.callback(Output('columns-list', 'options'),
              [Input('upload-data', 'contents')],
              [State('upload-data', 'filename')])
def update_output(contents, filename):
    if contents is None:
        return []  # Return empty options if no file uploaded

    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    
    try:
        if 'csv' not in filename:
            return []  # Return empty options if file format is not CSV
        
        # Lee el archivo CSV
        df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        # Genera las opciones de columna
        columns_options = [{'label': col, 'value': col} for col in df.columns]
        return columns_options
    except Exception as e:
        print(e)
        return []  # Return empty options in case of any error

# Callback para mostrar el Label de las variables independientes después de cargar el archivo
@app.callback(Output('label-indep-var', 'style'),
              [Input('upload-data', 'contents')])
def show_label(contents):
    if contents:
        return {'margin-top': '10px', 'display': 'block'}  # Mostrar el Label después de cargar el archivo
    else:
        return {'display': 'none'}  # Ocultar el Label si no hay archivo cargado

# Callback para mostrar la tabla después de seleccionar las columnas y cargar el archivo
@app.callback(Output('output-data-upload', 'children'),
              [Input('columns-list', 'value')],
              [State('upload-data', 'contents')])
def display_dataframe(selected_columns, contents):
    if contents is None or not selected_columns:
        return html.Div()  # Return empty Div if no file uploaded or no columns selected
    
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    
    try:
        df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        df_filtered = df[selected_columns]  # Filter DataFrame by selected columns
        return html.Div([
            html.H5('Filtered DataFrame:'),
            html.Table([
                html.Thead(
                    html.Tr([html.Th(col) for col in df_filtered.columns])
                ),
                html.Tbody([
                    html.Tr([
                        html.Td(df_filtered.iloc[i][col]) for col in df_filtered.columns
                    ]) for i in range(min(len(df_filtered), 10))
                ])
            ])
        ])
    except Exception as e:
        print(e)
        return html.Div('An error occurred while processing the DataFrame.')

# Ejecuta la aplicación
if __name__ == '__main__':
    app.run_server(debug=True)
