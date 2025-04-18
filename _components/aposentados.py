import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd

# Carregar os dados do arquivo "Projeção folha - CMVC.xlsx"
from utils import carregar_dados_drive
df_projecao_2 = carregar_dados_drive()

# Limpar e processar os dados
df_projecao_2_cleaned = df_projecao_2.iloc[2:].reset_index(drop=True)
df_projecao_2_cleaned.columns = [
    'Regime', 'Qtd', 'Salário Base Total (R$)', 'Outros Vencimentos (R$)', 'H. Extras', 
    'Diárias', '1/3 de Férias', 'Total de Vencimentos (R$)', 'INSS', 'IRRF', 'Outros Descontos', 'Total de Descontos'
]

# Limpar a coluna 'Regime' para verificar os períodos
df_projecao_2_cleaned['Regime'] = df_projecao_2_cleaned['Regime'].str.strip()

# Filtrando os dados dos "Aposentados" e extraindo as colunas relevantes
df_aposentados = df_projecao_2_cleaned[df_projecao_2_cleaned['Regime'] == 'Aposentado']
aposentados_data = df_aposentados[['Regime', 'Qtd', 'Salário Base Total (R$)', 'Outros Vencimentos (R$)', 
                                   'H. Extras', 'Diárias', '1/3 de Férias', 'Total de Vencimentos (R$)', 
                                   'INSS', 'IRRF', 'Outros Descontos', 'Total de Descontos']]

# Adicionando uma nova coluna 'Período' para associar os dados ao período correspondente
df_aposentados['Período'] = pd.NA

# Iterar sobre as linhas para associar o período a cada valor
current_period = None
for index, row in df_aposentados.iterrows():
    if pd.notna(row['Regime']) and '2025' in str(row['Regime']):  # Identificando um período válido
        current_period = row['Regime']
    if current_period:
        df_aposentados.at[index, 'Período'] = current_period  # Atribuindo o período correspondente

# Definir os meses (de Janeiro a Dezembro + 13º mês)
meses = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 
         'Outubro', 'Novembro', 'Dezembro', '13º Mês']

# Garantir que temos exatamente 13 entradas
if len(df_aposentados) == 13:
    df_aposentados['Mês'] = meses  # Atribuindo os meses à coluna 'Mês'
else:
    print("Erro: o número de entradas para 'Aposentados' não corresponde a 13 meses.")

# Verificando se a coluna 'Mês' foi corretamente adicionada
print(f"\nDataFrame com 'Mês' adicionado para Aposentados:")
print(df_aposentados.head())

# Gráfico de Qtd (Novo Gráfico - fig0_aposentados)
fig0_aposentados = go.Figure()

fig0_aposentados.add_trace(go.Bar(
    x=df_aposentados['Mês'],  # Usando os meses no eixo X
    y=df_aposentados['Qtd'],  # Qtd no eixo Y
    name='Qtd',  # Nome para a legenda
    marker=dict(color='blue')  # Cor da barra de Qtd
))

# Atualizando o layout da fig0_aposentados
fig0_aposentados.update_layout(
    title='Quantidade (Qtd) por Mês',  # Título do gráfico
    xaxis_title='Meses',  # Título do eixo X
    yaxis_title='Quantidade',  # Título do eixo Y
    barmode='group',  # Agrupar as barras lado a lado
    legend_title='Categorias',  # Título da legenda
    showlegend=True  # Mostrar a legenda
)

# Gráfico de Total de Vencimentos (fig1_aposentados)
fig1_aposentados = go.Figure()

fig1_aposentados.add_trace(go.Bar(
    x=df_aposentados['Mês'],  # Usando os meses no eixo X
    y=df_aposentados['Total de Vencimentos (R$)'],  # Total de Vencimentos (R$) no eixo Y
    name='Total de Vencimentos',  # Nome para a legenda
    marker=dict(color='orange')  # Cor da barra de Total de Vencimentos
))

# Atualizando o layout da fig1_aposentados
fig1_aposentados.update_layout(
    title='Comparação de Total de Vencimentos (R$) por Mês',  # Título do gráfico
    xaxis_title='Meses',  # Título do eixo X
    yaxis_title='Valores (R$)',  # Título do eixo Y
    barmode='group',  # Agrupar as barras lado a lado
    legend_title='Categorias',  # Título da legenda
    showlegend=True  # Mostrar a legenda
)

# Gráfico de Outros Vencimentos (R$), H. Extras, Diárias, 1/3 de Férias, Total de Vencimentos (R$) (fig2_aposentados)
fig2_aposentados = go.Figure()

fig2_aposentados.add_trace(go.Bar(
    x=df_aposentados['Mês'],  # Usando os meses no eixo X
    y=df_aposentados['Outros Vencimentos (R$)'],  # Outros Vencimentos (R$) no eixo Y
    name='Outros Vencimentos',  # Nome para a legenda
    marker=dict(color='green')  # Cor da barra de Outros Vencimentos
))

fig2_aposentados.add_trace(go.Bar(
    x=df_aposentados['Mês'],  # Usando os meses no eixo X
    y=df_aposentados['H. Extras'],  # H. Extras no eixo Y
    name='H. Extras',  # Nome para a legenda
    marker=dict(color='red')  # Cor da barra de H. Extras
))

