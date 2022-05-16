from django.shortcuts import render
import graphviz
from scapy.all import *
from zigota.settings import STATIC_URL
from .models import Document, MainPCAP
from django.http import JsonResponse
from .pcap_parser_test import getDataset

import os

import pandas as pd
import json


# глобальный датафрейм с данными из PCAP файла
g_df = pd.DataFrame()


def check_dataframe(request):
    global g_df
    if g_df.empty:
        print("Файл не выбран")
        index(request)
        render(request, 'main/main.html', {'data':""})


def index(request):
    global g_df
    if g_df.empty:
        uploadedFile = 'Файл не выбран'
    else:
        try:
            uploadedFile = MainPCAP.objects.all()[0].name
        except:
            uploadedFile = 'Файл не выбран'

    if request.method == "POST":
        
        # Fetching the form data
        fileTitle = request.POST["fileTitle"]
        uploadedFile = request.FILES["uploadedFile"]
        document = Document(
            title = fileTitle,
            uploadedFile = uploadedFile
        )
        document.save()

        try:
            object = MainPCAP.objects.all()[0]
            object.name = str( request.FILES["uploadedFile"])   
            object.save()
        except:
            pcap = MainPCAP(name=str( request.FILES["uploadedFile"]))
            pcap.save()

        start_time = datetime.now()
        g_df = pd.DataFrame(getDataset())

        # Если необходимо сохранить датафрейм
        #  g_df.to_pickle("./dummy.pkl")
        print(f"pandas + db reading = {datetime.now() - start_time}")
        # g_df = pd.read_pickle("./dummy.pkl")

    return render(request, 'main/main.html', {'data': uploadedFile})

 

def test(request):
    check_dataframe(request)
    return render(request, 'main/test.html')


def res_malware(request):
    global g_df
    check_dataframe(request)

    alert_df = g_df[(g_df['extinfo'] != 'no malware') & (g_df['extinfo'] != 'undefined')]
    return render(request, 'main/res_malware.html', {'data': dict(alert_df['extinfo'].value_counts())})


def res_mac(request):
    context = {
        'src': dict(g_df['src_vendor'].value_counts()),
        'dst': dict(g_df['dst_vendor'].value_counts())
    }
    return render(request, 'main/res_mac.html', context)


def mac_data(request):

    global g_df
    check_dataframe(request)

    df1 = g_df[['src_mac', 'src_vendor', 'dst_mac', 'dst_vendor']]
    return JsonResponse({'data': json.loads(df1.to_json(orient='records'))})


def malware_data(request):
    global g_df
    check_dataframe(request)

    df_tall = g_df[(g_df['extinfo'] != 'no malware') & (g_df['extinfo'] != 'undefined')]
    df1 = df_tall[['id_pack', 'source_ip','country1', 'destination_ip','country2','extinfo', 'dst_port']]
    return JsonResponse({'data': json.loads(df1.to_json(orient='records'))})


def cap_data(request):
   
    global g_df
    check_dataframe(request)

    df1 = g_df[['id_pack','time', 'source_ip', 'destination_ip','src_port',
                'dst_port', 'src_mac','dst_mac','protocol', 'ttl', 'packet_length']]
    js = df1.to_json(orient='records')   
    return JsonResponse({'data': json.loads(js)})

 
def protocol(request):

    global g_df
    check_dataframe(request)
    return render(request, 'main/protocol.html', {'data': dict(g_df['protocol'].value_counts())})


def get_map_data(request):
    # для аджакс запроса со страницы отображения карты
    global g_df
    check_dataframe(request)
    df1 = g_df[['city1','city2','country1','country2','source_ip', 'destination_ip',
                'lat1', 'long1', 'lat2','long2']].drop_duplicates()
    
    js = df1[df1['source_ip'] != 'no info'].to_json(orient='records')   
    return JsonResponse({'data': json.loads(js)})


def results_http(request):
    check_dataframe(request)
    return render(request, 'main/res_http.html')


