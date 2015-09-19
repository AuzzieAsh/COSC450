#include <opencv/cv.h>
#include <opencv/highgui.h>

int main () {

  cv::namedWindow("Display");
  cv::Mat img(cv::Size(640,480), CV_8UC3);
  img.setTo(cv::Scalar(0,255,0));
  cv::circle(img, cv::Point(320,240), 200, cv::Scalar(255,0,0), -1);
  cv::circle(img, cv::Point(320,240), 100, cv::Scalar(0,0,255), -1);

  cv::imshow("Display", img);
  cv::waitKey();

}
