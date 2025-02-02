from numpy import genfromtxt
import numpy
import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.layers import Dense
import time
import keras
import keras.metrics
import csv
import pickle


def data_preprocessing():
    with open(simulacao_path + '/bin/diagnosticos_list.bin', 'rb') as f:
        diagnosticos = pickle.load(f)
    with open(simulacao_path + '/CSV/duracao_ativs_diag.csv') as csvfile:
        reader = csv.reader(csvfile, delimiter=",", quotechar='|')
        # codPaciente, diagnostico, pontosNAS(atividade)
        next(reader, None)  # skip the headers
        next(reader, None)
        tabela = [row for row in reader]

    nova_tabela = []
    for linha in tabela:
        linha.pop(0)  # cod paciente
        linha.pop(0)  # dia
        nova_linha = [diagnostico_str_to_float(linha.pop(0), simulacao_path)]  # normalizado
        nova_linha.extend(linha)

        nova_tabela.append(nova_linha)

    with open(simulacao_path + '/CSV/duracao_ativs_diag_prepr.csv', 'w', newline='') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for i in nova_tabela:
            filewriter.writerow(i)


def diagnostico_str_to_float(diag, simulacao_path):
    with open(simulacao_path + '/bin/diagnosticos_list.bin', 'rb') as f:
        diagnosticos = pickle.load(f)
    return diagnosticos.index(diag) / (len(diagnosticos)-1)


def atividades_fl_to_str(atividades_fl):
    atividades_fl = list(atividades_fl)
    atividades_fl = [int(i) for i in atividades_fl]
    atividades = []
    if atividades_fl.pop(0) == 1:
        atividades.append('1a')
        atividades_fl.pop(0)
        atividades_fl.pop(0)
    elif atividades_fl.pop(0) == 1:
        atividades.append('1b')
        atividades_fl.pop(0)
    elif atividades_fl.pop(0) == 1:
        atividades.append('1c')
    else:
        raise Exception

    if atividades_fl.pop(0) == 1:
        atividades.append('2')
    if atividades_fl.pop(0) == 1:
        atividades.append('3')

    if atividades_fl.pop(0) == 1:
        atividades.append('4a')
        atividades_fl.pop(0)
        atividades_fl.pop(0)
    elif atividades_fl.pop(0) == 1:
        atividades.append('4b')
        atividades_fl.pop(0)
    elif atividades_fl.pop(0) == 1:
        atividades.append('4c')
    else:
        raise Exception

    if atividades_fl.pop(0) == 1:
        atividades.append('5')

    if atividades_fl.pop(0) == 1:
        atividades.append('6a')
        atividades_fl.pop(0)
        atividades_fl.pop(0)
    elif atividades_fl.pop(0) == 1:
        atividades.append('6b')
        atividades_fl.pop(0)
    elif atividades_fl.pop(0) == 1:
        atividades.append('6c')
    else:
        raise Exception

    if atividades_fl.pop(0) == 1:
        atividades.append('7a')
        atividades_fl.pop(0)
    elif atividades_fl.pop(0) == 1:
        atividades.append('7b')
    else:
        raise Exception

    if atividades_fl.pop(0) == 1:
        atividades.append('8a')
        atividades_fl.pop(0)
        atividades_fl.pop(0)
    elif atividades_fl.pop(0) == 1:
        atividades.append('8b')
        atividades_fl.pop(0)
    elif atividades_fl.pop(0) == 1:
        atividades.append('8c')
    else:
        raise Exception

    next_ativ = 9  # até 23
    while atividades_fl:
        if atividades_fl.pop(0) == 1:
            atividades.append(str(next_ativ))
        next_ativ += 1

    return atividades


def evaluate_batch(diagnosticos, simulacao_path):
    model = keras.models.load_model('modelo_regressao')
    diagnosticos_fl = [diagnostico_str_to_float(d, simulacao_path) for d in diagnosticos]
    duracao_ativs = model.predict(numpy.array(diagnosticos_fl), verbose=0)

    return duracao_ativs


def save_history(history):
    with open('modelo_regressao/history.bin', 'wb') as f:
        pickle.dump(history.history, f)


def load_history():
    with open('modelo_regressao/history.bin', 'rb') as f:
        history = pickle.load(f)
    return history


if __name__ == '__main__':

    treinar = False
    # Treinamento da rede neural
    tempoi = time.time()

    # path pros dados a serem usados para o treinamento
    simulacao_path = 'simulacoes/simulacao1'

    data_preprocessing()
    dataset = genfromtxt(r'simulacoes/simulacao1/CSV/duracao_ativs_diag_prepr.csv', encoding='latin-1', delimiter=',')

    # data_norm = normalize(dataset, axis=0, norm='max')
    data_norm = dataset

    X = data_norm[:, 0]  # diagnostico
    Y = data_norm[:, 1:]  # [i, j) [duracao por atividade]

    if treinar:
        model = Sequential()
        model.add(Dense(150, input_dim=1, activation='tanh'))
        model.add(Dense(150, activation='tanh'))
        model.add(Dense(23))

        model.compile(loss='mean_squared_error', optimizer='adam')
        history = model.fit(X, Y, epochs=50, batch_size=100, validation_split=0.2)
        save_history(history)
        history = history.history
        model.save('modelo_regressao')

    else:  # nao treinar
        model = keras.models.load_model('modelo_regressao')
        history = load_history()
        # model.evaluate(X, Y)

    predict_y = model.predict(X)
    print('predict diagnosticos:')
    aux = model.predict([0, 1/3, 2/3, 3/3])
    print(aux)

    tempof = time.time()
    print("tempo de execucao (s):", tempof - tempoi)

    # graficos de acuracia e validacao
    plt.plot(history['loss'])
    plt.plot(history['val_loss'])
    plt.ylabel('Erro quadrático médio')
    plt.xlabel('Época')
    plt.legend(['Treinamento', 'Teste'])
    plt.show()
