def valida_cpf(cpf):
    if len(cpf) == 11:
        soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
        resto = (soma * 10) % 11 if (soma * 10) % 11 < 10 else 0
        print('soma 1: ', soma)
        print('resto 1: ', resto)
        if int(cpf[-2]) == resto:
            soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
            resto = (soma * 10) % 11 if (soma * 10) % 11 < 10 else 0
            print('soma 2: ', soma)
            print('resto 2: ', resto)
            if int(cpf[-1]) == resto:
                return True
    return False    

cpf = input('Digite o cpf: ')
print(valida_cpf(cpf))
