import os
import pyaes
import tkinter as tk
from tkinter import filedialog, messagebox
import threading

def encrypt_file_thread():
    threading.Thread(target=encrypt_file, daemon=True).start()

def decrypt_file_thread():
    threading.Thread(target=decrypt_file, daemon=True).start()

def select_file():
    file_path = filedialog.askopenfilename(title="Selecione um arquivo")
    entry_file.delete(0, tk.END)
    entry_file.insert(0, file_path)

def encrypt_file():
    file_name = entry_file.get()
    key = entry_key.get().encode()
    
    if not file_name or not key:
        messagebox.showerror("Erro", "Selecione um arquivo e insira uma chave válida.")
        return
    
    if len(key) not in [16, 24, 32]:
        messagebox.showerror("Erro", "A chave deve ter 16, 24 ou 32 caracteres.")
        return
    
    with open(file_name, 'rb') as file:
        file_data = file.read()
    
    aes = pyaes.AESModeOfOperationCTR(key)
    crypto_data = aes.encrypt(file_data)
    
    os.remove(file_name)
    new_file_name = file_name + ".arquivocrypto"
    with open(new_file_name, 'wb') as new_file:
        new_file.write(crypto_data)
    
    messagebox.showinfo("Sucesso", f"Arquivo criptografado salvo como:\n{new_file_name}")

def decrypt_file():
    file_name = entry_file.get()
    key = entry_key.get().encode()
    
    if not file_name or not key:
        messagebox.showerror("Erro", "Selecione um arquivo e insira uma chave válida.")
        return
    
    if len(key) not in [16, 24, 32]:
        messagebox.showerror("Erro", "A chave deve ter 16, 24 ou 32 caracteres.")
        return
    
    with open(file_name, 'rb') as file:
        encrypted_data = file.read()
    
    aes = pyaes.AESModeOfOperationCTR(key)
    decrypted_data = aes.decrypt(encrypted_data)
    
    original_file_name = file_name.replace(".arquivocrypto", "")
    with open(original_file_name, 'wb') as file:
        file.write(decrypted_data)
    
    messagebox.showinfo("Sucesso", f"Arquivo descriptografado salvo como:\n{original_file_name}")

# Criando a interface
tk_root = tk.Tk()
tk_root.title("Criptografia de Arquivos")

tk.Label(tk_root, text="Arquivo:").grid(row=0, column=0, padx=10, pady=5)
entry_file = tk.Entry(tk_root, width=50)
entry_file.grid(row=0, column=1, padx=10, pady=5)
tk.Button(tk_root, text="Selecionar", command=select_file).grid(row=0, column=2, padx=10, pady=5)

tk.Label(tk_root, text="Chave (16, 24 ou 32 caracteres):").grid(row=1, column=0, padx=10, pady=5)
entry_key = tk.Entry(tk_root, width=50, show="*")
entry_key.grid(row=1, column=1, padx=10, pady=5)

tk.Button(tk_root, text="Criptografar", command=encrypt_file).grid(row=2, column=0, columnspan=2, pady=10)
tk.Button(tk_root, text="Descriptografar", command=decrypt_file).grid(row=2, column=1, columnspan=2, pady=10)

tk_root.mainloop()
