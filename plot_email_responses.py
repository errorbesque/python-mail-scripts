from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
from datetime import datetime
import pickle

eventdata=pickle.load(open("eventdata.p","rb"))

df = pd.DataFrame(eventdata)
df = df.drop(df[df.sender=='email@mail.com'].index) # don't count entries from this email
df = df.sort_values(by='time')
df['just1']=1
df['Cumulative_Value'] = df.groupby('event')['just1'].cumsum()
df['timeuntilevent']/=(-1*24*3600)

fig = px.line(df, x="timeuntilevent", y="Cumulative_Value", color="event")
fig.update_layout(
    title=dict(text="Response rate by event"),
    xaxis=dict(title=dict(text="Time until event start (d)")),
    yaxis=dict(title=dict(text="Cumulative emails received (#)"))
)

fig.show()
