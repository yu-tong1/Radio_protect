# 辐射防护中药成分筛选系统

## 1. 系统概述

本系统是一个基于 Flask 框架开发的辐射防护中药成分筛选平台，旨在帮助研究人员快速筛选具有辐射防护作用的中药成分和方剂。系统集成了多种功能模块，包括化合物筛选、方剂筛选、重金属诱导排泄预测等，为辐射防护研究提供了有力的工具支持。

### 1.1 技术架构

- **后端**：Flask 框架
- **前端**：HTML、CSS、JavaScript、Bootstrap
- **数据处理**：Pandas、RDKit（分子指纹生成）
- **机器学习**：使用 joblib 加载模型
- **API 集成**：BATMAN2 API（靶点预测）

### 1.2 系统目录结构

```
website/
├── Compound screening results/    # 筛选结果存储目录
├── templates/                      # 前端模板
│   ├── web_database_files/         # 静态资源文件
│   ├── Compound_screening.html     # 化合物筛选页面
│   ├── Herb_and_Formula_screening.html  # 中药和方剂筛选页面
│   ├── Herb_miRNA_data.html        # 中药 miRNA 数据页面
│   ├── Heavy_Metal_Induced_Excretion_Compound_Screening.html  # 重金属诱导排泄筛选页面
│   └── AI_Analysis.html            # AI 分析页面
├── Compound_Induced_Excretion_Prediction.py  # 重金属诱导排泄预测模块
├── Compound_screening_cancer.py    # 癌症模式下的化合物筛选
├── Compound_screening_normal.py    # 正常模式下的化合物筛选
├── Herb_and_Formula_screening.py   # 中药和方剂筛选模块
├── AI_Analysis.py                  # AI 分析模块
├── U_RF_model.joblib               # 重金属诱导排泄预测模型
├── app.py                          # 主应用程序
└── Test-file Zisu.csv                # 测试用例文件
```

## 2. 功能模块

### 2.1 辐射防护化合物筛选 (RadioProtect Compound Screening)

**功能说明**：
- 上传中药成分 CSV 文件，筛选具有辐射防护作用的化合物
- 支持两种筛选模式：正常模式和癌症模式
- 生成匹配和未匹配的结果文件
- 提供结果下载功能

**技术实现**：
- 使用 `Compound_screening_normal.py` 和 `Compound_screening_cancer.py` 处理不同模式的筛选
- 通过 pandas 进行数据处理和匹配
- 调用 BATMAN2 API 进行靶点预测

### 2.2 辐射防护方剂筛选 (RadioProtect Formula Screening)

**功能说明**：
- 提供 17 种辐射防护中药及其成分
- 根据辐射防护化合物搜索相关中药和方剂
- 展示方剂中包含的辐射防护化合物数量

**技术实现**：
- 使用 `Herb_and_Formula_screening.py` 实现筛选逻辑
- 通过 Counter 统计方剂中辐射防护化合物的数量
- 从 `herb_batman_matched.csv` 和 `formula_batman_matched.csv` 加载数据

### 2.3 重金属诱导排泄化合物筛选 (Heavy Metal Induced Excretion Compound Screening)

**功能说明**：
- 上传包含 SMILES 结构的 CSV 文件
- 预测化合物的重金属诱导排泄能力
- 展示预测结果，包括化合物结构、预测值和使用的指纹类型

**技术实现**：
- 使用 `Compound_Induced_Excretion_Prediction.py` 实现预测功能
- 基于 RDKit 生成分子指纹（3D 药效团指纹、2D 药效团指纹、Morgan 指纹）
- 使用预训练的随机森林模型进行预测

### 2.4 中药 miRNA 数据 (Herb miRNA data)

**功能说明**：
- 展示中药 miRNA 相关数据

**技术实现**：
- 通过前端页面展示 miRNA 数据

### 2.5 AI 解读筛选结果 (AI Analysis of Screening Results)

**功能说明**：
- 智能分析化合物筛选结果，生成专业的分析报告
- 支持不同辐射类型（X-rays、γ-rays、α-particles、Heavy Metal、protons）的分析
- 提供 API 配置选项，支持多种 AI 模型
- 可自定义系统提示词，调整分析方向

