import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
import asyncio
import os

# Set event loop policy for Windows
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

async def execute_notebook(parametro, notebook_path):
    # Get the directory of the notebook
    notebook_dir = os.path.dirname(notebook_path)

    with open(notebook_path) as ff:
        nb_in = nbformat.read(ff, nbformat.NO_CONVERT)

    # Inject the parameter into the notebook cells
    parameter_code = f"parametro = {parametro}"
    code_cell = nbformat.v4.new_code_cell(parameter_code)
    nb_in.cells.insert(0, code_cell)

    # Create and configure the ExecutePreprocessor
    ep = ExecutePreprocessor(timeout=600, kernel_name='python3')

    # Execute the notebook with the modified content
    return ep.preprocess(nb_in, {'metadata': {'path': notebook_dir}})

# Create a new event loop
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

# Número de vezes que deseja executar o notebook
num_execucoes = 10

# Lista de caminhos dos notebooks
notebook_paths = [
    './Novatos/Dados/dadosFicticios.ipynb',
    './Veteranos/Dados/dadosFicticios.ipynb'
]

# Create a list to store the tasks
tasks = []

# Loop para executar os notebooks várias vezes com diferentes parâmetros
for notebook_path in notebook_paths:
    for i in range(num_execucoes):
        # Parâmetro que você deseja passar para o notebook
        parametro = i + 1
        
        # Create a task for each notebook execution
        task = loop.create_task(execute_notebook(parametro, notebook_path))
        tasks.append(task)

# Run all tasks concurrently
loop.run_until_complete(asyncio.gather(*tasks))

# Close the event loop
loop.close()