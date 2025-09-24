import json
import os
from datetime import datetime
import tkinter as tk
from tkinter import messagebox, scrolledtext

# Cria a pasta 'data' se não existir
os.makedirs('data', exist_ok=True)

# Nome do arquivo para salvar as tarefas (na pasta data/)
ARQUIVO_TAREFAS = 'data/tarefas_escolares.json'


def carregar_tarefas():
    """
    Carrega as tarefas salvas do arquivo JSON.
    Se o arquivo não existir, retorna uma lista vazia.
    """
    if os.path.exists(ARQUIVO_TAREFAS):
        with open(ARQUIVO_TAREFAS, 'r', encoding='utf-8') as arquivo:
            return json.load(arquivo)
    return []


def salvar_tarefas(tarefas):
    """
    Salva as tarefas no arquivo JSON.
    """
    with open(ARQUIVO_TAREFAS, 'w', encoding='utf-8') as arquivo:
        json.dump(tarefas, arquivo, ensure_ascii=False, indent=4)


class OrganizadorTarefas:
    def __init__(self, root):
        self.root = root
        self.root.title("Organizador de Tarefas Escolares")
        self.root.geometry("500x400")
        self.tarefas = carregar_tarefas()

        # Campo de entrada para descrição da tarefa
        tk.Label(root, text="Descrição da Tarefa:", font=("Arial", 10)).pack(pady=5)
        self.entry_descricao = tk.Entry(root, width=50, font=("Arial", 10))
        self.entry_descricao.pack(pady=5)

        # Botão Adicionar
        tk.Button(root, text="Adicionar Tarefa", command=self.adicionar_tarefa,
                  bg="lightgreen", font=("Arial", 10)).pack(pady=5)

        # Lista de tarefas (com scroll)
        tk.Label(root, text="Lista de Tarefas:", font=("Arial", 10)).pack(anchor="w", padx=10, pady=5)
        self.lista_tarefas = tk.Listbox(root, width=60, height=10, font=("Arial", 9))
        scrollbar = tk.Scrollbar(root)
        self.lista_tarefas.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.lista_tarefas.yview)
        self.lista_tarefas.pack(side="left", fill="both", expand=True, padx=10, pady=5)
        scrollbar.pack(side="right", fill="y", pady=5)

        # Botões para remover e atualizar
        frame_botoes = tk.Frame(root)
        frame_botoes.pack(pady=10)

        tk.Button(frame_botoes, text="Remover Tarefa Selecionada", command=self.remover_tarefa,
                  bg="lightcoral", font=("Arial", 10)).pack(side="left", padx=5)
        tk.Button(frame_botoes, text="Atualizar Lista", command=self.atualizar_lista,
                  bg="lightblue", font=("Arial", 10)).pack(side="left", padx=5)

        # Área de status
        self.status = tk.Label(root, text="Bem-vindo! Adicione sua primeira tarefa.",
                               font=("Arial", 9), fg="blue")
        self.status.pack(pady=10)

        # Carrega a lista inicial
        self.atualizar_lista()

    def adicionar_tarefa(self):
        descricao = self.entry_descricao.get().strip()
        if descricao:
            tarefa = {
                'descricao': descricao,
                'data_criacao': datetime.now().strftime('%d/%m/%Y %H:%M')
            }
            self.tarefas.append(tarefa)
            salvar_tarefas(self.tarefas)
            self.entry_descricao.delete(0, tk.END)  # Limpa o campo
            self.atualizar_lista()
            self.status.config(text="Tarefa adicionada com sucesso!", fg="green")
        else:
            messagebox.showwarning("Aviso", "A descrição não pode estar vazia!")

    def atualizar_lista(self):
        self.lista_tarefas.delete(0, tk.END)
        if not self.tarefas:
            self.lista_tarefas.insert(tk.END, "Nenhuma tarefa cadastrada.")
            self.status.config(text="Nenhuma tarefa. Adicione uma!", fg="orange")
            return

        for i, tarefa in enumerate(self.tarefas, 1):
            texto = f"{i}. {tarefa['descricao']} (Criada em: {tarefa['data_criacao']})"
            self.lista_tarefas.insert(tk.END, texto)
        self.status.config(text=f"{len(self.tarefas)} tarefas salvas.", fg="blue")

    def remover_tarefa(self):
        selecao = self.lista_tarefas.curselection()
        if selecao:
            indice = selecao[0]
            tarefa_removida = self.tarefas.pop(indice)
            salvar_tarefas(self.tarefas)
            self.atualizar_lista()
            self.status.config(text=f"Tarefa removida: {tarefa_removida['descricao']}", fg="red")
        else:
            messagebox.showwarning("Aviso", "Selecione uma tarefa na lista para remover!")


# Executa a aplicação gráfica
if __name__ == "__main__":
    root = tk.Tk()
    app = OrganizadorTarefas(root)
    root.mainloop()