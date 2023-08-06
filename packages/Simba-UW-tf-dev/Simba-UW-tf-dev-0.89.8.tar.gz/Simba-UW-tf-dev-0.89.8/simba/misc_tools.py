from configparser import NoSectionError
import numpy as np

def check_directionality_viable(noAnimals, col_headers_lower_case):
    directionalitySetting = True
    if noAnimals > 1:
        NoseCoords = []
        EarLeftCoords = []
        EarRightCoords = []
        for animal in range(noAnimals):
            possible_NoseCoords = ['nose_' + str(animal + 1) + '_x', 'nose_' + str(animal + 1) + '_y']
            possible_EarLeftCoords = ['ear_left_' + str(animal + 1) + '_x', 'ear_left_' + str(animal + 1) + '_y']
            possible_EarRightCoords = ['ear_right_' + str(animal + 1) + '_x', 'ear_right_' + str(animal + 1) + '_y']
            directionalityCordHeaders = possible_NoseCoords + possible_EarLeftCoords + possible_EarRightCoords
            if not set(directionalityCordHeaders).issubset(col_headers_lower_case):
                possible_EarLeftCoords = ['left_ear_' + str(animal + 1) + '_x', 'left_ear_' + str(animal + 1) + '_y']
                possible_EarRightCoords = ['right_ear' + str(animal + 1) + '_x', 'right_ear_' + str(animal + 1) + '_y']
                directionalityCordHeaders = possible_NoseCoords + possible_EarLeftCoords + possible_EarRightCoords
                if not set(directionalityCordHeaders).issubset(col_headers_lower_case):
                    return False, NoseCoords, EarLeftCoords, EarRightCoords
                else:
                    NoseCoords.extend((possible_NoseCoords))
                    EarLeftCoords.extend((possible_EarLeftCoords))
                    EarRightCoords.extend((possible_EarRightCoords))
            else:
                NoseCoords.extend((possible_NoseCoords))
                EarLeftCoords.extend((possible_EarLeftCoords))
                EarRightCoords.extend((possible_EarRightCoords))

    else:
        NoseCoords = ['nose_x', 'nose_y']
        EarLeftCoords = ['ear_left_x', 'ear_left_y']
        EarRightCoords = ['ear_right_x', 'ear_right_y']
        directionalityCordHeaders = NoseCoords + EarLeftCoords + EarRightCoords
        if not set(directionalityCordHeaders).issubset(col_headers_lower_case):
            EarLeftCoords = ['left_ear_x', 'left_ear_y']
            EarRightCoords = ['right_ear_x', 'right_ear_y']
            directionalityCordHeaders = NoseCoords + EarLeftCoords + EarRightCoords
            if not set(directionalityCordHeaders).issubset(col_headers_lower_case):
                return False, NoseCoords, EarLeftCoords, EarRightCoords


    return directionalitySetting, NoseCoords, EarLeftCoords, EarRightCoords


def check_multi_animal_status(config, noAnimals):
    try:
        multiAnimalIDList = config.get('Multi animal IDs', 'id_list')
        multiAnimalIDList = multiAnimalIDList.split(",")
        if multiAnimalIDList[0] != '':
            multiAnimalStatus = True
            print('Applying settings for multi-animal tracking...')
            return multiAnimalStatus, multiAnimalIDList

        else:
            multiAnimalStatus = False
            multiAnimalIDList = []
            for animal in range(noAnimals):
                multiAnimalIDList.append('Animal_' + str(animal + 1))
            print('Applying settings for classical tracking...')
            return multiAnimalStatus, multiAnimalIDList

    except NoSectionError:
        multiAnimalIDList = []
        for animal in range(noAnimals):
            multiAnimalIDList.append('Animal_' + str(animal + 1))
        multiAnimalStatus = False
        print('Applying settings for classical tracking...')
        return multiAnimalStatus, multiAnimalIDList

def line_length(p, q, n, M, coord):
    Px = np.abs(p[0] - M[0])
    Py = np.abs(p[1] - M[1])
    Qx = np.abs(q[0] - M[0])
    Qy = np.abs(q[1] - M[1])
    Nx = np.abs(n[0] - M[0])
    Ny = np.abs(n[1] - M[1])
    Ph = np.sqrt(Px*Px + Py*Py)
    Qh = np.sqrt(Qx*Qx + Qy*Qy)
    Nh = np.sqrt(Nx*Nx + Ny*Ny)
    if (Nh < Ph and Nh < Qh and Qh < Ph):
        coord.extend((q[0], q[1]))
        return True, coord
    elif (Nh < Ph and Nh < Qh and Ph < Qh):
        coord.extend((p[0], p[1]))
        return True, coord
    else:
        return False, coord