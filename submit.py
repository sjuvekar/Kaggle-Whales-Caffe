import pandas as pd
import caffe

if __name__ == "__main__":
  classifier = caffe.Classifier("train/predict.prototxt", "classifier_iter_45600.caffemodel", image_dims=[384, 384], input_scale=0.00392156862745, channel_swap=[2, 1, 0])
  sample_df = pd.read_csv("data/sample_submission.csv")
  final_df = pd.DataFrame(columns=sample_df.columns, index=sample_df.index)
  final_df.Image = sample_df.Image
  batch_size = 8
  start_index = 0
  sample_len = len(sample_df)
  while start_index < sample_len:
    end_index = min(start_index + batch_size, sample_len)
    print "predicting ", start_index, ":", end_index
    img = [caffe.io.load_image("data/test/{}".format(sample_df.Image[i])) for i in range(start_index, end_index)]
    preds = classifier.predict(img, oversample=False)
    final_df.ix[range(start_index, end_index), 1:] = preds
    start_index = end_index
  output_file = "caffe.csv"
  print "Writing output to", output_file
  final_df.to_csv(output_file, index=False)
