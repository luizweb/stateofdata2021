import streamlit as st
import pandas as pd
import time
from sklearn.linear_model import LogisticRegression

# Use the full page instead of a narrow central column
st.set_page_config(layout="wide")

icone_seta = "<svg xmlns='http://www.w3.org/2000/svg' width='20' height='20' fill='currentColor' class='bi bi-arrow-down-square' viewBox='0 0 16 16'><path fill-rule='evenodd' d='M15 2a1 1 0 0 0-1-1H2a1 1 0 0 0-1 1v12a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1V2zM0 2a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V2zm8.5 2.5a.5.5 0 0 0-1 0v5.793L5.354 8.146a.5.5 0 1 0-.708.708l3 3a.5.5 0 0 0 .708 0l3-3a.5.5 0 0 0-.708-.708L8.5 10.293V4.5z'/></svg>"
icone_moeda = "<svg xmlns='http://www.w3.org/2000/svg' width='30' height='30' fill='currentColor' class='bi bi-coin' viewBox='0 0 16 16'><path d='M5.5 9.511c.076.954.83 1.697 2.182 1.785V12h.6v-.709c1.4-.098 2.218-.846 2.218-1.932 0-.987-.626-1.496-1.745-1.76l-.473-.112V5.57c.6.068.982.396 1.074.85h1.052c-.076-.919-.864-1.638-2.126-1.716V4h-.6v.719c-1.195.117-2.01.836-2.01 1.853 0 .9.606 1.472 1.613 1.707l.397.098v2.034c-.615-.093-1.022-.43-1.114-.9H5.5zm2.177-2.166c-.59-.137-.91-.416-.91-.836 0-.47.345-.822.915-.925v1.76h-.005zm.692 1.193c.717.166 1.048.435 1.048.91 0 .542-.412.914-1.135.982V8.518l.087.02z'/><path d='M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14zm0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16z'/><path d='M8 13.5a5.5 5.5 0 1 1 0-11 5.5 5.5 0 0 1 0 11zm0 .5A6 6 0 1 0 8 2a6 6 0 0 0 0 12z'/></svg>"


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



st.markdown('#### Calculadora de Faixa Salarial')
st.write('Preencha os campos abaixo e clique no botão para o algoritmo de Machine Learning estimar a faixa salarial!')

# --- colunas --- #
# col1, col2, col3 = st.columns(3)

col1, padding, col2, padding, col3 = st.columns((10,1,10,1,10))

col1.markdown(icone_seta + ' **Dados Demográficos**', unsafe_allow_html=True)
col2.markdown(icone_seta + ' **O trabalho na Área de Dados**', unsafe_allow_html=True)
col3.markdown(icone_seta + ' **Conhecimentos Técnicos**', unsafe_allow_html=True)


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


resultado = col3.button('Estimar a faixa salarial!')


# --- Execução da Predição ---
if resultado:
    
    with st.spinner('Calculando...Por favor, aguarde...'):
        time.sleep(4)


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
        

    


    st.markdown('--------')
    st.markdown(icone_moeda + " <font size=5>Foi estimado uma <b>Faixa Salarial " + descricao + "</b></font>", unsafe_allow_html=True)
    # st.success('Obrigado por utilizar a calculadora!') 

else:
    st.markdown('--------')
    st.markdown('**O resultado será exibido aqui!** Preencha o formulário e calcule uma estimativa da faixa salarial. ')


# --- Ordem:
# faixa_idade,graduacao,nivel,experiencia,sexo,ling_sql,ling_r,ling_python,
# fonte_relacional,bd_mysql,bd_sqlserver,bd_mongodb,cloud_amazon,cloud_google,cloud_microsoft,
# bi_powerbi,bi_tableau,bi_google,trab_CLT,trab_exterior,
# regiao_Centro_Oeste,regiao_Exterior,regiao_Nordeste,regiao_Norte,regiao_Sudeste,regiao_Sul,
# forma_trab_hibrido_com_dias_fixos,forma_trab_hibrido_flexível,forma_trab_totalmente_presencial,forma_trab_totalmente_remoto,
# atuacao_Analise_Dados,atuacao_Ciencia_Dados,atuacao_Engenharia_Dados,atuacao_Gestor,atuacao_Outra
