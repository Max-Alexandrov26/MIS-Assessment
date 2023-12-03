from ultralytics import YOLO

#Choose the best model
model = YOLO('best.pt')
def get_predictions(source_directory):
    #Infer the model to get predictions
    model.predict(source=source_directory, hide_labels=False, line_thickness=6, save=True, save_txt=True,project = 'YOLO_predictions',name = 'Latest_run')
