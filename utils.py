import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os

def gerar_painel_financeiro(output_dir="static/graficos"):
    os.makedirs(output_dir, exist_ok=True)

    def gerar_arquivo(path, gerar_func):
        if not os.path.exists(path):
            gerar_func()
            plt.savefig(path)
            plt.close()

    # 1. Net Profit
    gerar_arquivo(f"{output_dir}/net_profit.png", lambda: (
        plt.figure(figsize=(4, 2)),
        plt.axis('off'),
        plt.text(0.5, 0.7, 'Net Profit', ha='center', fontsize=12, weight='bold'),
        plt.text(0.5, 0.4, '$58.20M', ha='center', fontsize=20, color='green', weight='bold')
    ))

    # 2. Net Sales
    gerar_arquivo(f"{output_dir}/net_sales.png", lambda: (
        plt.figure(figsize=(4, 2)),
        plt.axis('off'),
        plt.text(0.5, 0.7, 'Net Sales', ha='center', fontsize=12, weight='bold'),
        plt.text(0.5, 0.4, '$416.78M', ha='center', fontsize=20, color='red', weight='bold')
    ))

    # 3. Pizza - COGS Breakdown
    gerar_arquivo(f"{output_dir}/cogs_pizza.png", lambda: (
        plt.figure(figsize=(4, 4)),
        plt.pie([23.4, 19.4, 19.2, 19.2, 18.8],
                labels=['Shipping', 'Materials', 'Returns', 'Production', 'Labor'],
                autopct='%1.1f%%',
                colors=['#006D77', '#83C5BE', '#EDF6F9', '#FFDDD2', '#E29578'],
                startangle=140),
        plt.title("Cost of Goods Sold Breakdown")
    ))

    # 4. Barras Horizontais - Profitability Ratios
    gerar_arquivo(f"{output_dir}/profit_ratios.png", lambda: (
        plt.figure(figsize=(6, 3)),
        plt.barh(
            ['Gross Profit Margin', 'Operating Profit Margin', 'Pretax Profit Margin', 'Net Profit Margin'],
            [30.5, 25.61, 17.61, 13.46],
            color=['#264653', '#2a9d8f', '#e9c46a', '#f4a261']
        ),
        plt.xlabel('%'),
        plt.title('Profitability Indicator Ratios')
    ))

    # 5. Linhas - Net Profit Margin por Canal
    gerar_arquivo(f"{output_dir}/margin_region.png", lambda: (
        pd.DataFrame({
            'Quarter': ['2022 Q1', '2022 Q2', '2022 Q3', '2022 Q4'],
            'Online': [25, -100, 10, 15],
            'Retail': [20, 15, 10, 12],
            'Other': [22, 18, 25, 24],
            'Wholesales': [15, 14, 17, 16]
        }).set_index('Quarter').plot(marker='o', figsize=(6, 3)),
        plt.ylabel('Net Profit Margin %'),
        plt.title('Net Profit Margin by Region / Channel'),
        plt.grid(True)
    ))

    # 6. Barras + Linha - Comparativo
    gerar_arquivo(f"{output_dir}/profit_comparison.png", lambda: (
        plt.figure(figsize=(6, 3)),
        plt.bar(np.arange(4) - 0.25, [13, 14, 10, 15], 0.25, label='Previous Year', color='#264653'),
        plt.bar(np.arange(4), [16, 14, 13, 17], 0.25, label='Current Year - Actual', color='#2a9d8f'),
        plt.plot(np.arange(4) + 0.25, [15, 15, 15, 15], marker='o', color='orange', label='Current Year - Target'),
        plt.xticks(np.arange(4), ['2022 Q1', '2022 Q2', '2022 Q3', '2022 Q4']),
        plt.ylabel('Net Profit %'),
        plt.title('Net Profit: Past Year vs Target vs Actual'),
        plt.legend()
    ))

def gerar_grafico_verba_projeto(projeto_data, id_projeto, output_dir="static/graficos"):
    os.makedirs(output_dir, exist_ok=True)
    
    labels = ['Verba Gasta', 'Verba Disponível']
    valores = [float(projeto_data['Verba Gasta (R$)']), float(projeto_data['Verba Disponível (R$)'])]

    if sum(valores) == 0:
        print(f"Aviso: Não há dados de verba para o projeto {id_projeto}. Gráfico não será gerado.")
        return None
    
    plt.figure(figsize=(6, 6))
    plt.pie(valores, labels=labels, autopct='%1.1f%%', startangle=90, colors=['#FF6347', '#4682B4'])
    plt.title(f"Distribuição de Verba - {projeto_data['Nome do Projeto']}")

    grafico_path = f"{output_dir}/grafico_verba_{id_projeto}.png"
    plt.savefig(grafico_path)
    plt.close()
    return "/" + grafico_path

def gerar_grafico_progresso_projeto(projeto_data, id_projeto, output_dir="static/graficos"):
    os.makedirs(output_dir, exist_ok=True)

    conclusao_percentual = float(projeto_data['Percentual de Conclusão (%)'])
    valores_barras = [conclusao_percentual, 100 - conclusao_percentual]
    labels_barras = ['Concluído', 'Restante']
    cores_barras = ['#28a745', '#dc3545']

    plt.figure(figsize=(8, 4))
    plt.bar(labels_barras, valores_barras, color=cores_barras)
    plt.ylabel('Percentual (%)')
    plt.title(f"Progresso do Projeto: {projeto_data['Nome do Projeto']}")
    plt.ylim(0, 100)
    
    plt.text(labels_barras[0], conclusao_percentual + 2, f'{conclusao_percentual:.2f}%', ha='center', va='bottom')
    plt.text(labels_barras[1], (100 - conclusao_percentual) + 2, f'{100 - conclusao_percentual:.2f}%', ha='center', va='bottom')

    grafico_path = f"{output_dir}/grafico_progresso_{id_projeto}.png"
    plt.savefig(grafico_path)
    plt.close()
    return "/" + grafico_path
