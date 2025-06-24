import mysql.connector

ALFABETO = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
CHAVE     = [[3, 5], [1, 2]]
CHAVE_INV = [[2, -5], [-1, 3]]

def hill_cipher(texto, matriz):
    txt = "".join(c for c in texto.upper() if c in ALFABETO)
    if len(txt) % 2:
        txt += "A"
    res = ""
    for i in range(0, len(txt), 2):
        a = ALFABETO.index(txt[i])
        b = ALFABETO.index(txt[i+1])
        c = (matriz[0][0]*a + matriz[0][1]*b) % 26
        d = (matriz[1][0]*a + matriz[1][1]*b) % 26
        res += ALFABETO[c] + ALFABETO[d]
    return res

def criptografia(texto):
    return hill_cipher(texto, CHAVE)

def descriptografia(texto_cifrado):
    res = hill_cipher(texto_cifrado, CHAVE_INV)
    if res.endswith("A"):
        res = res[:-1]
    return _MAP_CLASSIFICACOES.get(res, res)

_MAP_CLASSIFICACOES = {
    "ALTASUSTENTABILIDADE":    "Alta Sustentabilidade",
    "MODERADASUSTENTABILIDADE": "Moderada Sustentabilidade",
    "BAIXASUSTENTABILIDADE":   "Baixa Sustentabilidade",
}

conn = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="32423215Juan@",
    database="bd_projetoti",
)
cursor = conn.cursor()

def classif_agua(litros):
    if litros < 150:
        return "Alta Sustentabilidade"
    elif 150 <= litros <= 200:
        return "Moderada Sustentabilidade"
    else:
        return "Baixa Sustentabilidade"

def classif_energia(energia):
    if energia < 5:
        return "Alta Sustentabilidade"
    elif 5 <= energia <= 10:
        return "Moderada Sustentabilidade"
    else:
        return "Baixa Sustentabilidade"

def classif_reciclados(reciclados):
    if reciclados > 50:
        return "Alta Sustentabilidade"
    elif 20 <= reciclados <= 50:
        return "Moderada Sustentabilidade"
    else:
        return "Baixa Sustentabilidade"

def classif_transporte(opc1, opc2, opc3, opc4, opc5, opc6):
    if (opc1 == "S" or opc2 == "S" or opc3 == "S" or opc5 == "S") and opc4 == "N" and opc6 == "N":
        return "Alta Sustentabilidade"
    elif (opc1 == "S" or opc2 == "S" or opc3 == "S" or opc5 == "S") and (opc4 == "S" or opc6 == "S"):
        return "Moderada Sustentabilidade"
    elif opc1 == "N" and opc2 == "N" and opc3 == "N" and opc5 == "N" and (opc4 == "S" or opc6 == "S"):
        return "Baixa Sustentabilidade"
    else:
        return "Moderada Sustentabilidade"

def cadastrardados():
    data = input("Qual é a data (yyyy-MM-dd): ")
    cursor.execute("SELECT * FROM valores_sustentabilidade WHERE data = %s", (data,))
    if cursor.fetchone():
        print("\nJá existe um registro para essa data.\n")
        return

    litros = int(input("\nQuantos litros de água você consumiu hoje? (Aprox. em litros): "))
    energia = float(input("Quantos kWh de energia elétrica você consumiu hoje?: "))
    residuos = float(input("Quantos kg de resíduos não recicláveis você gerou hoje?: "))
    reciclados = int(input("Qual a porcentagem de resíduos reciclados no total (em %)?: "))

    print("\nResponda com 'S' e 'N' qual meio de transporte você usou hoje?:")
    opc1 = input('1. Transporte público (ônibus, metrô, trem): ').upper()
    opc2 = input('2. Bicicleta: ').upper()
    opc3 = input('3. Caminhada: ').upper()
    opc4 = input('4. Carro (combustível fósseis): ').upper()
    opc5 = input('5. Carro elétrico: ').upper()
    opc6 = input('6. Carona compartilhada (Fósseis): ').upper()

    consumo_agua = criptografia(classif_agua(litros))
    consumo_energia = criptografia(classif_energia(energia))
    geracao_residuos = criptografia(classif_reciclados(reciclados))
    uso_transporte = criptografia(classif_transporte(opc1, opc2, opc3, opc4, opc5, opc6))

    transportes_str = ""
    if opc1 == 'S': transportes_str += "| Transporte Público |"
    if opc2 == 'S': transportes_str += "| Bicicleta |"
    if opc3 == 'S': transportes_str += "| Caminhada |"
    if opc4 == 'S': transportes_str += "| Carro (combustível fósseis) |"
    if opc5 == 'S': transportes_str += "| Carro Elétrico |"
    if opc6 == 'S': transportes_str += "| Carona compartilhada (Fósseis) |"

    insert_resultados = """
    INSERT INTO resultados_sustentabilidade (data, consumo_agua, consumo_energia, geracao_residuos, uso_transporte)
    VALUES (%s, %s, %s, %s, %s)
    """
    insert_valores = """
    INSERT INTO valores_sustentabilidade (data, valor_agua, valor_energia, valor_residuos, valor_reciclaveis, valor_transporte)
    VALUES (%s, %s, %s, %s, %s, %s)
    """

    valores_resultados = (data, consumo_agua, consumo_energia, geracao_residuos, uso_transporte)
    valores_valores = (data, litros, energia, residuos, reciclados, transportes_str)

    cursor.execute(insert_resultados, valores_resultados)
    cursor.execute(insert_valores, valores_valores)
    conn.commit()

    print("\nDados inseridos com sucesso.")

