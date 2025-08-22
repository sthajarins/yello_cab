from flask import Flask, render_template, jsonify
import pandas as pd
import plotly.express as px
import json

app = Flask(__name__)

# Load CSV
df = pd.read_csv("data/final_yello.csv")
df['pickup_datetime'] = pd.to_datetime(df['pickup_datetime'])
df['date'] = pd.to_datetime(df['date'])

def calculate_metrics():
    total_trips = len(df)
    total_revenue = df['total_amount'].sum()
    avg_fare = df['total_amount'].mean()
    revenue_per_trip = total_revenue / total_trips
    return {
        "total_trips": int(total_trips),
        "total_revenue": round(float(total_revenue), 2),
        "avg_fare": round(float(avg_fare), 2),
        "revenue_per_trip": round(float(revenue_per_trip), 2)
    }

@app.route("/")
def index():
    metrics = calculate_metrics()
    return render_template("index.html", metrics=metrics)

@app.route("/api/charts")
def charts():
    # Bar Chart: Trips by Weekday
    trips_weekday = df.groupby('weekday').size().reset_index(name='trips')
    fig_bar = px.bar(trips_weekday, x='weekday', y='trips', title="Trips by Weekday")

    # Pie Chart: Payment Type Distribution
    payment_counts = df['payment_type'].value_counts().reset_index()
    payment_counts.columns = ['payment_type', 'count']
    fig_pie = px.pie(payment_counts, names='payment_type', values='count', title="Payment Type Distribution")

    # Line Chart: Revenue by Hour
    revenue_hour = df.groupby('hour')['total_amount'].sum().reset_index()
    fig_line = px.line(revenue_hour, x='hour', y='total_amount', title="Revenue by Hour")

    return jsonify({
        "bar": json.loads(fig_bar.to_json()),
        "pie": json.loads(fig_pie.to_json()),
        "line": json.loads(fig_line.to_json())
    })

@app.route("/api/data")
def table_data():
    return df.head(100).to_json(orient="records")

if __name__ == "__main__":
    app.run(debug=True)