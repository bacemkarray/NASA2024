def accuratePredictor(array1, array2):
    if len(array1) >= len(array2):
        x = len(array2)
    if len(array1) < len(array2):
        x = (len(array1))


    overLaps = []
    for i in range(x):
        if array1[i][0] >= array2[i][0] and array1[i][0] <= array2[i][1]:
            averageOn = (array1[i][0] + array2[i][0])/2
            averageOff = (array1[i][1] + array2[i][1])/2
            overLaps.append([averageOn, averageOff])

        if array2[i][0] >= array1[i][0] and array2[i][0] <= array1[i][1]:
            averageOn = (array1[i][0] + array2[i][0])/2
            averageOff = (array1[i][1] + array2[i][1])/2
            overLaps.append([averageOn, averageOff])

            
    
    return overLaps
