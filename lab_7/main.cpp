#include <opencv2/opencv.hpp>
#include "FaceDetector.h"
#include <iostream>

int main() {
    cv::VideoCapture cap(0);
    if (!cap.isOpened()) {
        std::cerr << "Помилка: неможливо відкрити камеру!" << std::endl;
        return -1;
    }

    FaceDetector detector("deploy.prototxt", "res10_300x300_ssd_iter_140000.caffemodel");
    detector.start();

    cv::Mat frame;
    bool detectionEnabled = false; 

    std::cout << "Натисніть 'F' для увімкнення/вимкнення детекції облич." << std::endl;
    std::cout << "Натисніть 'ESC' або 'Q' для виходу." << std::endl;

    while (true) {
        cap >> frame;
        if (frame.empty()) {
            std::cerr << "Помилка: порожній кадр!" << std::endl;
            break;
        }

        cv::flip(frame, frame, 1);

        if (detectionEnabled) {
            detector.setFrame(frame);
            
            std::vector<cv::Rect> faces = detector.getFaces();
            
            for (const auto& face : faces) {
                cv::rectangle(frame, face, cv::Scalar(0, 255, 0), 2);
                cv::putText(frame, "Face", cv::Point(face.x, face.y - 10), 
                            cv::FONT_HERSHEY_SIMPLEX, 0.5, cv::Scalar(0, 255, 0), 2);
            }
        }

        cv::putText(frame, "Kyrakivskiy Oleksandr (FB-44)", cv::Point(10, 30), 
                    cv::FONT_HERSHEY_SIMPLEX, 0.6, cv::Scalar(255, 255, 255), 2);
        
        std::string modeText = detectionEnabled ? "Detection: ON (Press F)" : "Detection: OFF (Press F)";
        cv::putText(frame, modeText, cv::Point(10, 60), 
                    cv::FONT_HERSHEY_SIMPLEX, 0.6, detectionEnabled ? cv::Scalar(0, 255, 0) : cv::Scalar(0, 0, 255), 2);

        cv::imshow("Lab 7: Computer Vision & Multithreading", frame);

        char key = (char)cv::waitKey(1);
        if (key == 27 || key == 'q' || key == 'Q') {
            break; 
        } else if (key == 'f' || key == 'F') {
            detectionEnabled = !detectionEnabled; 
        }
    }

    detector.stop();
    return 0;
}
