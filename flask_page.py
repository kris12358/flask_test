from flask import Flask, render_template, request
import psycopg2
import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO
import base64

app = Flask(__name__)

# PostgreSQL connection details
DB_HOST = 'localhost'
DB_NAME = 'finance'
DB_USER = 'postgres'
DB_PASSWORD = '123'


def get_data_from_database(start_date, end_date):
    conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD)
    cursor = conn.cursor()

    # Query your data from the database using the specified date range
    cursor.execute("SELECT * FROM stock_data WHERE date BETWEEN %s AND %s", (start_date, end_date))
    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return data


def generate_plot(x, y):
    # Create the plot
    plt.plot(x, y)
    plt.xlabel('X')
    plt.ylabel('Y')

    # Save the plot to a BytesIO object
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plot_data = base64.b64encode(buffer.getvalue()).decode()

    plt.close()

    return plot_data


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        start_date = request.form['start_date']
        end_date = request.form['end_date']

        # Retrieve data from the database based on the selected date range
        data = get_data_from_database(start_date, end_date)

        # Generate the plot using the new data
        x = np.linspace(0, 10, len(data))
        y = np.sin(x)
        plot_data = generate_plot(x, y)

        return render_template('index.html', data=data, plot_data=plot_data)
    else:
        return render_template('index.html')


if __name__ == '__main__':
    app.run()
