import numpy as np

def dwelltimes(data, dt):
    """Measure dwell times and count positive and negative transition events.
    
    Parameters
    ----------
    data : array
           Stator number data, with each row containing a different experiment  
    dt : timestep (seconds)
    Returns
    -------
    t : dwell times for each level (list of lists)
    t_plus : dwell times that end with a positive transition (list of lists)
    t_minus : dwell times that end with a negative transition (list of lists)
    n_plus : number of positive transitions for each level (1D np array)
    n_minus : number of negative transisions for each level (1D np array)
    """
    
    sequence = data.flatten() # reshape into one long sequence
    t = [[] for i in range(int(np.max(sequence))+1)] # empty list of lists
    t_plus = [[] for i in range(int(np.max(sequence))+1)] # empty list of lists
    t_minus = [[] for i in range(int(np.max(sequence))+1)] # empty list of lists
    n_plus = np.zeros(int(np.max(sequence))+1) # empty 1D array
    n_minus = np.zeros(int(np.max(sequence))+1) # empty 1D array
    
    start_state = sequence[0]
    counter = 0
    for state in sequence:
        if state == start_state:
            counter += 1
        else:
            if start_state >= 0: # remove rare negative states
                t[int(start_state)].append(dt*counter) # store dwell time
                if state > start_state:
                    t_plus[int(start_state)].append(dt*counter)
                    n_plus[int(start_state)] += 1
                else:
                    t_minus[int(start_state)].append(dt*counter)
                    n_minus[int(start_state)] += 1

            counter = 1
            start_state = state
    if start_state >= 0: # remove rare negative states
        t[int(start_state)].append(dt*counter) # store dwell time
        if state > start_state:
            t_plus[int(start_state)].append(dt*counter)
            n_plus[int(start_state)] += 1
        else:
            t_minus[int(start_state)].append(dt*counter)
            n_minus[int(start_state)] += 1
    
    return t, t_plus, t_minus, n_plus, n_minus

