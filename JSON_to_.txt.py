import json
import os

class_mapping = {
    "person": 1,
    "bike": 2,
    "car": 3,
    "motorcycle": 4,
    "bus": 5,
    "train": 6,
    "truck": 7,
    "light": 8,
    "hydrant": 9,
    "sign": 10,
    "dog": 11,
    "skateboard": 12,
    "stroller": 13,
    "scooter": 14,
    "other vehicle": 15
}

image_width = 640  # image width
image_height = 512  # image height

def save_annotation_to_txt(annotation, txt_filename):
    with open(txt_filename, 'w') as txt_file:
        for obj in annotation.get('annotations', []):
            bounding_box = obj.get('boundingBox', {})
            labels = obj.get('labels', [])
            label_id = class_mapping.get(labels[0].lower(), -1) if labels and labels[0].lower() in class_mapping else -1
            if label_id != -1:
                x = (bounding_box['x'] + bounding_box['w'] / 2) / image_width
                y = (bounding_box['y'] + bounding_box['h'] / 2) / image_height
                width = bounding_box['w'] / image_width
                height = bounding_box['h'] / image_height
                txt_file.write(f'{label_id} {x} {y} {width} {height}\n')

def process_json(json_filename, image_folder, output_folder):
    with open(json_filename, 'r') as json_file:
        data = json.load(json_file)

    for image_filename in os.listdir(image_folder):
        if image_filename.endswith('.jpg') or image_filename.endswith('.png'):
            image_file_path = os.path.join(image_folder, image_filename)
            frame_id = os.path.splitext(image_filename)[0]
            for frame in data.get('frames', []):
                if frame.get('datasetFrameId') == frame_id:
                    txt_filename = os.path.join(output_folder, f"{frame_id}.txt")
                    save_annotation_to_txt(frame, txt_filename)
                    break
            else:
                print(f"No annotations found for image: {frame_id}")

if __name__ == "__main__":
    json_filename = "/home/user/Music/prasad/index.json"
    image_folder = "/home/user/Music/prasad/data"
    output_folder = "/home/user/Music/prasad/image"
    process_json(json_filename, image_folder, output_folder)
