#pragma once
#include <opencv2/opencv.hpp>
#include <opencv2/dnn.hpp>
#include <thread>
#include <mutex>
#include <atomic>
#include <vector>

class FaceDetector {
public:
    FaceDetector(const std::string& modelTxt, const std::string& modelBin);
    ~FaceDetector();

    void start();
    void stop();
    
    void setFrame(const cv::Mat& frame);
    
    std::vector<cv::Rect> getFaces();

private:
    void workerLoop();

    cv::dnn::Net net;
    
    std::thread workerThread;
    std::mutex mtx;
    std::atomic<bool> running{false};

    cv::Mat currentFrame;
    bool hasNewFrame{false};
    std::vector<cv::Rect> faces;
};
