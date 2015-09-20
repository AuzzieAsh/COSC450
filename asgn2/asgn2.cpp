#include <opencv/cv.h>
#include <opencv/highgui.h>

#include <vector>
#include <random>
#include <climits>

/*
 Starting point from /home/cshome/s/steven/Public/Segmentation/segmentation.cpp
 */

struct SegmentationResult {
    std::vector<cv::Vec3b> centres; // centre/cluster points
    cv::Mat segmented; // segmented image result
    cv::Mat labels; // cluster labels
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
    result.labels = cv::Mat(image.size(), CV_32SC1);
    result.segmented.setTo(0);
    result.labels.setTo(0);
    result.centres.resize(0); // Ensure it's empty

    // Add k centre/cluster points to result.centres
    for (int c = 0; c < k; c++) {
        int rand_x = rand() % image.size().width;
        int rand_y = rand() % image.size().height;
        result.centres.push_back(image.at<cv::Vec3b>(rand_y, rand_x));
    }

    int iterations = 0;
    bool done = false;
    while (!done) {
        for (int x = 0; x < image.size().width; x++) {
            for (int y = 0; y < image.size().height; y++) {
                double min_distance = std::numeric_limits<double>::max();
                for (int c = 0; c < k; c++) {

                    double r = image.at<cv::Vec3b>(y,x)[0] - result.centres[c][0];
                    double g = image.at<cv::Vec3b>(y,x)[1] - result.centres[c][1];
                    double b = image.at<cv::Vec3b>(y,x)[2] - result.centres[c][2];

                    double distance = sqrt(pow(r,2) + pow(g,2) + pow(b,2));

                    if (distance < min_distance) {
                        result.labels.at<unsigned char>(y,x) = c;
                        min_distance = distance;
                    }
                }
            }
        }
        for (int c = 0; c < k; c++) {
            double r = 0, g = 0, b = 0;
            int count = 0;
            for (int x = 0; x < image.size().width; x++) {
                for (int y = 0; y < image.size().height; y++) {
                    if (result.labels.at<unsigned char>(y,x) == c) {
                        r += image.at<cv::Vec3b>(y,x)[0];
                        g += image.at<cv::Vec3b>(y,x)[1];
                        b += image.at<cv::Vec3b>(y,x)[2];
                        count++;
                    }
                }
            }
            result.centres[c] = cv::Vec3b(r/count, g/count, b/count);
        }
        std::cout << "iterations: " << iterations++ << "\n";
        if (iterations > 10)
            done = true;
    }

    return result;
}

int main (int argc, char **argv) {

    // Check that there are enough command line paramters
    // Arguments are input image, k, then output image.
    if (argc != 4) {
        std::cout << "Usage: " << argv[0] << " <input image> <k> <output image>" << std::endl;
        exit(1);
    }

    int k = atoi(argv[2]);
    // Read the image and display it
    cv::Mat image = cv::imread(argv[1]);
    cv::imshow("Original Image", image);
    cv::waitKey(); // Need to call waitKey to refresh display

    // Segment the image
    SegmentationResult sr = kMeans(image, k);

    // Loop over the image
    for (int c = 0; c < k; c++) {
        for (int x = 0; x < image.size().width; ++x) {
            for (int y = 0; y < image.size().height; ++y) {
                if (sr.labels.at<unsigned char>(y,x) == c) {
                    // Set each pixel value to the corresponding centre/cluster
                    image.at<cv::Vec3b>(y,x) = sr.centres[c];
                }
            }
        }
    }
    
    // Display the result, save it, and then wait for a key press
    cv::imwrite(argv[3], image);
    cv::imshow("Segmented Image", image);
    cv::waitKey();
    
    return 0;
}
