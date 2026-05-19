#include "FaceDetector.h"
#include <chrono>
#include <iostream>

FaceDetector::FaceDetector(const std::string& modelTxt, const std::string& modelBin) {
    net = cv::dnn::readNetFromCaffe(modelTxt, modelBin);
}

FaceDetector::~FaceDetector() { 
    stop(); 
}

void FaceDetector::start() {
    running = true;
    workerThread = std::thread(&FaceDetector::workerLoop, this);
}

void FaceDetector::stop() {
    running = false;
    if (workerThread.joinable()) {
        workerThread.join();
    }
}

void FaceDetector::setFrame(const cv::Mat& frame) {
    std::lock_guard<std::mutex> lock(mtx);
    currentFrame = frame.clone();
    hasNewFrame = true;
}

std::vector<cv::Rect> FaceDetector::getFaces() {
    std::lock_guard<std::mutex> lock(mtx);
    return faces;
}

void FaceDetector::workerLoop() {
    while (running) {
        cv::Mat frameForDetection;
        
        {
            std::lock_guard<std::mutex> lock(mtx);
            if (!hasNewFrame || currentFrame.empty()) {
                
                continue; 
            }
            frameForDetection = currentFrame.clone();
            hasNewFrame = false;
        }

        if (frameForDetection.empty()) {
            std::this_thread::sleep_for(std::chrono::milliseconds(10));
            continue;
        }

        cv::Mat blob = cv::dnn::blobFromImage(frameForDetection, 1.0, cv::Size(300, 300), cv::Scalar(104.0, 177.0, 123.0));
        net.setInput(blob);
        cv::Mat detections = net.forward();

        std::vector<cv::Rect> currentFaces;
        cv::Mat detectionMat(detections.size[2], detections.size[3], CV_32F, detections.ptr<float>());

        for (int i = 0; i < detectionMat.rows; i++) {
            float confidence = detectionMat.at<float>(i, 2);
            if (confidence > 0.5) {
                int x1 = static_cast<int>(detectionMat.at<float>(i, 3) * frameForDetection.cols);
                int y1 = static_cast<int>(detectionMat.at<float>(i, 4) * frameForDetection.rows);
                int x2 = static_cast<int>(detectionMat.at<float>(i, 5) * frameForDetection.cols);
                int y2 = static_cast<int>(detectionMat.at<float>(i, 6) * frameForDetection.rows);
                
                currentFaces.push_back(cv::Rect(cv::Point(x1, y1), cv::Point(x2, y2)));
            }
        }


        std::this_thread::sleep_for(std::chrono::milliseconds(500));

        {
            std::lock_guard<std::mutex> lock(mtx);
            faces = currentFaces;
        }
    }
}
