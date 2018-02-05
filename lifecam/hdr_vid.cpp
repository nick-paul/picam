#include <iostream>
#include <vector>
#include <algorithm>
#include <sstream>

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

void getExposureTimes(int argc, char* argv[], vector<float>& times) {
    for (int i = 1; i < argc; i++) {
        istringstream ss(argv[i]);
        float n;
        if (ss >> n) {
            times.push_back(n);
        } else {
            cerr << "Invalid number " << argv[i] << endl;
            times.clear();
            return;
        }
    }
}

void hdrFrame(VideoCapture& cap,
        const vector<float>& times,
        vector<Mat>& frames) {


    
    // Grab frames
    int count = 0;
    while (count < times.size()) {
        //cap.set(CAP_PROP_EXPOSURE, times[count]);
        cap.read(frames[count]);
        // cout << "Frame read: " << count << endl << flush;
        imshow("mid", frames[count]);
        //waitKey(10);
        count++;
    }

    
    /*
    Mat fusion;
    Ptr<MergeMertens> merge_mertens = createMergeMertens();
    merge_mertens->process(frames, fusion);

    imshow("fusion", fusion);
    imwrite("fusion.png", fusion * 255);
    waitKey(20);
    */
}

int main(int argc, char* argv[]) {
    printVersion();

    // Read exposure times from input
    vector<float> times;
    getExposureTimes(argc, argv, times);

    //Defaults
    if (times.size() == 0) {
        times.push_back(0.0f);
        times.push_back(0.01f);
        times.push_back(10.0f);
    }

    cout << "Using exposure times: { ";
    for (const float& f : times) {
        cout << f << " ";
    }
    cout << "}" << endl << flush;

    // Open webcam
    VideoCapture cap(1);
    if (!cap.isOpened()) {
        cout << "cannot open stream" << endl;
    }

    // Manual exposure
    cap.set(CAP_PROP_AUTO_EXPOSURE, 0.25);
    cap.set(CV_CAP_PROP_FPS, 25);

    vector<Mat> frames(times.size());

    int iters = 10;
    for (int i = 0; i < iters; i++) {
        hdrFrame(cap, times, frames); 
    }

    return 0;
}
