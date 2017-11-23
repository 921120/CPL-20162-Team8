import math
import smtplib

# 단위는 mm로

def ConvertToXYZ() :
    ffc = open('C:\Pycharm_exam\FinalProject\input.txt', 'r')
    ffi = open('C:\Pycharm_exam\FinalProject\input.txt', 'r')
    ffo = open('C:\Pycharm_exam\FinalProject\output.txt', 'w')

    start_x = 140  # 시작 위치 (단위 mm)
    step_to_mm = 0.0007
    cnt_all = 0  # 점의 갯수
    cnt = 0
    using_refraction = 1.17 # 굴절률

    # 전체 점의 갯수
    while True:
        res_data = ffc.readline()
        if res_data == '':
            break
        l1 = res_data.rstrip('\n').split('\t')
        if 45 < float(l1[2]) < 315:
            continue

        if l1[3] == '':
            if float(l1[4]) > 700 or 0 <= float(l1[4]) < 70:
                continue
        else:
            if float(l1[3]) > 700 or 0 <= float(l1[3]) < 70:
                continue
        cnt_all += 1
    ffc.close()

    ffo.write('ply\n')
    ffo.write('format ascii 1.0\n')
    ffo.write('element vertex %d\n' % cnt_all)
    ffo.write('property float x\n')
    ffo.write('property float y\n')
    ffo.write('property float z\n')
    ffo.write('element face 0\n')
    ffo.write('property list uchar int vertex_indices\n')
    ffo.write('property list uchar float texcoord\n')
    ffo.write('end_header\n')

    while True:
        res_data = ffi.readline()
        # print(res_data)
        if res_data == '':
            break

        l1 = res_data.rstrip('\n').split('\t')
        # sin_y의 정의
        tan_y = -math.tan(math.radians(float(l1[2])))
        cos_z = math.cos(math.radians(float(l1[2])))
        using_sin = math.sin(math.radians(float(l1[2])))
        # drop
        if 45 < float(l1[2]) < 315:
            continue

        if l1[3] == '':
            if float(l1[4]) > 700 or 0 <= float(l1[4]) < 70:
                continue
        else:
            if float(l1[3]) > 700 or 0 <= float(l1[3]) < 70:
                continue

        cnt += 1

        # if float(l1[2]) > 345 :
        #    input_y = (float(l1[2])-360)/2
        # else :
        #    input_y = float(l1[2])/2

        if l1[3] == '':
            input_x = start_x + (-float(l1[5]) * step_to_mm)
            #input_y = input_x * tan_y * using_refraction
            input_y = float(l1[4]) * using_sin
            input_z = float(l1[4]) - input_x / cos_z
        else:
            input_x = start_x + (-float(l1[4]) * step_to_mm)
            #input_y = input_x * tan_y * using_refraction
            input_y = float(l1[3]) * using_sin
            input_z = float(l1[3]) - input_x / cos_z

        ffo.write(' {0} {1} {2}\n'.format(input_x, input_y, input_z))
        # print(l1[2], end=' ')
        # print(l1[3])

    #print(cnt)
    ffi.close()
    ffo.close()

if __name__ == "__main__" :
    ConvertToXYZ()