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

// I use these a lot
#define for_x for (int x = 0; x < image.size().width; x++)
#define for_y for (int y = 0; y < image.size().height; y++)
#define for_c for (int c = 0; c < k; c++)

struct SegmentationResult {
    std::vector<cv::Vec3b> clusters; // cluster points
    cv::Mat labels; // cluster labels
};

struct Point {
    int x;
    int y;
};

/*
 k-Means algorithm - Does k-Means stuff
 */
SegmentationResult kMeans(const cv::Mat& image, unsigned int k, unsigned int c_type) {


    // Set up the SegmentationResult
    SegmentationResult result;
    result.labels = cv::Mat(image.size(), CV_32SC1);
    result.labels.setTo(0);
    result.clusters.resize(0); // Ensure it's empty

    // Cluster Variables
    int rand_x, rand_y;
    std::vector<unsigned char> cluster_assign; // case 1
    std::vector<double> cluster_distance; // case 2
    std::vector<Point> cluster_centres; // case 2

    // Add k cluster points to result.centres
    switch (c_type) {

        case 0: // Random Selection
            for_c {
                rand_x = rand() % image.size().width;
                rand_y = rand() % image.size().height;
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
            for_c {
                double r = 0, g = 0, b = 0;
                int count = 0;

                for_x {
                    for_y {

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

        case 2: // k-Means++ (I think)

            // 1. Choose one centre uniformly at random from the data points
            rand_x = rand() % image.size().width;
            rand_y = rand() % image.size().height;
            result.clusters.push_back(image.at<cv::Vec3b>(rand_y, rand_x));
            Point cent; cent.x = rand_x; cent.y = rand_y;
            cluster_centres.push_back(cent);

            // 4. Repeat steps 2 and 3 until all k centres are selected
            for (int c = 1; c < k; c++) {
                // 2. For each data point p compute D(p)
                // the distance between p and the nearest centre chosen
                cluster_distance.resize(0);
                cent = cluster_centres[c-1];
                double count = 0;

                for_x {
                    for_y {
                        int x_res = cent.x - x;
                        int y_res = cent.y - y;
                        double distance = std::abs(x_res*x_res + y_res*y);
                        cluster_distance.push_back(distance);
                        count += distance;
                    }
                }

                // 3. Choose one new point at random, using weighted probability
                // which has weighted probability proportional to D(p)^2
                while (cluster_centres.size() == c) {
                    rand_x = rand() % image.size().width;
                    rand_y = rand() % image.size().height;
                    double prob = pow(cluster_distance[rand_x*rand_y],2)/count;
                    double chance = rand()/(RAND_MAX+1.0);
                    std::cout << "Prob: " << prob << ", Chance: " << chance << "\n";
                    if (prob > chance) {
                        cent.x = rand_x;
                        cent.y = rand_y;
                        cluster_centres.push_back(cent);
                        result.clusters.push_back(image.at<cv::Vec3b>(rand_y, rand_x));
                    }
                }
            }

            for_c {
                std::cout << "Cluster " << c << " RGB: " << result.clusters[c] << "\n";
            }
            
            // 5. Continue
            break;

        default:
            std::cout << "c_type too dank\n";
            exit(1);
    }

    int iterations = 0;
    bool done = false;

    while (!done) {

        for_x {
            for_y {

                double min_distance = std::numeric_limits<double>::max();

                for_c {

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

        for_c {

            double r = 0, g = 0, b = 0;
            int count = 0;

            for_x {
                for_y {

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
    for_c {
        for_x {
            for_y {
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
