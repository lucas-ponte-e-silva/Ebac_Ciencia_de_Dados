import streamlit as st
import nbformat
import ast

def extract_code_from_notebook(notebook_path):
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)
    
    code_cells = [cell for cell in nb.cells if cell.cell_type == 'code']
    python_code = '\n\n'.join(cell.source for cell in code_cells)
    return python_code

def execute_code(code):
    tree = ast.parse(code)
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            exec(compile(ast.parse(ast.unparse(node)), filename="<ast>", mode="exec"))
    
    for node in tree.body:
        if not isinstance(node, ast.FunctionDef):
            exec(compile(ast.parse(ast.unparse(node)), filename="<ast>", mode="exec"))

# Caminho para o seu arquivo .ipynb
notebook_path = 'seu_notebook.ipynb'

# Extrair o código do notebook
code = extract_code_from_notebook(notebook_path)

# Interface Streamlit
st.title('Previsão de Renda')

# Campos de entrada para os dados
sexo = st.selectbox('Sexo', ['M', 'F'])
posse_de_veiculo = st.checkbox('Possui veículo')
posse_de_imovel = st.checkbox('Possui imóvel')
qtd_filhos = st.number_input('Quantidade de filhos', min_value=0, step=1)
tipo_renda = st.selectbox('Tipo de renda', ['Assalariado', 'Empresário', 'Servidor público', 'Pensionista', 'Bolsista'])
educacao = st.selectbox('Educação', ['Primário', 'Secundário', 'Superior incompleto', 'Superior completo', 'Pós graduação'])
estado_civil = st.selectbox('Estado civil', ['Solteiro', 'Casado', 'Separado', 'Viúvo', 'União'])
tipo_residencia = st.selectbox('Tipo de residência', ['Casa', 'Apartamento', 'Com os pais', 'Aluguel', 'Outros'])
idade = st.number_input('Idade', min_value=18, max_value=100, step=1)
tempo_emprego = st.number_input('Tempo de emprego (anos)', min_value=0, step=1)
qt_pessoas_residencia = st.number_input('Quantidade de pessoas na residência', min_value=1, step=1)

if st.button('Prever Renda'):
    dados_entrada = {
        'sexo': sexo,
        'posse_de_veiculo': posse_de_veiculo,
        'posse_de_imovel': posse_de_imovel,
        'qtd_filhos': qtd_filhos,
        'tipo_renda': tipo_renda,
        'educacao': educacao,
        'estado_civil': estado_civil,
        'tipo_residencia': tipo_residencia,
        'idade': idade,
        'tempo_emprego': tempo_emprego,
        'qt_pessoas_residencia': qt_pessoas_residencia
    }
    
    # Executar o código do notebook
    execute_code(code)
    
    # Criar DataFrame com os dados de entrada
    entrada = pd.DataFrame([dados_entrada])
    
    # Aplicar one-hot encoding
    entrada_encoded = pd.get_dummies(entrada)
    
    # Garantir que todas as colunas do modelo estejam presentes
    entrada_processada = entrada_encoded.reindex(columns=X.columns, fill_value=0)
    
    # Fazer a previsão
    renda_prevista = melhor_modelo.predict(entrada_processada)[0]
    
    st.write(f"Renda estimada: R${renda_prevista:.2f}")

    # Visualizar importância das features
    st.subheader("Top 10 Features Mais Importantes")
    feature_importance = pd.DataFrame({
        'feature': X.columns,
        'importance': melhor_modelo.feature_importances_
    }).sort_values('importance', ascending=False)
    
    st.bar_chart(feature_importance.head(10).set_index('feature'))