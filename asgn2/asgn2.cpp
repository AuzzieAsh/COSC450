/*
 File: asgn2.cpp
 Author: Ashley Manson
 Starting point from /home/cshome/s/steven/Public/Segmentation/segmentation.cpp
 */

#include <opencv/cv.h>
#include <opencv/highgui.h>

#include <iostream>
#include <fstream>
#include <vector>
#include <random> // rngesus
#include <climits> // infinity

#define WRITE_OUT 1
//#define USER_WAIT 1

#define CLUSTER_MIN_CHANGE 0
#define LABEL_MIN_CHANGE 0

// I use these a lot
#define for_x for (int x = 0; x < image.size().width; x++)
#define for_y for (int y = 0; y < image.size().height; y++)
#define for_c for (int c = 0; c < k; c++)

unsigned issac_seed;

struct SegmentationResult {
    std::vector<cv::Vec3b> clusters; // cluster points
    cv::Mat labels; // cluster labels
};

double compute_distance(cv::Vec3b point, cv::Vec3b centre, int d_type) {
    switch (d_type) {
        case 0: // RGB
            return sqrt(pow(point[0] - centre[0], 2) + // r
                        pow(point[1] - centre[1], 2) + // g
                        pow(point[2] - centre[2], 2)); // b
        case 1: // HSV
            // Scale Hue
            point[0] = ((double)point[0]/180.0) * 256;
            centre[0] = ((double)centre[0]/180.0) * 256;
            return sqrt(pow(point[0] - centre[0], 2) + // h
                        pow(point[1] - centre[1], 2)); // s
        default:
            std::cout << "d_type incorrect, try agin\n";
            exit(1);
    }
}

/*
 k-Means algorithm - Does k-Means stuff
 */
