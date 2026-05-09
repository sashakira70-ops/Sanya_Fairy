#ifndef VIDEOPROCESSOR_HPP
#define VIDEOPROCESSOR_HPP

#include <opencv2/opencv.hpp>
#include <string>

class VideoProcessor {
public:
    VideoProcessor(int cameraId = 0);
    ~VideoProcessor();
    void run();

private:
    cv::VideoCapture cap;
    std::string windowName;
    int mode;
    int brightness;
    
    void process(cv::Mat& frame);
    static void onMouse(int event, int x, int y, int flags, void* userdata);
};

#endif
