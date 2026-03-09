from dash import Dash, html
import dash_ag_grid as dag
import pandas as pd

df = pd.read_csv('articles.csv')

app = Dash()

app.layout = [html.Div(children="Hello World")]

if __name__=='__main__':
    app.run(debug=True)