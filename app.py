from flask import Flask, render_template
from utils import build_headline, build_subtext, truncate
from streamate_api import get_performers

app = Flask(__name__)

@app.route('/')
def index():
    # Fetch real performers from Streamate
    performers = get_performers(max_results=10, stream_type="live")
    # You can still use your sample_data for filters, etc.
    # For featured_model, you can pick the first performer or random
    featured_model = performers[0] if performers else None
    
    return render_template(
        'index.html',
        theme=['Dancer', 'Artist'],
        ethnicity=['Asian', 'European'],
        age_range=[20, 30],
        fetishes=['Photography', 'Music'],
        build_headline=build_headline,
        build_subtext=build_subtext,
        truncate=truncate,
        featured_model=featured_model,
        performers=performers,
        footer_data={
            'ethnicities': ['Asian', 'European', 'Latin'],
            'fetishes': ['Photography', 'Music', 'Dance', 'Art'],
            'ages': ['18-25', '25-30', '30+']
        }
    )

if __name__ == '__main__':
    app.run(debug=True) 