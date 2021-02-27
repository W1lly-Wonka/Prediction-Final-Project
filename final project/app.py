from flask import Flask, render_template, request
import plotly
import plotly.graph_objs as go
import pandas as pd
import json
from sqlalchemy import create_engine
import pickle

import joblib

app = Flask(__name__)


loans = pd.read_csv(r'C:\Users\William\Downloads\Purwadhika Data Science\Final Project Purwadhika\Final Project WillyWonka\HR Analytics Job Change of Data Scientists\project5\project5\hr_clean.csv')


# category plot function
def category_plot(
    cat_plot = 'histplot',
    cat_x = 'gender', cat_y = 'training_hours',
    estimator = 'count', hue = 'target'):

    

    # jika menu yang dipilih adalah histogram
    if cat_plot == 'histplot':
        # siapkan list kosong untuk menampung konfigurasi hist
        data = []
        # generate config histogram dengan mengatur sumbu x dan sumbu y
        for val in loans[hue].unique():
            hist = go.Histogram(
                x=loans[loans[hue]==val][cat_x],
                y=loans[loans[hue]==val][cat_y],
                histfunc=estimator,
                name=str(val)
                )
            #masukkan ke dalam array
            data.append(hist)
        #tentukan title dari plot yang akan ditampilkan
        title='Histogram'
    elif cat_plot == 'boxplot':
        data = []

        for val in loans[hue].unique():
            box = go.Box(
                x=loans[loans[hue] == val][cat_x], #series
                y=loans[loans[hue] == val][cat_y],
                name=str(val)
            )
            data.append(box)
        title='Box'
    # menyiapkan config layout tempat plot akan ditampilkan
    # menentukan nama sumbu x dan sumbu y
    if cat_plot == 'histplot':
        layout = go.Layout(
            title=title,
            xaxis=dict(title=cat_x),
            yaxis=dict(title='frequency'),
            # boxmode group digunakan berfungsi untuk mengelompokkan box berdasarkan hue
            boxmode = 'group'
        )
    else:
        layout = go.Layout(
            title=title,
            xaxis=dict(title=cat_x),
            yaxis=dict(title=cat_y),
            # boxmode group digunakan berfungsi untuk mengelompokkan box berdasarkan hue
            boxmode = 'group'
        )
    #simpan config plot dan layout pada dictionary
    result = {'data': data, 'layout': layout}

    #json.dumps akan mengenerate plot dan menyimpan hasilnya pada graphjson
    graphJSON = json.dumps(result, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON

# akses halaman menuju route '/' untuk men-test
# apakah API sudah running atau belum
@app.route('/')
def index():
    plot = category_plot()
    # dropdown menu
    # kita lihat pada halaman dashboard terdapat menu dropdown
    # terdapat lima menu dropdown, sehingga kita mengirimkan kelima variable di bawah ini
    # kita mengirimnya dalam bentuk list agar mudah mengolahnya di halaman html menggunakan looping
    list_plot = [('histplot', 'Histogram'), ('boxplot', 'Box')]
    list_x = [('city', 'city'), ('gender', 'gender'), ('relevent_experience', 'relevent_experience'),('enrolled_university','enrolled_university'),('education_level','education_level'),('major_discipline','major_discipline'),('experience','experience'),('company_size','company_size'),('company_type','company_type'),('last_new_job','last_new_job'),('target','target')]
    list_y = [('city_development_index', 'city_development_index'), ('training_hours', 'training_hours')]
    list_estimator = [('count', 'Count'), ('sum', 'Sum'),('avg','Average'), ('min', 'Minimum'), ('max', 'Maximum')]
    list_hue = [('target', 'target')]

    return render_template(
        # file yang akan menjadi response dari API
        'category.html',
        # plot yang akan ditampilkan
        plot=plot,
        # menu yang akan tampil di dropdown 'Jenis Plot'
        focus_plot='histplot',
        # menu yang akan muncul di dropdown 'sumbu X'
        focus_x='gender',

        # untuk sumbu Y tidak ada, nantinya menu dropdown Y akan di disable
        # karena pada histogram, sumbu Y akan menunjukkan kuantitas data

        # menu yang akan muncul di dropdown 'Estimator'
        focus_estimator='count',
        # menu yang akan tampil di dropdown 'Hue'
        focus_hue='target',
        # list yang akan digunakan looping untuk membuat dropdown 'Jenis Plot'
        drop_plot= list_plot,
        # list yang akan digunakan looping untuk membuat dropdown 'Sumbu X'
        drop_x= list_x,
        # list yang akan digunakan looping untuk membuat dropdown 'Sumbu Y'
        drop_y= list_y,
        # list yang akan digunakan looping untuk membuat dropdown 'Estimator'
        drop_estimator= list_estimator,
        # list yang akan digunakan looping untuk membuat dropdown 'Hue'
        drop_hue= list_hue)

# ada dua kondisi di mana kita akan melakukan request terhadap route ini
# pertama saat klik menu tab (Histogram & Box)
# kedua saat mengirim form (saat merubah salah satu dropdown) 
@app.route('/cat_fn/<nav>')
def cat_fn(nav):

    # saat klik menu navigasi
    if nav == 'True':
        cat_plot = 'histplot'
        cat_x = 'gender'
        cat_y = 'training_hours'
        estimator = 'count'
        hue = 'target'
    
    # saat memilih value dari form
    else:
        cat_plot = request.args.get('cat_plot')
        cat_x = request.args.get('cat_x')
        cat_y = request.args.get('cat_y')
        estimator = request.args.get('estimator')
        hue = request.args.get('hue')

    # Dari boxplot ke histogram akan None
    if estimator == None:
        estimator = 'count'
    
    # Saat estimator == 'count', dropdown menu sumbu Y menjadi disabled dan memberikan nilai None
    if cat_y == None:
        cat_y = 'training_hours'

    # Dropdown menu
    list_plot = [('histplot', 'Histogram'), ('boxplot', 'Box')]
    list_x = [('city', 'city'), ('gender', 'gender'), ('relevent_experience', 'relevent_experience'),('enrolled_university','enrolled_university'),('education_level','education_level'),('major_discipline','major_discipline'),('experience','experience'),('company_size','company_size'),('company_type','company_type'),('last_new_job','last_new_job'),('target','target')]
    list_y = [('city_development_index', 'city_development_index'), ('training_hours', 'training_hours')]
    list_estimator = [('count', 'Count'), ('sum', 'Sum'),('avg','Average'), ('min', 'Minimum'), ('max', 'Maximum')]
    list_hue = [('target', 'target')]


    plot = category_plot(cat_plot, cat_x, cat_y, estimator, hue)
    return render_template(
        # file yang akan menjadi response dari API
        'category.html',
        # plot yang akan ditampilkan
        plot=plot,
        # menu yang akan tampil di dropdown 'Jenis Plot'
        focus_plot=cat_plot,
        # menu yang akan muncul di dropdown 'sumbu X'
        focus_x=cat_x,
        focus_y=cat_y,

        # menu yang akan muncul di dropdown 'Estimator'
        focus_estimator=estimator,
        # menu yang akan tampil di dropdown 'Hue'
        focus_hue=hue,
        # list yang akan digunakan looping untuk membuat dropdown 'Jenis Plot'
        drop_plot= list_plot,
        # list yang akan digunakan looping untuk membuat dropdown 'Sumbu X'
        drop_x= list_x,
        # list yang akan digunakan looping untuk membuat dropdown 'Sumbu Y'
        drop_y= list_y,
        # list yang akan digunakan looping untuk membuat dropdown 'Estimator'
        drop_estimator= list_estimator,
        # list yang akan digunakan looping untuk membuat dropdown 'Hue'
        drop_hue= list_hue
    )

##################
## SCATTER PLOT ##
##################

# scatter plot function
def scatter_plot(cat_x, cat_y, hue):


    data = []

    for val in loans[hue].unique():
        scatt = go.Scatter(
            x = loans[loans[hue] == val][cat_x],
            y = loans[loans[hue] == val][cat_y],
            mode = 'markers',
            name = str(val)
        )
        data.append(scatt)

    layout = go.Layout(
        title= 'Scatter',
        title_x= 0.5,
        xaxis=dict(title=cat_x),
        yaxis=dict(title=cat_y)
    )

    result = {"data": data, "layout": layout}

    graphJSON = json.dumps(result,cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON

@app.route('/scatt_fn')
def scatt_fn():
    cat_x = request.args.get('cat_x')
    cat_y = request.args.get('cat_y')
    hue = request.args.get('hue')

    # WAJIB! default value ketika scatter pertama kali dipanggil
    if cat_x == None and cat_y == None and hue == None:
        cat_x = 'training_hours'
        cat_y = 'city_development_index'
        hue = 'target'

    # Dropdown menu
    
    list_x = [('training_hours', 'training_hours'), ('city_development_index', 'city_development_index')]
    list_y = [('training_hours', 'training_hours'), ('city_development_index', 'city_development_index')]
    list_hue = [('target','target')]


    plot = scatter_plot(cat_x, cat_y, hue)

    return render_template(
        'scatter.html',
        plot=plot,
        focus_x=cat_x,
        focus_y=cat_y,
        focus_hue=hue,
        drop_x= list_x,
        drop_y= list_y,
        drop_hue= list_hue
    )

##############
## PIE PLOT ##
##############

def pie_plot(hue = 'BAD'):
    


    vcounts = loans[hue].value_counts()

    labels = []
    values = []

    for item in vcounts.iteritems():
        labels.append(item[0])
        values.append(item[1])
    
    data = [
        go.Pie(
            labels=labels,
            values=values
        )
    ]

    layout = go.Layout(title='Pie', title_x= 0.48)

    result = {'data': data, 'layout': layout}

    graphJSON = json.dumps(result,cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON

@app.route('/pie_fn')
def pie_fn():
    hue = request.args.get('hue')

    if hue == None:
        hue = 'target'

    list_hue = [('target', 'target'),('gender','gender'),('education_level','education_level'),('enrolled_university','enrolled_university'),('major_discipline','major_discipline')]

    plot = pie_plot(hue)
    return render_template('pie.html', plot=plot, focus_hue=hue, drop_hue= list_hue)



@app.route('/predict', methods=['POST','GET'])
def predict():
    return render_template('predict.html')

@app.route('/result', methods=['POST','GET'])
def result():
    if request.method=='POST':
        input = request.form

        df_to_predict = pd.DataFrame({
            'city': [input['cit']],
            'city_development_index': [input['citdev']],
            'gender' : [input['gen']],
            'relevent_experience' : [input['rel']],
            'enrolled_university' : [input['enrol']],
            'education_level' : [input['ed']],
            'major_discipline' : [input['maj']],
            'experience' : [input['exp']],
            'company_size' : [input['size']],
            'company_type' : [input['tipe']],
            'last_new_job' : [input['last']]
            

        })

        prediksi = model.predict_proba(df_to_predict)[:,1]

        if prediksi > 0.5:
            quality = 'Job Changed'
        else:
            quality = 'Not Changed'
        
        return render_template('result.html', data=input, pred=quality)

if __name__ == '__main__':
   
    filename = r'C:\Users\William\Downloads\Purwadhika Data Science\Final Project Purwadhika\Final Project WillyWonka\HR Analytics Job Change of Data Scientists\project5\project5\dtc_final.sav'
    
    model = pickle.load(open(filename, 'rb'))
    app.run(debug=True, port=8000)