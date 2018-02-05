#include <iostream>
#include <vector>
#include <algorithm>


#include <opencv2/photo.hpp>
#include "opencv2/imgcodecs.hpp"
#include <opencv2/highgui.hpp>

using namespace std;
using namespace cv;

void printVersion() {
    cout << "Using OpenCV v"
        << CV_MAJOR_VERSION << "."
        << CV_MINOR_VERSION << "."
        << CV_SUBMINOR_VERSION << endl;
}

int main() {
    printVersion();


    // Open webcam
    VideoCapture cap(1);
    if (!cap.isOpened()) {
        cout << "cannot open stream" << endl;
        return -1;
    }

    cap.set(CAP_PROP_AUTO_EXPOSURE, 1);

    int count = 0;
    // Grab frames
    while (true) {
        Mat frame;
        cout << cap.get(CAP_PROP_EXPOSURE) << endl << flush;
        cap.read(frame);

        if (count == 60) {
            imwrite("normal.png", frame);
            cout << "wrote frame" << endl;
            count ++;
            continue;
        }
        imshow("preview", frame);

        if (waitKeyEx(1) == 27)
            break;

        count ++;
    }

    return 0;
}
