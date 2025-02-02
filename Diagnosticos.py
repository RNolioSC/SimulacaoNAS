from ProbabsNas import ProbabsNAS


def add_atividades_faltantes():
    for i in Index:
        diagnostico = Index[i]
        for atividade in ProbabsNAS:
            if atividade not in diagnostico:
                diagnostico[atividade] = ProbabsNAS[atividade]


# caso o diagnostico nao seja conhecido, usar valores padrao
Desconhecido = ProbabsNAS

Covid = {  # (BRUYNEEL et al., 2021)

    '1a': 220/905,
    '1b': 489/905,
    '1c': 196/905,
    '4a': 41/905,
    '4b': 535/905,
    '4c': 329/905,
    '6a': 53/905,
    '6b': 637/905,
    '6c': 215/905,

}

Queimado = {  # (CAMUCI et al., 2014)

    '1a': 3.4/100,
    '1b': 68.3/100,
    '1c': 28.2/100,
    '2': 100/100,
    '3': 100/100,
    '4a': 51.4/100,
    '4b': 34.9/100,
    '4c': 13.4/100,
    '5': 74.6/100,
    '6a': 19.3/100,
    '6b': 69/100,
    '6c': 11.2/100,
    '7a': 71/100,
    '7b': 0,
    '8a': 91.8/100,
    '8b': 8.1/100,
    '8c': 0,
    '9': 83.6/100,
    '10': 68.7/100,
    '11': 97.2/100,
    '12': 34.3/100,
    '13': 17.4/100,
    '14': 0.1/100,
    '15': 0.4/100,
    '16': 6.6/100,
    '17': 99.6/100,
    '18': 0,
    '19': 0.1/100,
    '20': 1.4/100,
    '21': 87.7/100,
    '22': 1.2/100,
    '23': 36.3/100,
}

Trauma = {  # (NOGUEIRA, 2015)


    '1a': 20.6/100,
    '1b': 66.9/100,
    '1c': 12.5/100,
    '2': 1,
    '3': 1,
    '4a': 64/100,
    '4b': 35.3/100,
    '4c': 0.7/100,
    '5': 99.3/100,
    '6a': 0,
    '6b': 72.8/100,
    '6c': 27.2/100,
    '7a': 97.1/100,
    '7b': 2.9/100,
    '8a': 1,
    '8b': 0,
    '8c': 0,
    '9': 97.8/100,
    '10': 89.7/100,
    '11': 94.1/100,
    '12': 64.7/100,
    '13': 16.2/100,
    '14': 0,
    '15': 0.7/100,
    '16': 0.7/100,
    '17': 1,
    '18': 12.5/100,
    '19': 11.8/100,
    '20': 0,
    '21': 13.2/100,
    '22': 19.1/100,
    '23': 29.4/100,

}

Index = {

    # probablidade de cada atividade NAS ser escolhida
    'desconhecido': Desconhecido,
    'covid-19': Covid,
    'queimado': Queimado,
    'trauma': Trauma,
}