def http_data(request):
    global g_df
    check_dataframe(request)

    df_tall = g_df[g_df['info'] != 'no info found']
    df1 = df_tall[['source_ip','protocol', 'info', 'packet_length']]
    return JsonResponse({'data': json.loads(df1.to_json(orient='records'))})


def results_geolocation(request):

    global g_df
    check_dataframe(request)

    context = {
        'countries1':  dict(g_df['country1'].value_counts()),
        'countries2': dict(g_df['country2'].value_counts()),
        'cities1': dict(g_df['city1'].value_counts()),
        'cities2': dict(g_df['city2'].value_counts())
    }

    return render(request, 'main/geolocation.html',context) 


def results_packets_size(request):
    global g_df
    check_dataframe(request)

    # todo если есть ip с большим числом пакетов => получается некрасивый график
    context = {
        'time': g_df['id_pack'].tolist(),
        'plenght':  g_df['packet_length'].tolist(),
        'source_ip':  dict(g_df['source_ip'].value_counts().loc[lambda x: x < 10000]),
        'destination_ip': dict(g_df['destination_ip'].value_counts().loc[lambda x: x < 10000])
    }
    return render(request, 'main/packets_size.html', context)


def getMap(request):
    global g_df
    check_dataframe(request)
    return render(request, 'main/map.html')


def graphs(request):
    global g_df
    check_dataframe(request)
    try:
        MAIN_FILE = MainPCAP.objects.all()[0].name

    except:
        print('Not Upload File')

    pcap_file = STATIC_URL + 'UploadedFiles/' + MAIN_FILE
    maxOfPacetsToDraw = 50
    maxOfSessionToDraw = 50

    # делаем карту сессий
    f = graphviz.Digraph('NetworkGraph', engine='dot', format='png',
                         filename=STATIC_URL + 'graphsImage/' + 'sessionsMap.gv')
    f.body.append('dpi = 700\n')
    f.attr(rankdir='LR', size='2,5')
    a = rdpcap(pcap_file)
    sessions = a.sessions()
    counter = 0
    for s in sessions:
        if counter < maxOfSessionToDraw:
            temp = s.split()
            if len(temp) > 3:
                f.edge(temp[1], temp[3], label=temp[0])
                counter += 1
    f.save()
    f.render()

    # делаем карту пакетов
    f = graphviz.Digraph('NetworkGraph', engine='dot', format='png',
                         filename=STATIC_URL + 'graphsImage/' + 'packetsMap.gv')
    f.body.append('dpi = 700\n')
    f.attr(rankdir='LR', size='2,5')
    f.attr('node', shape='circle')
    a = 0
    for packet in PcapReader(pcap_file):
        try:
            if a < maxOfPacetsToDraw:
                f.edge(str(packet[IP].src), str(packet[IP].dst), label=str('packet' + str(a)))
                a += 1
        except:
            pass
    f.render()
    f.save()

    return render(request, 'main/graphs.html')


from .FileDetect.sirogane import all_files


def detectFiles(request):
    global g_df
    check_dataframe(request)
    try:
        MAIN_FILE = MainPCAP.objects.all()[0].name
    except:
        print('Not Upload File')

    pcap_file = STATIC_URL + 'UploadedFiles/' + MAIN_FILE
    pathToFiles, fileName = all_files(pcap_file, STATIC_URL, MAIN_FILE)

    context = {
        'files': pathToFiles,
        'filesName': fileName
    }
    if not fileName:
        print('NO FIND FILES')

    return render(request, 'main/detectFiles.html', context)




