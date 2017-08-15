#include <iostream>

#include "opencv2/highgui/highgui.hpp"
#include "opencv2/videoio.hpp"
#include "opencv2/opencv.hpp"

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

    VideoCapture cap(1);

    cap.set(CAP_PROP_AUTO_EXPOSURE, 0.25); // where 0.25 means "manual exposure, manual iris"


    if (!cap.isOpened()) {
        cout << "cannot open stream" << endl;
    }

    int count = 0;
    float exp1 = 10.0f;
    float exp2 = 0.0f;
    int flipFrames = 4;


    while (true) {
        Mat frame;
        cap.read(frame);
        imshow("preview", frame);
        if (waitKey(30) >= 0) {
            break;
        }

        if (count % flipFrames == flipFrames/2-1) {
            cap.set(CAP_PROP_EXPOSURE, exp1);
            cout << "exp set to " << exp1 << endl;
        } else if (count % flipFrames == 0) {
            cap.set(CAP_PROP_EXPOSURE, exp2);
            cout << "exp set to " << exp2 << endl;
        }

        count++;
    }

    return 0;
}
