from custom_rsa import *
import os
from tkinter import *
from tkinter import ttk, messagebox, filedialog


rsaCryptor = RsaCryptor()
rsaValidator = RsaValidator()

_var_public_4: StringVar
_label_public_4: ttk.Label
_var_private_4: StringVar
_label_private_4: ttk.Label

_var_public_5: StringVar
_label_public_5: ttk.Label
_var_private_5: StringVar
_label_private_5: ttk.Label

def onGenerateKeysButtonPressed():
    try:
        saveDir = filedialog.askdirectory(title="Choose directory for public.key and private.key")
        if not saveDir:
            return

        keyGenerator = RsaKeyGenerator()
        public, private = keyGenerator.getPrivateAndPublickKey()
    

        with open(f'{saveDir}public.key', 'w', encoding='utf8') as publicFile:
            for keyPart in public:
                publicFile.write(f'{keyPart}\n')
    
        with open(f'{saveDir}private.key', 'w', encoding='utf8') as privateFile:
            for keyPart in private:
                privateFile.write(f'{keyPart}\n')
    
    except Exception as ex:
        messagebox.showerror(title='Key generation failed.', message=str(ex))    
    else:
        messagebox.showinfo(title='Public and private keys generation', message='Generating keys finished successfully.')


def onSetPublicKeyButtonPressed(sign: bool):
    global rsaCryptor
    global rsaValidator
    
    publicKeyPath = filedialog.askopenfilename(title="Choose public key file", defaultextension='key')
    if not publicKeyPath:
        return
    
    if not sign:
        _var_public_4.set(f'Public Key: {publicKeyPath}')
    else:
        _var_public_5.set(f'Public Key: {publicKeyPath}')
    
    rsaCryptor.setEncryptionKey(publicKeyPath)
    rsaValidator.setValidatingKey(publicKeyPath)


def onSetPrivateKeyButtonPressed(sign: bool):
    global rsaCryptor
    privateKeyPath = filedialog.askopenfilename(title="Choose private key file", defaultextension='key')
    
    if not privateKeyPath:
        return
    
    if not sign:
        _var_private_4.set(f'Private Key: {privateKeyPath}')
    else:
        _var_private_5.set(f'Private Key: {privateKeyPath}')
    
    rsaValidator.setSigningKey(privateKeyPath)
    rsaCryptor.setDecryptionKey(privateKeyPath)


def onEncryptButtonPressed():
    try:
        filePath = filedialog.askopenfilename(title="Choose file for encryption")

        if not filePath:
            return
        
        if os.path.getsize(filePath) > 256:
            raise RuntimeError('File size must be less than 256 bytes')

        savePath = filedialog.asksaveasfilename(title="Choose where to save encrypted file")

        if not savePath:
            return
        
        with open(filePath, 'rb') as fileToEncrypt, open(savePath, 'wb') as encryptedFile:
            data = fileToEncrypt.read(-1)
            encryptedData = rsaCryptor.encrypt(data)
            encryptedFile.write(b'\xbf\x86\x07\\\xea\xb2\xaf4\xc4\xbf\x04iY6\xf6R+8<\xeek\r7zA\x0bG\x04\x99\xabT\x85')
            encryptedFile.write(encryptedData)
    
    except Exception as ex:
        messagebox.showerror(title='Encryption error', message=str(ex))

    else:
        messagebox.showinfo('Encryption info', 'Encryption finished successfully')


def onDecryptButtonPressed():
    try:
        filePath = filedialog.askopenfilename(title="Choose file for decryption")
        
        if not filePath:
            return

        savePath = filedialog.asksaveasfilename(title="Choose where to save decrypted file")
        
        if not savePath:
            return
        
        with open(filePath, 'rb') as fileToDecrypt, open(savePath, 'wb') as fileDecrypted:
            data = fileToDecrypt.read(32)
            
            if data != b'\xbf\x86\x07\\\xea\xb2\xaf4\xc4\xbf\x04iY6\xf6R+8<\xeek\r7zA\x0bG\x04\x99\xabT\x85':
                raise RuntimeError('File is not encrypted.')
            
            data = fileToDecrypt.read(-1)
            decryptedData = rsaCryptor.decrypt(data)
            fileDecrypted.write(decryptedData)
    
    except Exception as ex:
        messagebox.showerror('Decryption error', str(ex))
    
    else:
        messagebox.showinfo('Decryption info', 'Decryption finished succesfully')


