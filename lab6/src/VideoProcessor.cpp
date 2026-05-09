#include "../include/VideoProcessor.hpp"
#include <iostream>
#include <vector>

VideoProcessor::VideoProcessor(int cameraId) : windowName("Lab 6"), mode(0), brightness(50) {
    cap.open(cameraId, cv::CAP_V4L2);
    if (!cap.isOpened()) {
        exit(-1);
    }
    
    cap.set(cv::CAP_PROP_FRAME_WIDTH, 1920);
    cap.set(cv::CAP_PROP_FRAME_HEIGHT, 1080);

    cv::namedWindow(windowName);
    cv::setMouseCallback(windowName, VideoProcessor::onMouse, this);
    cv::createTrackbar("Brightness", windowName, &brightness, 100);
}

VideoProcessor::~VideoProcessor() {
    cap.release();
    cv::destroyAllWindows();
}

void VideoProcessor::onMouse(int event, int x, int y, int flags, void* userdata) {
    if (event == cv::EVENT_LBUTTONDOWN) {
        std::cout << x << " " << y << std::endl;
    }
}

void VideoProcessor::process(cv::Mat& frame) {
    cv::flip(frame, frame, 1);

    int beta = brightness - 50;
    frame.convertTo(frame, -1, 1, beta);

    if (mode == 0) {
        return;
    } else if (mode == 1) {
        cv::cvtColor(frame, frame, cv::COLOR_BGR2GRAY);
    } else if (mode == 2) {
        cv::Mat gray, edges;
        cv::cvtColor(frame, gray, cv::COLOR_BGR2GRAY);
        cv::Canny(gray, edges, 50, 150);
        frame = edges;
    } else if (mode == 3) {
        cv::bitwise_not(frame, frame);
    } else if (mode == 4) {
        cv::Mat gray, grad_x, grad_y, abs_grad_x, abs_grad_y;
        cv::cvtColor(frame, gray, cv::COLOR_BGR2GRAY);
        cv::Sobel(gray, grad_x, CV_16S, 1, 0, 3);
        cv::Sobel(gray, grad_y, CV_16S, 0, 1, 3);
        cv::convertScaleAbs(grad_x, abs_grad_x);
        cv::convertScaleAbs(grad_y, abs_grad_y);
        cv::addWeighted(abs_grad_x, 0.5, abs_grad_y, 0.5, 0, frame);
    } else if (mode == 5) {
        cv::cvtColor(frame, frame, cv::COLOR_BGR2GRAY);
        cv::threshold(frame, frame, 128, 255, cv::THRESH_BINARY);
    } else if (mode == 6) {
        std::vector<cv::Mat> channels;
        cv::split(frame, channels);
        cv::Mat shift_mat = (cv::Mat_<double>(2,3) << 1, 0, 15, 0, 1, 0);
        cv::warpAffine(channels[2], channels[2], shift_mat, channels[2].size());
        cv::merge(channels, frame);
    } else if (mode == 8) {
        cv::GaussianBlur(frame, frame, cv::Size(15, 15), 0);
    }
}

void VideoProcessor::run() {
    cv::Mat frame;
    while (true) {
        cap >> frame;
        if (frame.empty()) break;

        process(frame);
        cv::imshow(windowName, frame);

        char key = (char)cv::waitKey(30);
        if (key == 'q') break;
        if (key >= '0' && key <= '9') {
            mode = key - '0';
        }
    }
}
