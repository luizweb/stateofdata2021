import streamlit as st
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression

df = pd.read_csv('dados_modelo_stateofdata.csv', sep=";", index_col=0, low_memory=False)
# st.write(df)


# --- Variaveis preditoras e target
X = df.drop('faixa_salarial', axis=1) 
y = df[['faixa_salarial']] 

dicio_faixa_salarial = {
    "Menos de R\$ 1.000/mês" : 1,
    "de R\$ 1.001/mês a R\$ 2.000/mês" : 2,
    "de R\$ 2.001/mês a R\$ 3000/mês" : 3,
    "de R\$ 3.001/mês a R\$ 4.000/mês" : 4,
    "de R\$ 4.001/mês a R\$ 6.000/mês" : 5,
    "de R\$ 6.001/mês a R\$ 8.000/mês" : 6,
    "de R\$ 8.001/mês a R\$ 12.000/mês" : 7,
    "de R\$ 12.001/mês a R\$ 16.000/mês" : 8,
    "de R\$ 16.001/mês a R\$ 20.000/mês" : 9,
    "de R\$ 20.001/mês a R\$ 25.000/mês" : 10,
    "de R\$ 25.001/mês a R\$ 30.000/mês" : 11,
    "de R\$ 30.001/mês a R\$ 40.000/mês" : 12,
    "Acima de R\$ 40.001/mês" : 13
    }



#st.title('State of Data 2021')
#st.header('State of Data 2021')
st.subheader('State of Data 2021')

# --- colunas --- #
col1, col2, col3 = st.columns(3)
col1.write('Dados Demográficos')
col2.write('O trabalho na área de dados')
col3.write('Conhecimentos técnicos')


# --- coluna 1 --- #
# --- Dados Demográficos ---#
faixa_idade = {"17-21" : 1,
                "22-24" : 2,
                "25-29" : 3,
                "30-34" : 4,
                "35-39" : 5,
                "40-44" : 6,
                "45-49" : 7,
                "50-54" : 8,
                "55+" : 9}
faixa_idade_sel = col1.selectbox('Faixa de Idade', faixa_idade)

sexo = {"Feminino":1, "Masculino":0}
sexo_sel = col1.select_slider('Sexo', options=sexo)

regiao = ["Centro Oeste","Exterior","Nordeste","Norte","Sudeste","Sul"]
regiao_sel = col1.selectbox('Região onde mora', regiao)

graduacao = {"Não tenho graduação formal":0,
                 "Estudante de Graduação":1,
                 "Graduação/Bacharelado":2,
                 "Pós-graduação":3,
                 "Mestrado":4,
                 "Doutorado ou Phd":5}
graduacao_sel = col1.selectbox('Graduação', graduacao)


# --- coluna 2 --- #
# --- O trabalho na área de dados ---#

atuacao = ["Analista de Dados", "Cientista de Dados", "Engenheiro de Dados", "Gestor", "Outra"]
atuacao_sel = col2.selectbox('Atuação', atuacao)

nivel = {
        "Júnior" : 1,
        "Pleno" : 2,
        "Sênior" : 3,
        "Outros": 4
        }
nivel_sel = col2.selectbox('Nível', nivel)


experiencia = {
            "Não tenho experiência na área de dados" : 0,
            "Menos de 1 ano" : 1,
            "de 1 a 2 anos" : 2,
            "de 2 a 3 anos": 3,
            "de 4 a 5 anos": 4,
            "de 6 a 10 anos": 5,
            "Mais de 10 anos": 6
            }
experiencia_sel = col2.selectbox('Experiência na área de dados', experiencia)

trab_clt = {"Outros":0, "CLT":1}
trab_clt_sel = col2.select_slider('Tipo de trabalho', options=trab_clt)

trab_exterior = {"Brasil":0, "Exterior":1}
trab_exterior_sel = col2.select_slider('Local do trabalho', options=trab_exterior)

forma_trab = ["hibrido com dias fixos","hibrido flexível","totalmente presencial","totalmente remoto"]
forma_trab_sel = col2.selectbox('Forma de trabalho', forma_trab)

# --- coluna 3 --- #
# --- Conhecimentos técnicos ---#
#linguagem = ["Nenhuma", "Python", "R", "SQL"]
#linguagem_sel = col3.selectbox('Principal linguagem', linguagem)
col3.write("Principais linguagens:")
python_sel = col3.checkbox("Python", value=True)
r_sel = col3.checkbox("R")
sql_sel = col3.checkbox("SQL")


fonte_relacional = {"NoSQL":0,"SQL":1}
fonte_relacional_sel = col3.select_slider('Fontes de Dados:', options=fonte_relacional)

# bancos_dados = ["Nenhum","SQL Server", "MySQL", "MongoDB"]
# bancos_dados_sel = col3.selectbox('Principal Banco de Dados', bancos_dados)
col3.write("Principais Bancos de Dados:")
sqlserver_sel = col3.checkbox("SQL Server", value=True)
mysql_sel = col3.checkbox("MySQL")
mongodb_sel = col3.checkbox("MongoDB")


