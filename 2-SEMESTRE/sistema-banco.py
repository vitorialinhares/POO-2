import tkinter as tk
from tkinter import messagebox, simpledialog


class Endereco:
    def __init__(self, rua, numero, bairro, cidade):
        self.__rua = rua
        self.__numero = numero
        self.__bairro = bairro
        self.__cidade = cidade
    def get_rua(self):
        return self.__rua
    def get_numero(self):
        return self.__numero
    def get_bairro(self):
        return self.__bairro
    def get_cidade(self):
        return self.__cidade


class Cliente:
    def __init__(self, nome, cpf, endereco):
        self.__nome = nome
        self.__cpf = cpf
        self.__endereco = endereco
        self.__contas = []

    def get_nome(self):
        return self.__nome
    def get_cpf(self):
        return self.__cpf
    def get_endereco(self):
        return self.__endereco
    def adicionar_conta(self, conta):
        self.__contas.append(conta)


class ContaBancaria:
    numeros_contas = []

    def __init__(self, cliente, numero, saldo):
        self.__cliente = cliente
        self.__numero = numero

        if saldo < 0:
            self.__saldo = 0
        else:
            self.__saldo = saldo

        ContaBancaria.numeros_contas.append(numero)
        cliente.adicionar_conta(self)

    def get_titular(self):
        return self.__cliente

    def get_numero(self):
        return self.__numero

    def get_saldo(self):
        return self.__saldo

    def depositar(self, valor):
        if valor > 0:
            self.__saldo += valor
            return True
        return False

    def sacar(self, valor):
        if valor > 0 and self.__saldo >= valor:
            self.__saldo -= valor
            return True
        return False

    def transferir(self, valor, conta_destino):
        if self.sacar(valor):
            conta_destino.depositar(valor)
            return True
        return False

    def exibir_dados(self):
        endereco = self.__cliente.get_endereco()
        return (
            f"Nome: {self.__cliente.get_nome()}\n"
            f"CPF: {self.__cliente.get_cpf()}\n"
            f"Rua: {endereco.get_rua()}\n"
            f"Bairro: {endereco.get_bairro()}\n"
            f"Conta: {self.__numero}\n"
            f"Saldo: R$ {self.__saldo:.2f}"
        )

    @classmethod
    def existe_conta_duplicada(cls):
        return len(cls.numeros_contas) != len(set(cls.numeros_contas))
    @classmethod
    def contas_duplicadas(cls):
        duplicadas = []

        for numero in cls.numeros_contas:
            if cls.numeros_contas.count(numero) > 1 and numero not in duplicadas:
                duplicadas.append(numero)

        return duplicadas


