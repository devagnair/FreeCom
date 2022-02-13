from flask import Flask,render_template,request,Response
from price_comp import comp
from prod_comp import detail
from qr_decoder import generate_frames,__del__
app=Flask(__name__)

@app.route("/")
@app.route("/home")
def home_page():
    return render_template("home.html")

@app.route("/result")
def result_page():
    if request.method=='GET':
        x=request.args['query']
        print(x)
        x_name=x

        cont=True
        while cont:
             try:
                items=comp(x)
                cont=False
                 
             except:
                cont=True  #change

        #print(z)
        #items=comp(x)
        #print(len(items))
    
    return render_template("result.html",items=items,x_name=x_name) #items=items

@app.route("/prod")
def product():
    return render_template("prod_input.html")

@app.route("/result2", methods=['post', 'get'])
def product_result():
       if request.method=='POST':
         one=request.form.get('nm1')
         two=request.form.get('nm2')
         #x_one=one
         #x_two=two
         print(one)
         print(two)
         det=detail(one,two)
         print(det)
         comb=one +' and '+ two
       return render_template("result_2.html",det=det,comb=comb)

@app.route('/qr')
def qr_disp():
    return render_template('disp.html')

@app.route('/video')
def video():
    return Response(generate_frames(),mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(debug=True)