def alterar_dados():
    data = input("Digite a data do registro que deseja alterar (YYYY-MM-DD): ")
    cursor.execute("SELECT id FROM valores_sustentabilidade WHERE data = %s", (data,))
    resultado = cursor.fetchone()
    if not resultado:
        print("\nNenhum registro encontrado para essa data.\n")
        return

    litros = int(input("\nNovo valor - Quantos litros de água foram consumidos?: "))
    energia = float(input("Novo valor - Quantos kWh foram consumidos?: "))
    residuos = float(input("Novo valor - Quantos kg de resíduos não recicláveis foram gerados?: "))
    reciclados = int(input("Novo valor - Qual a porcentagem de resíduos reciclados (em %)? : "))

    print("\nResponda com 'S' ou 'N' sobre os meios de transporte usados no dia:")
    opc1 = input('1. Transporte público (ônibus, metrô, trem): ').upper()
    opc2 = input('2. Bicicleta: ').upper()
    opc3 = input('3. Caminhada: ').upper()
    opc4 = input('4. Carro (combustível fósseis): ').upper()
    opc5 = input('5. Carro elétrico: ').upper()
    opc6 = input('6. Carona compartilhada (Fósseis): ').upper()

    consumo_agua = criptografia(classif_agua(litros))
    consumo_energia = criptografia(classif_energia(energia))
    geracao_residuos = criptografia(classif_reciclados(reciclados))
    uso_transporte = criptografia(classif_transporte(opc1, opc2, opc3, opc4, opc5, opc6))

    transportes_str = ""
    if opc1 == 'S': transportes_str += "| Transporte Público |"
    if opc2 == 'S': transportes_str += "| Bicicleta |"
    if opc3 == 'S': transportes_str += "| Caminhada |"
    if opc4 == 'S': transportes_str += "| Carro (combustível fósseis) |"
    if opc5 == 'S': transportes_str += "| Carro Elétrico |"
    if opc6 == 'S': transportes_str += "| Carona compartilhada (Fósseis) |"

    update_valores = """
    UPDATE valores_sustentabilidade 
    SET valor_agua = %s, valor_energia = %s, valor_residuos = %s, 
        valor_reciclaveis = %s, valor_transporte = %s
    WHERE data = %s
    """
    cursor.execute(update_valores, (litros, energia, residuos, reciclados, transportes_str, data))

    update_resultados = """
    UPDATE resultados_sustentabilidade 
    SET consumo_agua = %s, consumo_energia = %s, 
        geracao_residuos = %s, uso_transporte = %s 
    WHERE data = %s
    """
    cursor.execute(update_resultados, (consumo_agua, consumo_energia, geracao_residuos, uso_transporte, data))

    conn.commit()
    print("\nDados atualizados com sucesso!")

def excluir_dados():
    data = input("\nDigite a data do registro que deseja excluir (YYYY-MM-DD): ")
    cursor.execute("DELETE FROM resultados_sustentabilidade WHERE data = %s", (data,))
    cursor.execute("DELETE FROM valores_sustentabilidade WHERE data = %s", (data,))
    conn.commit()
    print("\nRegistro excluído com sucesso!")

def listar_dados():
    select_query = """
    SELECT 
        v.data, 
        v.valor_agua,    r.consumo_agua,
        v.valor_energia, r.consumo_energia,
        v.valor_residuos,
        v.valor_reciclaveis, r.geracao_residuos, 
        v.valor_transporte,   r.uso_transporte
    FROM valores_sustentabilidade v
    JOIN resultados_sustentabilidade r ON v.data = r.data
    ORDER BY v.data DESC
    """
    cursor.execute(select_query)
    registros = cursor.fetchall()

    if not registros:
        print("\nNenhum monitoramento cadastrado.\n")
        return

    for (data, litros, cod_agua, energia, cod_energia, residuos, reciclaveis, cod_residuos, transportes_str, cod_transporte) in registros:
        classif_agua_txt = descriptografia(cod_agua)
        classif_energia_txt = descriptografia(cod_energia)
        classif_resid_txt = descriptografia(cod_residuos)
        classif_transp_txt = descriptografia(cod_transporte)

        print(f"Data: {data}\n")
        print(f"Consumo de Água: {litros:.2f} litros (Classificação: {classif_agua_txt})")
        print(f"Consumo de Energia: {energia:.2f} kWh (Classificação: {classif_energia_txt})")
        print(f"Resíduos não recicláveis gerados: {residuos:.2f} kg | Porcentagem de reciclados: {reciclaveis:.2f}% (Classificação: {classif_resid_txt})")
        print(f"Uso de Transporte: {transportes_str} (Classificação: {classif_transp_txt})")
        print("--------------------------------------------------")

