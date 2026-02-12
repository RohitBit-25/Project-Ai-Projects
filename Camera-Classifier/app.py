import tkinter as tk
from tkinter import simpledialog, messagebox
import cv2 as cv
import os
import PIL.Image, PIL.ImageTk
import camera
import model
import time

import collections

class App:
    def __init__(self, window=None, window_title="Camera Classifier"):
        if window is None:
            self.window = tk.Tk()
        else:
            self.window = window
        self.window.title(window_title)
        self.window.geometry("1400x800") # Larger default size

        # Dictionary to store {ClassName: next_index}
        self.counters = {}
        
        # Initialize Model
        self.model = model.Model()
        
        self.auto_predict = False
        
        self.video_source = 0
        self.vid = camera.Camera()
        
        # Main Layout: Two Columns
        self.window.grid_columnconfigure(0, weight=1) # Video Area
        self.window.grid_columnconfigure(1, weight=0, minsize=400) # Sidebar
        self.window.grid_rowconfigure(0, weight=1)

        # 1. Video Area
        self.video_frame = tk.Frame(self.window, bg="black")
        self.video_frame.grid(row=0, column=0, sticky="nsew")
        
        self.canvas = tk.Canvas(self.video_frame, width=self.vid.width, height=self.vid.height, bg="black", highlightthickness=0)
        self.canvas.pack(expand=True)

        # 2. Sidebar ("Form Type" Controls)
        self.sidebar = tk.Frame(self.window, bg="#f0f0f0", padx=20, pady=20)
        self.sidebar.grid(row=0, column=1, sticky="nsew")
        
        # Title
        tk.Label(self.sidebar, text="Control Panel", font=("Arial", 24, "bold"), bg="#f0f0f0").pack(pady=(0, 20))
        
        # Tip
        tk.Label(self.sidebar, text="💡 Tip: Train a 'Nothing' class\nfor the empty background!", font=("Arial", 10, "italic"), fg="gray", bg="#f0f0f0").pack(pady=(0, 10))

        # Section 1: Data Collection
        self.frame_data = tk.LabelFrame(self.sidebar, text="1. Gather Data", font=("Arial", 14, "bold"), bg="#f0f0f0", padx=10, pady=10)
        self.frame_data.pack(fill=tk.X, pady=10)
        
        self.btn_add_class = tk.Button(self.frame_data, text="Add New Class", font=("Arial", 12), bg="lightblue", command=self.add_class)
        self.btn_add_class.pack(fill=tk.X, pady=5)
        
        self.classes_frame = tk.Frame(self.frame_data, bg="#f0f0f0")
        self.classes_frame.pack(fill=tk.X)

        # Section 2: Training
        self.frame_train = tk.LabelFrame(self.sidebar, text="2. Train", font=("Arial", 14, "bold"), bg="#f0f0f0", padx=10, pady=10)
        self.frame_train.pack(fill=tk.X, pady=10)

        self.btn_train = tk.Button(self.frame_train, text="Train Model", font=("Arial", 12), bg="lightgray", command=self.train_wrapper)
        self.btn_train.pack(fill=tk.X, pady=5)
        
        self.lbl_train_status = tk.Label(self.frame_train, text="Status: Not Trained", font=("Arial", 10), fg="red", bg="#f0f0f0")
        self.lbl_train_status.pack()

        # Section 3: Prediction
        self.frame_predict = tk.LabelFrame(self.sidebar, text="3. Recognition", font=("Arial", 14, "bold"), bg="#f0f0f0", padx=10, pady=10)
        self.frame_predict.pack(fill=tk.X, pady=10)
        
        self.btn_predict = tk.Button(self.frame_predict, text="Toggle Auto-Predict", font=("Arial", 12), bg="lightgray", command=self.auto_predict_toggle)
        self.btn_predict.pack(fill=tk.X, pady=5)
        
        self.lbl_result = tk.Label(self.frame_predict, text="...", font=("Arial", 24, "bold"), fg="blue", bg="#f0f0f0")
        self.lbl_result.pack(pady=10)
        
        self.lbl_conf = tk.Label(self.frame_predict, text="Confidence: -", font=("Arial", 12), bg="#f0f0f0")
        self.lbl_conf.pack()

        # Reset
        self.btn_reset = tk.Button(self.sidebar, text="Reset All Data", font=("Arial", 10), fg="red", command=self.reset)
        self.btn_reset.pack(side=tk.BOTTOM, fill=tk.X, pady=20)
        
        self.delay = 15
        self.frame_count = 0 
        
        # Stability: Keep last 7 predictions
        self.history = collections.deque(maxlen=7)
        
        # Ensure clean state
        self.reset() 
        self.update()
        
        self.window.mainloop()


    
    def reset(self):
        for classname in self.counters:
            self.counters[classname] = 1
        self.model = model.Model()
        
        # Clear UI
        self.lbl_train_status.config(text="Status: Not Trained", fg="red")
        self.lbl_result.config(text="...", fg="blue")
        self.lbl_conf.config(text="Confidence: -")
        
        for widget in self.classes_frame.winfo_children():
            widget.destroy()
        self.counters = {}
        self.history.clear()
            
        print("Session reset.")
    
    def update(self):
        # Capture
        ret, frame = self.vid.get_frame()
        self.frame_count += 1
        
        if ret:
            # Draw Viewfinder (Green Box)
            height, width, _ = frame.shape
            x1 = int(width/2 - 150)
            y1 = int(height/2 - 150)
            x2 = int(width/2 + 150)
            y2 = int(height/2 + 150)
            
            # Extract ROI for prediction
            roi = frame[y1:y2, x1:x2]
            # Convert ROI to BGR for model because camera frame is RGB
            roi_bgr = cv.cvtColor(roi, cv.COLOR_RGB2BGR)

            # Auto Predict - Faster update
            if self.auto_predict and self.frame_count % 2 == 0:
                try:
                    prediction, confidence = self.model.predict(roi_bgr)
                    
                    # Smart Filter: Ignore "Nothing" class and low confidence
                    # This fulfills "classify only when it comes under green screen otherwise ignore"
                    if prediction in ["Nothing", "nothing", "Background", "background", "Empty", "empty"]:
                        prediction = None
                    
                    if confidence < 0.5: # Require majority vote
                        prediction = None

                    if prediction:
                        self.history.append(prediction)
                        # Relaxed Stability: Show if 3 out of last 5 match
                        if len(self.history) == 5 and self.history.count(prediction) >= 3:
                            # Sidebar Update
                            self.lbl_result.config(text=f"{prediction}", fg="green")
                            self.lbl_conf.config(text=f"Confidence: {confidence*100:.0f}%")
                            
                            # Video Overlay: High Visibility with Background
                            label_text = f"{prediction} ({confidence*100:.0f}%)"
                            font = cv.FONT_HERSHEY_SIMPLEX
                            font_scale = 1.2
                            thickness = 3
                            
                            # Get text size
                            (text_width, text_height), baseline = cv.getTextSize(label_text, font, font_scale, thickness)
                            
                            # Background Rectangle
                            cv.rectangle(frame, (x1, y1 - 40 - text_height), (x1 + text_width, y1 - 40 + baseline), (0, 0, 0), cv.FILLED)
                            
                            # Text
                            cv.putText(frame, label_text, (x1, y1 - 40), font, font_scale, (0, 255, 0), thickness)
                        else:
                            # Unstable, don't show old result
                            self.lbl_result.config(text="...", fg="gray")
                            self.lbl_conf.config(text="Scanning...")
                    else:
                        # Explicitly ignored (Background or Low Conf)
                        self.history.clear() # Reset history if we lose the object
                        self.lbl_result.config(text="...", fg="gray")
                        self.lbl_conf.config(text="Waiting for Object...")
                        
                except Exception:
                    self.lbl_train_status.config(text="Status: Model Not Trained!", fg="red")
            
            # Draw rectangle on display frame (RGB)
            cv.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            
            # Display
            self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
            
        self.window.after(self.delay, self.update)
    def train_wrapper(self):
        # Explicit Training Phase
        if not self.model.samples:
            messagebox.showwarning("No Data", "Please gather samples first! Add a class and click its button.")
            return
            
        try:
            self.model.train_model()
            self.lbl_train_status.config(text="Status: Model Trained! (Ready)", fg="green")
            messagebox.showinfo("Success", "Model Trained! Ready to Predict.")
        except Exception as e:
             messagebox.showerror("Error", f"Training Failed: {e}")

    def add_class(self):
        classname = simpledialog.askstring("Class Name", "Enter the name of the new class:", parent=self.window)
        if classname and classname not in self.counters:
            self.counters[classname] = 1
            if not os.path.exists(classname):
                os.mkdir(classname)
            
            # Button in the sidebar list
            btn = tk.Button(self.classes_frame, text=f"Collect: {classname} (0)", width=30, command=lambda c=classname: self.save_for_class(c))
            btn.pack(pady=2)
            
            # Store reference to update text later if needed
            # For simplicity, we can verify count updates in save_for_class by rebuilding or lookup.
            # But let's just make sure it passes the classname correctly.

    def save_for_class(self, class_label):
        ret, frame = self.vid.get_frame()
        if not ret:
            return

        if not os.path.exists(class_label):
            os.mkdir(class_label)
            
        file_path = f"{class_label}/frame{self.counters[class_label]}.jpg"
        self.counters[class_label] += 1
        
        # Extract ROI (Region of Interest)
        height, width, _ = frame.shape
        # Center crop 300x300
        x1 = int(width/2 - 150)
        y1 = int(height/2 - 150)
        x2 = int(width/2 + 150)
        y2 = int(height/2 + 150)
        
        roi = frame[y1:y2, x1:x2]
            
        # Save to disk (for persistence) as BGR
        save_img = cv.cvtColor(roi, cv.COLOR_RGB2BGR)
        cv.imwrite(file_path, save_img)
        
        # Gather Samples (Do NOT auto-train)
        self.model.add_sample(save_img, class_label)
        
        # Visual Feedback: Update count on button
        # Brute-force find the button (simple for this scale)
        for widget in self.classes_frame.winfo_children():
            if widget['text'].startswith(f"Collect: {class_label}"):
                count = self.counters[class_label] - 1
                widget.config(text=f"Collect: {class_label} ({count})")
        
    def auto_predict_toggle(self):
        self.auto_predict = not self.auto_predict
        if self.auto_predict:
            self.btn_predict.config(bg="lightgreen", text="Stop Auto-Predict")
        else:
            self.btn_predict.config(bg="lightgray", text="Start Auto-Predict")
        
    def reset(self):
        for classname in self.counters:
            self.counters[classname] = 1
        self.model = model.Model()
        
        # Clear UI
        self.lbl_train_status.config(text="Status: Not Trained", fg="red")
        self.lbl_result.config(text="...", fg="blue")
        self.lbl_conf.config(text="Confidence: -")
        
        for widget in self.classes_frame.winfo_children():
            widget.destroy()
        self.counters = {}
            
        print("Session reset.")

    def update(self):
        # Capture
        ret, frame = self.vid.get_frame()
        self.frame_count += 1
        
        if ret:
            # Draw Viewfinder (Green Box)
            height, width, _ = frame.shape
            x1 = int(width/2 - 150)
            y1 = int(height/2 - 150)
            x2 = int(width/2 + 150)
            y2 = int(height/2 + 150)
            
            # Extract ROI for prediction
            roi = frame[y1:y2, x1:x2]
            # Convert ROI to BGR for model because camera frame is RGB
            # (Wait, app logic: Camera gives RGB. Model.add_sample converts BGR->GRAY.
            # So if we pass RGB to predict, we need to convert RGB->GRAY.
            # Model.predict uses BGR2GRAY. So we must pass BGR to predict)
            roi_bgr = cv.cvtColor(roi, cv.COLOR_RGB2BGR)

            # Auto Predict
            if self.auto_predict and self.frame_count % 5 == 0:
                try:
                    prediction, confidence = self.model.predict(roi_bgr)
                    
                    if prediction:
                        self.lbl_result.config(text=f"{prediction}", fg="green")
                        self.lbl_conf.config(text=f"Confidence: {confidence*100:.1f}%")
                    else:
                        self.lbl_result.config(text="...", fg="gray")
                        self.lbl_conf.config(text="Scanning...")
                except Exception:
                    self.lbl_train_status.config(text="Status: Model Not Trained!", fg="red")
            
            # Draw rectangle on display frame (RGB)
            cv.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            
            # Display
            self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
            
        self.window.after(self.delay, self.update)
 
if __name__ == '__main__':
    App()