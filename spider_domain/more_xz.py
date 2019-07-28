def xz_more(xz):
    ret_data = [xz]
    #plus_xz 0.01大约一公里
    plus_xz=0.01
    #根据坐标轴添加附近的坐标
    ret_data.append([str(float(ret_data[0][0])+plus_xz),str(float(ret_data[0][1])+plus_xz)])
    ret_data.append([str(float(ret_data[0][0])+plus_xz),str(float(ret_data[0][1])-plus_xz)])
    ret_data.append([str(float(ret_data[0][0])-plus_xz),str(float(ret_data[0][1])-plus_xz)])
    ret_data.append([str(float(ret_data[0][0])-plus_xz),str(float(ret_data[0][1])+plus_xz)])

    return ret_data