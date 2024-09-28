import plotly.graph_objects as go
import pandas as pd
import numpy as np
# from sklearn.cluster import KMeans
# from PIL import Image as im
import sklearn.datasets as datasets
from sklearn.metrics import pairwise_distances

centers = [[0, 0], [2, 2], [-3, 2], [2, -4]]
X, y = datasets.make_blobs(n_samples=300, centers=centers, cluster_std=1, random_state=0)

x_val = X[:, 0]
y_val = X[:, 1]

class KMeans():
    def __init__(self, data, k, method, manual_points):
        self.data = data
        self.k = k
        self.assignment = [-1 for _ in range(len(data))]
        self.manual_points = manual_points
        

        x_val = data[:, 0]
        y_val = data[:, 1]

        fig = go.Figure(data=go.Scatter(x=x_val, y=y_val, mode='markers', 
            marker = dict(
                color = self.assignment, 
                colorscale = 'Viridis', 
                line = dict(width = 1)
            )
        ))

        fig.update_layout(clickmode='event+select')


        self.snaps = [fig]
        self.method = method

    def snap(self, centers):

        x_centers = centers[:,0]
        y_centers = centers[:,1]
        x_val = self.data[:, 0]
        y_val = self.data[:, 1]
        fig = go.Figure(data=go.Scatter(x=x_val, y=y_val, mode='markers', 
            marker = dict(
                color = self.assignment, 
                colorscale = 'Viridis', 
                line = dict(width = 1)
            )
        ))

        fig.add_trace(go.Scatter(x = x_centers, y = y_centers, mode = 'markers', 
                        marker = dict(
                            color = 'rgba(220, 0, 0, 0.8)', 
                            size = 10
                        )))
        fig.update_layout(clickmode='event+select')
        self.snaps.append(fig)
        # print("added trace")

    def isunassigned(self, i):
        return self.assignment[i] == -1

    def initialize(self):
        method = self.method
        print(method)
        if(method == 'random'):
            print("INIT WITH RANDOM")
            return self.data[np.random.choice(len(self.data) - 1, size=self.k, replace=False)]
        elif(method == 'ff'):
            print("INIT WITH FF")
            n_samples = self.data.shape[0]
            centroids = [self.data[np.random.choice(n_samples)]]
            for _ in range(1, self.k):
                # Compute distances from the current centroids to all points
                distances = pairwise_distances(self.data, centroids).min(axis=1)
                
                # Select the point farthest from the current centroids
                next_centroid_idx = np.argmax(distances)
                centroids.append(self.data[next_centroid_idx])
            return centroids

        elif(method == 'kmeans'):
            print("INIT WITH KMEANS")
            n_samples, n_features = self.data.shape
            centroids = [self.data[np.random.choice(range(self.data.shape[0]))]]
            for _ in range(1, self.k):
                # Compute squared distances between each point and the nearest centroid
                distances = np.array([min(np.sum((x - c) ** 2) for c in centroids) for x in self.data])
                
                # Compute probabilities proportional to the squared distances
                probabilities = distances / distances.sum()
                
                # Select the next centroid based on the computed probabilities
                next_centroid_idx = np.random.choice(range(n_samples), p=probabilities)
                centroids.append(self.data[next_centroid_idx])
            return centroids
        else:
            # print([list(self.data[x]) for x in self.manual_points])
            return self.data[self.manual_points]


    
    def make_clusters(self, centers):
        for i in range(len(self.assignment)):
            for j in range(self.k):
                if self.isunassigned(i):
                    self.assignment[i] = j
                    dist = self.dist(centers[j], self.data[i])
                else:
                    new_dist = self.dist(centers[j], self.data[i])
                    if new_dist < dist:
                        self.assignment[i] = j
                        dist = new_dist
                        
    def compute_centers(self):
        centers = []
        for i in range(self.k):
            cluster = []
            for j in range(len(self.assignment)):
                if self.assignment[j] == i:
                    cluster.append(self.data[j])
            centers.append(np.mean(np.array(cluster), axis=0))

        return np.array(centers)
    
    def unassign(self):
        self.assignment = [-1 for _ in range(len(self.data))]

    def are_diff(self, centers, new_centers):
        for i in range(self.k):
            if self.dist(centers[i], new_centers[i]) != 0:
                return True
        return False

    def dist(self, x, y):
        # Euclidean distance
        return sum((x - y)**2) ** (1/2)

    def lloyds(self):
        centers = self.initialize()
        self.snap(centers)
        self.make_clusters(centers)
        new_centers = self.compute_centers()
        
        self.snap(new_centers)
        while self.are_diff(centers, new_centers):
            self.unassign()
            centers = new_centers
            self.make_clusters(centers)
            new_centers = self.compute_centers()
            self.snap(new_centers)
        return


# kmeans = KMeans(X, len(centers), 'Random')
# kmeans.lloyds()

# print("lloyds finished")