class BancoApp:
    def __init__(self, janela):
        self.janela = janela
        self.janela.title("Sistema Bancário - POO em Python")
        self.janela.geometry("850x400")

        end1 = Endereco("Rua A", 100, "Centro", "São Paulo")
        cliente1 = Cliente("Mateus", "000.000.000-01", end1)

        end2 = Endereco("Rua B", 50, "Jardim", "São Paulo")
        cliente2 = Cliente("Pedro", "111.111.111-11", end2)

        end3 = Endereco("Rua C", 200, "Vila Nova", "São Paulo")
        cliente3 = Cliente("Esther", "222.222.222-22", end3)

        self.contas = [
            ContaBancaria(cliente1, 1002, 1000),
            ContaBancaria(cliente2, 1003, 300),
            ContaBancaria(cliente3, 1004, 20)
        ]

        self.criar_interface()

    def criar_interface(self):
        titulo = tk.Label(
            self.janela,
            text="Banco Python - Contas Bancárias",
            font=("Arial", 18, "bold")
        )
        titulo.pack(pady=15)

        self.frame_contas = tk.Frame(self.janela)
        self.frame_contas.pack()

        self.atualizar_tela()

    def atualizar_tela(self):
        for widget in self.frame_contas.winfo_children():
            widget.destroy()
        for conta in self.contas:
            frame = tk.Frame(
                self.frame_contas,
                borderwidth=2,
                relief="groove",
                padx=10,
                pady=10
            )
            frame.pack(side="left", padx=10, pady=10)
            lbl_titular = tk.Label(
                frame,
                text=conta.get_titular().get_nome(),
                font=("Arial", 14, "bold")
            )
            lbl_titular.pack()
            lbl_numero = tk.Label(
                frame,
                text=f"Conta: {conta.get_numero()}"
            )
            lbl_numero.pack()
            lbl_saldo = tk.Label(
                frame,
                text=f"Saldo: R$ {conta.get_saldo():.2f}",
                font=("Arial", 12)
            )
            lbl_saldo.pack(pady=5)
            btn_depositar = tk.Button(
                frame,
                text="Depositar",
                width=15,
                command=lambda c=conta: self.depositar(c)
            )
            btn_depositar.pack(pady=2)
            btn_sacar = tk.Button(
                frame,
                text="Sacar",
                width=15,
                command=lambda c=conta: self.sacar(c)
            )
            btn_sacar.pack(pady=2)
            btn_transferir = tk.Button(
                frame,
                text="Transferir",
                width=15,
                command=lambda c=conta: self.transferir(c)
            )
            btn_transferir.pack(pady=2)
            btn_dados = tk.Button(
                frame,
                text="Exibir Dados",
                width=15,
                command=lambda c=conta: self.exibir_dados(c)
            )
            btn_dados.pack(pady=2)
    def depositar(self, conta):
        valor = simpledialog.askfloat(
            "Depósito",
            "Digite o valor do depósito:"
        )
        if valor is not None:
            if conta.depositar(valor):
                messagebox.showinfo(
                    "Sucesso",
                    "Depósito realizado."
                )
            else:
                messagebox.showerror(
                    "Erro",
                    "Valor inválido."
                )
        self.atualizar_tela()
    def sacar(self, conta):
        valor = simpledialog.askfloat(
            "Saque",
            "Digite o valor do saque:"
        )
        if valor is not None:
            if conta.sacar(valor):
                messagebox.showinfo(
                    "Sucesso",
                    "Saque realizado."
                )
            else:
                messagebox.showerror(
                    "Erro",
                    "Saldo insuficiente ou valor inválido."
                )

        self.atualizar_tela()

    def transferir(self, conta_origem):
        valor = simpledialog.askfloat(
            "Transferência",
            "Digite o valor:"
        )
        if valor is None:
            return
        numero_destino = simpledialog.askinteger(
            "Transferência",
            "Digite o número da conta destino:"
        )
        conta_destino = None
        for conta in self.contas:
            if conta.get_numero() == numero_destino:
                conta_destino = conta
                break
        if conta_destino is None:
            messagebox.showerror(
                "Erro",
                "Conta destino não encontrada."
            )
            return
        if conta_origem == conta_destino:
            messagebox.showerror(
                "Erro",
                "Não é possível transferir para a mesma conta."
            )
            return
        if conta_origem.transferir(
            valor,
            conta_destino
        ):
            messagebox.showinfo(
                "Sucesso",
                "Transferência realizada."
            )
        else:
            messagebox.showerror(
                "Erro",
                "Saldo insuficiente ou valor inválido."
            )

        self.atualizar_tela()

        def exibir_dados(self, conta):
            dados = conta.exibir_dados()
        if ContaBancaria.existe_conta_duplicada():
            dados += (
                "\n\nExistem contas duplicadas."
                f"\nNúmeros duplicados: "
                f"{ContaBancaria.contas_duplicadas()}"
            )
        else:
            dados += "\n\nNão existem contas duplicadas."
        messagebox.showinfo(
            "Dados da Conta",
            dados
        )


janela = tk.Tk()
app = BancoApp(janela)
janela.mainloop()