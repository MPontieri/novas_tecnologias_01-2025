from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from utils import gerar_painel_financeiro, gerar_grafico_verba_projeto, gerar_grafico_progresso_projeto

from utils import gerar_painel_financeiro
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

if not os.path.exists("static/graficos"):
    os.makedirs("static/graficos")

df = pd.read_csv("dados.csv", dtype={"ID": str})
gerar_painel_financeiro()


# NOVA HOMEPAGE
@app.get("/", response_class=HTMLResponse)
async def pagina_inicial(request: Request):
    return templates.TemplateResponse("inicial.html", {"request": request})

# CATÁLOGO DE PROJETOS (index.html)
@app.get("/projetos", response_class=HTMLResponse)
async def catalogo_projetos(request: Request):
    termo_busca = request.query_params.get("busca", "").lower()
    categoria_ativa = request.query_params.get("categoria", "todos")

    projetos_filtrados = df.copy()

    if termo_busca:
        projetos_filtrados = df[df.apply(
            lambda row: termo_busca in str(row['Nome do Projeto']).lower() or termo_busca in str(row['ID']), axis=1)]
    
    if categoria_ativa != "todos":
        projetos_filtrados = projetos_filtrados[projetos_filtrados['Tipo'].str.strip().str.lower() == categoria_ativa.lower()] # usando a coluna Tipo no csv


    projetos = projetos_filtrados.to_dict(orient="records")
    return templates.TemplateResponse("index.html", {
        "request": request,
        "projetos": projetos,
        "busca": termo_busca,
        "categoria_ativa": categoria_ativa # passa a categoria ativa para o template
    })

@app.get("/relatorio/{id}", response_class=HTMLResponse)
async def relatorio(request: Request, id: str):
    projeto = df[df['ID'] == id]

    if projeto.empty:
        return HTMLResponse(content="Projeto não encontrado", status_code=404)

    projeto = projeto.iloc[0].to_dict()

    grafico_verba_path = gerar_grafico_verba_projeto(projeto, id)
    grafico_progresso_path = gerar_grafico_progresso_projeto(projeto, id)

    return templates.TemplateResponse("relatorio.html", {
        "request": request,
        "projeto": projeto,
        "grafico_verba_path": grafico_verba_path,
        "grafico_progresso_path": grafico_progresso_path

    })

@app.get("/", response_class=HTMLResponse)
async def homepage(request: Request):
    termo_busca = request.query_params.get("busca", "").lower()
    
    if termo_busca:
        projetos_filtrados = df[df.apply(lambda row: termo_busca in str(row['Nome do Projeto']).lower() or termo_busca in str(row['ID']), axis=1)]
    else:
        projetos_filtrados = df

    projetos = projetos_filtrados.to_dict(orient="records")
    return templates.TemplateResponse("index.html", {
        "request": request,
        "projetos": projetos,
        "busca": termo_busca
    })

@app.get("/painel", response_class=HTMLResponse)
async def painel_financeiro(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