**技术实现**：
- 使用 `AI_Analysis.py` 实现后端分析逻辑
- 通过前端页面 `AI_Analysis.html` 提供用户交互界面
- 集成 OpenAI SDK，调用 AI 模型进行分析
- 从 `Compound screening results` 目录读取筛选结果文件
- 按药材分组，统计主要基因、通路、化合物类型等信息
- 生成结构化的分析报告，包括化合物种类富集、主要基因通路、药物相似性和口服生物利用度、防护机制等方面

## 3. 操作指南

### 3.1 系统启动

1. 确保安装了所需的依赖包：
   ```
   pip install flask pandas rdkit joblib requests openai sklearn numpy
   ```

   **注意**：如果使用 AI 分析功能，需要额外安装 openai 库。

2. 进入 website 目录，运行应用：
   ```
   python app.py
   ```

3. 打开浏览器，访问 http://localhost:5000

### 3.2 辐射防护化合物筛选操作步骤

1. 在导航栏中点击 "Tools" > "RadioProtect Compound Screening"
2. 在页面中选择筛选模式（正常或癌症）
3. 点击 "选择文件" 按钮，上传包含中药成分的 CSV 文件
4. 点击 "Submit" 按钮提交
5. 等待系统处理完成
6. 查看筛选结果，包括匹配和未匹配的化合物
7. 点击 "Download" 按钮下载结果文件

### 3.3 辐射防护方剂筛选操作步骤

1. 在导航栏中点击 "Tools" > "RadioProtect Formula Screening"
2. 系统自动加载并展示筛选结果
3. 查看正常模式和癌症模式下的方剂筛选结果
4. 查看相关中药列表

### 3.4 重金属诱导排泄化合物筛选操作步骤

1. 在导航栏中点击 "Tools" > "Heavy Metal Decorporation Compound Screening"
2. 点击 "选择文件" 按钮，上传包含 SMILES 结构的 CSV 文件
3. 点击 "Submit" 按钮提交
4. 等待系统处理完成
5. 查看预测结果，包括化合物结构、预测值和使用的指纹类型

### 3.5 中药 miRNA 数据操作步骤

1. 在导航栏中点击 "Tools" > "Plant microRNA Targets in Human"
2. 进入外部链接页面进行 miRNA 靶点预测

### 3.6 AI 解读筛选结果操作步骤

1. 在导航栏中点击 "Tools" > "AI Analysis"
2. 在页面中选择分析模式（Compound AI Analysis）
3. 选择子模式（Cancer Mode 或 Normal Mode）
4. 选择辐射类型（根据所选模式不同，可选的辐射类型会有所不同）
5. 配置 API 设置：
   - 输入 API Key
   - 设置 API Base URL（默认为 https://api.deepseek.com）
   - 选择 AI 模型
6. 可根据需要修改系统提示词，调整分析方向
7. 点击 "Run AI Analysis" 按钮开始分析
8. 等待系统处理完成，查看 AI 生成的分析报告

**注意**：使用 AI 分析功能需要先进行化合物筛选，生成筛选结果文件，AI 会从 `Compound screening results` 目录读取这些文件进行分析。

## 4. 数据格式要求

### 4.1 辐射防护化合物筛选数据格式

CSV 文件应包含以下列（任意一种）：
- CID 列：`cid`, `CID`, `Cid`, `cID`, `pubchem_id`, `PubChem_id`, `PubChem_ID`
- 基因名列：`gene_name`, `Gene_name`

**示例文件**：`Test-file Zisu.csv`

### 4.2 重金属诱导排泄化合物筛选数据格式

CSV 文件应包含 `SMILE` 列，用于存储化合物的 SMILES 结构。

## 5. 结果解释

### 5.1 辐射防护化合物筛选结果

- **Matching results**：包含与辐射防护靶点匹配的化合物
- **Unmapped results**：未匹配的化合物

