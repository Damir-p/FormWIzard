from flask import Flask, request, jsonify, abort
from tinydb import TinyDB
import logging

app = Flask(__name__)
app.config['DB_NAME'] = 'database.json'
app.logger.setLevel(logging.INFO)

handler = logging.FileHandler('app.log')
handler.setLevel(logging.INFO)
app.logger.addHandler(handler)

db = TinyDB(app.config['DB_NAME'])

test_templates = [
    {
        "name": "MyForm",
        "field_name_1": "email",
        "field_name_2": "phone"
    },
    {
        "name": "OrderForm",
        "field_name_1": "text",
        "field_name_2": "date"
    }
]

db.insert_multiple(test_templates)

@app.route('/get_form', methods=['GET', 'POST'])
def get_form():
    try:
        form_data = request.form.to_dict()

        templates = db.all()
        for template in templates:
            template_fields = set(template.keys()) - {'name'}
            if set(form_data.keys()).issuperset(template_fields):
                return jsonify({"template_name": template["name"]})

        field_types = {"date": "Дата", "phone": "Телефон", "email": "Email", "text": "Текст"}
        field_type_order = ["date", "phone", "email", "text"]

        missing_fields = {}
        for field_name in form_data.keys():
            for field_type in field_type_order:
                if field_name.startswith(field_type):
                    missing_fields[field_name] = field_types[field_type]
                    break

        return jsonify(missing_fields)

    except Exception as e:
        app.logger.error(f"Error processing request: {e}")
        abort(500)

if __name__ == '__main__':
    app.run(debug=True)