def media_dados():
    cursor.execute("""
        SELECT 
            v.valor_agua, v.valor_energia, v.valor_residuos, v.valor_reciclaveis,
            r.consumo_agua, r.consumo_energia, r.geracao_residuos, r.uso_transporte
        FROM valores_sustentabilidade v
        JOIN resultados_sustentabilidade r ON v.data = r.data
    """)
    dados = cursor.fetchall()

    total = len(dados)
    if total == 0:
        print("\nNenhum dado encontrado para cálculo de média.\n")
        return

    soma_agua = soma_energia = soma_residuos = soma_reciclaveis = 0
    cont_agua = {"Alta": 0, "Moderada": 0, "Baixa": 0}
    cont_energia = {"Alta": 0, "Moderada": 0, "Baixa": 0}
    cont_residuos = {"Alta": 0, "Moderada": 0, "Baixa": 0}
    cont_transporte = {"Alta": 0, "Moderada": 0, "Baixa": 0}

    for agua, energia, residuos, reciclaveis, ca, ce, cr, ct in dados:
        soma_agua += float(agua)
        soma_energia += float(energia)
        soma_residuos += float(residuos)
        soma_reciclaveis += float(reciclaveis)

        texto_ca = descriptografia(ca)
        texto_ce = descriptografia(ce)
        texto_cr = descriptografia(cr)
        texto_ct = descriptografia(ct)

        if "Alta" in texto_ca: cont_agua["Alta"] += 1
        elif "Baixa" in texto_ca: cont_agua["Baixa"] += 1
        else: cont_agua["Moderada"] += 1

        if "Alta" in texto_ce: cont_energia["Alta"] += 1
        elif "Baixa" in texto_ce: cont_energia["Baixa"] += 1
        else: cont_energia["Moderada"] += 1

        if "Alta" in texto_cr: cont_residuos["Alta"] += 1
        elif "Baixa" in texto_cr: cont_residuos["Baixa"] += 1
        else: cont_residuos["Moderada"] += 1

        if "Alta" in texto_ct: cont_transporte["Alta"] += 1
        elif "Baixa" in texto_ct: cont_transporte["Baixa"] += 1
        else: cont_transporte["Moderada"] += 1

    def classificacao_media(cont):
        if cont["Alta"] == total: return "Alta Sustentabilidade"
        if cont["Baixa"] == total: return "Baixa Sustentabilidade"
        return "Moderada Sustentabilidade"

    print("\nMédia dos valores")
    print(f"Média de Consumo de Água:     {soma_agua / total:.2f} litros")
    print(f"Média de Consumo de Energia:  {soma_energia / total:.2f} kWh")
    print(f"Média de Resíduos Gerados:    {soma_residuos / total:.2f} kg")
    print(f"Média de Resíduos Reciclados: {soma_reciclaveis / total:.2f}%")
    print("\nMédia das classificações")
    print("Consumo de Água:     ", classificacao_media(cont_agua))
    print("Consumo de Energia:  ", classificacao_media(cont_energia))
    print("Geração de Resíduos: ", classificacao_media(cont_residuos))
    print("Uso de Transporte:   ", classificacao_media(cont_transporte))

def menu():
    opcao = ""
    while opcao != "6":
        print(
            "\nMenu:\n"
            "1. Inserir dados de monitoramento\n"
            "2. Alterar dados de monitoramento\n"
            "3. Apagar dados de monitoramento\n"
            "4. Listar cada monitoramento diário e classificar\n"
            "5. Calcular e mostrar as médias dos parâmetros de monitoramento e classificar\n"
            "6. Saída do sistema"
        )
        opcao = input("\nEscolha uma opção: ")
        if opcao == "1": cadastrardados()
        elif opcao == "2": alterar_dados()
        elif opcao == "3": excluir_dados()
        elif opcao == "4": listar_dados()
        elif opcao == "5": media_dados()
        elif opcao == "6":
            print("\nSaindo do sistema.\n")
            cursor.close()
            conn.close()

menu()
