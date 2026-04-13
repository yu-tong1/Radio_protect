import os
import csv
import json

# ===================== OpenAI SDK 导入 =====================
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

# AI设置
DEFAULT_AI_SETTINGS = {
    'model': 'gpt-3.5-turbo',
    'api_key': '',  # 请在使用前设置API密钥
    'api_base': 'https://api.deepseek.com'
}


def analyze_compound(radiation_type, api_key=None, api_base=None, system_prompt=None, model=None):
    """
    分析化合物筛选结果
    :param radiation_type: 辐射类型 (X-rays, α-particles, γ-rays)
    :param api_key: API密钥
    :param api_base: API基础URL
    :param system_prompt: 系统提示词
    :param model: AI模型
    :return: AI分析结果
    """
    if not OPENAI_AVAILABLE:
        return {"success": False, "error": "OpenAI SDK未安装，请运行: pip install openai"}
    
    # 使用前端传递的API配置或默认配置
    api_key = api_key or DEFAULT_AI_SETTINGS['api_key']
    api_base = api_base or DEFAULT_AI_SETTINGS['api_base']
    model = model or DEFAULT_AI_SETTINGS['model']
    
    if not api_key:
        return {"success": False, "error": "请先在前端页面设置API密钥"}
    
    try:
        # 读取Compound screening results文件夹中的所有Matching文件
        results_dir = 'Compound screening results'
        matching_files = []
        
        for filename in os.listdir(results_dir):
            if filename.endswith('.csv'):
                # 检查文件名前两个单词是否为'Matching normal'或'Matching cancer'
                parts = filename.split(' ')
                if len(parts) >= 2 and parts[0] == 'Matching' and (parts[1] == 'normal' or parts[1] == 'cancer'):
                    matching_files.append(os.path.join(results_dir, filename))
        
        if not matching_files:
            return {"success": False, "error": "未找到符合条件的文件"}
        
        # 收集数据
        all_data = []
        for file_path in matching_files:
            # 检查文件名类型
            filename = os.path.basename(file_path)
            parts = filename.split(' ')
            is_cancer_file = len(parts) >= 2 and parts[0] == 'Matching' and parts[1] == 'cancer'
            
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    row_radiation_type = row.get('type_of_radiation')
                    
                    # 根据文件类型应用不同的辐射类型过滤规则
                    if is_cancer_file:
                        # cancer文件：不使用Heavy Metal和α-particles，使用其他辐射类型（包括protons）
                        if row_radiation_type == radiation_type and row_radiation_type not in ['Heavy Metal', 'α-particles']:
                            all_data.append({
                                'file': filename,
                                'CID': row.get('CID', ''),
                                'Name': row.get('Name', ''),
                                'Ingredient_name': row.get('Ingredient_name', ''),
                                'gene_name': row.get('gene_name', ''),
                                'pathway': row.get('pathway', ''),
                                'dose': row.get('dose', ''),
                                'tissue_cell_line': row.get('tissue_cell_line', ''),
                                'time_after_irradiation': row.get('time_after_irradiation', ''),
                                'Drug_likeness': row.get('Drug_likeness', ''),
                                'OB_score': row.get('OB_score', '')
                            })
                    else:
                        # normal文件：使用所有辐射类型
                        if row_radiation_type == radiation_type:
                            all_data.append({
                                'file': filename,
                                'CID': row.get('CID', ''),
                                'Name': row.get('Name', ''),
                                'Ingredient_name': row.get('Ingredient_name', ''),
                                'gene_name': row.get('gene_name', ''),
                                'pathway': row.get('pathway', ''),
                                'dose': row.get('dose', ''),
                                'tissue_cell_line': row.get('tissue_cell_line', ''),
                                'time_after_irradiation': row.get('time_after_irradiation', ''),
                                'Drug_likeness': row.get('Drug_likeness', ''),
                                'OB_score': row.get('OB_score', '')
                            })
        
        if not all_data:
            return {"success": False, "error": f"未找到{radiation_type}辐射类型的数据"}
        
        # 格式化数据用于AI分析
        input_text = f"化合物筛选结果分析（辐射类型：{radiation_type}）：\n\n"
        input_text += f"共找到 {len(all_data)} 条相关记录\n\n"
        
        # 按药材分组
        herb_data = {}
        for item in all_data:
            # 从文件名中提取药材名称（第五个单词）
            try:
                herb_name = item['file'].split(' ')[4]
            except IndexError:
                # 如果文件名格式不正确，使用默认名称
                herb_name = '未知药材'
            if herb_name not in herb_data:
                herb_data[herb_name] = []
            herb_data[herb_name].append(item)
        
        for herb_name, items in herb_data.items():
            input_text += f"【{herb_name}】\n"
            input_text += f"  相关化合物数量: {len(items)}\n"
            
            # 统计主要基因和通路
            gene_count = {}
            pathway_count = {}
            drug_likeness_values = []
            ob_score_values = []
            compound_types = {}
            
            for item in items:
                if item['gene_name']:
                    gene_count[item['gene_name']] = gene_count.get(item['gene_name'], 0) + 1
                if item['pathway']:
                    pathway_count[item['pathway']] = pathway_count.get(item['pathway'], 0) + 1
                if item['Drug_likeness']:
                    try:
                        drug_likeness_values.append(float(item['Drug_likeness']))
                    except ValueError:
                        pass
                if item['OB_score']:
                    try:
                        ob_score_values.append(float(item['OB_score']))
                    except ValueError:
                        pass
                if item['Ingredient_name']:
                    compound_types[item['Ingredient_name']] = compound_types.get(item['Ingredient_name'], 0) + 1
            
            # 显示前3个主要基因
            top_genes = sorted(gene_count.items(), key=lambda x: x[1], reverse=True)[:3]
            if top_genes:
                input_text += "  主要基因: " + ", ".join([f"{g} ({c}次)" for g, c in top_genes]) + "\n"
            
            # 显示前3个主要通路
            top_pathways = sorted(pathway_count.items(), key=lambda x: x[1], reverse=True)[:3]
            if top_pathways:
                input_text += "  主要通路: " + ", ".join([f"{p} ({c}次)" for p, c in top_pathways]) + "\n"
            
            # 显示药物相似性和口服生物利用度
            if drug_likeness_values:
                avg_drug_likeness = sum(drug_likeness_values) / len(drug_likeness_values)
                input_text += f"  平均药物相似性: {avg_drug_likeness:.2f}\n"
            if ob_score_values:
                avg_ob_score = sum(ob_score_values) / len(ob_score_values)
                input_text += f"  平均口服生物利用度: {avg_ob_score:.2f}\n"
            
            # 显示主要化合物类型
            top_compound_types = sorted(compound_types.items(), key=lambda x: x[1], reverse=True)[:3]
            if top_compound_types:
                input_text += "  主要化合物类型: " + ", ".join([f"{t} ({c}次)" for t, c in top_compound_types]) + "\n"
            
            input_text += "\n"
        
        # 使用OpenAI SDK创建客户端
        client = OpenAI(
            api_key=api_key,
            base_url=api_base
        )
        
        
        # 构建消息
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": input_text}
        ]
        
        # 发送请求
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            stream=False
        )
        
        # 获取结果
        result = response.choices[0].message.content
        
        return {"success": True, "result": result}
        
    except Exception as e:
        return {"success": False, "error": str(e)}