def voip(request):

    if os.name != "posix":
        return render(request, 'main/voip.html', context = {})
    else:

        global g_df
        check_dataframe(request)
        print('VoIP start')
        os.system("rm -rf /home/user/Документы/MainProject/static/voip_result/voip_app_files")
        try:
            MAIN_FILE = MainPCAP.objects.all()[0].name
        except:
            print('Not Upload File')

        pcap_file = STATIC_URL + 'UploadedFiles/' + MAIN_FILE  # /static/UploadedFiles/q3

        # os.system('python3 main/VOIPdetect/voip.py '+pcap_file+' '+'main/TEST/')

        # FIXME !!!! Пути к файлам прописать
        # 1 voip2.py
        # 2 PCAP файл, из которого берется инфа
        # 3 куда сохранять
        try:
            os.system(
                f'python3 /home/user/Документы/MainProject/main/voip2.py '
                f'/home/user/Документы/MainProject/static/UploadedFiles/{MAIN_FILE}'
                f' /home/user/Документы/MainProject/static/voip_result')
            print('+' * 40)
            # voip_extract('../'+STATIC_URL+'/'+MAIN_FILE, STATIC_URL + 'voip_result')
        except:
            pass
        print('=' * 40)
        go_back = os.getcwd()
        os.chdir(os.getcwd() + '/static/voip_result/voip_app_files')
        # foldername = os.getcwd().split('/')[-1]
        foldername = os.listdir()[0]
        os.chdir(os.getcwd() + '/' + foldername)
        filename = os.listdir('Voice_output')[0]
        print(foldername, filename)
        context = {
            'files': STATIC_URL + 'voip_result/voip_app_files/' + foldername + '/Voice_output/' + filename,
            'filesName': filename,
            'png': STATIC_URL + 'voip_result/voip_app_files/' + foldername + '/Plots/' + 'VoiP.stream 1.png'
        }
        os.chdir(go_back)
        print(os.getcwd())
        return render(request, 'main/voip.html', context)


def graphs(request):

    if os.name != "posix":
        return render(request, 'main/graphs.html')
    else:

        MAIN_FILE = None
        try:
            MAIN_FILE = MainPCAP.objects.all()[0].name
        except:
            print('Not Upload File')
        print('=' * 40)
        pcap_file = STATIC_URL + 'UploadedFiles/' + MAIN_FILE
        maxOfPacetsToDraw = 50
        maxOfSessionToDraw = 50

        # делаем карту сессий
        f = graphviz.Digraph('NetworkGraph', engine='dot', format='png',
                             filename=STATIC_URL + 'graphsImage/' + 'sessionsMap.gv')
        f.body.append('dpi = 500\n')
        f.attr(rankdir='LR', size='2,5')
        f.attr('node', shape='doublecircle', style="filled")
        dict_color_ses = {}
        a = rdpcap(pcap_file)
        sessions = a.sessions()
        counter = 0
        for s in sessions:
            if counter < maxOfSessionToDraw:
                temp = s.split()
                if len(temp) > 3:
                    list_str = temp[1].split(":")
                    if list_str[0] not in dict_color_ses:
                        dict_color_ses[list_str[0]] = rand_color()
                        f.node(list_str[0], fillcolor=dict_color_ses[list_str[0]])
                    f.edge(temp[1], temp[3], label=temp[0], color=dict_color_ses[list_str[0]])
                    counter += 1
        f.save()
        f.render()

        # делаем карту пакетов
        f = graphviz.Digraph('NetworkGraph', engine='dot', format='png',
                             filename=STATIC_URL + 'graphsImage/' + 'packetsMap.gv')
        f.body.append('dpi = 500\n')
        f.attr(rankdir='LR', size='2,5')
        f.attr('node', shape='doublecircle', style="filled")
        dict_color_pac = {}
        a = 0
        for packet in PcapReader(pcap_file):
            try:
                if a < maxOfPacetsToDraw:
                    list_str = str(packet[IP].src).split(":")
                    if list_str[0] not in dict_color_pac:
                        dict_color_pac[list_str[0]] = rand_color()
                        f.node(list_str[0], fillcolor=dict_color_pac[list_str[0]])
                    f.edge(str(packet[IP].src), str(packet[IP].dst), label=str('packet' + str(a)),
                           style="dashed", color=dict_color_pac[list_str[0]])
                    a += 1
            except:
                pass
        f.render()
        f.save()

        return render(request, 'main/graphs.html')


def rand_color():
    r = lambda: random.randint(0, 255)
    str = '#%02X%02X%02X' % (r(), r(), r())
    return str