结果文件保存在 `Compound screening results` 目录中，命名格式为：
- 正常模式：`Matching normal results of [文件名] ingredients.csv`
- 癌症模式：`Matching cancer results of [文件名] ingredients.csv`

### 5.2 辐射防护方剂筛选结果

- **Normal Formula**：正常模式下的方剂筛选结果，显示方剂名称和包含的辐射防护化合物数量
- **Cancer Formula**：癌症模式下的方剂筛选结果
- **Herb Normal**：正常模式下的中药列表
- **Herb Cancer**：癌症模式下的中药列表

### 5.3 重金属诱导排泄化合物筛选结果

- **smiles**：化合物的 SMILES 结构
- **prediction**：预测值（1 表示具有重金属诱导排泄能力，0 表示不具有）
- **fp_type**：使用的指纹类型（3d_pharmacophore、2d_pharmacophore 或 morgan）

## 6. 系统配置与维护

### 6.1 配置文件

- **app.py**：主配置文件，包含路由和核心功能
- **UPLOAD_FOLDER**：上传文件存储目录（默认为 'uploads'）
- **BATMAN2_API_URL**：BATMAN2 API 地址（默认为 'http://batman2api.cloudna.cn/queryTarget'）

### 6.2 模型文件

- **U_RF_model.joblib**：重金属诱导排泄预测模型

### 6.3 数据文件

- **DEGs_normal.csv**：正常模式下的差异表达基因
- **DEGs_cancer.csv**：癌症模式下的差异表达基因
- **herb_ingredient.csv**：中药成分数据
- **results of target matching normal.csv**：正常模式下的靶点匹配结果
- **results of target matching cancer.csv**：癌症模式下的靶点匹配结果
- **herb_batman_matched.csv**：中药与 BATMAN 匹配数据
- **formula_batman_matched.csv**：方剂与 BATMAN 匹配数据

## 7. 常见问题与解决方案

### 7.1 上传文件失败

- **问题**：上传文件后系统提示错误
- **解决方案**：检查文件格式是否正确，确保文件包含所需的列（如 CID 或 SMILE）

### 7.2 筛选结果为空

- **问题**：筛选后没有匹配的化合物
- **解决方案**：检查输入文件中的 CID 或基因名是否正确，确保数据格式符合要求

### 7.3 系统运行缓慢

- **问题**：处理大型文件时系统响应缓慢
- **解决方案**：减小文件大小，或分批处理数据

### 7.4 API 调用失败

- **问题**：BATMAN2 API 调用失败
- **解决方案**：检查网络连接，确保 API 地址正确

## 8. 示例使用流程

### 8.1 使用测试文件进行辐射防护化合物筛选

1. 启动系统后，进入 "RadioProtect Compound Screening" 页面
2. 选择 "normal" 模式
3. 上传 "Test-file Zisu.csv"
4. 点击 "Submit" 按钮
5. 查看筛选结果，下载 "Matching normal results of Test-file Zisu ingredients.csv"

### 8.2 进行重金属诱导排泄化合物筛选

1. 准备包含 SMILES 结构的 CSV 文件
2. 进入 "Heavy Metal Decorporation Compound Screening" 页面
3. 上传 "Test-file Zisu.csv"
4. 点击 "Submit" 按钮
5. 查看预测结果，分析化合物的重金属诱导排泄能力

## 9. 技术支持

- **联系人**：马家骅教授 Email: jiahuama@swust.edu.cn
- **开发者**：
            马家骅（博士，教授，西南科技大学生命科学与农林学院）；
            柒世龙（硕士在读，西南科技大学生命科学与农林学院）；
            周阳（本科在读，西南科技大学生命科学与农林学院）。
- **机构**：西南科技大学生命科学与农林学院
- **项目**：辐射防护中药成分筛选系统

## 10. 更新日志

- **2026/4/13**：添加 AI 解读筛选结果功能，支持智能分析化合物筛选结果并生成专业报告
- **2026/3/30**：修改基于 Gene name 的映射逻辑，适配 BATMAN API 数据
- **2026/3/16**：添加辐射防护方剂筛选功能
- **2026/3/14**：添加辐射防护中药化合物筛选功能
