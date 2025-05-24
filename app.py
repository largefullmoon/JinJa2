from flask import Flask, render_template, request
from utils import build_headline, build_subtext, truncate
from streamate_api import get_performers

app = Flask(__name__)

@app.route('/')
def index():
    # Get URL parameters
    age_param = request.args.get('age')
    ethnicity_param = request.args.get('ethnicity')
    count_param = request.args.get('count')
    gender_param = request.args.get('gender')
    fetish_param = request.args.get('fetish')
    keyword_param = request.args.get('keyword')
    keyword_list = keyword_param.split(',') if keyword_param else []

    if count_param is None:
        count_param = 9
    
    # Parse age parameter (format: 10to20)
    age_range = [20, 30]  # default age range
    if age_param:
        try:
            start_age, end_age = map(int, age_param.split('to'))
            age_range = [start_age, end_age]
        except (ValueError, AttributeError):
            pass  # Keep default if parsing fails
    
    # Get ethnicity parameter
    ethnicity_list = ['Asian', 'European']  # default ethnicities
    if ethnicity_param:
        ethnicity_list = [ethnicity_param]
    # Fetch real performers from Streamate
    performers = get_performers(max_results=count_param, stream_type="live", max_age=age_range[1], min_age=age_range[0], ethnicity=ethnicity_list, keyword=keyword_list, gender=gender_param, fetish=fetish_param)
    # Filter performers based on URL parameters if needed
    featured_model = performers[0] if performers else None
    
    return render_template(
        'index.html',
        theme=['Dancer', 'Artist'],
        ethnicity=ethnicity_list,
        age_range=age_range,
        fetishes=['Photography', 'Music'],
        build_headline=build_headline,
        build_subtext=build_subtext,
        truncate=truncate,
        featured_model=featured_model,
        performers=performers,
        footer_data={
            'ethnicities': ethnicity_list,
            'fetishes': ['Photography', 'Music', 'Dance', 'Art'],
            'ages': [age_range]
        }
    )

if __name__ == '__main__':
    app.run(debug=True)