def onSignButtonPressed():
    try:
        filePath = filedialog.askopenfilename(title="Choose file for signing")        
        if not filePath:
            return        
        rsaValidator.signFile(filePath)
    
    except Exception as ex:
        messagebox.showerror('Signing error', str(ex))    
    else:
        messagebox.showinfo('Signing info', 'File successfully signed.')


def onValidateButtonPressed():
    try:        
        filePath = filedialog.askopenfilename(titile="Choose for signature validation")        
        if not filePath:
            return        
        message = 'Validation status: [{}]'.format('Success' if rsaValidator.validateFile(filePath) else 'Failure')
    
    except Exception as ex:
        messagebox.showerror('Validating error', str(ex))
    
    else:
        messagebox.showinfo('Validating info', message)


def main():
    window = Tk()
    frm = ttk.Frame(window, padding=10)
    frm.winfo_toplevel().title('Lab 4-5')
    frm.grid()

    tab_parent = ttk.Notebook(frm)
    lab4 = ttk.Frame(tab_parent)
    lab4.columnconfigure([_ for _ in range(2)], weight=1)
    lab4.rowconfigure([_ for _ in range(8)], weight=1)
    lab5 = ttk.Frame(tab_parent)
    lab5.columnconfigure([_ for _ in range(2)], weight=1)
    lab5.rowconfigure([_ for _ in range(8)], weight=1)

    tab_parent.add(lab4, text="Encryption&Decryption")
    tab_parent.add(lab5, text="Cryptographic Signature")
    tab_parent.pack(expand=1, fill='both')

    ttk.Label(lab4, text='RSA Cryptor', justify='center').grid(column=0, row=0, columnspan=2)
    ttk.Label(lab5, text='RSA Signer', justify='center').grid(column=0, row=0, columnspan=2)

    ttk.Button(lab4, text='Generate keys', command=onGenerateKeysButtonPressed).grid(column=0, row=1, columnspan=2, sticky='news')
    ttk.Button(lab5, text='Generate keys', command=onGenerateKeysButtonPressed).grid(column=0, row=1, columnspan=2, sticky='news')
    
    ttk.Button(lab4, text='Load public key', command=lambda: onSetPublicKeyButtonPressed(False)).grid(column=0, row=2, sticky='news')
    ttk.Button(lab5, text='Load public key', command=lambda: onSetPublicKeyButtonPressed(True)).grid(column=0, row=2, sticky='news')
    
    ttk.Button(lab4, text='Load private key', command=lambda: onSetPrivateKeyButtonPressed(False)).grid(column=1, row=2, sticky='news')
    ttk.Button(lab5, text='Load private key', command=lambda: onSetPrivateKeyButtonPressed(True)).grid(column=1, row=2, sticky='news')
    
    ttk.Button(lab4, text='Encrypt', command=onEncryptButtonPressed).grid(column=0, row=3, sticky='news')
    ttk.Button(lab4, text='Decrypt', command=onDecryptButtonPressed).grid(column=1, row=3, sticky='news')

    ttk.Button(lab5, text='Validate', command=onValidateButtonPressed).grid(column=0, row=4, sticky='news')
    ttk.Button(lab5, text='Sign', command=onSignButtonPressed).grid(column=1, row=4, sticky='news')

    global _label_public_4
    global _var_public_4
    global _label_private_4
    global _var_private_4

    global _label_public_5
    global _var_public_5
    global _label_private_5
    global _var_private_5

    _var_public_4 = StringVar(lab4, "Public Key: -")
    _var_private_4 = StringVar(lab4, "Private Key: -")

    _var_public_5 = StringVar(lab5, "Public Key: -")
    _var_private_5 = StringVar(lab5, "Private Key: -")

    _label_public_4 = ttk.Label(lab4, textvariable=_var_public_4)
    _label_public_4.grid(column=0, row=6, columnspan=2, sticky='news')
    _label_private_4 = ttk.Label(lab4, textvariable=_var_private_4)
    _label_private_4.grid(column=0, row=7, columnspan=2, sticky='news')
    
    _label_public_5 = ttk.Label(lab5, textvariable=_var_public_5)
    _label_public_5.grid(column=0, row=6, columnspan=2, sticky='news')
    _label_private_5 = ttk.Label(lab5, textvariable=_var_private_5)
    _label_private_5.grid(column=0, row=7, columnspan=2, sticky='news')

    window.mainloop()


if __name__ == '__main__':
    main()

else:
    print(f'{__name__} is intended to be main.')
    exit()