fig2_aposentados.add_trace(go.Bar(
    x=df_aposentados['Mês'],  # Usando os meses no eixo X
    y=df_aposentados['Diárias'],  # Diárias no eixo Y
    name='Diárias',  # Nome para a legenda
    marker=dict(color='blue')  # Cor da barra de Diárias
))

fig2_aposentados.add_trace(go.Bar(
    x=df_aposentados['Mês'],  # Usando os meses no eixo X
    y=df_aposentados['1/3 de Férias'],  # 1/3 de Férias no eixo Y
    name='1/3 de Férias',  # Nome para a legenda
    marker=dict(color='purple')  # Cor da barra de 1/3 de Férias
))

# Atualizando o layout da fig2_aposentados
fig2_aposentados.update_layout(
    title='Comparação de Vencimentos por Mês',  # Título do gráfico
    xaxis_title='Meses',  # Título do eixo X
    yaxis_title='Valores (R$)',  # Título do eixo Y
    barmode='group',  # Agrupar as barras lado a lado
    legend_title='Categorias',  # Título da legenda
    showlegend=True  # Mostrar a legenda
)

# Gráfico de Total de Descontos (fig3_aposentados)
fig3_aposentados = go.Figure()

fig3_aposentados.add_trace(go.Bar(
    x=df_aposentados['Mês'],  # Usando os meses no eixo X
    y=df_aposentados['Total de Descontos'],  # Total de Descontos no eixo Y
    name='Total de Descontos',  # Nome para a legenda
    marker=dict(color='pink')  # Cor da barra de Total de Descontos
))

# Atualizando o layout da fig3_aposentados
fig3_aposentados.update_layout(
    title='Total de Descontos por Mês',  # Título do gráfico
    xaxis_title='Meses',  # Título do eixo X
    yaxis_title='Descontos (R$)',  # Título do eixo Y
    barmode='group',  # Agrupar as barras lado a lado
    legend_title='Categorias',  # Título da legenda
    showlegend=True  # Mostrar a legenda
)

# Gráfico de INSS, IRRF e Outros Descontos (fig4_aposentados)
fig4_aposentados = go.Figure()

fig4_aposentados.add_trace(go.Bar(
    x=df_aposentados['Mês'],  # Usando os meses no eixo X
    y=df_aposentados['INSS'],  # INSS no eixo Y
    name='INSS',  # Nome para a legenda
    marker=dict(color='cyan')  # Cor da barra de INSS
))

fig4_aposentados.add_trace(go.Bar(
    x=df_aposentados['Mês'],  # Usando os meses no eixo X
    y=df_aposentados['IRRF'],  # IRRF no eixo Y
    name='IRRF',  # Nome para a legenda
    marker=dict(color='yellow')  # Cor da barra de IRRF
))

fig4_aposentados.add_trace(go.Bar(
    x=df_aposentados['Mês'],  # Usando os meses no eixo X
    y=df_aposentados['Outros Descontos'],  # Outros Descontos no eixo Y
    name='Outros Descontos',  # Nome para a legenda
    marker=dict(color='gray')  # Cor da barra de Outros Descontos
))

# Atualizando o layout da fig4_aposentados
fig4_aposentados.update_layout(
    title='Descontos (INSS, IRRF, Outros) por Mês',  # Título do gráfico
    xaxis_title='Meses',  # Título do eixo X
    yaxis_title='Descontos (R$)',  # Título do eixo Y
    barmode='group',  # Agrupar as barras lado a lado
    legend_title='Categorias',  # Título da legenda
    showlegend=True  # Mostrar a legenda
)

# Layout de Aposentados, com todos os gráficos
aposentados_layout = dbc.Row([

    # Gráfico de Total de Vencimentos
    dbc.Col(dbc.Card(dbc.CardBody([  
        dcc.Graph(
            id='fig1_aposentados',
            figure=fig1_aposentados,  # Preenchido com o gráfico de Total de Vencimentos
            style={'height': '400px', 'width': '100%', 'padding': '0'}
        ),
    ])), xs=12, md=12),

    # Gráfico de Qtd
    dbc.Col(dbc.Card(dbc.CardBody([  
        dcc.Graph(
            id='fig0_aposentados',
            figure=fig0_aposentados,  # Preenchido com o gráfico de Qtd
            style={'height': '400px', 'width': '100%', 'padding': '0'}
        ),
    ])), xs=12, md=12),

    # Gráfico de Outros Vencimentos (R$) e outros
    dbc.Col(dbc.Card(dbc.CardBody([  
        dcc.Graph(
            id='fig2_aposentados',
            figure=fig2_aposentados,  # Preenchido com o gráfico de Outros Vencimentos, H. Extras, etc.
            style={'height': '400px', 'width': '100%', 'padding': '0'}
        ),
    ])), xs=12, md=12),

    # Gráfico de Total de Descontos
    dbc.Col(dbc.Card(dbc.CardBody([  
        dcc.Graph(
            id='fig3_aposentados',
            figure=fig3_aposentados,  # Preenchido com o gráfico de Total de Descontos
            style={'height': '400px', 'width': '100%', 'padding': '0'}
        ),
    ])), xs=12, md=12),

    # Gráfico de INSS, IRRF, Outros Descontos
    dbc.Col(dbc.Card(dbc.CardBody([  
        dcc.Graph(
            id='fig4_aposentados',
            figure=fig4_aposentados,  # Preenchido com o gráfico de INSS, IRRF, Outros Descontos
            style={'height': '400px', 'width': '100%', 'padding': '0'}
        ),
    ])), xs=12, md=12),
])
