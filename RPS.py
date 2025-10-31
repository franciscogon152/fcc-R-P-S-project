import random

def player(prev_play, state={}):
    
    """
    Un bot de Piedra, Papel o Tijeras que utiliza un modelo predictivo 
    basado en secuencias para aprender y contrarrestar 
    la estrategia del contrincante.
    """
    
    # Definir la jugada ganadora
    ideal_response = {'P': 'S', 'R': 'P', 'S': 'R'}
    
    # Inicializar el estado en la primera llamada
    if not state:
        state['my_history'] = []
        state['opponent_history'] = []
        # El 'modelo' almacena las predicciones.
        # La clave es una secuencia de N jugadas (ej: "RPSR").
        # El valor es un conteo de la *siguiente* jugada del oponente (ej: {'R': 1, 'P': 3, 'S': 0}).
        state['model'] = {}
        # 'n' es la longitud de la secuencia que usaremos para predecir.
        state['n'] = 4 

    # Manejar el reinicio al comienzo de un nuevo encuentro
    if prev_play == "":
        state['my_history'].clear()
        state['opponent_history'].clear()
        state['model'].clear()
        
        # Jugar 'R' (Roca) como primera jugada
        my_move = "R"
        state['my_history'].append(my_move)
        return my_move

    # Actualizar el historial y entrenar el modelo (para todas las jugadas después de la primera)
    state['opponent_history'].append(prev_play)
    
    # Necesitamos suficientes datos para formar una secuencia
    if len(state['opponent_history']) > state['n']:
        key = "".join(state['opponent_history'][-(state['n'] + 1):-1])
        
        result = prev_play 
        # Inicializar la clave en el modelo si no existe
        if key not in state['model']:
            state['model'][key] = {'R': 0, 'P': 0, 'S': 0}
            
        # Incrementar el contador para esa jugada resultante
        state['model'][key][result] += 1

    # Hacer una predicción
    
    # Por defecto, jugar 'S' (Tijeras) si no tenemos datos
    my_move = "S" 
    
    # Solo predecir si tenemos al menos N jugadas en el historial
    if len(state['opponent_history']) >= state['n']:
    
        current_key = "".join(state['opponent_history'][-state['n']:])

        # Comprobar si hemos visto esta secuencia antes
        if current_key in state['model']:
            # Predecir que el oponente jugará la movida más frecuente 
            # que haya hecho después de esta secuencia.
            predictions = state['model'][current_key]
            
            if any(predictions.values()): # Asegurarse de que no todos los contadores sean 0
                opp_prediction = max(predictions, key=predictions.get)
            
                # Nuestra jugada es la que vence a la predicción
                my_move = ideal_response[opp_prediction]

    # Guardar nuestra jugada y devolverla
    state['my_history'].append(my_move)
    return my_move