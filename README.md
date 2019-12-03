# 专业综合设计

## 环境配置
- python: 3.7.0
- django: 2.2.7
- djangorestframework: 3.10.3
- pypinyin: 0.36.0
格式化工具为autopep8 1.4.4

## 功能划分
主要分为以下4个模块：
- User: 用户模块。其中处理与用户（包括医院医生、职工、各科室工作人员、病人等）、医院部门等相关交互。
- Finance: 财务模块。处理与财务相关的事项，如费用缴纳、账目结算等。
- Medicine: 药品模块。处理与药品相关事宜，如病人领药、配药等。
- Outpatient: 门诊模块。处理与病人在门诊处看病相关事宜，如分诊台分诊、病人就诊、医生诊疗等。