#include <opencv/cv.h>
#include <opencv/highgui.h>

#include <vector>

/*
 * Segmentation result storage.
 * 
 * The result is a list of cluster centers (means) and a mapping
 * from pixels to clusters. This mapping is stored as an OpenCV
 * image (segmented). The (x,y) pixel of this image is the index 
 * into means, so the pixel values should be integer values. 
 */
struct SegmentationResult {
  std::vector<cv::Vec3b> means;
  cv::Mat segmented;
};


/*
 * k-Means algorithm
 *
 * Given an image and a value for k, apply k-means segmentation.
 * 
 * The result's mean vector should have k values, and each value in the
 * segmented image is an index into this vector (an integer from 0 to k-1). 
 *
 * The implementation provided is *not* k-means. Rather, it takes the sum
 * of the red, green, and blue values. This gives a value in [0, 3*255],
 * and the image is segmented by dividing that range into k slices.
 */
SegmentationResult kMeans(const cv::Mat& image, unsigned int k) {

  // Set up the SegmentationResult
  SegmentationResult result;
  // Since integers are 4-bytes on most platforms, 32S will store an int
  result.segmented = cv::Mat(image.size(), CV_32SC1);
  result.segmented.setTo(0);
  // This will have k segments
  result.means.resize(k);

  // This is not k-means, just splitting on sum of R, G, and B.
  // So the 'means' are k grey values spread across the range [0,255]
  for (int s = 0; s < k; ++s) {
    result.means[s][0] = s*256/k;
    result.means[s][1] = s*256/k;
    result.means[s][2] = s*256/k;
  }

  // The step between segments, which is (3/255) split k ways.
  int step = (3*255/k);

  // Loop over each pixel in the image
  for (int x = 0; x < image.size().width; ++x) {
    for (int y = 0; y < image.size().height; ++y) {
      // Compute the sum of the colour channels
      cv::Vec3b colour = image.at<cv::Vec3b>(y,x);
      int sum = colour[0] + colour[1] + colour[2];
      // Pixel segment is the number of steps in the sum
      result.segmented.at<unsigned char>(y,x) = sum/step;
    }
  }

  return result;
}

int main (int argc, char *argv[]) {

  // Check that there are enough command line paramters
  // Arguments are input image, k, then output image.
  if (argc != 4) {
    std::cout << "Usage: segmentation <input image> <k> <output image>" << std::endl;
    exit(1);
  }

  // Read the image and display it
  cv::Mat image = cv::imread(argv[1]);
  cv::namedWindow("Display");
  cv::imshow("Display", image);
  cv::waitKey(); // Need to call waitKey to refresh display

  // Segment the image
  SegmentationResult sr = kMeans(image, atoi(argv[2]));

  // Loop over the image
  for (int x = 0; x < image.size().width; ++x) {
    for (int y = 0; y < image.size().height; ++y) {
      // Set each pixel value to the corresponding mean
      int index = sr.segmented.at<unsigned char>(y,x);
      image.at<cv::Vec3b>(y,x) = sr.means[index];
    }
  }
  
  // Display the result, save it, and then wait for a key press
  cv::imshow("Display", image);
  cv::imwrite(argv[3], image);
  cv::waitKey();
}
