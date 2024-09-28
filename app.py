import json
from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
import os
import numpy as np
from PIL import Image
from io import BytesIO
# from sklearn.cluster import KMeans
# from image_compression_impl import load_image, image_compression
from kmeans_impl import KMeans
import plotly.graph_objects as go
import plotly.io as pio
import sklearn.datasets as datasets

app = Flask(__name__)

# Path to save uploaded files
# UPLOAD_FOLDER = 'uploads'
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# # Create upload folder if it doesn't exist
# if not os.path.exists(UPLOAD_FOLDER):
#     os.makedirs(UPLOAD_FOLDER)

# centers = [[0, 0], [2, 2], [-3, 2], [2, -4]]
# X, y = datasets.make_blobs(n_samples=300, centers=centers, cluster_std=1, random_state=0)
data = np.random.uniform(-10, 10, (300, 2))

init_method = 'random'

manual_points = []

clusters = 4


kmeans = KMeans(data, clusters, init_method, manual_points)
kmeans.lloyds()
figures = kmeans.snaps
figure_index = 0

@app.route('/')
def index():
    global figures
    graph_html = pio.to_html(figures[figure_index], full_html=False)
    return render_template('index.html', graph_html=graph_html)

@app.route('/clusters/<value>')
def clusters(value):
	global figures
	global clusters

	global kmeans
	global data
	global init_method
	global manual_points

	print(value)

	clusters = int(value)


	kmeans = KMeans(data, clusters, init_method, manual_points)
	kmeans.lloyds()
	figures = kmeans.snaps
	return  jsonify({"status": "success", "received value": value})

@app.route('/step_through/<value>')
def step_through_kmeans(value):
	global figures
	index = min(int(value), len(figures) - 1)
	graph_html = pio.to_html(figures[index], full_html=False)
	return jsonify(graph_html=graph_html)

@app.route('/methods/<value>')
def choose_init_method(value):
	global figures
	global kmeans
	global data
	global init_method
	global manual_points

	init_method = value

	print(manual_points)

	kmeans = KMeans(data, clusters, init_method, manual_points)
	kmeans.lloyds()
	figures = kmeans.snaps
	graph_html = pio.to_html(figures[0], full_html=False)
	return jsonify(graph_html=graph_html)

@app.route('/init_points', methods=['POST'])
def receive_data():
	global figures
	global kmeans
	global data
	global init_method
	global manual_points
	point_data = request.json
	points_list = point_data.get('points', [])

	if (len(points_list) != 0):
		manual_points = points_list

	return jsonify({"status": "success", "received_points": points_list})

    # return jsonify({"status": "success", "received_points": points})


@app.route('/run_to/')
def run_to_converge():
	global figures
	index = len(figures) - 1
	graph_html = pio.to_html(figures[index], full_html=False)
	return jsonify(graph_html=graph_html)

@app.route('/reset/')
def reset_algorithm():
	global figures
	global manual_points
	manual_points = []
	index = 0
	graph_html = pio.to_html(figures[index], full_html=False)
	return jsonify(graph_html=graph_html)

@app.route('/gen_new/')
def gen_new():
	global figures
	global kmeans
	global init_method
	global data
	global manual_points
	data = np.random.uniform(-10, 10, (300, 2))

	kmeans = KMeans(data, clusters, init_method, manual_points)
	kmeans.lloyds()
	figures = kmeans.snaps

	graph_html = pio.to_html(figures[figure_index], full_html=False)
	return jsonify(graph_html=graph_html)



if __name__ == '__main__':
    app.run(port=3000, debug=True)