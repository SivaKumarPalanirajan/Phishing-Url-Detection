from flask import Flask,jsonify,request
import pickle 
import logging 
from scipy.sparse import hstack
import tldextract
import os 
from huggingface_hub import hf_hub_download

logging.basicConfig(level=logging.INFO,format="%(asctime)s - %(levelname)s - %(module)s - %(lineno)s - %(message)s")

app=Flask(__name__)

@app.route('/')
def home():
    return jsonify({'AppName': "PhishingUrlDetection",
                    'Description': "The model can predict if an URL is Phishing or not by using various values derived from the URL",
                    'Version':'v2',
                    'Endpoints':['/health','/predict'],
                    "Status":'Running'}),200

@app.route('/health')
def health():
    try:
        model_path = os.path.join('models','datascaler.pkl')
        model=pickle.load(open(model_path,'rb'))
        return jsonify({'response':'healthy'}),200 
    except:
        return jsonify({'response':'unhealthy'}),503 

@app.route('/predict',methods=['POST'])
def predict():
    try:
        logging.info('Received inferencing request')
        payload=request.get_json() 
        url=payload.get('url')
        url=str(url)
        model_path=os.path.join('models',"model.pkl") 
        model=pickle.load(open(model_path,'rb'))
        logging.info('Loaded model')

        if url is not None:
            if url.startswith("https"):
                is_https=1
            else:
                is_https=0
            digit_cnt=0
            for i in url:
                if i.isnumeric():
                    digit_cnt+=1

            ext = tldextract.extract(url)
            dom,tld=ext.domain+"."+ext.suffix, ext.suffix
            logging.info('Created new features')

            for col in ['dom','tld','url']:
                encoder_path=os.path.join('models',f"dataencoder_{col}.pkl")
                encoder=pickle.load(open(encoder_path,'rb'))
                logging.info(f'Loaded {col} encoder')
                if col=='dom':
                    dom_encoded=encoder.transform([dom])[0]
                elif col=='tld':
                    tld_encoded=encoder.transform([tld])[0]
                elif col=='url':
                    url_encoded=encoder.transform([url])[0]

            logging.info(f'Encoded features')

            scaler_path=os.path.join('models','datascaler.pkl')
            scaler=pickle.load(open(scaler_path,'rb'))
            logging.info(f'Loaded scaler')

            numerical_vals=scaler.transform([[digit_cnt,is_https]])[0]
            logging.info(f'Performed scaling')

            inp_vals=hstack([url_encoded,tld_encoded,dom_encoded,numerical_vals])
            prediction=model.predict(inp_vals)[0]

            logging.info(f'Inferencing completed')
            
            prediction_value={0:'Not Phishing',1:'Phishing'}.get(prediction)
            return jsonify({"prediction":prediction_value,
                            'dom':dom,'tld':tld,'digit_cnt':digit_cnt,'is_https':is_https}),200
        
    except Exception as e:
        logging.exception(f'Error occured during inferencing: {str(e)}')
        return jsonify({'response':f'Error occured: {str(e)}'}),500

@app.errorhandler(500)
def server_error(e):
    return jsonify({"response": str(e)}), 500
    

if __name__=="__main__":
    app.run(host='0.0.0.0',port=7860)