#clouds = ["Nenhuma","AWS - Amazon", "Azure - Microsoft", "Google Cloud"]
#clouds_sel = col3.selectbox('Principal plataforma de Cloud', clouds)
col3.write("Principais plataformas de Cloud:")
aws_sel = col3.checkbox("AWS - Amazon")
azure_sel = col3.checkbox("Azure - Microsoft")
googlecloud_sel = col3.checkbox("Google Cloud")


#ferramenta_bi = ["Nenhuma","Power BI", "Tableau", "Google DS"]
#ferramenta_bi_sel = col3.selectbox('Principal ferramenta BI', ferramenta_bi)
col3.write("Principais ferramentas de BI:")
powerbi_sel = col3.checkbox("Power BI")
tableau_sel = col3.checkbox("Tableau")
googleds_sel = col3.checkbox("Google DS")



resultado = col3.button('Descubra sua faixa salarial')


# --- Execução da Predição ---
if resultado:
    
    def buscar_dicionario(dicio, selecao):
        for k,v in dicio.items():
            if k == selecao:
                return selecao, v

    def buscar_lista(lista, selecao):
        lista_resultado = []
        for v in lista:
            if v == selecao:
                lista_resultado.append(1)
            else:
                lista_resultado.append(0)
        return lista_resultado

    def buscar_checkbox(selecao):
        if selecao:
            return 1
        else:
            return 0

    def buscar_resultado(dicio, selecao):
        for k,v in dicio.items():
            if v == selecao:
                return selecao, k

    
    #st.write(f"Dados demográficos: " + faixa_idade_sel,sexo_sel,regiao_sel,graduacao_sel,
    #        "O trabalho na área de dados: " + atuacao_sel,nivel_sel,experiencia_sel,trab_clt_sel,trab_exterior_sel,forma_trab_sel,
    #        "Conhecimentos técnicos: ",python_sel,r_sel,sql_sel,fonte_relacional_sel,sqlserver_sel,mysql_sel,mongodb_sel,aws_sel,azure_sel,googlecloud_sel,powerbi_sel,tableau_sel,googleds_sel)

    
    regressao_logistica = LogisticRegression(max_iter=1000)
    regressao_logistica.fit(X, y.values.flatten())

    predicao = [
        buscar_dicionario(faixa_idade, faixa_idade_sel)[1],
        buscar_dicionario(graduacao, graduacao_sel)[1],
        buscar_dicionario(nivel, nivel_sel)[1],
        buscar_dicionario(experiencia, experiencia_sel)[1],
        buscar_dicionario(sexo, sexo_sel)[1],
        buscar_checkbox(sql_sel),
        buscar_checkbox(r_sel),
        buscar_checkbox(python_sel),
        buscar_dicionario(fonte_relacional, fonte_relacional_sel)[1],
        buscar_checkbox(mysql_sel),
        buscar_checkbox(sqlserver_sel),
        buscar_checkbox(mongodb_sel),
        buscar_checkbox(aws_sel),
        buscar_checkbox(googlecloud_sel),
        buscar_checkbox(azure_sel),
        buscar_checkbox(powerbi_sel),
        buscar_checkbox(tableau_sel),
        buscar_checkbox(googleds_sel),
        buscar_dicionario(trab_clt, trab_clt_sel)[1],
        buscar_dicionario(trab_exterior, trab_exterior_sel)[1]]
    predicao = predicao + buscar_lista(regiao, regiao_sel)   
    predicao = predicao + buscar_lista(forma_trab, forma_trab_sel)
    predicao = predicao + buscar_lista(atuacao, atuacao_sel)

    # st.write(predicao)

    resultado = regressao_logistica.predict([predicao])
    descricao = str(buscar_resultado(dicio_faixa_salarial, resultado[0].astype(int))[1])
        

    # .str.replace(, , regex=True)
    st.subheader("Resultado: faixa salaria " + descricao)




# --- Ordem:
# faixa_idade,graduacao,nivel,experiencia,sexo,ling_sql,ling_r,ling_python,
# fonte_relacional,bd_mysql,bd_sqlserver,bd_mongodb,cloud_amazon,cloud_google,cloud_microsoft,
# bi_powerbi,bi_tableau,bi_google,trab_CLT,trab_exterior,
# regiao_Centro_Oeste,regiao_Exterior,regiao_Nordeste,regiao_Norte,regiao_Sudeste,regiao_Sul,
# forma_trab_hibrido_com_dias_fixos,forma_trab_hibrido_flexível,forma_trab_totalmente_presencial,forma_trab_totalmente_remoto,
# atuacao_Analise_Dados,atuacao_Ciencia_Dados,atuacao_Engenharia_Dados,atuacao_Gestor,atuacao_Outra

