def cpf_validation(cpf):
    operacoes_digito1 = []
    c = 2
    for d1 in range(len(cpf)-3,-1, -1):
        n1 = int(cpf[d1]) * c
        operacoes_digito1.append(n1)
        c += 1
    soma_digito1 = sum(operacoes_digito1)

    if (soma_digito1%11) < 2:
        digito1 = 0 
        if digito1 == int(cpf[-2]):
            c = 2
            operacoes_digito2 = []
            for d2 in range(len(cpf)-2,-1, -1):
                n2 = int(cpf[d2]) * c
                operacoes_digito2.append(n2)
                c += 1
            soma_digito2 = sum(operacoes_digito2)
            if (soma_digito2%11) < 2:
                digito2 = 0 
                if digito2 == int(cpf[-1]):
                    return True
                else:
                    return False
            else:
                digito2 = 11 - (soma_digito2%11)
                if digito2 == int(cpf[-1]):
                    return True
                else:
                    return False  
        else:
            return False
    else:
        digito1 = 11 - (soma_digito1%11)
        if digito1 == int(cpf[-2]):
            c = 2
            operacoes_digito2 = []
            for d2 in range(len(cpf)-2,-1, -1):
                n2 = int(cpf[d2]) * c
                operacoes_digito2.append(n2)
                c += 1
            soma_digito2 = sum(operacoes_digito2)
            if (soma_digito2%11) < 2:
                digito2 = 0 
                if digito2 == int(cpf[-1]):
                    return True
                else:
                    return False
            else:
                digito2 = 11 - (soma_digito2%11)
                if digito2 == int(cpf[-1]):
                    return True
                else:
                    return False
        else:
            return False