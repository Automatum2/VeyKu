import re

files = [
    r'd:\Microsoft_VS_Code\CV_WEB\Pak_karma\Veyku\templates\layout\base_survey.html',
    r'd:\Microsoft_VS_Code\CV_WEB\Pak_karma\Veyku\templates\admin\dashboard.html',
    r'd:\Microsoft_VS_Code\CV_WEB\Pak_karma\Veyku\templates\admin\respondents.html',
    r'd:\Microsoft_VS_Code\CV_WEB\Pak_karma\Veyku\templates\admin\respondent_detail.html',
    r'd:\Microsoft_VS_Code\CV_WEB\Pak_karma\Veyku\templates\survey\statistik.html'
]

for file_path in files:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if there is an extra_css block inside the style tags
    if '{% block extra_css %}{% endblock %}' in content:
        new_content = re.sub(r'<style>.*?</style>', '<style>\n        {% block extra_css %}{% endblock %}\n    </style>', content, flags=re.DOTALL)
    else:
        new_content = re.sub(r'<style>.*?</style>', '', content, flags=re.DOTALL)
        
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
        
print('Done replacing CSS in all files.')
