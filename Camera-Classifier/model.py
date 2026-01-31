import cv2 as cv
import numpy as np
import os

class Model:
    def __init__(self):
        self.model = cv.ml.KNearest_create()
        self.samples = []
        self.labels = []
        self.is_trained = False
        # Map class_label (string) to class_id (int)
        self.label_map = {} 
        self.inv_label_map = {}
        self.next_id = 0

    def add_sample(self, frame, class_label):
        # Frame should be the ROI (130x130 or similar)
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        resize = cv.resize(gray, (130, 130))
        flatten = resize.reshape(16900).astype(np.float32)
        
        self.samples.append(flatten)
        
        if class_label not in self.label_map:
            self.label_map[class_label] = self.next_id
            self.inv_label_map[self.next_id] = class_label
            self.next_id += 1
            
        self.labels.append(self.label_map[class_label])

    def train_model(self):
        if not self.samples:
            print("No samples to train.")
            return

        samples_arr = np.array(self.samples, dtype=np.float32)
        labels_arr = np.array(self.labels, dtype=np.int32)
        
        self.model.train(samples_arr, cv.ml.ROW_SAMPLE, labels_arr)
        self.is_trained = True
        print("Model auto-trained via OpenCV KNN!")

    def predict(self, frame):
        if not self.is_trained:
            return None
        
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        resize = cv.resize(gray, (130, 130))
        flatten = resize.reshape(16900).astype(np.float32)
        sample = np.array([flatten], dtype=np.float32)
        
        # Dynamic K: Use 5 for stability, but don't exceed number of samples
        k_val = min(len(self.samples), 5)
        # Ensure k is odd to avoid ties if possible, though OpenCV handles it.
        # But if we have 2 samples, k=2 is fine. 
        # Ideally k should be at least 1.
        if k_val < 1: k_val = 1

        ret, results, neighbours, dist = self.model.findNearest(sample, k=k_val)
        
        predicted_id = int(results[0][0])
        label = self.inv_label_map.get(predicted_id, "Unknown")
        
        # Calculate Confidence
        if k_val > 0:
            # Flatten neighbours array which is (1, k)
            neigh_flat = neighbours.flatten().astype(int)
            # Count occurrences of the predicted ID
            count = np.sum(neigh_flat == predicted_id)
            confidence = float(count) / k_val
            
            # Distance check (Basic outlier removal)
            # dist contains squared distances. If average distance is very high, reduce confidence
            avg_dist = np.mean(dist)
            # Heuristic: If distance is massive, it's likely a bad match. 
            # But calculating a universal threshold is hard without normalization.
            # We'll stick to vote confidence for now.
        else:
            confidence = 0.0
            
        return label, confidence