SegmentationResult kMeans(const cv::Mat& image, int k, int c_type, int d_type, int e_type, int max_iterations) {

#ifdef WRITE_OUT
    std::ofstream cluster_file;
    cluster_file.open("cluster_output.txt", std::fstream::app);
#endif

    // Set up the SegmentationResult
    SegmentationResult result;
    result.labels = cv::Mat(image.size(), CV_32SC1);
    result.labels.setTo(-1);
    result.clusters.resize(0); // Ensure it's empty

    // Random Variables
    std::default_random_engine rngesus(issac_seed);
    std::uniform_int_distribution<int> get_rand_x (0, image.size().width-1);
    std::uniform_int_distribution<int> get_rand_y (0, image.size().height-1);
    std::uniform_int_distribution<int> get_rand_k (0, k-1);

    // Cluster Variables
    int rand_x, rand_y;
    std::vector<unsigned char> cluster_assign; // case 1
    std::vector<double> cluster_distances; // case 2

    // Add k cluster points to result.clusters
    switch (c_type) {

        case 0: // Random Selection
            for_c {
                rand_x = get_rand_x(rngesus);
                rand_y = get_rand_y(rngesus);
                result.clusters.push_back(image.at<cv::Vec3b>(rand_y, rand_x));
            }
            break;

        case 1: // Random Clustering
            // Assign each data element to one k cluster
            for (int l = 0; l < image.size().width*image.size().height; l++) {
                cluster_assign.push_back(get_rand_k(rngesus));
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
            }
            break;

        case 2: // k-Means++ (I think)

            // 1. Choose one centre uniformly at random from the data points
            rand_x = get_rand_x(rngesus);
            rand_y = get_rand_y(rngesus);
            result.clusters.push_back(image.at<cv::Vec3b>(rand_y, rand_x));

            // 4. Repeat steps 2 and 3 until all k centres are selected
            for (int c = 1; c < k; c++) {
                // 2. For each data point p compute D(p)
                // the distance between p and the nearest centre chosen
                cluster_distances.resize(0); // Empty It
                cv::Vec3b centre = result.clusters[c-1]; // Select Last Centre Found
                double count = 0;

                for_x {
                    for_y {
                        double distance = std::abs(compute_distance(image.at<cv::Vec3b>(y,x), centre, d_type));
                        cluster_distances.push_back(distance);
                        count += distance;
                    }
                }

                std::uniform_real_distribution<double> prob_distribution(0, count);

                // 3. Choose one new point at random, using weighted probability
                // which has weighted probability proportional to D(p)^2
                while (result.clusters.size() == c) {

                    rand_x = get_rand_x(rngesus);
                    rand_y = get_rand_y(rngesus);

                    double chance = pow(cluster_distances[rand_x*rand_y],2);
                    double prob = prob_distribution(rngesus);

                    std::cout << "Chance: " << chance << ", Prob: " << prob;
                    if (chance > prob) {
                        result.clusters.push_back(image.at<cv::Vec3b>(rand_y, rand_x));
                        std::cout << " | Sucessful k " << c;
                    }
                    std::cout << "\n";
                }
            }

            // 5. Continue with k-means clustering
            break;

        default:
            std::cout << "c_type incorrect, try again\n";
            exit(1);
    }

    for_c {
        std::cout << "Cluster " << c << ": Colour " << result.clusters[c] << "\n";
    }

    int iterations = 0;
    int label_difference;
    int cluster_difference;
    bool done = false;

    while (!done) {

        label_difference = 0;
        cluster_difference = 0;

        for_x {
            for_y {

                // Infinity
                double min_distance = std::numeric_limits<double>::max();
                unsigned char prev_c = result.labels.at<unsigned char>(y,x);

                for_c {
                    // Calculate the Distance
                    double distance = compute_distance(image.at<cv::Vec3b>(y,x), result.clusters[c], d_type);
                    if (distance < min_distance) {
                        result.labels.at<unsigned char>(y,x) = c;
                        min_distance = distance;
                    }
                }
                if (prev_c != result.labels.at<unsigned char>(y,x))
                    label_difference++;
            }
        }
        for_c {

            double r = 0, g = 0, b = 0;
            cv::Vec3b temp_cluster = result.clusters[c];
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
            r = std::abs(result.clusters[c][0] - temp_cluster[0]);
            g = std::abs(result.clusters[c][1] - temp_cluster[1]);
            b = std::abs(result.clusters[c][2] - temp_cluster[2]);
            cluster_difference += (r + g + b);
        }

        std::cout << "Iteration: " << iterations++ << "\n" \
        << "Cluster Difference: " << cluster_difference << "\n" \
        << "Label Difference: " << label_difference << "\n";

        switch (e_type) {
            case 0:
                if (iterations >= max_iterations)
                    done = true;
                break;
            case 1:
                if (cluster_difference <= CLUSTER_MIN_CHANGE)
                    done = true;
                break;
            case 2:
                if (label_difference <= LABEL_MIN_CHANGE)
                    done = true;
                break;
            default:
                std::cout << "e_type incorrect, try again\n";
                exit(1);
        }

    }

#ifdef WRITE_OUT
    cluster_file << iterations << std::endl;
#endif

    return result;
}

int main (int argc, char **argv) {

    // Check that there are enough command line paramters
    // cluster type [0-2], distance type [0-1], end type [0-2]
    if (argc != 8) {
        std::cout << "Usage: " << argv[0] << " <input image> <output image> <k> <cluster type> <distance type> <end type> <max iterations>\n";
        exit(1);
    }

    issac_seed = std::chrono::system_clock::now().time_since_epoch().count();
    int k = atoi(argv[3]);
    int c_type = atoi(argv[4]);
    int d_type = atoi(argv[5]);
    int e_type = atoi(argv[6]);
    int max_iterations = atoi(argv[7]);

    // Read the image and display it
    cv::Mat image = cv::imread(argv[1]);
    cv::imshow("Original Image", image);
#ifdef USER_WAIT
    cv::waitKey();
#endif


    if (d_type == 1) {
        cv::cvtColor(image, image, CV_BGR2HSV);
    }
    // Segment the image
    SegmentationResult result = kMeans(image, k, c_type, d_type, e_type, max_iterations);


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

    if (d_type == 1) {
        cv::cvtColor(image, image, CV_HSV2BGR);
    }

    // Save the result, diplay it, and then wait for a key press
    cv::imwrite(argv[2], image);
    cv::imshow("Segmented Image", image);
#ifdef USER_WAIT
    cv::waitKey();
#endif
    
    return 0;
}
