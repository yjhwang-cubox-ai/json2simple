import argparse
import os
import json

def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument("--label_dir", type=str)
    parser.add_argument("--img_dir", type=str)
    parser.add_argument("--out_label_dir", type=str)
    return parser.parse_args()

def get_file_list(file_dir):
    file_lists = []
    if file_dir is None or not os.path.exists(file_dir):
        raise Exception("not found ant file in {}".format(file_dir))
    
    if os.path.isdir(file_dir):
        for single_file in os.listdir(file_dir):
            file_path = os.path.join(file_dir, single_file)
            file_lists.append(file_path)
    if len(file_lists) == 0:
        raise Exception("not found ant file in {}".format(file_dir))
    file_lists = sorted(file_lists)
    return file_lists

def main():
    args = parse()
    file_list = get_file_list(args.label_dir)
    # train_labels = []
    # val_labels = []
    total_labels = []
    
    for idx, file_path in enumerate(file_list):
        print("[{}]:{}".format(idx, file_path))
        f = open(file_path, 'rt', encoding='UTF8')
        data = json.load(f)
        filename = data["image"]["file_name"]
        word = data["text"]["word"]
        bbox_list = []
        for item in word:
            wordbox = item["wordbox"]
            text = item["value"]
            annotation = {
                "transcription": text,
                "points": [[wordbox[0],wordbox[1]],[wordbox[2],wordbox[1]],[wordbox[2],wordbox[3]],[wordbox[0],wordbox[3]]],
                "difficult": False
            }
            bbox_list.append(annotation)
        
        label = "{}\t{}\n".format(filename, json.dumps(bbox_list))
        total_labels.append(label)
        # if idx % 10 == 0:
        #     val_labels.append(label)
        # else:
        #     train_labels.append(label)
    
    total_label_path = os.path.join(args.out_label_dir, "train_label.txt")
    print("Write to {}".format(total_label_path))
    with open(total_label_path, 'w', encoding='utf-8') as f:
        for label in total_labels:
            f.write(label)
    
    # train_label_path = os.path.join(args.out_label_dir, "train_label.txt")
    # print("Write to {}".format(train_label_path))
    # with open(train_label_path, 'w', encoding='utf-8') as f:
    #     for label in train_labels:
    #         f.write(label)
    
    # val_label_path = os.path.join(args.out_label_dir, "val_label.txt")
    # print("Write to {}".format(val_label_path))
    # with open(val_label_path, 'w', encoding='utf-8') as f:
    #     for label in val_labels:
    #         f.write(label)

if __name__ == "__main__":
    main()