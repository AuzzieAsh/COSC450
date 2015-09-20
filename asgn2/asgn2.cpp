/*
 File: asgn2.cpp
 Author: Ashley Manson
 Starting point from /home/cshome/s/steven/Public/Segmentation/segmentation.cpp
 */

#include <opencv/cv.h>
#include <opencv/highgui.h>

#include <vector>
#include <random> // rngesus
#include <climits> // infinity

struct SegmentationResult {
    std::vector<cv::Vec3b> clusters; // cluster points
    cv::Mat labels; // cluster labels
};

/*
 k-Means algorithm - Does k-Means stuff
 */
SegmentationResult kMeans(const cv::Mat& image, unsigned int k, unsigned int c_type) {

    std::vector<unsigned char> cluster_assign;

    // Set up the SegmentationResult
    SegmentationResult result;
    result.labels = cv::Mat(image.size(), CV_32SC1);
    result.labels.setTo(0);
    result.clusters.resize(0); // Ensure it's empty

    // Add k cluster points to result.centres
    switch (c_type) {

        case 0: // Random Selection
            for (int c = 0; c < k; c++) {
                int rand_x = rand() % image.size().width;
                int rand_y = rand() % image.size().height;
                result.clusters.push_back(image.at<cv::Vec3b>(rand_y, rand_x));

                std::cout << "Cluster " << c << ": [" << rand_x << "," << rand_y << "]";
                std::cout << " RGB: " << result.clusters[c] << "\n";
            }
            break;

        case 1: // Random Clustering (I think)
            // Assign each data element to one k cluster
            for (int l = 0; l < image.size().width*image.size().height; l++) {
                cluster_assign.push_back(rand() % k);
            }

            // Go through and get the average for each k cluster
            for (int c = 0; c < k; c++) {

                double r = 0, g = 0, b = 0;
                int count = 0;

                for (int x = 0; x < image.size().width; x++) {
                    for (int y = 0; y < image.size().height; y++) {

                        if (c == cluster_assign[y*x]) {
                            r += image.at<cv::Vec3b>(y,x)[0];
                            g += image.at<cv::Vec3b>(y,x)[1];
                            b += image.at<cv::Vec3b>(y,x)[2];
                            count++;
                        }
                    }
                }

                cv::Vec3b average(r/count, g/count, b/count);
                result.clusters.push_back(average);

                std::cout << "Cluster " << c << " RGB: " << result.clusters[c] << "\n";
            }
            break;
/*
        case 2: // k-Means++
            int rand_x = rand() % image.size().width;
            int rand_y = rand() % image.size().height;
            result.clusters.push_back(image.at<cv::Vec3b>(rand_y, rand_x));

            for (int c = 1; c < k; c++) {

            }
            break;
*/
        default:
            std::cout << "c_type too dank\n";
            exit(1);
    }

    int iterations = 0;
    bool done = false;

    while (!done) {

        for (int x = 0; x < image.size().width; x++) {
            for (int y = 0; y < image.size().height; y++) {

                double min_distance = std::numeric_limits<double>::max();

                for (int c = 0; c < k; c++) {

                    double r = image.at<cv::Vec3b>(y,x)[0] - result.clusters[c][0];
                    double g = image.at<cv::Vec3b>(y,x)[1] - result.clusters[c][1];
                    double b = image.at<cv::Vec3b>(y,x)[2] - result.clusters[c][2];

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

            result.clusters[c] = cv::Vec3b(r/count, g/count, b/count);
        }

        std::cout << "Iterations: " << iterations++ << "\n";
        if (iterations >= 10)
            done = true;
    }

    return result;
}

int main (int argc, char **argv) {

    // Check that there are enough command line paramters
    // Arguments are input image, k, then output image.
    if (argc != 5) {
        std::cout << "Usage: " << argv[0] << " <input image> <k> <output image> <cluster type>\n";
        exit(1);
    }

    srand(time(NULL)); // seed for different pseudo random numbers
    int k = atoi(argv[2]);
    int c_type = atoi(argv[4]);

    // Read the image and display it
    cv::Mat image = cv::imread(argv[1]);
    cv::imshow("Original Image", image);
    cv::waitKey(); // Need to call waitKey to refresh display

    // Segment the image
    SegmentationResult result = kMeans(image, k, c_type);

    // Loop over the image
    for (int c = 0; c < k; c++) {
        for (int x = 0; x < image.size().width; x++) {
            for (int y = 0; y < image.size().height; y++) {
                if (result.labels.at<unsigned char>(y,x) == c) {
                    // Set each pixel value to the corresponding centre/cluster
                    image.at<cv::Vec3b>(y,x) = result.clusters[c];
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
