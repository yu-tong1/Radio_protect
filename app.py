# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify, send_from_directory, render_template
import os
import csv
import uuid
import requests
import webbrowser
import threading
import time
from Compound_screening_normal import process_tcm_file_normal
from Compound_screening_cancer import process_tcm_file_cancer
from Herb_and_Formula_screening import screen_herb_formula
from Compound_Induced_Excretion_Prediction import predict_target, process_data
from AI_Analysis import analyze_compound



app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs('Compound screening results', exist_ok=True)

BATMAN2_API_URL = 'http://batman2api.cloudna.cn/queryTarget'


@app.route('/web_database_files/<path:filename>')
def serve_static(filename):
    return send_from_directory('templates/web_database_files', filename)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/Compound_screening.html')
def compound_screening_normal():
    return render_template('Compound_screening.html')

@app.route('/Herb_and_Formula_screening.html')
def herb_and_formula_screening():
    return render_template('Herb_and_Formula_screening.html')

@app.route('/Herb_miRNA_data.html')
def herb_miRNA_data():
    return render_template('Herb_miRNA_data.html')

@app.route('/AI_Analysis.html')
def AI_analysis():
    return render_template('AI_Analysis.html')

@app.route('/Heavy_Metal_Induced_Excretion_Compound_Screening.html')
def heavy_metal():
    return render_template('Heavy_Metal_Induced_Excretion_Compound_Screening.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'Empty filename'}), 400

    original_filename = file.filename
    ext = os.path.splitext(original_filename)[1]
    temp_filename = str(uuid.uuid4()) + ext
    temp_path = os.path.join(UPLOAD_FOLDER, temp_filename)
    file.save(temp_path)

    try:
        model_file = 'U_RF_model.joblib'
        predictions = process_data(temp_path, model_file, original_filename)
        results = []
        for smiles, prediction, fp_type in predictions:
            if hasattr(prediction, 'item'):
                prediction = prediction.item()
            results.append({
                'smiles': smiles,
                'prediction': prediction,
                'fp_type': fp_type
            })
        return jsonify({'results': results})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except:
                pass

@app.route('/run_herb_formula', methods=['POST'])
def run_herb_formula_screening():
    try:
        normal_dict, cancer_dict, herb_normal, herb_cancer = screen_herb_formula()
        
        normal_list = [{'formula': key, 'count': value} for key, value in normal_dict.items()]
        cancer_list = [{'formula': key, 'count': value} for key, value in cancer_dict.items()]
        
        return jsonify({
            'normal': normal_list,
            'cancer': cancer_list,
            'herb_normal': herb_normal,
            'herb_cancer': herb_cancer
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/run', methods=['POST'])
def run_screening():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'Empty filename'}), 400

    mode = request.form.get('mode', 'normal')

    if mode not in ['normal', 'cancer']:
        return jsonify({'error': 'Invalid mode. Must be "normal" or "cancer"'}), 400

    ext = os.path.splitext(file.filename)[1]
    temp_filename = str(uuid.uuid4()) + ext
    temp_path = os.path.join(UPLOAD_FOLDER, temp_filename)
    file.save(temp_path)

    original_filename = os.path.basename(file.filename)

    try:
        if mode == 'normal':
            matched, unmatched = process_tcm_file_normal(temp_path, original_filename)
        else:
            matched, unmatched = process_tcm_file_cancer(temp_path, original_filename)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        os.remove(temp_path)

    base_name = os.path.splitext(original_filename)[0]
    if mode == 'normal':
        matched_file = "Matching normal results of " + base_name + " ingredients.csv"
        unmatched_file = "Unmapped normal results of " + base_name + " ingredients.csv"
    else:
        matched_file = "Matching cancer results of " + base_name + " ingredients.csv"
        unmatched_file = "Unmapped cancer results of " + base_name + " ingredients.csv"

    matched_data = matched.fillna('').to_dict('records') if hasattr(matched, 'to_dict') else matched
    unmatched_data = unmatched.fillna('').to_dict('records') if hasattr(unmatched, 'to_dict') else unmatched

    return jsonify({
        'matched': matched_data,
        'unmatched': unmatched_data,
        'matched_file': matched_file,
        'unmatched_file': unmatched_file
    })

@app.route('/query_target', methods=['POST'])
def query_target():
    try:
        data = request.get_json()
        if not data or 'content' not in data:
            return jsonify({'error': 'Invalid request: missing content'}), 400

        mode = data.get('mode', 'normal')
        if mode not in ['normal', 'cancer']:
            return jsonify({'error': 'Invalid mode. Must be "normal" or "cancer"'}), 400

        # 提取药材/药方名称作为文件名
        content = data['content']
        if not content or not isinstance(content, list):
            return jsonify({'error': 'Invalid content format'}), 400

        first_item = content[0]
        item_name = first_item.get('clusterName', 'unnamed')
        filename = item_name.replace(' ', '_') + '.csv'
        temp_file_path = os.path.join(UPLOAD_FOLDER, filename)

        response = requests.post(
            BATMAN2_API_URL,
            json=data,
            headers={'Content-Type': 'application/json'},
            timeout=60
        )

        if response.status_code != 200:
            return jsonify({'error': 'API error: ' + str(response.status_code)}), response.status_code

        result = response.json()
        
        with open(temp_file_path, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['CID', 'Name', 'gene_name', 'gene_id', 'score']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            processed_results = []
            if isinstance(result, list):
                for item in result:
                    cid = item.get('cid', '')
                    name = item.get('name', '')
                    target_list = item.get('target', [])
                    
                    if target_list:
                        for target_item in target_list:
                            gene_name = target_item.get('gene_name', '')
                            gene_id = target_item.get('gene_id', '')
                            score = target_item.get('score', '')
                            writer.writerow({'CID': cid, 'Name': name, 'gene_name': gene_name, 'gene_id': gene_id, 'score': score})
                            processed_results.append({
                                'name': name,
                                'cid': cid,
                                'gene_name': gene_name,
                                'gene_id': gene_id,
                                'score': score,
                            })
                    else:
                        writer.writerow({'CID': cid, 'Name': name, 'gene_name': '', 'gene_id': '', 'score': ''})
                        processed_results.append({
                            'name': name,
                            'cid': cid,
                            'gene_name': '',
                            'gene_id': '',
                            'score': '',
                        })

        # 调用处理函数
        try:
            if mode == 'normal':
                matched, unmatched = process_tcm_file_normal(temp_file_path, filename)
            else:
                matched, unmatched = process_tcm_file_cancer(temp_file_path, filename)
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        finally:
            # 处理完成后删除临时文件
            if os.path.exists(temp_file_path):
                try:
                    os.remove(temp_file_path)
                except:
                    pass

        base_name = os.path.splitext(filename)[0]
        if mode == 'normal':
            matched_file = "Matching normal results of " + base_name + " ingredients.csv"
            unmatched_file = "Unmapped normal results of " + base_name + " ingredients.csv"
        else:
            matched_file = "Matching cancer results of " + base_name + " ingredients.csv"
            unmatched_file = "Unmapped cancer results of " + base_name + " ingredients.csv"

        matched_data = matched.fillna('').to_dict('records') if hasattr(matched, 'to_dict') else matched
        unmatched_data = unmatched.fillna('').to_dict('records') if hasattr(unmatched, 'to_dict') else unmatched

        return jsonify({
            'results': processed_results,
            'matched': matched_data,
            'unmatched': unmatched_data,
            'matched_file': matched_file,
            'unmatched_file': unmatched_file
        })

    except requests.exceptions.Timeout:
        return jsonify({'error': 'API request timeout'}), 504
    except requests.exceptions.RequestException as e:
        return jsonify({'error': 'API request failed: ' + str(e)}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download/<path:filename>')
def download_file(filename):
    return send_from_directory('Compound screening results', filename, as_attachment=True)

@app.route('/api/analyze-compound', methods=['POST'])
def analyze_compound_api():
    try:
        data = request.get_json()
        if not data or 'radiation_type' not in data:
            return jsonify({'success': False, 'error': 'Missing radiation_type parameter'}), 400
        
        radiation_type = data['radiation_type']
        api_key = data.get('api_key')
        api_base = data.get('api_base')
        system_prompt = data.get('system_prompt')
        model = data.get('model')
        result = analyze_compound(radiation_type, api_key, api_base, system_prompt, model)
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    # 在服务器启动前打开浏览器
    
    def open_browser():
        time.sleep(1)  # 给服务器1秒启动时间
        webbrowser.open('http://localhost:5000')
    
    # 启动浏览器线程
    threading.Thread(target=open_browser).start()
    
    # 运行Flask应用
    app.run(debug=False)
